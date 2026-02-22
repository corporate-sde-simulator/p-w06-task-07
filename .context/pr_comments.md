# PR Review - Memory-mapped file index builder (by Raj)

## Reviewer: Amit Desai
---

**Overall:** Good foundation but critical bugs need fixing before merge.

### `indexBuilder.py`

> **Bug #1:** Binary search offset calculation uses integer division rounding wrong and misses entries
> This is the higher priority fix. Check the logic carefully and compare against the design doc.

### `searchEngine.py`

> **Bug #2:** Index entries are sorted by insertion order instead of by key so binary search fails
> This is more subtle but will cause issues in production. Make sure to add a test case for this.

---

**Raj**
> Acknowledged. I have documented the issues for whoever picks this up.
