---
tags:
  - cnt
  - obsidian
  - workflow
  - protocol
aliases:
  - CNT v2 OBSIDIAN INTEGRATED OPERATING PROTOCOL
---

# CNT v2 OBSIDIAN INTEGRATED OPERATING PROTOCOL

## Purpose

This document consolidates the practical operating protocol for:

- CNT runtime execution
- shadow observation
- Obsidian review writing
- Canvas state tracking

It is intended to function as the unified judgement protocol for `breakout_v3`.

## Core Rule

The CNT operating split is fixed as follows:

- code = execution
- Python and runtime data = analysis
- Obsidian markdown = judgement
- Canvas = state interface

Obsidian is therefore not treated as a notes app only.

Within this protocol it acts as the strategy decision interface.

## Operating Components

The integrated system contains four parts.

### 1. Templates

Templates are the judgement tools.

Current template set:

- `templates/observation_review.md`
- `templates/allowed_signal_log.md`
- `templates/activation_review_checklist.md`

### 2. Canvas

Canvas is the visual state map.

Recommended strategy state model:

```text
CNT SYSTEM
|- pullback_v1 (ACTIVE)
|- breakout_v2 (FAILED)
\- breakout_v3 (OBSERVATION -> REVIEW -> FUTURE)
```

Recommended color rules:

- active = green
- failed = red
- observation = yellow

### 3. Workflow

Workflow determines when a document must be written.

### 4. State Transition Rules

State transitions determine the next valid decision after each review.

## Template Usage Lock

### Observation Review

Use:

- every `20 to 30` new shadow events

Purpose:

- periodic structural judgement

### Allowed Signal Log

Use:

- only when an actual allowed shadow signal appears

Purpose:

- event-specific evidence capture

### Activation Review Checklist

Use:

- only when activation becomes a real question

Purpose:

- final go / no-go discipline

These usage rules should not be changed casually.

## Workflow Triggers

### Normal State

Most of the time, no Obsidian action is required.

Expected behavior:

- `run.ps1` continues
- shadow events accumulate
- snapshot updates

### Trigger 1: `20 to 30` Additional Events

Action:

- create an observation review

Expected output example:

- `docs/CNT v2 BREAKOUT V3 FIRST SHADOW OBSERVATION REVIEW.md`

### Trigger 2: First Allowed Signal

Action:

- create or update the allowed signal log

Expected output example:

- `docs/breakout_v3 allowed signal log.md`

### Trigger 3: Activation Question

Action:

- open the activation checklist

Expected output example:

- `docs/CNT v2 BREAKOUT V3 ACTIVATION REVIEW CHECKLIST.md`

## State Transition Rules

Observation reviews must resolve into one of the following operational states.

### STILL_OVER_FILTERED

Typical pattern:

- allowed remains `0`
- soft pass counts cluster at the low end

Next step:

- continue observation

### FIRST_ALLOWED_DETECTED

Typical pattern:

- `allowed_signal_count >= 1`

Next step:

- log the allowed event
- continue observation

### STRUCTURE_IMPROVING

Typical pattern:

- blocker concentration weakens
- soft pass counts move upward

Next step:

- continue observation
- later consider threshold review only if repeated evidence appears

### NEEDS_REDESIGN

Typical pattern:

- allowed remains `0`
- a blocker or stage dominates structurally

Next step:

- redesign preparation

## Canvas Update Rules

Canvas should be updated only after a formal review, not after every runtime cycle.

### If review result is `STILL_OVER_FILTERED`

Keep:

- `breakout_v3 -> Observation Window`

### If review result is `FIRST_ALLOWED_DETECTED`

Add:

- allowed signal node

### If review result is `STRUCTURE_IMPROVING`

Emphasize:

- review branch
- observation progress

### If review result is `NEEDS_REDESIGN`

Move:

- `breakout_v3 -> redesign branch`

## Current Phase Lock

At the present CNT phase:

- `breakout_v3 = SHADOW_ONLY`
- activation = prohibited
- tuning = prohibited
- engine path changes = prohibited during observation

Therefore the valid action now is:

- event accumulation
- periodic review writing
- evidence logging

The invalid actions are:

- activation
- threshold relaxation
- hard/soft gate redesign during the initial observation window

## Final Record

The CNT Obsidian operating stack is now defined as a unified protocol:

- templates control judgement form
- Canvas controls visible strategy state
- workflow controls timing
- transition rules control next decisions

This protocol exists to keep strategic judgement consistent while runtime execution remains separate.
