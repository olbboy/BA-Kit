#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BA-Kit Knowledge Engine — BM25 search for Business Analysis knowledge base.
Forked from ui-ux-pro-max core.py, adapted for BA domains.
Zero external dependencies (stdlib only).
"""

import csv
import re
import unicodedata
from pathlib import Path
from math import log
from collections import defaultdict

# ============ CONFIGURATION ============
DATA_DIR = Path(__file__).parent.parent / "data"
MAX_RESULTS = 3

# CSV schema: entry_id, domain, type, title, content, tags, agents, source
SEARCH_COLS = ["title", "content", "tags", "type"]
OUTPUT_COLS = ["entry_id", "domain", "type", "title", "content", "tags", "agents", "source"]

# Domain → CSV file mapping
DOMAIN_FILES = {
    "writing": "writing.csv",
    "elicitation": "elicitation.csv",
    "validation": "validation.csv",
    "nfr": "nfr.csv",
    "process": "process.csv",
    "prioritization": "prioritization.csv",
    "traceability": "traceability.csv",
    "conflict": "conflict.csv",
    "solution": "solution.csv",
    "systems": "systems.csv",
    "agile": "agile.csv",
    "identity": "identity.csv",
    "workshop": "workshop.csv",
    "innovation": "innovation.csv",
    "metrics": "metrics.csv",
    "modeling": "modeling.csv",
    "ux-research": "ux-research.csv",
    "business-rules": "business-rules.csv",
    "integration": "integration.csv",
    "compliance": "compliance.csv",
    "communication": "communication.csv",
    "testing": "testing.csv",
    "data-analytics": "data-analytics.csv",
}

# Domain auto-detection keywords
DOMAIN_KEYWORDS = {
    "writing": [
        "requirement", "user story", "acceptance criteria", "gherkin",
        "given when then", "ears", "ambiguous", "testable", "invest",
        "functional requirement", "specification", "brd", "srs", "frd",
        "passive voice", "template", "draft", "write", "document",
    ],
    "elicitation": [
        "interview", "elicitation", "question", "stakeholder",
        "workshop", "brainstorm", "observation", "survey",
        "funnel", "probing", "colombo", "5w1h", "requirement gathering",
    ],
    "validation": [
        "validation", "verification", "inspect", "review", "defect",
        "quality check", "ambiguity", "health score", "peer review",
        "checklist", "fagan", "walkthrough",
    ],
    "nfr": [
        "nfr", "non-functional", "performance", "security", "reliability",
        "availability", "scalability", "usability", "iso 25010",
        "response time", "throughput", "gdpr", "owasp", "planguage",
    ],
    "process": [
        "process", "bpmn", "workflow", "swimlane", "activity diagram",
        "flowchart", "as-is", "to-be", "lean", "value stream",
        "bottleneck", "waste", "mermaid",
    ],
    "prioritization": [
        "prioritize", "priority", "moscow", "rice", "wsjf", "kano",
        "backlog", "ranking", "weighted criteria", "cost benefit",
        "must have", "should have", "could have",
    ],
    "traceability": [
        "trace", "traceability", "rtm", "impact", "blast radius",
        "dependency", "change control", "baseline", "coverage",
    ],
    "conflict": [
        "conflict", "negotiation", "disagree", "stakeholder war",
        "batna", "harvard", "mediat", "adr", "decision record",
    ],
    "solution": [
        "roi", "npv", "irr", "business case", "cost benefit",
        "payback", "break even", "financial", "investment",
    ],
    "systems": [
        "system thinking", "feedback loop", "reinforcing", "balancing",
        "archetype", "leverage point", "stocks", "flows", "causal",
    ],
    "agile": [
        "agile", "scrum", "sprint", "story map", "mvp",
        "hypothesis", "build measure learn", "epic", "backlog refinement",
    ],
    "identity": [
        "stakeholder", "raci", "power interest", "persona",
        "competency", "certification", "babok", "ireb",
    ],
    "workshop": [
        "workshop", "facilitat", "agenda", "brainstorm", "dot voting",
        "parking lot", "odec", "silent brainstorm", "ground rules",
    ],
    "innovation": [
        "innovation", "experiment", "a/b test", "hypothesis",
        "pilot", "design thinking", "scamper", "prototype",
    ],
    "metrics": [
        "metric", "kpi", "spc", "control chart", "defect density",
        "sigma", "cpk", "quality dashboard",
    ],
    "modeling": [
        "data model", "erd", "entity", "relationship", "use case",
        "state diagram", "context diagram", "crud", "class diagram",
        "sequence diagram", "dfd", "decision table",
    ],
    "ux-research": [
        "persona", "user journey", "empathy map", "usability",
        "heuristic", "card sorting", "wireframe", "prototype",
        "user research", "ux", "accessibility", "wcag", "sus score",
        "think aloud", "task analysis", "information architecture",
    ],
    "business-rules": [
        "business rule", "derivation", "inference", "constraint",
        "action enabler", "policy", "rule catalog", "authorization rule",
        "temporal rule", "data rule", "validation rule",
    ],
    "integration": [
        "api", "rest", "graphql", "webhook", "microservice",
        "integration", "endpoint", "oauth", "cors", "rate limit",
        "circuit breaker", "idempotent", "openapi", "swagger",
        "kafka", "rabbitmq", "event driven", "sftp",
    ],
    "compliance": [
        "gdpr", "pci-dss", "hipaa", "sox", "compliance", "regulation",
        "privacy", "consent", "data protection", "audit trail",
        "data residency", "breach notification", "coppa",
        "cookie", "right to erasure", "dpia",
    ],
    "communication": [
        "communication plan", "status report", "meeting minutes",
        "escalation", "presentation", "stakeholder update",
        "decision log", "risk register", "scope creep",
        "sprint review", "steering committee",
    ],
    "testing": [
        "test case", "uat", "acceptance test", "regression",
        "boundary value", "equivalence partition", "smoke test",
        "performance test", "security test", "test scenario",
        "bug report", "defect lifecycle", "test data",
        "end to end", "exploratory test",
    ],
    "data-analytics": [
        "data dictionary", "etl", "data warehouse", "data lake",
        "reporting", "dashboard", "data quality", "data governance",
        "data lineage", "dimensional model", "data migration",
        "data classification", "master data", "bi tool",
    ],
}

AVAILABLE_DOMAINS = list(DOMAIN_FILES.keys())


# ============ BM25 IMPLEMENTATION ============
class BM25:
    """BM25 ranking algorithm for text search."""

    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus = []
        self.doc_lengths = []
        self.avgdl = 0
        self.idf = {}
        self.doc_freqs = defaultdict(int)
        self.N = 0

    @staticmethod
    def tokenize(text):
        """Tokenize text: lowercase, strip diacritics, remove punctuation, filter short words."""
        text = str(text).lower()
        # Strip Vietnamese/Unicode diacritics for matching
        text = unicodedata.normalize("NFD", text)
        text = re.sub(r"[\u0300-\u036f]", "", text)
        text = re.sub(r"[^\w\s]", " ", text)
        return [w for w in text.split() if len(w) > 2]

    def fit(self, documents):
        """Build BM25 index from document list."""
        self.corpus = [self.tokenize(doc) for doc in documents]
        self.N = len(self.corpus)
        if self.N == 0:
            return
        self.doc_lengths = [len(doc) for doc in self.corpus]
        self.avgdl = sum(self.doc_lengths) / self.N

        for doc in self.corpus:
            seen = set()
            for word in doc:
                if word not in seen:
                    self.doc_freqs[word] += 1
                    seen.add(word)

        for word, freq in self.doc_freqs.items():
            self.idf[word] = log((self.N - freq + 0.5) / (freq + 0.5) + 1)

    def score(self, query):
        """Score all documents against query, return sorted (idx, score) pairs."""
        query_tokens = self.tokenize(query)
        scores = []

        for idx, doc in enumerate(self.corpus):
            doc_score = 0
            doc_len = self.doc_lengths[idx]
            term_freqs = defaultdict(int)
            for word in doc:
                term_freqs[word] += 1

            for token in query_tokens:
                if token in self.idf:
                    tf = term_freqs[token]
                    idf_val = self.idf[token]
                    numerator = tf * (self.k1 + 1)
                    denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)
                    doc_score += idf_val * numerator / denominator

            scores.append((idx, doc_score))

        return sorted(scores, key=lambda x: x[1], reverse=True)


# ============ SEARCH FUNCTIONS ============
_csv_cache = {}  # filepath → (mtime, rows) — avoids re-reading unchanged files


def _load_csv(filepath):
    """Load CSV file with mtime-based caching."""
    fp = str(filepath)
    mtime = filepath.stat().st_mtime
    if fp in _csv_cache and _csv_cache[fp][0] == mtime:
        return _csv_cache[fp][1]
    with open(filepath, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    _csv_cache[fp] = (mtime, rows)
    return rows


def _search_domain(filepath, query, max_results):
    """Search a single domain CSV using BM25."""
    if not filepath.exists():
        return []

    data = _load_csv(filepath)
    if not data:
        return []

    # Build search documents from search columns
    documents = [
        " ".join(str(row.get(col, "")) for col in SEARCH_COLS)
        for row in data
    ]

    bm25 = BM25()
    bm25.fit(documents)
    ranked = bm25.score(query)

    results = []
    for idx, score in ranked[:max_results]:
        if score > 0:
            row = data[idx]
            entry = {col: row.get(col, "") for col in OUTPUT_COLS if col in row}
            entry["_score"] = round(score, 3)
            results.append(entry)

    return results


def detect_domain(query):
    """Auto-detect the most relevant domain from query keywords."""
    query_lower = str(query).lower()

    scores = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = sum(
            1 for kw in keywords
            if re.search(r"\b" + re.escape(kw) + r"\b", query_lower)
        )
        scores[domain] = score

    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "writing"


def search(query, domain=None, max_results=MAX_RESULTS):
    """Search knowledge base. Auto-detects domain if not specified."""
    if domain is None:
        domain = detect_domain(query)

    csv_file = DOMAIN_FILES.get(domain)
    if csv_file is None:
        return {"error": f"Unknown domain: {domain}. Available: {', '.join(AVAILABLE_DOMAINS)}"}

    filepath = DATA_DIR / csv_file
    if not filepath.exists():
        return {
            "error": f"No data file for domain '{domain}' yet ({csv_file}). Available domains with data: "
                     + ", ".join(d for d, f in DOMAIN_FILES.items() if (DATA_DIR / f).exists()),
            "domain": domain,
        }

    results = _search_domain(filepath, query, max_results)

    return {
        "domain": domain,
        "query": query,
        "file": csv_file,
        "count": len(results),
        "results": results,
    }


def search_multi(query, domains=None, max_results=MAX_RESULTS):
    """Search across multiple domains, merge and re-rank results."""
    if domains is None:
        domains = [d for d, f in DOMAIN_FILES.items() if (DATA_DIR / f).exists()]

    all_results = []
    for domain in domains:
        csv_name = DOMAIN_FILES.get(domain)
        if not csv_name:
            continue
        filepath = DATA_DIR / csv_name
        if filepath and filepath.exists():
            results = _search_domain(filepath, query, max_results)
            for r in results:
                r["domain"] = domain
            all_results.extend(results)

    # Re-rank by BM25 score across domains
    all_results.sort(key=lambda x: x.get("_score", 0), reverse=True)
    return {
        "query": query,
        "domains": domains,
        "count": len(all_results[:max_results]),
        "results": all_results[:max_results],
    }
