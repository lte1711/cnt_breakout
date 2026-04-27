---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/validation
  - type/operation
  - strategy/breakout_v3
  - obsidian
  - type/analysis
  - status/completed
  - cnt-docs-korean-migration-plan
---

# CNT Docs Korean Migration Plan

## Purpose

This document defines the phased migration path for Korean mirrors across the CNT documentation set.

The goal is not to translate everything at once.

The goal is to make Korean the practical working language without disrupting active runtime observation work.

## Current Snapshot

Current repository state at planning time:

- root markdown documents under `docs/`: `132`
- Korean mirror documents under `docs/ko/`: `4`

This means Korean coverage exists, but only for a small subset of active operating documents.

## Migration Principle

Migration must proceed in the following order:

1. active operating documents
2. active breakout observation documents
3. current workflow and protocol documents
4. legacy validation and architecture documents
5. long-term memos

This prevents localization work from blocking current strategy observation.

## Phase 1

Priority:

- current Obsidian workflow
- current operating protocol
- current breakout_v3 observation start and review path

Status:

- started
- partially complete

## Phase 2

Priority:

- all newly created breakout_v3 review and observation documents
- all newly created activation-related documents
- all newly created CNT operation and validation documents

Rule:

- every new important document must ship with a Korean mirror in the same change

## Phase 3

Priority:

- breakout_v2 archive and redesign chain
- major v2 validation reports
- live readiness and gate documents

Goal:

- ensure the most referenced historical documents become readable in Korean

## Phase 4

Priority:

- v1 archive
- long-term memos
- older engineering and implementation records

This is lower priority because it does not directly affect current breakout_v3 operation.

## Mandatory Rule For New Documents

From now on:

- no important new doc should be added under `docs/` alone
- a matching Korean mirror should be added under `docs/ko/`

## Review Trigger

The migration plan should be reviewed when:

- the Korean mirror count materially increases
- a new operating phase begins
- breakout_v3 changes state

## Final Direction

CNT should move toward a stable dual-document system:

- official repository docs in `docs/`
- user-facing Korean mirrors in `docs/ko/`

This is the forward documentation direction unless explicitly changed by the user.

## Obsidian Links

- [[CNT TOOLCHAIN INTEGRATION REPORT]]

