
import express from 'express';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { SSEServerTransport } from '@modelcontextprotocol/sdk/server/sse.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';

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
    }

    // 1. Connect to Stdio Server (Perplexity)
    console.log('Connecting to Perplexity Stdio Server...');
    const transport = new StdioClientTransport({
        command: 'npx',
        args: ['-y', 'server-perplexity-ask'],
        env: process.env
    });

    const client = new Client(
        { name: 'bridge-client', version: '1.0.0' },
        { capabilities: {} }
    );
    await client.connect(transport);
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

    // Important: Parse JSON bodies for POST requests
    app.use(express.json());

    const transports = new Map();

    app.get('/sse', async (req, res) => {
        console.log('New SSE connection');

        // Create a unique session ID
        const sessionId = Date.now().toString();
        const endpoint = `/message?session=${sessionId}`;

        // Create new transport with custom endpoint
        const transport = new SSEServerTransport(endpoint, res);

        // Store transport
        transports.set(sessionId, transport);

        // Connect server to transport
        await server.connect(transport);

        // Cleanup on close
        res.on('close', () => {
            console.log(`SSE connection closed: ${sessionId}`);
            transports.delete(sessionId);
        });
    });

    app.post('/message', async (req, res) => {
        const sessionId = req.query.session;
        if (!sessionId) {
            return res.status(400).send('Missing session ID');
        }

        const transport = transports.get(sessionId);
        if (!transport) {
            return res.status(404).send('Session not found');
        }

        await transport.handlePostMessage(req, res);
    });

    app.listen(PORT, () => {
        console.log(`MCP Bridge running on port ${PORT}`);
    });
}

main().catch(console.error);
