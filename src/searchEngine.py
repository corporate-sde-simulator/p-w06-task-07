"""
Search Engine — high-level search API using the index builder.

Provides query parsing, result highlighting, and pagination.

Author: Priya Menon (Search team)
Last Modified: 2026-03-12
"""

from typing import Dict, List, Optional, Tuple


class SearchEngine:
    def __init__(self, index_builder):
        self.index = index_builder
        self.search_history: List[Dict] = []

    def search(self, query: str, page: int = 1, page_size: int = 10) -> Dict:
        """Execute a search query with pagination."""
        all_results = self.index.search(query, max_results=100)

        start = (page - 1) * page_size
        end = start + page_size
        page_results = all_results[start:end]

        results = []
        for doc_id, score in page_results:
            content = self.index.documents.get(doc_id, '')
            snippet = self._make_snippet(content, query)
            results.append({
                'doc_id': doc_id,
                'score': round(score, 4),
                'snippet': snippet,
            })

        self.search_history.append({
            'query': query,
            'total_results': len(all_results),
            'page': page,
        })

        return {
            'query': query,
            'results': results,
            'total': len(all_results),
            'page': page,
            'pages': max(1, (len(all_results) + page_size - 1) // page_size),
        }

    def _make_snippet(self, content: str, query: str, max_length: int = 200) -> str:
        """Extract a relevant snippet from the document."""
        content_lower = content.lower()
        query_lower = query.lower()

        # Find first occurrence of any query word
        query_words = query_lower.split()
        best_pos = len(content)
        for word in query_words:
            pos = content_lower.find(word)
            if 0 <= pos < best_pos:
                best_pos = pos

        # Extract snippet around the match
        start = max(0, best_pos - 50)
        end = min(len(content), start + max_length)

        snippet = content[start:end]
        if start > 0:
            snippet = '...' + snippet
        if end < len(content):
            snippet += '...'

        return snippet

    def get_suggestions(self, prefix: str, max_suggestions: int = 5) -> List[str]:
        """Get term suggestions based on prefix matching."""
        suggestions = []
        for term in self.index.index.keys():
            if term.startswith(prefix.lower()):
                suggestions.append(term)
            if len(suggestions) >= max_suggestions:
                break
        return suggestions

    def get_stats(self) -> Dict:
        return {
            'index_stats': self.index.get_index_stats(),
            'total_searches': len(self.search_history),
        }
