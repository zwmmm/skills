#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UniApp UI Core - BM25 search engine for UniApp component mapping
"""

import csv
import re
from pathlib import Path
from math import log
from collections import defaultdict

# ============ CONFIGURATION ============
DATA_DIR = Path(__file__).parent.parent / "data"
MAX_RESULTS = 3

CSV_CONFIG = {
    "wotui": {
        "file": "wotui.csv",
        "search_cols": ["Component Name", "HTML Pattern", "CSS Classes", "Use Case"],
        "output_cols": ["Component Name", "Props", "Use Case", "Code Example", "Docs URL", "Category", "Priority"]
    },
    "custom": {
        "file": "components.csv",
        "search_cols": ["Component Name", "HTML Pattern", "CSS Classes", "Use Case"],
        "output_cols": ["Component Name", "File Path", "Props", "Events", "Code Example", "Use Case", "Category", "Priority"]
    },
    "template": {
        "file": "templates.csv",
        "search_cols": ["Template Name", "Keywords", "Use Cases"],
        "output_cols": ["Template Name", "File Name", "Description", "Required Components", "Keywords", "Use Cases", "Complexity"]
    },
    "unocss": {
        "file": "unocss-patterns.csv",
        "search_cols": ["Pattern Name", "Use Case", "Description"],
        "output_cols": ["Pattern Name", "CSS Classes", "Example", "Use Case", "Description"]
    },
    "best-practice": {
        "file": "best-practices.csv",
        "search_cols": ["Category", "Guideline", "Description"],
        "output_cols": ["Category", "Guideline", "Do", "Don't", "Code Good", "Code Bad", "Severity", "Platform"]
    },
    "uni-component": {
        "file": "uni-components.csv",
        "search_cols": ["Component Name", "HTML Tag", "Description"],
        "output_cols": ["Component Name", "HTML Tag", "Description", "Props", "Platform Support", "Docs URL"]
    }
}

AVAILABLE_DOMAINS = list(CSV_CONFIG.keys())


# ============ BM25 IMPLEMENTATION ============
class BM25:
    """BM25 ranking algorithm for text search"""

    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus = []
        self.doc_lengths = []
        self.avgdl = 0
        self.idf = {}
        self.doc_freqs = defaultdict(int)
        self.N = 0

    def tokenize(self, text):
        """Lowercase, split, remove punctuation, filter short words"""
        text = re.sub(r'[^\w\s]', ' ', str(text).lower())
        return [w for w in text.split() if len(w) > 2]

    def fit(self, documents):
        """Build BM25 index from documents"""
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
        """Score all documents against query"""
        query_tokens = self.tokenize(query)
        scores = []

        for idx, doc in enumerate(self.corpus):
            score = 0
            doc_len = self.doc_lengths[idx]
            term_freqs = defaultdict(int)
            for word in doc:
                term_freqs[word] += 1

            for token in query_tokens:
                if token in self.idf:
                    tf = term_freqs[token]
                    idf = self.idf[token]
                    numerator = tf * (self.k1 + 1)
                    denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)
                    score += idf * numerator / denominator

            scores.append((idx, score))

        return sorted(scores, key=lambda x: x[1], reverse=True)


# ============ SEARCH FUNCTIONS ============
def _load_csv(filepath):
    """Load CSV and return list of dicts"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def _search_csv(filepath, search_cols, output_cols, query, max_results):
    """Core search function using BM25"""
    if not filepath.exists():
        return []

    data = _load_csv(filepath)

    # Build documents from search columns
    documents = [" ".join(str(row.get(col, "")) for col in search_cols) for row in data]

    # BM25 search
    bm25 = BM25()
    bm25.fit(documents)
    ranked = bm25.score(query)

    # Get top results with score > 0
    results = []
    for idx, score in ranked[:max_results]:
        if score > 0:
            row = data[idx]
            results.append({col: row.get(col, "") for col in output_cols if col in row})

    return results


def detect_domain(query):
    """Auto-detect the most relevant domain from query"""
    query_lower = query.lower()

    domain_keywords = {
        "custom": ["custom", "project", "my", "user", "product", "card"],
        "wotui": ["button", "input", "cell", "form", "checkbox", "radio", "select", "picker", "tab", "navbar", "toast", "modal", "loading"],
        "template": ["page", "form", "list", "detail", "tab", "search", "grid", "login", "register"],
        "unocss": ["flex", "grid", "card", "container", "center", "shadow", "rounded", "padding", "margin"],
        "best-practice": ["best", "practice", "guideline", "navigation", "storage", "performance", "optimization", "cross-platform"],
        "uni-component": ["view", "text", "image", "scroll", "swiper", "built-in", "native"]
    }

    scores = {domain: sum(1 for kw in keywords if kw in query_lower) for domain, keywords in domain_keywords.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "wotui"


def search(query, domain=None, max_results=MAX_RESULTS):
    """Main search function with auto-domain detection"""
    if domain is None:
        domain = detect_domain(query)

    config = CSV_CONFIG.get(domain, CSV_CONFIG["wotui"])
    filepath = DATA_DIR / config["file"]

    if not filepath.exists():
        return {"error": f"File not found: {filepath}", "domain": domain}

    results = _search_csv(filepath, config["search_cols"], config["output_cols"], query, max_results)

    return {
        "domain": domain,
        "query": query,
        "file": config["file"],
        "count": len(results),
        "results": results
    }
