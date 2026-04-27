---
aliases:
  - CNT v2 OBSIDIAN REVIEW WORKFLOW GUIDE
---

# CNT v2 OBSIDIAN REVIEW WORKFLOW GUIDE

## Purpose

This guide locks the operational use of Obsidian review templates for `breakout_v3`.

Core rule:

- analysis is performed in Python and runtime artifacts
- judgement is recorded in Obsidian-compatible markdown
- Obsidian acts as the document hub
- CNT runtime and strategy code remain unchanged by this workflow

## Added Template Files

The following template files are stored under `templates/`:

- `templates/observation_review.md`
- `templates/allowed_signal_log.md`
- `templates/activation_review_checklist.md`

These files are writing aids only.

Official CNT judgement documents should still be created under `docs/`.

## Dual-Language Lock

CNT now uses a Korean-first dual-document workflow.

This means:

- the official repository document remains under `docs/`
- the user-facing Korean mirror should be added under `docs/ko/`

For all new important documents, the preferred rule is:

- create the official document
- create the Korean mirror in the same step

This workflow guide therefore supports both:

- English repository path stability
- Korean reading and judgement convenience

## Recommended Folder Usage

Suggested vault structure:

```text
Vault/
|- docs/
|- daily/
|- templates/
|  |- observation_review.md
|  |- allowed_signal_log.md
|  \- activation_review_checklist.md
\- dashboard/
```

Interpretation:

- `docs/` = official CNT records
- `templates/` = reusable Obsidian writing aids

## Template Usage Rules

### 1. Observation Review

Use when:

- `breakout_v3` shadow events have accumulated by `20 to 30` additional events
- or a meaningful structural shift appears:
  - first allowed signal
  - major blocker distribution change
  - repeated `soft_pass_count >= 3`

Recommended output path:

- `docs/CNT v2 BREAKOUT V3 FIRST SHADOW OBSERVATION REVIEW.md`
- `docs/CNT v2 BREAKOUT V3 SECOND SHADOW OBSERVATION REVIEW.md`

This is a periodic review document, not a per-cycle note.

### 2. Allowed Signal Log

Use only when:

- an actual `allowed = true` shadow event appears
- or a rare allowed event deserves separate review

Recommended output path:

- `docs/breakout_v3 allowed signal log.md`

If allowed events become frequent later, they may be split into dedicated per-event files.

### 3. Activation Review Checklist

Do **not** use this at the current phase.

Use only when:

- allowed signals already exist
- at least one observation review has been completed
- an activation question becomes realistic

Recommended output path:

- `docs/CNT v2 BREAKOUT V3 ACTIVATION REVIEW CHECKLIST.md`

## Manual Use Without Templater

This is the safest method.

Steps:

1. open the relevant template under `templates/`
2. copy the full markdown body
3. create a new official document under `docs/`
4. paste and fill the fields manually

Advantages:

- no plugin dependency
- fewer workflow surprises
- fully compatible with repo markdown rules

## Optional Use With Templater

If Obsidian `Templater` is enabled:

1. set template folder to `templates`
2. create a target document under `docs/`
3. insert the relevant template

The included date placeholders:

- `<% tp.date.now("YYYY-MM-DD") %>`
- `<% tp.date.now("YYYY-MM-DD HH:mm") %>`

work only when Templater is enabled.

Without Templater, replace them manually with actual dates.

## Recommended Review Sequence

Operational order:

1. runtime accumulates `shadow_breakout_v3.jsonl`
2. runtime updates `shadow_breakout_v3_snapshot.json`
3. after `20 to 30` new shadow events, create an observation review
4. if an allowed signal appears, create or update the allowed signal log
5. only much later, if evidence supports it, open the activation checklist

## Canvas Role

Canvas is not treated as a decorative diagram.

Within CNT it should function as a strategy state map.

Recommended high-level structure:

```text
CNT SYSTEM
|- pullback_v1 (ACTIVE)
|- breakout_v2 (FAILED)
\- breakout_v3 (OBSERVATION -> REVIEW -> FUTURE)
```

Recommended visual status rules:

- active = green
- failed = red
- observation = yellow

Recommended breakout_v3 linked evidence:

- CNT v2 BREAKOUT V3 DESIGN DRAFT
- CNT v2 BREAKOUT V3 SHADOW OBSERVATION WINDOW START
- CNT v2 BREAKOUT V3 FIRST SHADOW OBSERVATION REVIEW

Canvas therefore acts as a state interface, not just a notes surface.

## State Transition Rules

The review workflow should use fixed transition labels.

### STILL_OVER_FILTERED

Typical evidence:

- allowed stays at `0`
- soft pass counts remain concentrated at `0 to 1`

Next step:

- continue observation

### FIRST_ALLOWED_DETECTED

Typical evidence:

- `allowed_signal_count >= 1`

Next step:

- create or update the allowed signal log
- continue observation

### STRUCTURE_IMPROVING

Typical evidence:

- `soft_pass_count` distribution shifts upward
- blocker concentration weakens

Next step:

- continue observation
- later consider threshold review only if evidence repeats

### NEEDS_REDESIGN

Typical evidence:

- allowed remains `0`
- blocker dominance becomes structurally concentrated

Next step:

- redesign preparation

These rules exist to stop arbitrary activation or tuning decisions.

## Review Questions To Preserve

Each first observation review should answer at least:

1. Does `breakout_v3` produce any allowed candidates?
2. Is first-blocker dominance still concentrated?
3. Do hard gates pass while soft quality still blocks?
4. Is `v3` structurally better than `v2` even if activation is still prohibited?

## File Linking Guidance

Prefer linking evidence, not copying runtime code into notes.

Examples:

- `[engine.py](../src/engine.py)`
- `[breakout_v3_shadow_eval.py](../src/shadow/breakout_v3_shadow_eval.py)`
- `[shadow_breakout_v3_snapshot.json](../data/shadow_breakout_v3_snapshot.json)`

## Operating Principle

These templates are not just formatting aids.

They exist to enforce:

- fixed judgement criteria
- repeatable reviews
- controlled activation discipline
- protection against impulsive tuning

## Current Rule Lock

At the current CNT phase:

- `breakout_v3 = SHADOW_ONLY`
- `activation = PROHIBITED`
- `tuning = PROHIBITED`

Therefore:

- observation review is the active document type
- allowed signal log is event-driven and conditional
- activation checklist is deferred

## Final Record

The `templates/` folder is now the standard Obsidian review support layer for `breakout_v3`.

Official CNT decisions must still be recorded under `docs/`.

## Obsidian Links

- [[00 Docs Index]]

