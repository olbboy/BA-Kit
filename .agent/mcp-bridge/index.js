
import crypto from 'crypto';
import express from 'express';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { SSEServerTransport } from '@modelcontextprotocol/sdk/server/sse.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';

// Session TTL: 5 minutes
const SESSION_TTL_MS = 5 * 60 * 1000;

const transports = new Map();
const sessionTimestamps = new Map();

// Auth middleware: Bearer token if MCP_BRIDGE_TOKEN is set, else localhost-only
function authMiddleware(req, res, next) {
    const token = process.env.MCP_BRIDGE_TOKEN;
    if (!token) {
        // No token configured: allow localhost only
        const ip = req.ip || req.connection.remoteAddress;
        if (ip === '127.0.0.1' || ip === '::1' || ip === '::ffff:127.0.0.1') {
            return next();
        }
        return res.status(403).send('Remote access requires MCP_BRIDGE_TOKEN');
    }
    const auth = req.headers.authorization;
    if (auth === `Bearer ${token}`) {
        return next();
    }
    return res.status(401).send('Unauthorized');
}

function shutdown() {
    console.log('Shutting down MCP Bridge...');
    for (const [id] of transports) {
        transports.delete(id);
        sessionTimestamps.delete(id);
    }
    process.exit(0);
}

process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);

async function main() {
    console.log('Starting MCP Bridge...');

    // Ensure API Key is set
    if (!process.env.PERPLEXITY_API_KEY && process.env.PERPLEXITY_API_KEYS) {
        console.log('Mapping PERPLEXITY_API_KEYS to PERPLEXITY_API_KEY');
        process.env.PERPLEXITY_API_KEY = process.env.PERPLEXITY_API_KEYS;
    }

    if (!process.env.PERPLEXITY_API_KEY) {
        console.error('Error: PERPLEXITY_API_KEY is missing from environment');
        // process.exit(1);
    } else {
        console.log('API key configured.');
    }

    // 1. Connect to Stdio Server (Perplexity)
    console.log('Connecting to Perplexity Stdio Server...');
    const stdioTransport = new StdioClientTransport({
        command: 'npx',
        args: ['-y', 'server-perplexity-ask'],
        env: process.env
    });

    const client = new Client(
        { name: 'bridge-client', version: '1.0.0' },
        { capabilities: {} }
    );
    await client.connect(stdioTransport);
    console.log('Connected to Perplexity Stdio Server.');

    // 2. Discover Tools
    console.log('Discovering tools...');
    const toolsList = await client.listTools();
    console.log(`Found ${toolsList.tools.length} tools.`);

    // 3. Create SSE Server
    const server = new McpServer({
        name: 'perplexity-bridge',
        version: '1.0.0'
    });

    // 4. Register Tools Proxy
    for (const tool of toolsList.tools) {
        console.log(`Registering tool: ${tool.name}`);
        server.tool(tool.name, tool.inputSchema, async (args) => {
            console.log(`Calling tool: ${tool.name}`);
            try {
                const result = await client.callTool({
                    name: tool.name,
                    arguments: args
                });
                return result;
            } catch (error) {
                console.error(`Error calling tool ${tool.name}:`, error);
                throw error;
            }
        });
    }

    // 5. Setup Express with session handling
    const app = express();
    const PORT = 3845;

    app.use(express.json());

    // Periodic cleanup of stale sessions every 60 seconds
    setInterval(() => {
        const now = Date.now();
        for (const [id, ts] of sessionTimestamps) {
            if (now - ts > SESSION_TTL_MS) {
                transports.delete(id);
                sessionTimestamps.delete(id);
                console.log(`Session expired: ${id}`);
            }
        }
    }, 60_000);

    app.get('/sse', authMiddleware, async (req, res) => {
        console.log('New SSE connection');

        // Cryptographically random session ID
        const sessionId = crypto.randomUUID();
        const endpoint = `/message?session=${sessionId}`;

        const sseTransport = new SSEServerTransport(endpoint, res);

        transports.set(sessionId, sseTransport);
        sessionTimestamps.set(sessionId, Date.now());

        await server.connect(sseTransport);

        res.on('close', () => {
            console.log(`SSE connection closed: ${sessionId}`);
            transports.delete(sessionId);
            sessionTimestamps.delete(sessionId);
        });
    });

    app.post('/message', authMiddleware, async (req, res) => {
        const sessionId = req.query.session;
        if (!sessionId) {
            return res.status(400).send('Missing session ID');
        }

        const sseTransport = transports.get(sessionId);
        if (!sseTransport) {
            return res.status(404).send('Session not found');
        }

        // Refresh session timestamp on activity
        sessionTimestamps.set(sessionId, Date.now());

        try {
            await sseTransport.handlePostMessage(req, res);
        } catch (error) {
            console.error(`Error handling message for session ${sessionId}:`, error.message);
            if (!res.headersSent) {
                res.status(500).send('Internal server error');
            }
        }
    });

    app.listen(PORT, () => {
        console.log(`MCP Bridge running on port ${PORT}`);
    });
}

main().catch(console.error);
