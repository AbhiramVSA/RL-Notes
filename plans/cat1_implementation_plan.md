# Implementation Plan - Reinforcement Learning Study Guide

## Course Info

- **Subject**: Reinforcement Learning (CSE4037)
- **University**: VIT-AP University
- **Instructor**: Dr. D. John Pradeep
- **Exam Type**: CAT-1 (Continuous Assessment Test 1), Closed Book, 90 minutes, 50 marks
- **Coverage**: Modules 1 and 2
- **Knowledge Level**: Basic familiarity

---

## Source Materials

| File | Type | Pages/Slides | Content |
|------|------|-------------|---------|
| Module1.pdf | PDF (slides) | ~35 slides | Banach Fixed Point Theorem and application to Bellman Equation |
| Module2.pdf | PDF (slides) | ~35 slides | RL Fundamentals, Bandit Problem, Action Selection Methods |

## Past Papers Identified

| File | Description | Questions | Date |
|------|-------------|-----------|------|
| image.png + image copy.png | Paper 1 (Set 2, Session AN) | 5 questions, 10 marks each | 05/02/2026 |
| WhatsApp Image...PM.jpeg + WhatsApp Image...56 PM.jpeg | Paper 2 (Set 4, Session FN) | 4 questions (Q1-Q4) | 05/02/2026 |

### Initial Past Paper Observations

Both papers share the same date (05/02/2026) but are different sets (Set 2 and Set 4) from different sessions (AN and FN). They cover Modules 1 and 2 with significant overlap in tested topics.

**Recurring themes across both papers:**
- RL application modeling (identify agent, environment, states, actions, rewards)
- Multi-armed bandit with Softmax algorithm (numerical computation from data table)
- Beta parameter comparison in Softmax (exploration vs exploitation effect)
- Contraction mapping (definition, verification, iterative convergence)
- Banach Fixed Point Theorem and its connection to Bellman equation
- Policy comparison using value functions and L-infinity norm
- PAC optimality, UCB, greedy vs epsilon-greedy comparison

---

## Topics Identified from Initial Scan

### From Module 1 (Banach Fixed Point Theorem)
1. Optimal policy existence in MDPs
2. Policy comparison via value functions
3. Fixed point problem (definition, iterative solution)
4. Metric space (definition, 4 properties)
5. Cauchy sequence (definition, intuition)
6. Complete metric space
7. Contraction mapping (definition, Lipschitz constant, worked example)
8. Banach Fixed Point Theorem (statement, proof of uniqueness, proof of existence)
9. Bellman Optimality Equation as operator
10. Proving Bellman operator is a contraction (L-infinity norm proof)

### From Module 2 (RL Fundamentals)
1. Supervised vs Unsupervised vs Reinforcement Learning
2. RL definition and characteristics
3. RL applications (helicopter, Atari, walking)
4. Exploration vs exploitation trade-off
5. MDP terms (Agent, Environment, State, Action, Reward)
6. Elements of RL (Policy, Value function, Model)
7. Temporal difference update
8. Multi-Armed Bandit problem (formal definition)
9. Notions for solving bandits (Asymptotic correctness, Regret, PAC)
10. Value function based methods (Greedy, Epsilon-greedy)
11. Softmax action selection (intuitive + Boltzmann with temperature)
12. UCB (Upper Confidence Bound) - mentioned in solving notions

---

## Proposed File Structure

```
study_guide/
+-- 00_past_paper_analysis.md      # Phase 1.5: Full past paper analysis
+-- 00_roadmap.md                  # Topic dependency map, priorities, study order
+-- 01_rl_fundamentals.md          # Introduction, SL vs UL vs RL, applications, MDP terms
+-- 02_elements_of_rl.md           # Policy, value function, reward, model, exploration/exploitation
+-- 03_bandit_problem.md           # MAB definition, greedy, epsilon-greedy, softmax, UCB, PAC, regret
+-- 04_mathematical_foundations.md  # Fixed point, metric space, Cauchy, complete metric space
+-- 05_contraction_and_bfpt.md     # Contraction mapping, Banach FPT, proofs
+-- 06_bellman_and_convergence.md   # Bellman operator, proving contraction, value iteration convergence
+-- 07_worked_problems.md          # All worked examples + all past paper solutions
+-- 08_formula_sheet.md            # All formulas organized by topic
+-- figures/                       # Extracted and referenced figures
+-- verification_checklist.md      # Phase 4 verification
```

---

## Verification Methodology

1. **Page Coverage**: Cross-reference every slide from both PDFs against study guide sections
2. **Problem Coverage**: Solve every worked example from the slides + all past paper questions
3. **Past Paper Coverage**: Transcribe and solve every question from all 4 past paper images
4. **Formula Coverage**: Catalog every equation from both modules into the formula sheet
5. **Figure Coverage**: Extract or describe all meaningful figures (diagrams, graphs)
6. **Link Integrity**: Verify all internal markdown links between files
7. **Exam Alignment**: Ensure topic priorities reflect actual past paper frequency

---

## Execution Order

1. Run extraction script on `resources/` -> `extracted_content/`
2. Read and transcribe all past paper questions (Phase 1.5)
3. Create `00_past_paper_analysis.md` with frequency tables and predictions
4. Create `00_roadmap.md` with dependency map and priorities
5. Create topic files 01-06 following the template structure
6. Create `07_worked_problems.md` with all solutions
7. Create `08_formula_sheet.md`
8. Handle figures (extract from PDFs, copy to study_guide/figures/)
9. Create `verification_checklist.md`
