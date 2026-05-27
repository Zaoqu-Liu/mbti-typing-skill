# Playbooks

## Table of Contents

- Operating principle
- Live adaptive interview
- Transcript audit
- Adjacent-type duel
- Report review
- Questionnaire or skill design
- Engagement design
- Stopping rules

## Operating Principle

Make the process feel unusually accurate because each question targets the current uncertainty. Do not make it feel accurate by flattering the subject or pretending certainty.

Always show:

- Current top candidates.
- What evidence moved.
- What is still unresolved.
- Why the next question exists.

Avoid revealing option-to-type mappings before the subject answers if it would bias them. Explain mappings after the answer.

## Live Adaptive Interview

Use this when the user wants to be typed from scratch or wants a claim tested.

### Opening

1. State that this is an interview-based working formulation, not a clinical or hiring instrument.
2. Capture prior claims and context.
3. Build a first candidate set with 3-6 types.
4. Start with one round of 4-6 concrete questions.

### Round Structure

Each round should have:

- A target conflict, for example `INFP vs INTJ vs ENTJ`.
- 4-6 forced-choice or ranking questions.
- At least one question about normal default cognition.
- At least one question about stress, conflict, or recovery.
- A post-round update:

```markdown
Current board:
- Leading: TYPE because...
- Runner-up: TYPE because...
- Dropped: TYPE because...
- Key contradiction:
- Next round target:
```

### Answer Handling

When the subject says "several fit":

1. Ask for top two.
2. Ask which one is automatic and which one is learned.
3. Ask which one costs more.

When the subject rejects the framing:

1. Accept the correction.
2. Record what was wrong.
3. Ask a replacement scene.
4. Update the candidate model.

### Deep Typing Path

Use 4 phases:

1. **Triage:** broad function and trait clues.
2. **Contradiction drill:** attack confusing signals.
3. **Top-two duel:** only pair-specific discriminators.
4. **Falsifier round:** ask what would make the current conclusion wrong.

Do not let the interview grow by adding random questions. Every question must name a target uncertainty.

## Transcript Audit

Use this when the user provides exported chats, PDFs, reports, or long notes.

### Ingest

1. Inventory files and sizes.
2. Read summaries first.
3. Search for reversal markers: `反转`, `证伪`, `误判`, `修正`, `评审`, `置信`, `不能解释`, `用户修正`, `overread`, `wrong`, `not accurate`.
4. Sample original turns around each reversal and correction.
5. Keep sensitive material out of reusable artifacts unless necessary.

### Produce

Create:

- A timeline of claims and reversals.
- A table of decisive evidence.
- A table of overclaims or weak inferences.
- The current best formulation and runner-up.
- A list of what the old conversation teaches the future workflow.

### Audit Questions

- Which conclusion survived the most attacks?
- Which conclusion was overconfident at any stage?
- Which evidence was later reinterpreted?
- Did the subject's correction improve the model?
- Are there repeated patterns across contexts, or only dramatic one-off stories?

## Adjacent-Type Duel

Use this when the user asks "X or Y?" or when the top two candidates share many features.

Protocol:

1. Load `type-map.md`.
2. Identify the shared function set or shared surface behavior.
3. Ask only discriminators that split the pair.
4. Require at least two independent wins before deciding.
5. Write both the winning explanation and the best steelman of the losing type.

Good duels:

- ENTJ vs INTJ: Te-dom external optimization vs Ni-dom private model priority.
- INFP vs INFJ: Fi-Ne personal congruence vs Ni-Fe relational pattern convergence.
- ESTJ vs ENTJ: Si-backed operational continuity vs Ni-backed future architecture.
- ENFP vs ENTP: value-pull and personal meaning vs Ti-style impersonal model testing.
- ISFJ vs INFJ: Si continuity and known obligations vs Ni pattern and future implication.

## Report Review

Use this when reviewing an existing MBTI/personality report.

Review stance:

- Findings first.
- Prioritize unsupported claims, circular reasoning, missing differential diagnosis, framework mixing, and unsafe uses.
- Then give a concise rewrite plan.

Checklist:

- Is there a real candidate set?
- Does the report explain why runner-up types lose?
- Are numerical scores justified?
- Are MBTI, Big Five, Enneagram, A/T, attachment, and culture kept separate?
- Does the report pathologize normal personality?
- Does it overfit one intimate or dramatic anecdote?
- Does it include falsifiers?

Run `scripts/report_audit.py` on Markdown drafts when available.

## Questionnaire Or Skill Design

Use this when the user wants a reusable test, questionnaire, or skill.

Design rules:

- Define the decision target: full 16-type screen, top-two duel, stress pattern, or report review.
- Use item blocks where options are similarly desirable.
- Include reverse or contradiction probes.
- Include "cost signature" questions: what drains, restores, threatens, or feels unbearable.
- Separate scoring from interpretation.
- Never claim the custom questionnaire is standardized unless it has validation data.

Deliver:

- Item bank.
- Scoring rubric or evidence ledger.
- Calibration notes.
- Known failure modes.
- Example output template.

## Engagement Design

Make the experience compelling with honest mechanics:

- **Progressive revelation:** after each round, show what changed and what remains unresolved.
- **Sharp questions:** ask scenes that make the subject say "that is exactly the difference".
- **Contradiction respect:** treat conflicts as the interesting part.
- **Prediction then verification:** state what each candidate would predict, then ask for evidence.
- **Personal utility:** translate the final formulation into one or two practical implications grounded in the subject's goals.

Do not:

- Hide uncertainty to sound impressive.
- Use "you are rare/special" as a hook.
- Keep asking questions after the stopping rule is met.
- Make identity dependence stronger than self-understanding.

## Stopping Rules

Stop and conclude when:

- The leading type beats the runner-up on at least two independent discriminators.
- Contradictions have been named and either resolved or preserved as uncertainty.
- The user has had a chance to reject the core framing.
- The final answer can list falsifiers.

Continue when:

- Top candidates share all decisive evidence.
- The result depends on one dramatic anecdote.
- Stress data contradicts normal-state data.
- The subject says the interpretation feels wrong.
