# GitHub UX Design

This repository is designed as a product experience, not just a file dump.

The first-time visitor should understand three things in the first 30 seconds:

- This is a serious evidence-based typing system, not a personality horoscope.
- It has a concrete workflow: interview, candidate set, evidence ledger, type duel, audit, benchmark.
- The project can be trusted because its claims are backed by tests, scorecards, and boundaries.

## First-Screen Strategy

The README opens with:

- A badge row for immediate operational credibility.
- A large visual hero that shows the system as a command center.
- A local-first Session Lab for visitors who want to paste their own evidence, get a usable next round immediately, copy a share link, and recover work through imported JSON.
- A Benchmark Arena case gallery for visitors who want to inspect traps, runner-ups, falsifiers, reusable prompts, and contribution seeds.
- A Calibration Lab for visitors who want to paste a report, see failed gates, copy a repair prompt, and turn misses into calibration issues.
- A static interactive playground for visitors who want to try the loop before installing anything.
- A one-minute demo path that links to a visual tour, demo session, and sample report.
- Six SVG blueprints that make the GitHub experience inspectable: `docs/assets/repository-experience-map.svg`, `docs/assets/typing-engine-blueprint.svg`, `docs/assets/trust-loop-dashboard.svg`, `docs/assets/benchmark-arena-pipeline.svg`, `docs/assets/type-coverage-matrix.svg`, and `docs/assets/calibration-loop-map.svg`.
- A short promise that explains the core product difference.
- A quick trust statement that prevents misuse.

The hero is intentionally visual rather than text-heavy. Generated text inside images often looks broken, so the project image uses abstract panels, charts, nodes, and evidence flows instead of readable UI copy.

The SVG blueprints carry precise labels because they are repository-native, reviewable, and stable under version control. Use generated bitmap images for atmosphere and product feel; use SVG for exact workflows, gates, and trust claims.

## Visitor Journey

```mermaid
flowchart TD
    A[Visitor lands on README] --> B{What are they looking for?}
    B -->|Can this type me better?| C[See adaptive interview loop]
    B -->|Can I trust it?| D[See evidence ledger and safety boundaries]
    B -->|Can I contribute?| E[Open Benchmark Arena]
    B -->|Can this output improve?| K[Open Calibration Lab]
    B -->|Can I install it fast?| F[Copy install command]
    C --> G[Try live typing prompt]
    D --> H[Read evaluation model]
    E --> I[Copy issue seed]
    K --> L[Copy repair prompt]
    F --> J[Use skill in Codex]
```

## Visual Hierarchy

1. Hero image: emotional hook and product shape.
2. Session Lab links: immediate proof that the repo is usable.
3. Benchmark Arena: visible traps and contribution path.
4. GitHub Visitor Experience Map: how different visitors should move.
5. Typing Engine Blueprint: why the reasoning loop is not a quiz.
6. Trust Loop Dashboard: why accuracy work is repeatable.
7. Benchmark Arena Pipeline: why public benchmark cases cannot drift from JSON.
8. Benchmark Type Coverage Matrix: why all 16 leading types are now represented.
9. Calibration Loop Map: why failed reports turn into repair prompts and issue seeds.
10. System map: how inputs become calibrated outputs.
11. Interview loop: why each round feels progressive.
12. Evidence ledger: why the answer is not a black box.
13. Quality gates: why the project is maintainable.

## Experience Promise

The experience should feel sticky because each round makes the user think:

```text
That question was chosen for me.
The system noticed my contradiction.
The runner-up explanation is being treated seriously.
I can see exactly what would change the conclusion.
```

The experience should never rely on:

- Fake certainty.
- Flattery.
- Fear-based identity hooks.
- Endless questioning without state updates.

## README Maintenance Rules

- Keep at least one strong bitmap hero image in `docs/assets/`.
- Keep a second journey-map visual in `docs/assets/`.
- Keep the six precise SVG blueprints in `docs/assets/`: `repository-experience-map.svg`, `typing-engine-blueprint.svg`, `trust-loop-dashboard.svg`, `benchmark-arena-pipeline.svg`, `type-coverage-matrix.svg`, and `calibration-loop-map.svg`.
- Keep `docs/session-lab.html` usable without a build step, external JavaScript, network calls, or account setup; preserve share links, JSON import, and local persistence.
- Keep `docs/case-gallery.html` usable without a build step or external runtime; preserve case filters, prompt copy, issue seed copy, all current benchmark cases, source-of-truth sync from `skill/mbti-typing/examples/benchmark-cases.json`, and safety boundaries.
- Keep `docs/calibration-lab.html` usable without a build step, external runtime, network calls, or account setup; preserve report paste, visible gates, Calibration Receipt, repair prompt, JSON receipt, issue seed copy, source-of-truth sync, and safety boundaries.
- Keep `docs/playground.html` usable without a build step, external JavaScript, or network calls.
- Keep public README and prompt recipe buttons pointing to GitHub repository URLs; parent-directory links break after GitHub Pages deploys the `docs/` folder.
- Keep at least four Mermaid diagrams in the English README.
- Keep demo session and sample report links visible in the first half of the README.
- Keep the Chinese README visually connected to the same hero.
- Do not hide caveats at the bottom; safety boundaries should be visible.
- Every major visual claim should map to a script, reference file, benchmark, or quality gate.
