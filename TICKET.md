# PLATFORM-2947: Investigate search index returning wrong results

**Status:** In Progress · **Priority:** Critical
**Sprint:** Sprint 28 · **Story Points:** 8
**Reporter:** Priya Menon (Search Lead) · **Assignee:** You (Intern)
**Due:** End of sprint (Friday)
**Labels:** `backend`, `python`, `search`, `performance`
**Task Type:** Code Debugging

---

## Description

The search index builder creates inverted indexes for full-text search. Users report that search results are incorrect — documents that should match aren't returned, and irrelevant documents appear.

**DEBUGGING task — no hint comments. Investigate from symptoms.**

## Symptoms

- Search for "python tutorial" returns documents about "java" but not about "python"
- Documents containing exact search terms get a relevance score of 0
- Index reports 500 documents indexed, but search over the full corpus returns only 50 results
- Case sensitivity seems inconsistent: "Python" finds results but "python" doesn't

## Acceptance Criteria

- [ ] Root cause found and fixed
- [ ] Search returns correct documents for given queries
- [ ] All unit tests pass
