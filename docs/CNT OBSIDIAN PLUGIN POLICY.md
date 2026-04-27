---
tags:
  - cnt
  - type/documentation
  - status/active
  - obsidian
  - type/analysis
  - cnt-obsidian-plugin-policy
---

# CNT Obsidian Plugin Policy

## Purpose

This document defines how Obsidian plugins are handled in the CNT repository.

## Current Policy

- The CNT repository tracks Obsidian plugin activation intent through `.obsidian/community-plugins.json`.
- The repository does **not** bundle third-party plugin code under `.obsidian/plugins/` by default.
- A fresh clone may therefore show enabled plugin names without locally installed plugin bundles.

## Why This Policy Exists

- Third-party plugin bundles are environment-specific.
- Bundled plugin code can create unnecessary repository noise and update churn.
- The repository should remain portable even when Obsidian plugins are not installed.

## Expected Behavior

- `docs/CNT DATA DASHBOARD.md` is designed for an Obsidian vault whose root is the CNT repository root.
- Dashboard queries that depend on Dataview require the user to install the `dataview` plugin locally.
- Template workflows that depend on Templater require the user to install the `templater-obsidian` plugin locally.

## Reproducibility Rule

- Repository-default behavior must not assume plugin bundles are present under `.obsidian/plugins/`.
- Documents should remain readable as plain Markdown even without Obsidian plugins.
- Plugin-dependent features should degrade gracefully when the plugin is missing.

## Installation Note

If a local environment needs full dashboard/template behavior, install the plugins listed in `.obsidian/community-plugins.json` inside Obsidian for this vault.

## Obsidian Links

- [[CNT TOOLCHAIN INTEGRATION REPORT]]

