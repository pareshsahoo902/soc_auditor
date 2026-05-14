# Governance Principles

## Principle 1 — Deterministic First
Governance logic MUST be deterministic whenever possible.
Examples:
- SLA calculations
- approval checks
- escalation timing
- evidence linkage
MUST NOT rely on LLM reasoning.
LLMs are enrichment layers ONLY.

## Principle 2 — Evidence-Centric
Every governance finding MUST include:
- source evidence
- timestamps
- source systems
- traceability
- confidence score
No unsupported findings allowed.

## Principle 3 — Async Event-Driven Architecture
All workflows must operate via:
- queues
- events
- workers
- async orchestration
Never design synchronous governance processing.

## Principle 4 — Provider Agnostic
Never tightly couple architecture to:
- Groq
- OpenAI
- specific models
Use provider abstraction everywhere.

## Principle 5 — Human-in-the-Loop
AI surfaces governance risks.
Humans validate.
Never build autonomous governance decision systems.

## Principle 6 — Explainability Mandatory
Every governance output must explain:
- why the finding exists
- which evidence supports it
- which controls are impacted
