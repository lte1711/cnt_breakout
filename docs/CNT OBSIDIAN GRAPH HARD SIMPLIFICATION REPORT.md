---
title: CNT OBSIDIAN GRAPH HARD SIMPLIFICATION REPORT
status: FINAL
language: en
updated: 2026-04-24
---

# CNT Obsidian Graph Hard Simplification Report

## Objective

Reduce the Obsidian graph further by simplifying both links and tags.

## Applied Changes

### 1. Link simplification

- non-index documents now keep only one wiki-link in the full document
- that single remaining link is the immediate parent link
- body-level cross-links were converted to plain text where needed

### 2. Parent grouping

Documents that previously pointed directly to the index were regrouped into broader parent hubs by filename pattern.

Representative parent hubs now include:

- `CNT v2 BREAKOUT QUALITY EVALUATION REPORT`
- `CNT v2 BREAKOUT V2 DESIGN`
- `CNT v2 BREAKOUT V3 DESIGN DRAFT`
- `CNT v2 VALIDATION REPORT`
- `CNT v2 LIVE READINESS GATE`
- `CNT v2 TESTNET PERFORMANCE REPORT`
- `CNT DATA DASHBOARD`
- `CNT TOOLCHAIN INTEGRATION REPORT`

### 3. Tag simplification

- all non-index markdown documents now have no tags
- `00 Docs Index.md` keeps only `cnt`
- `00 Docs Index KO.md` keeps only `cnt` and `ko`

## Verification

- non-index markdown files with more than one wiki-link: `0`
- markdown files with non-minimal tags outside index docs: `0`

## Result

The graph is now materially simpler because:

- leaf documents no longer form side-to-side link webs
- tag nodes no longer connect large batches of documents
- navigation remains possible through parent hubs and index documents
