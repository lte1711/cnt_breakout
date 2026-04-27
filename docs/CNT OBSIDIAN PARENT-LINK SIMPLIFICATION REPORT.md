---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/validation
  - graph-view
  - obsidian
  - type/analysis
---

---
---

# CNT Obsidian Parent-Link Simplification Report

## Objective

Simplify Obsidian navigation so that leaf documents connect only to their immediate parent document.

## Rule Applied

- top-level English documents connect to `00 Docs Index`
- top-level Korean mirror documents connect to `00 Docs Index KO`
- `00 Docs Index` connects to `00 CNT Vault Home`
- `00 Docs Index KO` connects to `00 Docs Index`
- leaf documents keep only one parent link in the `## Obsidian Links` section

## Implementation

- updated `scripts/simplify_graph_links.py` to normalize link sections into a parent-only structure
- applied the script across `docs/` and `docs/ko/`

## Verification

- sampled English and Korean leaf documents now contain exactly one Obsidian parent link
- sampled dashboard guide documents now point only to their immediate parent
- automated validation confirmed that no non-index markdown file contains more than one wiki-link in the whole document
- this means body-level cross-links were also reduced to plain text for leaf documents

## Result

The documentation graph is now simpler:

- leaf docs point to one parent only
- index docs remain the main hub
- cross-links in the dedicated Obsidian link section are removed
- body-level wiki-links in leaf documents are reduced to plain text

## Obsidian Links

- [[00 Docs Index]]

