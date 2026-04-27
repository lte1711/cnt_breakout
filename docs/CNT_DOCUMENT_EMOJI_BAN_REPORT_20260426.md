---
tags:
  - cnt
  - documentation
  - policy
  - cleanup
  - status/active
  - type/documentation
  - type/validation
  - type/operation
  - graph-view
  - type/analysis
---

# CNT Document Emoji Ban Report 20260426

## Design Summary

- Scope: apply the user-requested rule that all CNT documents must not use emoji.
- No runtime code, trading config, strategy logic, exchange state, order state, or data state was intentionally changed.
- The cleanup applies to Markdown, JSON, and HTML assets under `docs/`.

## Rule Added

The following rule is now part of the project constitution:

```text
DOCUMENT_EMOJI_USAGE=FORBIDDEN
```

The document storage policy now also states that emoji, emoticons, pictograms, and decorative symbol usage is forbidden in all project documents and docs-hosted assets.

## Cleanup Applied

Removed emoji and pictogram characters from docs-hosted files, including:

- Markdown headings and lists
- status/check markers
- graph/color guide examples
- docs-hosted dashboard HTML warning text
- docs-hosted JSON emoji fields

Plain text labels remain allowed. Examples:

- `PASS`
- `FAIL`
- `WARNING`
- `READY`
- `BLOCKED`
- color names such as green, blue, orange, purple, red

## Validation Result

```text
emoji_scan_target = docs/ and AGENTS.md
emoji_scan_status = clean after cleanup
policy_updated    = yes
runtime_changed   = no
```

## Record Text

CNT documentation now forbids emoji and decorative pictogram usage. Existing docs-hosted emoji characters were removed, and the rule was recorded in both `AGENTS.md` and the documentation policy. Future documents must use plain text status labels instead of emoji.

Related documents:

- [[AGENTS]]
- [[CNT DOCS KOREAN MIRROR POLICY]]
- [[CNT_ENCODING_CAUSE_AND_REPAIR_REPORT_20260426]]
- [[00 Docs Index]]
