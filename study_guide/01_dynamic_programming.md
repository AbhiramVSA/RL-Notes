---
type: topic
topic: dynamic-programming
module: 3
exam_weight: high
prerequisites: []
tags: [rl, cat2, dynamic-programming, policy-evaluation, bellman-equations]
---

# Dynamic Programming

> [!info] Roadmap Context
> This is the first and most foundational topic for CAT-2. DP methods assume a **perfect model** of the environment and use **Bellman equations as update rules** to compute value functions iteratively. Everything that follows (Monte Carlo, TD learning) relaxes the assumptions made here.
> See [[cat2_00_roadmap]] for the full study plan.

---

## Learning Objectives

By the end of this topic, you should be able to:

1. Explain what Dynamic Programming means in the context of reinforcement learning and how it differs from general RL.
2. State the key assumption DP requires (a perfect model / known transition dynamics).
3. Write out the Bellman expectation equation for $V^\pi$ and explain every term.
4. Execute the iterative policy evaluation algorithm by hand on a small gridworld.
5. Describe how policy evaluation converges and what the convergence criterion is.
6. Connect policy evaluation to the larger picture: policy iteration, value iteration, and generalized policy iteration.

---

## Ground-Up Explanation

### What Is Dynamic Programming?

Dynamic Programming is a collection of algorithms that can compute **optimal policies** given a **perfect model** of the environment as a Markov Decision Process (MDP). The word "dynamic" refers to the sequential, multi-stage nature of the problems, and "programming" refers to optimization (finding the best policy), not writing code.

The critical assumption is this: **we know the full transition dynamics** $p(s', r \mid s, a)$ for every state-action pair. This means DP solves a **planning problem** -- the agent does not need to interact with the environment to learn. It can compute everything from the model alone.

> [!warning] Planning vs. Learning
> DP is **not** reinforcement learning in the full sense. In RL, the environment can be complex and its specifics are unknown initially -- the agent must learn from trial and error. DP assumes all of that information is given upfront. We study DP because:
> - It finds **optimal solutions** to planning problems.
> - It is the **conceptual foundation** for understanding all RL algorithms that follow.

### Why Learn DP?

Even though the perfect-model assumption is unrealistic for most real problems, DP is worth studying for two reasons:

1. **Theoretical foundation**: The Bellman equations, the idea of iterative computation of value functions, and the policy evaluation / policy improvement loop all originate here. Every subsequent RL method (Monte Carlo, TD, Q-learning) is best understood as relaxing one or more DP assumptions.
2. **It works when the model is available**: Some problems (board games with known rules, inventory management with known demand distributions) do have known dynamics, and DP gives exact solutions.

### Motivating Example: Motorbike Rental Company

Sunny manages a motorbike rental company in Ladakh with **two locations**. Key details:

- Bikes are rented at **Rs 1200 per day**.
- Moving a bike from one location to the other costs **Rs 100**.
- Customer demand for rentals and returns at each location follows known probability distributions $g(n)$ and $h(n)$.
- **Goal**: Maximize total expected earnings by deciding each evening how many bikes to move between the two locations overnight.

This is a planning problem because the demand/return distributions are known. The state is the number of bikes at each location; the action is how many bikes to move. DP can find the optimal transfer policy by iteratively computing how valuable each state is under different policies.

This example illustrates the core DP setup:
- **States**: configurations of the system (bike counts at each location).
- **Actions**: decisions available (number of bikes to move).
- **Transition probabilities**: given by the demand and return distributions.
- **Rewards**: rental income minus transfer costs.
- **Goal**: find a policy (state -> action mapping) that maximizes expected cumulative reward.

### The Central Idea

DP uses **Bellman equations as update rules**. The Bellman equation expresses the value of a state in terms of the values of successor states. DP turns this recursive relationship into an iterative algorithm: start with an arbitrary guess for all state values, then repeatedly apply the Bellman equation to update each state's value until the values converge.

---

## Analogies

> [!tip] Analogy 1: Filling in a Spreadsheet
> Imagine a spreadsheet where each cell's value depends on other cells (like a formula referencing neighbors). You start by putting 0 in every cell. Then you recalculate every cell from its formula. The first pass gives rough estimates. You recalculate again -- the estimates improve because the cells they reference are now better. Repeat until nothing changes. That is iterative policy evaluation.

> [!tip] Analogy 2: Grading on a Curve
> Think of policy evaluation like repeatedly adjusting grades. Each student's "value" depends on how they compare to neighbors. In the first round, everyone is at 0. Each round propagates information about who is near the "terminal" (the top student or the bottom). After enough rounds, everyone has a stable relative ranking. The Bellman update propagates reward information from terminal states backward through the state space.

---

## Policy Evaluation (Iterative Prediction)

### The Problem

Given a policy $\pi$, compute the **state-value function** $V^\pi(s)$ for all states $s$. This is the **prediction problem**: we are not trying to improve the policy, only to evaluate how good it is.

$V^\pi(s)$ is the expected return (cumulative discounted reward) starting from state $s$ and following policy $\pi$ thereafter:

$$V^\pi(s) = \mathbb{E}_\pi \left[ \sum_{k=0}^{\infty} \gamma^k R_{t+k+1} \mid S_t = s \right]$$

### Bellman Expectation Equation for $V^\pi$

The value of state $s$ under policy $\pi$ satisfies:

$$V^\pi(s) = \sum_{a} \pi(a \mid s) \sum_{s', r} p(s', r \mid s, a) \left[ r + \gamma \, V^\pi(s') \right]$$

Breaking this down term by term:

| Symbol | Meaning |
|--------|---------|
| $\pi(a \mid s)$ | Probability of taking action $a$ in state $s$ under policy $\pi$ |
| $p(s', r \mid s, a)$ | Transition probability: probability of reaching state $s'$ with reward $r$ given state $s$ and action $a$ |
| $r$ | Immediate reward received |
| $\gamma$ | Discount factor, $0 \le \gamma \le 1$ |
| $V^\pi(s')$ | Value of the successor state $s'$ under the same policy |

The equation says: the value of $s$ is the **expected value** of (immediate reward + discounted value of where you end up), averaged over all actions (weighted by the policy) and all possible transitions (weighted by transition probabilities).

### Iterative Policy Evaluation Algorithm

We cannot solve the Bellman equation directly for large state spaces (it is a system of $|\mathcal{S}|$ simultaneous linear equations). Instead, we solve it iteratively.

> [!danger] Must Memorize: Iterative Policy Evaluation Pseudocode
> ```
> Input: policy pi to be evaluated
> Initialize V(s) = 0 for all s in S (or arbitrary, V(terminal) = 0)
> Repeat:
>     delta <- 0
>     For each s in S:
>         v <- V(s)                          // store old value
>         V(s) <- sum over a of pi(a|s) * sum over s',r of p(s',r|s,a) * [r + gamma * V(s')]
>         delta <- max(delta, |v - V(s)|)    // track largest change
>     Until delta < theta                     // theta is a small positive threshold
> Output: V approximately equal to V^pi
> ```

Key points about this algorithm:

- **In-place updates**: We update $V(s)$ immediately and use the new values in subsequent updates within the same sweep. This is called **in-place** dynamic programming and typically converges faster than maintaining two separate arrays.
- **Convergence**: The algorithm is guaranteed to converge to $V^\pi$ as the number of iterations approaches infinity. In practice, we stop when the maximum change $\delta$ across all states falls below a threshold $\theta$.
- **Computational cost per sweep**: $O(|\mathcal{S}|^2 \cdot |\mathcal{A}|)$ in the worst case (for each state, we consider each action and each possible successor state).

### Convergence Guarantee

> [!info] Why Does It Converge?
> The Bellman expectation operator $T^\pi$ defined by the right-hand side of the Bellman equation is a **contraction mapping** with contraction factor $\gamma$ (when $\gamma < 1$). By the **Banach fixed-point theorem**, repeated application of a contraction mapping converges to a unique fixed point, which is $V^\pi$.
>
> When $\gamma = 1$ (undiscounted, episodic tasks), convergence is still guaranteed as long as all states eventually reach a terminal state under $\pi$.

---

## Worked Example: 4x4 Gridworld Policy Evaluation

> [!example] Setup: Classic 4x4 Gridworld (Sutton & Barto Example 4.1)
>
> **Grid layout** (state numbers):
> ```
> | 0(T) |  1  |  2  |  3  |
> |  4   |  5  |  6  |  7  |
> |  8   |  9  | 10  | 11  |
> | 12   | 13  | 14  | 0(T)|
> ```
> - States 0 and 15 are **terminal states** (shown as state 0(T) in top-left and bottom-right).
> - States 1 through 14 are non-terminal.
> - **Actions**: Up, Down, Left, Right (4 actions from each non-terminal state).
> - **Policy**: Uniform random -- $\pi(a \mid s) = 0.25$ for all four actions in every non-terminal state.
> - **Reward**: $-1$ for every transition (regardless of action or destination).
> - **Discount factor**: $\gamma = 1$.
> - **Transitions**: Deterministic. If an action would take the agent off the grid, it stays in the same state (still receives $-1$ reward).

### Iteration 0 (Initialization)

All values initialized to 0:

```
|  0.0  |  0.0  |  0.0  |  0.0  |
|  0.0  |  0.0  |  0.0  |  0.0  |
|  0.0  |  0.0  |  0.0  |  0.0  |
|  0.0  |  0.0  |  0.0  |  0.0  |
```

### Iteration 1 (k=1)

We apply the Bellman update for each non-terminal state. Using **synchronous** (two-array) updates for clarity -- all updates in this sweep use the $k=0$ values.

For any non-terminal state $s$:

$$V_1(s) = \sum_{a} 0.25 \times \left[ -1 + 1 \times V_0(s') \right]$$

Since $V_0(s') = 0$ for all states, and each action yields reward $-1$:

$$V_1(s) = 4 \times 0.25 \times (-1 + 0) = -1.0$$

for every non-terminal state.

```
|  0.0  | -1.0  | -1.0  | -1.0  |
| -1.0  | -1.0  | -1.0  | -1.0  |
| -1.0  | -1.0  | -1.0  | -1.0  |
| -1.0  | -1.0  | -1.0  |  0.0  |
```

### Iteration 2 (k=2)

Now values from iteration 1 are used. Let us compute a few states in detail.

**State 1** (top row, second column):
- Up: goes off grid, stays at state 1. Reward $= -1$, $V_1(1) = -1.0$
- Down: goes to state 5. Reward $= -1$, $V_1(5) = -1.0$
- Left: goes to state 0 (terminal). Reward $= -1$, $V_1(0) = 0.0$
- Right: goes to state 2. Reward $= -1$, $V_1(2) = -1.0$

$$V_2(1) = 0.25 \times [(-1) + (-1.0)] + 0.25 \times [(-1) + (-1.0)] + 0.25 \times [(-1) + 0.0] + 0.25 \times [(-1) + (-1.0)]$$
$$= 0.25 \times (-2) + 0.25 \times (-2) + 0.25 \times (-1) + 0.25 \times (-2) = -0.5 - 0.5 - 0.25 - 0.5 = -1.75$$

**State 5** (second row, second column):
- Up: state 1, $V_1(1) = -1.0$
- Down: state 9, $V_1(9) = -1.0$
- Left: state 4, $V_1(4) = -1.0$
- Right: state 6, $V_1(6) = -1.0$

$$V_2(5) = 0.25 \times [(-1)+(-1)] \times 4 = 0.25 \times (-2) \times 4 = -2.0$$

By symmetry, interior states (5, 6, 9, 10) all have $V_2 = -2.0$. Corner-adjacent states differ based on how many neighbors are terminal or boundary.

Full grid after iteration 2:

```
|  0.0  | -1.75 | -2.0  | -2.0  |
| -1.75 | -2.0  | -2.0  | -2.0  |
| -2.0  | -2.0  | -2.0  | -1.75 |
| -2.0  | -2.0  | -1.75 |  0.0  |
```

### Iteration 3 (k=3)

**State 1**:
- Up: stay at 1. $-1 + V_2(1) = -1 + (-1.75) = -2.75$
- Down: state 5. $-1 + V_2(5) = -1 + (-2.0) = -3.0$
- Left: state 0 (terminal). $-1 + 0 = -1.0$
- Right: state 2. $-1 + V_2(2) = -1 + (-2.0) = -3.0$

$$V_3(1) = 0.25 \times (-2.75 - 3.0 - 1.0 - 3.0) = 0.25 \times (-9.75) = -2.4375$$

**State 5**:
- Up: state 1. $-1 + (-1.75) = -2.75$
- Down: state 9. $-1 + (-2.0) = -3.0$
- Left: state 4. $-1 + (-1.75) = -2.75$
- Right: state 6. $-1 + (-2.0) = -3.0$

$$V_3(5) = 0.25 \times (-2.75 - 3.0 - 2.75 - 3.0) = 0.25 \times (-11.5) = -2.875$$

Full grid after iteration 3:

```
|  0.0   | -2.44  | -2.94  | -3.0   |
| -2.44  | -2.88  | -3.0   | -2.94  |
| -2.94  | -3.0   | -2.88  | -2.44  |
| -3.0   | -2.94  | -2.44  |  0.0   |
```

> [!info] Convergence pattern
> Notice the **diagonal symmetry** in the grid -- states equidistant from the two terminal corners have the same value. As iterations continue, the values keep decreasing (becoming more negative) because the random policy is inefficient. The converged values (at $k = \infty$) are:
> ```
> |  0  | -14  | -20  | -22  |
> | -14 | -18  | -20  | -20  |
> | -20 | -20  | -18  | -14  |
> | -22 | -20  | -14  |  0   |
> ```
> These large negative values reflect how many steps the random policy takes on average to reach a terminal state.

---

## Key Formulas

> [!danger] Must Memorize: Core DP Formulas
>
> **Bellman Expectation Equation for $V^\pi$:**
> $$V^\pi(s) = \sum_{a} \pi(a \mid s) \sum_{s', r} p(s', r \mid s, a) \left[ r + \gamma \, V^\pi(s') \right]$$
>
> **Iterative Update Rule:**
> $$V_{k+1}(s) \leftarrow \sum_{a} \pi(a \mid s) \sum_{s', r} p(s', r \mid s, a) \left[ r + \gamma \, V_k(s') \right]$$
>
> **Convergence Criterion:**
> $$\max_s \left| V_{k+1}(s) - V_k(s) \right| < \theta$$
>
> **Bellman Expectation Equation for $Q^\pi$:**
> $$Q^\pi(s, a) = \sum_{s', r} p(s', r \mid s, a) \left[ r + \gamma \sum_{a'} \pi(a' \mid s') Q^\pi(s', a') \right]$$

---

## Derivations

### From the Bellman Equation to the Iterative Update

**Starting point**: The definition of $V^\pi(s)$ using the expected return.

$$V^\pi(s) = \mathbb{E}_\pi [G_t \mid S_t = s]$$

**Step 1**: Decompose the return $G_t$ into immediate reward plus discounted future return.

$$G_t = R_{t+1} + \gamma G_{t+1}$$

**Step 2**: Substitute and use the law of total expectation, conditioning on the action taken and the next state reached.

$$V^\pi(s) = \mathbb{E}_\pi [R_{t+1} + \gamma G_{t+1} \mid S_t = s]$$

$$= \sum_a \pi(a \mid s) \sum_{s'} \sum_r p(s', r \mid s, a) \left[ r + \gamma \, \mathbb{E}_\pi [G_{t+1} \mid S_{t+1} = s'] \right]$$

**Step 3**: Recognize that $\mathbb{E}_\pi [G_{t+1} \mid S_{t+1} = s'] = V^\pi(s')$ by definition.

$$V^\pi(s) = \sum_a \pi(a \mid s) \sum_{s', r} p(s', r \mid s, a) \left[ r + \gamma \, V^\pi(s') \right]$$

This is the **Bellman expectation equation** -- a recursive relationship where $V^\pi$ appears on both sides.

**Step 4**: Turn it into an iterative algorithm. Replace the exact $V^\pi$ on the left with $V_{k+1}$ and on the right with $V_k$:

$$V_{k+1}(s) \leftarrow \sum_a \pi(a \mid s) \sum_{s', r} p(s', r \mid s, a) \left[ r + \gamma \, V_k(s') \right]$$

Start with $V_0(s) = 0$ for all $s$. The sequence $V_0, V_1, V_2, \ldots$ converges to $V^\pi$.

> [!info] Why the iterative version works
> The update operator is a **contraction mapping** (it brings any two value functions closer together by a factor of at most $\gamma$ per iteration). The Banach fixed-point theorem guarantees convergence to the unique fixed point, which is $V^\pi$.

---

## Common Mistakes

> [!warning] Common Mistakes to Avoid
>
> 1. **Forgetting to keep terminal state values at 0.** Terminal states must always have $V(s_{\text{terminal}}) = 0$. If you update them, your values will be wrong.
>
> 2. **Confusing synchronous and in-place (asynchronous) updates.** In synchronous updates, you use a separate array for $V_{k+1}$ and compute all new values from $V_k$ only. In in-place updates, you write directly into the same array, so later states in the sweep may use already-updated values from the current sweep. Both converge, but to show clean iteration tables in exams, use synchronous unless told otherwise.
>
> 3. **Forgetting the boundary condition for grid actions.** When an action would move the agent off the grid, the agent stays in the same state but still receives the step reward ($-1$ in the gridworld example). Do not set the reward to 0 or skip the transition.
>
> 4. **Mixing up $V^\pi$ (policy evaluation) and $V^*$ (optimal value function).** Policy evaluation computes the value function for a **given, fixed** policy. It does NOT find the optimal policy -- that requires policy improvement or value iteration on top.
>
> 5. **Confusing the Bellman expectation equation with the Bellman optimality equation.** The expectation equation averages over actions using $\pi(a|s)$. The optimality equation takes the **max** over actions. They are different equations used for different purposes.
>
> 6. **Off-by-one in iteration counting.** $V_0$ is the initialization (all zeros). $V_1$ is the result after the first sweep. Be careful when an exam asks "after $k$ iterations."

---

## Self-Check Questions

> [!question]- Q1: What is the key assumption that distinguishes DP from general RL methods?
> DP requires a **perfect model of the environment** -- specifically, complete knowledge of the transition dynamics $p(s', r \mid s, a)$ for all states and actions. General RL methods learn from interaction without requiring this model.

> [!question]- Q2: Write the Bellman expectation equation for $V^\pi(s)$ and explain what each summation does.
> $$V^\pi(s) = \sum_{a} \pi(a \mid s) \sum_{s', r} p(s', r \mid s, a) \left[ r + \gamma \, V^\pi(s') \right]$$
> - The outer sum over $a$ averages over all actions the policy might take, weighted by $\pi(a|s)$.
> - The inner sum over $s', r$ averages over all possible next states and rewards, weighted by the transition probability $p(s',r|s,a)$.
> - The bracketed term $[r + \gamma V^\pi(s')]$ is the immediate reward plus the discounted value of the next state.

> [!question]- Q3: In the 4x4 gridworld with uniform random policy, why do all non-terminal states have $V_1 = -1.0$ after the first iteration?
> Because $V_0(s') = 0$ for all states, the update for every non-terminal state becomes:
> $$V_1(s) = \sum_a 0.25 \times (-1 + 1 \times 0) = 4 \times 0.25 \times (-1) = -1.0$$
> Every action yields reward $-1$, and all successor values are 0, so every non-terminal state gets the same value.

> [!question]- Q4: Why is $\gamma = 1$ acceptable in the gridworld example? Under what condition could $\gamma = 1$ cause problems?
> $\gamma = 1$ is acceptable here because the task is **episodic** -- all states eventually reach a terminal state (even under the random policy). If the task were **continuing** (no terminal state) and $\gamma = 1$, the returns could be infinite and the value function would be undefined. The contraction mapping argument requires $\gamma < 1$ for continuing tasks.

> [!question]- Q5: What is the difference between synchronous and in-place (asynchronous) updates in iterative policy evaluation?
> - **Synchronous**: Maintain two arrays. Compute all $V_{k+1}(s)$ values using only $V_k$ values. Swap arrays at the end of the sweep.
> - **In-place (asynchronous)**: Use a single array. Update $V(s)$ immediately, so later updates within the same sweep may use already-updated values from this sweep.
> Both converge to $V^\pi$. In-place updates typically converge faster because they propagate new information within a single sweep.

> [!question]- Q6: In the gridworld, state 5 has $V_2 = -2.0$ while state 1 has $V_2 = -1.75$. Why is state 1 slightly less negative?
> State 1 is adjacent to terminal state 0. One of its four actions (Left) transitions to the terminal state, which has value 0. This pulls state 1's value upward compared to state 5, which is surrounded entirely by non-terminal states (all with value $-1.0$ from iteration 1). Being closer to a terminal state means the expected return is less negative.

> [!question]- Q7: If the policy were changed from uniform random to always moving Left, would the converged value of state 3 (top-right corner) get better or worse?
> **Worse** (more negative). Under the always-Left policy, the agent starting at state 3 would traverse states $3 \to 2 \to 1 \to 0$ deterministically, taking 3 steps for a return of $-3$. Under the random policy, although the agent wanders, it has some probability of reaching terminal state 15 (bottom-right) which might be fewer steps away from certain interior states. For state 3 specifically, the always-Left policy gives $V(3) = -3$, whereas the converged random policy value is $V(3) = -22$ -- so actually the always-Left policy is **much better** for state 3. The random policy is terrible because it wanders aimlessly.

---

## Concept Links

| Related Topic | Connection | File |
|---------------|------------|------|
| Policy Iteration | Uses policy evaluation as a subroutine; alternates evaluation and improvement | [[02_policy_iteration]] |
| Value Iteration | Can be viewed as policy evaluation truncated to a single sweep, combined with a greedy policy improvement | [[03_value_iteration]] |
| Monte Carlo Prediction | Solves the same prediction problem ($V^\pi$) but without requiring a model; uses sampled returns instead of expected values | [[04_monte_carlo_prediction]] |
| Monte Carlo Control | Uses MC evaluation as the evaluation step in a GPI loop, analogous to how policy iteration uses DP evaluation | [[05_monte_carlo_control]] |
| Formula Sheet | All key equations collected in one place | [[cat2_08_formula_sheet]] |
| Worked Problems | Additional practice problems with full solutions | [[cat2_07_worked_problems]] |

---

> [!tip] Exam Strategy
> Policy evaluation questions typically ask you to:
> 1. Write out the Bellman expectation equation.
> 2. Perform 1-3 iterations of the algorithm on a small grid or MDP.
> 3. Explain convergence.
>
> Always set up a clear table for your value grid at each iteration. Label which iteration you are on. Show your work for at least one or two states in detail, then fill in the rest "by symmetry" or "by similar calculation" if pressed for time.
