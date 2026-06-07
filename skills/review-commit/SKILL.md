---
name: review-commit
description:
  Write git commit messages in Conventional Commit format
  (feat/fix/chore/docs/refactor/test) when the user asks
  to commit, stage, or create a commit message.
allowed-tools: Bash, Read
---

## Overview
Always write commits using the Conventional Commit specification.

## Format
type(scope): subject

Types: feat, fix, chore, docs, refactor, test, perf, ci
Scope: optional, lowercase module name
Subject: imperative mood, under 70 chars, no trailing period

## Constraints
- Never use past tense ("added" → "add")
- Never exceed 70 characters in the subject line
- Ask if the type is ambiguous before guessing
- Do not add a period at the end of the subject
