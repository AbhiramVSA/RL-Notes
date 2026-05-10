---
title: RL FAT Master Index
exam: Final FAT
subject: Reinforcement Learning
source_sets:
  - CAT 1 notes from rl/study_guide
  - CAT 2 notes from rl-2/study_guide
---

# RL FAT Master Index

Use this as the single Obsidian entry point for Final FAT revision.

## CAT 1 Coverage

- [CAT 1 Roadmap](./00_roadmap.md)
- [CAT 1 Past Paper Analysis](./00_past_paper_analysis.md)
- [RL Fundamentals](./01_rl_fundamentals.md)
- [Elements of RL](./02_elements_of_rl.md)
- [Bandit Problem](./03_bandit_problem.md)
- [Mathematical Foundations](./04_mathematical_foundations.md)
- [Contraction and BFPT](./05_contraction_and_bfpt.md)
- [Bellman and Convergence](./06_bellman_and_convergence.md)
- [CAT 1 Worked Problems](./07_worked_problems.md)
- [CAT 1 Formula Sheet](./08_formula_sheet.md)
- [CAT 1 Verification Checklist](./verification_checklist.md)

## CAT 2 Coverage

- [[cat2_00_roadmap]]
- [[01_dynamic_programming]]
- [[02_policy_iteration]]
- [[03_value_iteration]]
- [[04_monte_carlo_prediction]]
- [[05_monte_carlo_control]]
- [[06_importance_sampling]]
- [[cat2_07_worked_problems]]
- [[cat2_08_formula_sheet]]
- [[cat2_09_quick_review]]
- [[cat2_verification_checklist]]

## FAT Generation Workspace

Edit this prompt to generate the new FAT notes:

```text
../prompts/fat_study_guide_prompt_template.md
```

Suggested output target for generated FAT-only additions:

```text
study_guide/fat_generated/
```

Keep the existing CAT 1 and CAT 2 notes as source-confirmed reference material. Put new FAT-only modules, extra portions, final past-paper analysis, and final predicted questions in `fat_generated/` unless you intentionally merge them into the main note sequence.
