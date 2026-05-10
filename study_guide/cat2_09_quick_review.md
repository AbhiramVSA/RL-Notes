---
type: quick-review
tags: [rl, cat2, cheat-sheet, quick-review]
---

# Quick Review -- RL CAT-2

A rapid-fire review for last-minute revision. Skim this in the 15 minutes before the exam.

---

## One-Line Algorithm Summaries

- **Policy Evaluation**: Iteratively apply Bellman expectation equation until $V^\pi$ converges
- **Policy Improvement**: Make policy greedy w.r.t. current value function
- **Policy Iteration**: Alternate between full evaluation and improvement until stable
- **Value Iteration**: Apply Bellman optimality equation as update until convergence, extract policy at end
- **First-Visit MC**: Average returns from the first visit to each state across episodes
- **Every-Visit MC**: Average returns from every visit to each state across episodes
- **MC ES (Exploring Starts)**: MC control with random starting state-action pairs to ensure coverage
- **On-Policy MC**: MC control with epsilon-greedy exploration
- **Off-Policy MC**: Learn target policy using importance-weighted returns from behavior policy
- **Ordinary IS**: Unbiased but high variance -- simple average of weighted returns
- **Weighted IS**: Biased but low variance -- weighted average of returns (preferred in practice)

---

## All Four Bellman Equations Side by Side

|  | Expectation (given $\pi$) | Optimality ($V^*$ or $Q^*$) |
|--|--------------------------|---------------------------|
| **V** | $V^\pi(s) = \sum_a \pi(a \mid s) \sum_{s',r} p(s',r \mid s,a)[r + \gamma V^\pi(s')]$ | $V^*(s) = \max_a \sum_{s',r} p(s',r \mid s,a)[r + \gamma V^*(s')]$ |
| **Q** | $Q^\pi(s,a) = \sum_{s',r} p(s',r \mid s,a)[r + \gamma \sum_{a'} \pi(a' \mid s') Q^\pi(s',a')]$ | $Q^*(s,a) = \sum_{s',r} p(s',r \mid s,a)[r + \gamma \max_{a'} Q^*(s',a')]$ |

> [!tip] Quick Pattern
> **Expectation** = sum over $\pi$ (average) | **Optimality** = $\max$ (best action)
> **V** = action choice on the outside | **Q** = action already chosen, next action inside

---

## DP vs MC

| | DP | MC |
|--|----|----|
| Model | Required ($p(s',r \mid s,a)$) | Not required |
| Bootstrap | Yes (updates from estimates) | No (uses actual returns) |
| Episodes | Not required | Required (must terminate) |
| Update timing | Every sweep (synchronous) | After episode ends |
| Bias/Variance | Low variance, some bias from bootstrapping | No bias (first-visit), high variance |

---

## On-Policy vs Off-Policy

| | On-Policy | Off-Policy |
|--|-----------|-----------|
| Learns about | Same policy it follows | Different (target) policy |
| Exploration | Built into policy (epsilon-greedy) | Separate behavior policy handles exploration |
| Importance sampling | Not needed | Required to correct distribution mismatch |
| Finds | Best epsilon-soft policy | True optimal (deterministic) policy |

---

## Prediction vs Control

| | Prediction | Control |
|--|-----------|---------|
| Goal | Estimate $V^\pi$ or $Q^\pi$ for a given policy | Find optimal policy $\pi^*$ |
| Input | Fixed policy $\pi$ | No fixed policy -- must search |
| Output | Value function | Optimal policy + value function |
| DP example | Policy Evaluation | Policy Iteration, Value Iteration |
| MC example | First-Visit MC, Every-Visit MC | MC ES, On-Policy MC, Off-Policy MC |

---

## "If You See X, Use Y" Decision Guide

| Exam Question Pattern | Method to Use |
|----------------------|---------------|
| "Given policy $\pi$, compute $V(s)$..." | Policy Evaluation (DP) or MC Prediction |
| "Find the optimal policy for this MDP with known transitions..." | Policy Iteration or Value Iteration |
| "Given these episodes, estimate $V(s)$..." | First-Visit or Every-Visit MC |
| "Estimate value using a different policy than the one being evaluated..." | Importance Sampling (Off-Policy MC) |
| "Compute the importance sampling ratio..." | IS ratio formula: $\rho = \prod \frac{\pi(A_k \mid S_k)}{b(A_k \mid S_k)}$ |
| "Apply value iteration to this grid..." | Bellman optimality update, show table per iteration |
| "Improve this policy..." | Policy improvement: $\pi'(s) = \arg\max_a Q^\pi(s,a)$ |
| "What is $G_t$ for this trajectory?" | $G_t = R_{t+1} + \gamma G_{t+1}$, work backwards from terminal |

---

## Key Theorems (Without Proof)

> [!abstract] 1. Policy Improvement Theorem
> If $Q^\pi(s, \pi'(s)) \geq V^\pi(s)$ for all $s$, then $V^{\pi'}(s) \geq V^\pi(s)$ for all $s$.
> The new policy $\pi'$ is at least as good as $\pi$ everywhere.

> [!abstract] 2. MC Convergence
> First-visit MC converges to $v_\pi(s)$ as the number of visits to $s$ approaches infinity (by the law of large numbers).

> [!abstract] 3. Contraction Mapping
> The Bellman operator is a contraction with factor $\gamma < 1$, guaranteeing a unique fixed point. This is why DP converges.

> [!abstract] 4. IS Unbiasedness
> Ordinary IS gives unbiased estimates of $v_\pi(s)$. Weighted IS is biased but consistent (bias vanishes as $n \to \infty$).

---

## Critical Things to Remember

> [!danger] Do Not Forget These

1. $V(\text{terminal}) = 0$ always
2. DP needs the model $p(s',r \mid s,a)$; MC does **not**
3. MC needs complete episodes; DP does **not**
4. IS ratio uses **only policy probabilities**, not transition probabilities
5. Weighted IS is preferred in practice despite bias (much lower variance)
6. Policy iteration converges in **finite** steps; value iteration converges **asymptotically**
7. GPI (Generalized Policy Iteration) = any interleaving of evaluation and improvement
8. First-visit MC is **unbiased**; every-visit MC is **biased** but consistent
9. MC ES requires the (often unrealistic) assumption that every $(s,a)$ pair can be a starting point
10. In epsilon-greedy, all actions get at least $\frac{\epsilon}{\lvert A(s) \rvert}$ probability

---

## Last-Minute Computation Checklist

> [!note] When computing returns $G_t$
> Work **backwards** from the terminal state. $G_T = 0$, then $G_{t} = R_{t+1} + \gamma G_{t+1}$.

> [!note] When computing IS ratios
> Multiply policy probability ratios along the trajectory. If the target policy gives probability 0 to any action that was taken, the entire ratio is 0.

> [!note] When doing value iteration by hand
> For each state, compute $\max_a \sum_{s',r} p(s',r \mid s,a)[r + \gamma V_k(s')]$ across all actions. Write the winning action and new value. Repeat until stable.

> [!note] When doing policy evaluation by hand
> For each state, compute $\sum_a \pi(a \mid s) \sum_{s',r} p(s',r \mid s,a)[r + \gamma V_k(s')]$ using the given policy probabilities. No max -- just weighted average.

---

> [!abstract] See Also
> - [[cat2_08_formula_sheet]] for the complete formula reference
> - [[06_monte_carlo_methods]] for MC details
> - [[04_dynamic_programming]] for DP details
> - [[07_off_policy_mc]] for importance sampling details
