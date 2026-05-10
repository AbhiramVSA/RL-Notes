# Reinforcement Learning -- CAT-1 Study Roadmap

**Scope:** Modules 1 and 2 | VIT-AP University
**Based on:** Analysis of 2 past CAT-1 papers -- see [Past Paper Analysis](./00_past_paper_analysis.md)

---

## 1. Concept Dependency Map

The map below shows how topics build on each other. Study from top to bottom; never skip a dependency.

```
RL Fundamentals
|
|-- What is RL? (SL vs UL vs RL, applications)
|   |
|   |-- MDP Terminology (agent, environment, state, action, reward)
|   |   |
|   |   |-- RL Application Modeling (formulate real problems as MDPs)
|   |   |
|   |   |-- Immediate RL vs Full RL, concept of return
|   |
|   |-- Elements of RL (policy, value function, reward signal, model)
|       |
|       |-- Exploration vs Exploitation Trade-off
|           |
|           |-- Multi-Armed Bandit Problem
|           |   |
|           |   |-- Greedy & Epsilon-Greedy Action Selection
|           |   |
|           |   |-- Softmax Action Selection (Boltzmann)
|           |   |   |
|           |   |   |-- Beta Parameter & Temperature Effects
|           |   |
|           |   |-- UCB (Upper Confidence Bound)
|           |   |   |
|           |   |   |-- PAC Optimality & UCB Comparison
|           |   |
|           |   |-- Regret
|           |
|           |-- Bellman Equation (value-function recursion)
|               |
|               |-- Bellman Operator B
|
Mathematical Foundations (parallel track, can start early)
|
|-- Metric Space & Norms
|   |
|   |-- L-infinity Norm for Value Functions
|   |
|   |-- Cauchy Sequence & Convergent Series
|       |
|       |-- Complete Metric Space
|
|-- Fixed Point Problem (definition, relation to RL)
    |
    |-- Contraction Mapping (definition, verification)
        |
        |-- Banach Fixed Point Theorem (existence, uniqueness, convergence)
            |
            |-- Proving Bellman Operator is a Contraction
                |
                |-- Iterative Convergence of Value Iteration
```

---

## 2. Topic Priority Table

Priority is determined by past-paper frequency, mark weight, and likelihood of repetition.

| Priority | Topic | Complexity | Exam Weight | Past Paper Appearances (out of 2) | File |
|----------|-------|------------|-------------|-----------------------------------|------|
| P1 | RL application modeling (agent/env/states/actions/rewards) | Low | High | 2/2 | [01_rl_fundamentals.md](./01_rl_fundamentals.md) |
| P1 | Multi-armed bandit -- Softmax numerical computation | Medium | High | 2/2 | [03_bandit_problem.md](./03_bandit_problem.md) |
| P1 | Beta parameter comparison (exploration vs exploitation effect) | Low | Medium | 2/2 | [03_bandit_problem.md](./03_bandit_problem.md) |
| P1 | Contraction mapping (definition, verification, iterative convergence) | High | High | 2/2 | [05_contraction_and_bfpt.md](./05_contraction_and_bfpt.md) |
| P1 | Banach Fixed Point Theorem and Bellman equation connection | High | High | 2/2 | [05_contraction_and_bfpt.md](./05_contraction_and_bfpt.md) |
| P1 | Fixed point problem definition and relation to RL | Medium | Medium | 2/2 | [04_mathematical_foundations.md](./04_mathematical_foundations.md) |
| P2 | Exploration-exploitation trade-off (general discussion) | Low | Medium | 1/2 | [02_elements_of_rl.md](./02_elements_of_rl.md) |
| P2 | PAC optimality and UCB comparison | Medium | Medium | 1/2 | [03_bandit_problem.md](./03_bandit_problem.md) |
| P2 | Greedy vs epsilon-greedy | Low | Low | 1/2 | [03_bandit_problem.md](./03_bandit_problem.md) |
| P2 | L-infinity norm computation for value functions | Medium | Medium | 1/2 | [06_bellman_and_convergence.md](./06_bellman_and_convergence.md) |
| P2 | Immediate RL vs Full RL, concept of return | Low | Low | 1/2 | [01_rl_fundamentals.md](./01_rl_fundamentals.md) |
| P2 | Cauchy sequence as convergent series | Medium | Low | 1/2 | [04_mathematical_foundations.md](./04_mathematical_foundations.md) |

---

## 3. Suggested Study Order

The order below respects concept dependencies while front-loading the highest-priority exam topics.

| Phase | File | What to Focus On | Rationale |
|-------|------|-------------------|-----------|
| 1 | [01_rl_fundamentals.md](./01_rl_fundamentals.md) | SL vs UL vs RL distinctions; MDP terminology; RL application modeling | Modeling problems as MDPs appears in every paper. This is the conceptual foundation for everything else. |
| 2 | [02_elements_of_rl.md](./02_elements_of_rl.md) | Policy, value function, reward signal, model; exploration vs exploitation | Needed before bandits and Bellman. Exploration-exploitation is a standalone exam topic. |
| 3 | [03_bandit_problem.md](./03_bandit_problem.md) | Softmax numerical computation (with data table); beta parameter effects; greedy vs epsilon-greedy; UCB and PAC | Softmax numericals and beta comparison appear in every paper. Practice the computation steps until they are automatic. |
| 4 | [04_mathematical_foundations.md](./04_mathematical_foundations.md) | Metric space, fixed point definition, Cauchy sequences, complete metric space | Necessary prerequisites for contraction mapping and BFPT. Fixed point definition and its RL connection is a P1 topic. |
| 5 | [05_contraction_and_bfpt.md](./05_contraction_and_bfpt.md) | Contraction mapping definition and verification; BFPT statement and proof sketch; connection to Bellman equation | Core theory topics that appear in every paper. Be able to verify a mapping is a contraction and state the theorem precisely. |
| 6 | [06_bellman_and_convergence.md](./06_bellman_and_convergence.md) | Bellman operator as contraction proof; L-infinity norm computation; iterative convergence | Ties together the math foundations with RL. L-infinity norm computation is a likely numerical question. |
| 7 | [07_worked_problems.md](./07_worked_problems.md) | Full worked solutions for each past-paper question type | Do these under timed conditions after completing Phases 1--6. |
| 8 | [08_formula_sheet.md](./08_formula_sheet.md) | Quick review of all key formulas | Use as a final-day revision sheet. |

---

## 4. Quick-Reference: Topic-to-File Index

| Topic | File |
|-------|------|
| What is RL, SL vs UL vs RL | [01_rl_fundamentals.md](./01_rl_fundamentals.md) |
| Applications of RL | [01_rl_fundamentals.md](./01_rl_fundamentals.md) |
| MDP terminology (agent, environment, state, action, reward) | [01_rl_fundamentals.md](./01_rl_fundamentals.md) |
| RL application modeling (formulate a problem as MDP) | [01_rl_fundamentals.md](./01_rl_fundamentals.md) |
| Immediate RL vs Full RL, concept of return | [01_rl_fundamentals.md](./01_rl_fundamentals.md) |
| Policy | [02_elements_of_rl.md](./02_elements_of_rl.md) |
| Value function | [02_elements_of_rl.md](./02_elements_of_rl.md) |
| Reward signal | [02_elements_of_rl.md](./02_elements_of_rl.md) |
| Model of the environment | [02_elements_of_rl.md](./02_elements_of_rl.md) |
| Exploration vs exploitation trade-off | [02_elements_of_rl.md](./02_elements_of_rl.md) |
| Multi-armed bandit problem | [03_bandit_problem.md](./03_bandit_problem.md) |
| Greedy action selection | [03_bandit_problem.md](./03_bandit_problem.md) |
| Epsilon-greedy action selection | [03_bandit_problem.md](./03_bandit_problem.md) |
| Softmax (Boltzmann) action selection | [03_bandit_problem.md](./03_bandit_problem.md) |
| Beta parameter and temperature effects | [03_bandit_problem.md](./03_bandit_problem.md) |
| UCB (Upper Confidence Bound) | [03_bandit_problem.md](./03_bandit_problem.md) |
| PAC optimality | [03_bandit_problem.md](./03_bandit_problem.md) |
| Regret | [03_bandit_problem.md](./03_bandit_problem.md) |
| Metric space and norms | [04_mathematical_foundations.md](./04_mathematical_foundations.md) |
| Fixed point problem (definition, relation to RL) | [04_mathematical_foundations.md](./04_mathematical_foundations.md) |
| Cauchy sequence and convergent series | [04_mathematical_foundations.md](./04_mathematical_foundations.md) |
| Complete metric space | [04_mathematical_foundations.md](./04_mathematical_foundations.md) |
| Contraction mapping (definition, verification) | [05_contraction_and_bfpt.md](./05_contraction_and_bfpt.md) |
| Banach Fixed Point Theorem (existence, uniqueness, convergence) | [05_contraction_and_bfpt.md](./05_contraction_and_bfpt.md) |
| BFPT connection to Bellman equation | [05_contraction_and_bfpt.md](./05_contraction_and_bfpt.md) |
| Bellman equation and Bellman operator | [06_bellman_and_convergence.md](./06_bellman_and_convergence.md) |
| Proving Bellman operator is a contraction | [06_bellman_and_convergence.md](./06_bellman_and_convergence.md) |
| L-infinity norm computation for value functions | [06_bellman_and_convergence.md](./06_bellman_and_convergence.md) |
| Iterative convergence of value iteration | [06_bellman_and_convergence.md](./06_bellman_and_convergence.md) |
| Worked problems (all types) | [07_worked_problems.md](./07_worked_problems.md) |
| Formula sheet | [08_formula_sheet.md](./08_formula_sheet.md) |

---

## 5. Past Paper Analysis

For the full breakdown of questions, marks distribution, and topic frequency counts, see:

[00_past_paper_analysis.md](./00_past_paper_analysis.md)
