---
tags:
  - cnt
  - docs
  - instruction
aliases:
  - SHARING CHECKLIST
---

Before sharing project snapshots externally:

1. Exclude .env
2. Exclude .git
3. Exclude runtime.log and state.json from project root
4. Exclude docs.zip and src.zip unless explicitly needed
5. Include .env.example only
6. Verify data/state.json contains no sensitive live values
7. Verify logs/ does not expose secrets or private identifiers

---

## Obsidian Links

- [[00 CNT Vault Home|Vault Home]]
- [[00 Docs Index|Docs Index]]

### Related
- [[00 Docs Index|Docs Index]]
