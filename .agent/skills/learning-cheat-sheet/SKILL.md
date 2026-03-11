---
name: learning-cheat-sheet
description: Generate exam cheat sheets from slides, quizzes, and labs. Use when the user explicitly wants a printable cheat sheet, cram sheet, or highly compressed review sheet.
---

# Cheat Sheet Generator

## Purpose

This skill is for **compressed exam review material**.

Use it only when the user explicitly wants:

- a cheat sheet
- a cram sheet
- a quick review sheet
- a printable condensed summary

Primary outputs may include:

- `*_cheat_sheet.md`
- `*_cheat_sheet.json`
- `*_cheat_sheet.html`

## Core Rule

This skill optimizes for:

- compression
- printability
- quick lookup

It does **not** optimize for full concept coverage.

If the user wants comprehensive concept coverage, use `learning-concept_coverage` instead.

## Inputs

Read and merge:

- slides
- quizzes
- labs

Focus on:

- highly testable definitions
- formulas
- traps
- worked examples
- quick comparisons

## Output Guidance

The cheat sheet should be:

- concise
- structured
- printable
- exam-oriented

Prefer compact bullets and tables over long explanations.

