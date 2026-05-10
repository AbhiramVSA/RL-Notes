# Reinforcement Learning FAT Study Guide Prompt

Use this prompt from the root of the consolidated workspace:

```text
C:\Users\abhir\cool-stuff\rl-notes\rl-fat
```

The goal is to generate the missing Final FAT notes for Reinforcement Learning while preserving the existing CAT 1 and CAT 2 notes already present in `study_guide/`.

---

## THE PROMPT

```text
I have my Final FAT exam for Reinforcement Learning. The FAT includes all CAT 1 portions, all CAT 2 portions, and the new Module 6 material uploaded in `source_material/fat/`.

The existing CAT notes are already consolidated in `study_guide/`. Read them first and treat them as the base notes. Do not overwrite or regenerate them unless a new FAT source file directly corrects something.

New FAT source files currently uploaded:

1. `source_material/fat/MODULE6 1 Hierarchical Reinforcement Learning.pptx` - 26 slides
2. `source_material/fat/MODULE6 2 Semi MDP Model.pptx` - 9 slides
3. `source_material/fat/MODULE6 3 Types of Optimality.pptx` - 9 slides
4. `source_material/fat/MODULE6 4 Options.pptx` - 17 slides
5. `source_material/fat/MODULE6 5 Learning with Options.pptx` - 19 slides
6. `source_material/fat/MODULE6 6 Hierarchical Abstract Machines.pptx` - 10 slides
7. `source_material/fat/MODULE6 7 A Partially Observable Markov Decision Process.pptx` - 19 slides

These Module 6 files cover:

- Hierarchical Reinforcement Learning
- Temporal abstraction and state abstraction
- HRL advantages: credit assignment, exploration, transfer, training efficiency
- HRL challenges: automatic abstraction discovery, abstraction development, trajectory decomposition, composition
- Option-Critic framework and Feudal Reinforcement Learning
- MDP vs Semi-MDP
- Types of optimality, especially hierarchical-optimal and recursive-optimal policies over options
- Options framework: initiation set, termination condition, intra-option policy, policy-over-options
- Learning with options and subgoal discovery: landmarks, RL signal, bottleneck states, access states, graph partitioning, state clustering, skill chaining
- Options in high-dimensional state spaces, H-DRLN, and options as meta-learning tools
- Hierarchical Abstract Machines: machine hierarchy, action states, call states, choice states, stop states
- POMDPs: tuple definition, partial observability, belief update, belief MDP, approximate solution methods, policy/value function, applications

Create Final FAT notes that connect Module 6 to the already-existing CAT 1 and CAT 2 material.

---

## PHASE 0: Inventory and Plan

Create or update:

```text
fat_implementation_plan.md
```

The plan must include:

- Every source file in `source_material/cat1/`, `source_material/cat2/`, and `source_material/fat/`
- Every existing note file in `study_guide/`
- Exact Module 6 topics found from the FAT PPTs
- Proposed output files under `study_guide/fat_generated/`
- Which existing CAT notes each FAT topic depends on
- Verification method for slide coverage, figures, formulas, and links

Do not ask for approval. Continue through implementation and verification.

---

## PHASE 1: Extract and Verify FAT Material

Run the extraction script on the FAT PPTs:

```bash
python scripts/cat2_extract_course_material.py --input source_material/fat/ --output extracted_content/fat/
```

Review all extraction outputs:

- `extracted_content/fat/raw_text.txt`
- `extracted_content/fat/structured.md`
- `extracted_content/fat/equations.json`
- `extracted_content/fat/problems.json`
- `extracted_content/fat/tables.json`
- `extracted_content/fat/slide_notes.md`
- `extracted_content/fat/figures/`
- `extracted_content/fat/extraction_summary.md`

Manual verification is mandatory. Read every FAT PPT slide directly, not only the extraction output. Check for:

- Equations embedded as images or Unicode text
- Diagrams with text labels
- SmartArt, grouped shapes, tables, and callout boxes
- Slide images that need to be copied into `study_guide/figures/`
- Definitions that look exam-ready
- Comparisons likely to become 5-mark or 10-mark answers
- Ambiguous or suspicious content that should be marked for review instead of silently accepted

If extraction misses a slide or diagram, manually transcribe the missing content into the relevant note and record it in the verification checklist.

---

## PHASE 2: Existing Notes Gap Analysis

Read the existing notes before writing new FAT notes:

CAT 1 base notes:

- `study_guide/00_roadmap.md`
- `study_guide/01_rl_fundamentals.md`
- `study_guide/02_elements_of_rl.md`
- `study_guide/03_bandit_problem.md`
- `study_guide/04_mathematical_foundations.md`
- `study_guide/05_contraction_and_bfpt.md`
- `study_guide/06_bellman_and_convergence.md`
- `study_guide/07_worked_problems.md`
- `study_guide/08_formula_sheet.md`

CAT 2 base notes:

- `study_guide/cat2_00_roadmap.md`
- `study_guide/01_dynamic_programming.md`
- `study_guide/02_policy_iteration.md`
- `study_guide/03_value_iteration.md`
- `study_guide/04_monte_carlo_prediction.md`
- `study_guide/05_monte_carlo_control.md`
- `study_guide/06_importance_sampling.md`
- `study_guide/cat2_07_worked_problems.md`
- `study_guide/cat2_08_formula_sheet.md`
- `study_guide/cat2_09_quick_review.md`

Create:

```text
study_guide/fat_generated/01_fat_gap_analysis.md
```

This file must state:

- What CAT 1 and CAT 2 already cover
- What Module 6 adds
- Which FAT topics depend on earlier notes
- Which topics need new standalone notes
- Which formulas should be added to a final formula sheet
- Which likely exam questions are CAT-derived vs FAT-source-derived

Do not present CAT past-paper patterns as confirmed FAT patterns unless an actual FAT past paper is present.

---

## PHASE 3: Generate FAT Topic Notes

Create these Obsidian-native markdown files:

```text
study_guide/fat_generated/00_fat_roadmap.md
study_guide/fat_generated/01_fat_gap_analysis.md
study_guide/fat_generated/02_hierarchical_reinforcement_learning.md
study_guide/fat_generated/03_semi_markov_decision_process.md
study_guide/fat_generated/04_options_framework.md
study_guide/fat_generated/05_types_of_optimality.md
study_guide/fat_generated/06_learning_with_options.md
study_guide/fat_generated/07_hierarchical_abstract_machines.md
study_guide/fat_generated/08_partially_observable_markov_decision_process.md
study_guide/fat_generated/09_fat_final_synthesis.md
study_guide/fat_generated/10_fat_worked_problems.md
study_guide/fat_generated/11_fat_formula_sheet.md
study_guide/fat_generated/12_fat_predicted_questions.md
study_guide/fat_generated/verification_checklist.md
```

Every file must have YAML frontmatter.

Use this frontmatter pattern for topic notes:

```yaml
---
type: topic
subject: Reinforcement Learning
exam: FAT
module: 6
topic: topic-name
source_files:
  - source_material/fat/file-name.pptx
depends_on:
  - ../01_rl_fundamentals
  - ../cat2_00_roadmap
tags: [rl, fat, module6]
---
```

Each topic note must include:

1. Learning objectives
2. Ground-up explanation
3. Why the topic exists in RL
4. Formal definitions and notation
5. Algorithm/procedure where applicable
6. Worked example or mini-example
7. Exam answer templates for 2-mark, 5-mark, and 10-mark answers
8. Common mistakes and traps
9. Connections to CAT 1 and CAT 2 notes using Obsidian links
10. Figures/diagrams from slides where useful
11. Quick revision block at the end

Use Obsidian wiki links for internal links:

```text
[[01_rl_fundamentals]]
[[06_bellman_and_convergence]]
[[01_dynamic_programming]]
[[03_value_iteration]]
[[cat2_08_formula_sheet]]
```

Use Obsidian image embeds:

```text
![[figure_name.png|Description]]
```

Copy any referenced FAT figures into:

```text
study_guide/figures/
```

---

## PHASE 4: Required Content by File

### `00_fat_roadmap.md`

Must include:

- Full FAT study order from CAT 1 to CAT 2 to Module 6
- Mermaid dependency graph connecting MDPs, Bellman equations, DP, MC, IS, HRL, options, SMDPs, HAMs, and POMDPs
- Topic priority table
- What to revise first if time is limited
- Links to all generated FAT files and all important existing CAT notes

### `02_hierarchical_reinforcement_learning.md`

Must cover:

- HRL definition
- Long-horizon decision making
- Task decomposition
- Dining-table example
- Temporal abstraction
- State abstraction
- Credit assignment advantage
- Exploration advantage
- Transfer/reuse of learned sub-behaviors
- HRL training benefits
- Challenges: automatic discovery, development, demonstrations, composition
- Option-Critic framework overview
- Feudal RL overview

### `03_semi_markov_decision_process.md`

Must cover:

- MDP recap from existing notes
- Why MDPs are not enough for temporally extended actions
- SMDP definition
- Decision epochs
- Variable action duration
- MDP vs SMDP comparison table
- Why options induce an SMDP
- Expected return with temporally extended actions

### `04_options_framework.md`

Must cover:

- Option as generalized action
- Primitive actions as options
- Closed-loop sub-behavior
- Initiation set
- Termination condition
- Intra-option policy
- Policy-over-options
- Option architecture
- Single initiation/termination-state option
- How options speed learning
- How options connect to SMDPs

### `05_types_of_optimality.md`

Must cover:

- Principle of optimality
- Policy-over-options
- Hierarchical optimality
- Recursive optimality
- Difference between flat optimality, hierarchical optimality, and recursive optimality
- Which optimality concept is strongest/weakest and why
- Note any suspicious/possibly unrelated optimality slides separately if they refer to A/E/S/G optimality from design of experiments rather than RL

### `06_learning_with_options.md`

Must cover:

- Option/subgoal discovery
- Landmark states
- RL signal based subgoals
- Bottleneck states
- Access states
- Graph partitioning
- Q-Cut and L-Cut
- State clustering
- PCCA+
- Skill chaining
- High-dimensional state spaces
- H-DRLN
- Options as meta-learning
- MLSH

### `07_hierarchical_abstract_machines.md`

Must cover:

- HAM definition and purpose
- Why hierarchies matter
- Relationship to options and MAXQ
- Gridworld/obstacle example
- Machine hierarchy
- Action states
- Call states
- Choice states
- Stop states
- Where learning happens in HAMs
- Strengths and limitations

### `08_partially_observable_markov_decision_process.md`

Must cover:

- POMDP motivation
- Tuple `(S, A, T, R, Omega, O, gamma)`
- Difference between state and observation
- MDP vs POMDP comparison
- Belief state
- Belief update
- Belief MDP
- Curse of dimensionality
- Curse of history
- Approximate solution methods:
  - grid-based algorithms
  - online planning algorithms
  - history/pseudo-state methods
- Policy and value function
- Applications

### `09_fat_final_synthesis.md`

Must connect the entire course:

- From basic RL agent/environment to MDPs
- From Bellman equations to DP
- From DP to Monte Carlo
- From MC to off-policy importance sampling
- From flat RL to HRL and options
- From full observability to POMDPs
- One-page "how everything fits together" narrative

### `10_fat_worked_problems.md`

Create exam-style solved problems. Include at least:

- HRL definition and decomposition answer
- MDP vs SMDP comparison
- Option tuple explanation
- Initiation/termination/intra-option policy identification from an example
- Hierarchical vs recursive optimality comparison
- Subgoal discovery methods comparison
- HAM machine-state identification
- POMDP tuple and belief-state problem
- POMDP vs MDP comparison
- One integrated long-answer question connecting options, SMDPs, and HRL

For each problem:

- State the question
- Identify source/topic
- Give marks and expected answer length
- Solve step by step
- Add final exam-ready answer
- Add common mistakes

### `11_fat_formula_sheet.md`

Make a final formula/definition sheet that includes:

- Existing CAT 1 and CAT 2 high-value formulas by link, without duplicating every derivation
- SMDP notation and return handling for variable duration
- Option tuple notation
- Policy-over-options notation
- POMDP tuple
- Belief update notation
- Key definitions that behave like formulas in exams

### `12_fat_predicted_questions.md`

Create predicted questions only from evidence:

- Label predictions as `FAT-source-derived`, `CAT-pattern-derived`, or `low-confidence`
- Do not claim actual FAT frequency unless a FAT past paper exists
- Include likely 2-mark, 5-mark, and 10-mark questions
- Include short answer keys

### `verification_checklist.md`

Must verify:

- Every FAT PPT listed above is covered
- Every slide number is either covered, image-only/decorative, or explicitly marked unclear
- Every copied figure is listed
- Every generated file exists
- Every internal link target exists
- No existing CAT note was overwritten
- Ambiguous content is flagged instead of silently accepted

---

## PHASE 5: Update Master Index

Update:

```text
study_guide/00_fat_rl_index.md
```

Add a "FAT Generated Notes" section linking every generated FAT file.

Do not remove the existing CAT 1 or CAT 2 sections.

---

## Style Rules

- Use Obsidian-native markdown.
- Use YAML frontmatter in every generated markdown file.
- Use wiki links for internal note links.
- Use Mermaid diagrams where they clarify dependencies, options, HAMs, or POMDP belief updates.
- Use LaTeX for equations.
- Keep explanations exam-focused, not research-paper style.
- Make each note usable for fast revision the night before the exam.
- Keep source-derived facts separate from predictions.
- If something in the slides appears incorrect or unrelated to RL, flag it clearly in the note.

---

## Completion Criteria

The task is complete only when:

- FAT PPT extraction has been run or a clear reason is documented if it fails.
- Every Module 6 PPT is manually reviewed slide by slide.
- All required files under `study_guide/fat_generated/` exist.
- `study_guide/00_fat_rl_index.md` links to the full FAT path.
- `verification_checklist.md` proves slide coverage.
- All referenced images render from `study_guide/figures/`.
- Existing CAT 1 and CAT 2 notes remain intact.
```
