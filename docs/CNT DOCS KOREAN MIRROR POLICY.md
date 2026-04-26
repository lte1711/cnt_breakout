---
aliases:
  - CNT DOCS KOREAN MIRROR POLICY
---

# CNT Docs Korean Mirror Policy

## Purpose

This policy fixes CNT documentation into a dual-language operating model.

The user-facing working language is Korean.

The repository-compatible documentation structure remains dual:

- `docs/` = official repository document path
- `docs/ko/` = Korean mirror path for user-facing reading and judgement work

This policy does not change runtime, engine, strategy, or validation logic.

## Fixed Rule

From this point forward, every new CNT document must follow both rules below.

1. An official document must exist under `docs/`
2. A Korean mirror document must exist under `docs/ko/`

The two documents must be created in the same work step whenever practical.

## Emoji Ban

All CNT documents must avoid emoji, emoticons, pictograms, and decorative symbol markers.

This applies to:

- official documents under `docs/`
- Korean mirror documents under `docs/ko/`
- docs-hosted JSON, HTML, and dashboard/reference assets
- headings, tables, checklists, status labels, and examples

Use plain text labels such as `PASS`, `FAIL`, `WARNING`, `READY`, `BLOCKED`, and color names instead of emoji symbols.

## Naming Rule

Because CNT forbids Unicode filenames, filenames remain ASCII only.

Recommended pattern:

- official: `docs/CNT ... .md`
- Korean mirror: `docs/ko/CNT ... KO.md`

Example:

- `docs/CNT v2 BREAKOUT V3 FIRST SHADOW OBSERVATION REVIEW.md`
- `docs/ko/CNT v2 BREAKOUT V3 FIRST SHADOW OBSERVATION REVIEW KO.md`

## Korean-First Working Rule

The user may work primarily from the Korean mirror documents.

Operational interpretation:

- Korean mirror = preferred reading and review surface
- official doc path = repository source path that remains stable for indexing and references

This means new review, plan, checklist, and protocol documents should be readable in Korean from the beginning.

## Scope

This rule applies to:

- plans
- reports
- checklists
- reviews
- observation documents
- protocol documents
- workflow guides

This rule does not force immediate translation of all legacy documents in one step.

Legacy translation must proceed in phases so current observation and runtime work are not disrupted.

## Creation Checklist

Whenever a new document is created, the following must be checked.

- [ ] official document created under `docs/`
- [ ] Korean mirror created under `docs/ko/`
- [ ] both filenames remain ASCII-only
- [ ] root docs index updated when the document is official and important
- [ ] Korean docs index updated when the Korean mirror is added
- [ ] internal links remain readable in Obsidian

## Non-Disruption Rule

This policy must not be used as a reason to:

- change runtime flow
- change strategy logic
- change observation thresholds
- change review criteria
- reclassify strategy state without evidence

Documentation localization and runtime judgement are separate concerns.

## Execution Rule

If a task is about documentation only, dual-language creation is allowed.

If a task affects runtime or strategy behavior, localization must remain secondary and must not alter current validation flow.

## Current Direction

The current direction is:

- keep current CNT runtime and breakout observation unchanged
- create Korean mirror documents for all newly created important documents
- migrate older documents in controlled phases

## Final Lock

CNT documentation now operates under a Korean-first, dual-path rule.

All future official CNT documents should be accompanied by a Korean mirror unless the user explicitly suspends that rule.

## Obsidian Links

- [[CNT TOOLCHAIN INTEGRATION REPORT]]

