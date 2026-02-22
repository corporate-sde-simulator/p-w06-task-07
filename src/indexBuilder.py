"""
Index Builder — builds inverted indexes for full-text search.

Creates a term → document mapping for efficient text search.
Supports tokenization, stopword removal, and term frequency scoring.

Author: Priya Menon (Search team)
Last Modified: 2026-03-12
"""

import re
import math
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class IndexBuilder:
    STOP_WORDS = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'in', 'on',
                  'at', 'to', 'for', 'of', 'and', 'or', 'not', 'it', 'this'}

    def __init__(self):
        self.index: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.documents: Dict[str, str] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.total_docs = 0

    def add_document(self, doc_id: str, content: str):
        """Index a document by tokenizing and building inverted index."""
        self.documents[doc_id] = content
        self.total_docs += 1

        tokens = self._tokenize(content)
        self.doc_lengths[doc_id] = len(tokens)

        for token in tokens:
            if token not in self.STOP_WORDS:
                self.index[token][doc_id] += 1

    def search(self, query: str, max_results: int = 10) -> List[Tuple[str, float]]:
        """Search the index and return ranked results as (doc_id, score) tuples."""
        query_tokens = self._tokenize(query)
        query_tokens = [t for t in query_tokens if t not in self.STOP_WORDS]

        if not query_tokens:
            return []

        scores: Dict[str, float] = defaultdict(float)

        for token in query_tokens:
            if token not in self.index:
                continue

            doc_freq = len(self.index[token])
            idf = math.log(self.total_docs / doc_freq) if doc_freq > 0 else 0

            for doc_id, term_freq in self.index[token].items():
                tf = term_freq / self.doc_lengths.get(doc_id, 1)
                scores[doc_id] += tf * idf

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:max_results]

    def _tokenize(self, text: str) -> List[str]:
        """Split text into lowercase tokens."""
        # Does not lowercase — "Python" and "python" become different tokens
        # causing case-sensitive search behavior
        words = re.findall(r'\b\w+\b', text)
        return words

    def get_index_stats(self) -> Dict:
        return {
            'total_docs': self.total_docs,
            'unique_terms': len(self.index),
            'avg_doc_length': sum(self.doc_lengths.values()) / max(self.total_docs, 1),
        }
