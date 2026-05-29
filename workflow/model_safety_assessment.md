# Model Safety Assessment Workflow

## Overview

This document defines the standard procedure for evaluating a language model’s safety posture against adversarial, benign, and ambiguous inputs.

The workflow is designed to produce:
- consistent evaluations
- reproducible risk scores
- structured security reports
- measurable false positive / false negative rates

---

## Scope

This workflow applies to:
- Prompt injection testing
- Jailbreak resistance evaluation
- Instruction hierarchy validation
- Data exfiltration resistance
- General safety behavior benchmarking

It does NOT define model behavior.
It defines evaluation methodology.

---

## Inputs

The system consumes two primary datasets:

### 1. Adversarial Dataset
- prompt injection attempts
- jailbreak patterns
- role manipulation prompts
- context shifting attacks

### 2. Benign Dataset
- general knowledge prompts
- reasoning tasks
- creative writing
- technical explanations

---

## Workflow Stages

### Stage 1 — Input Loading

Load dataset(s) into evaluation engine:
- parse JSON test cases
- validate schema integrity
- assign unique test identifiers

---

### Stage 2 — Prompt Execution

Each prompt is processed individually:

1. Send prompt to assessment pipeline
2. Capture raw analysis output
3. Store detector signals
4. Store evaluator output
5. Store risk model output
6. Store confidence score

No prompt is skipped or modified.

---

### Stage 3 — Signal Analysis

For each prompt, extract:
- injection signals
- jailbreak signature matches
- instruction conflict indicators
- role manipulation attempts
- obfuscation patterns

Signals are treated as **observations only**, not final conclusions.

---

### Stage 4 — Risk Scoring

Risk is computed using:
- detection signals
- evaluator scoring output
- confidence weighting

Final risk categories:
- LOW
- MEDIUM
- HIGH
- CRITICAL

---

### Stage 5 — Confidence Calibration

Confidence is calculated to determine:
- reliability of detection
- ambiguity of input
- consistency of scoring signals

Low confidence indicates:
- uncertain classification
- ambiguous adversarial intent
