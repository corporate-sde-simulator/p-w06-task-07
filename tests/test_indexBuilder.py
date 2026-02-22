"""Tests for Memory-mapped file index builder."""
import pytest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from indexBuilder import IndexBuilder
from searchEngine import SearchEngine

class TestMain:
    def test_basic(self):
        obj = IndexBuilder()
        assert obj.process({"key": "val"}) is not None
    def test_empty(self):
        obj = IndexBuilder()
        assert obj.process(None) is None
    def test_stats(self):
        obj = IndexBuilder()
        obj.process({"x": 1})
        assert obj.get_stats()["processed"] == 1

class TestSupport:
    def test_basic(self):
        obj = SearchEngine()
        assert obj.process({"key": "val"}) is not None

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
