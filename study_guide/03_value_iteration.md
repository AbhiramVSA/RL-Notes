---
type: topic
topic: value-iteration
module: 3
exam_weight: high
prerequisites: [[01_dynamic_programming], [02_policy_iteration]]
tags: [rl, cat2, dynamic-programming, value-iteration]
---

# Value Iteration

---

## 1. Learning Objectives

By the end of this topic you should be able to:

- [ ] Explain value iteration as a form of truncated policy iteration
- [ ] State the four Bellman optimality equations from memory
- [ ] Run the value iteration algorithm by hand on a small MDP and extract the optimal policy
- [ ] Compare value iteration with policy iteration along at least five dimensions (update rule, convergence, cost, etc.)
- [ ] Describe the contraction mapping argument for why value iteration converges
- [ ] Distinguish synchronous from asynchronous DP updates

---

## 2. Ground-Up Explanation

### The Problem with Policy Iteration

Recall from [[02_policy_iteration]] that policy iteration repeats two phases:

1. **Policy Evaluation** -- solve (or iteratively approximate) $V^{\pi}(s)$ for the current policy $\pi$.
2. **Policy Improvement** -- derive a greedy policy $\pi'$ from $V^{\pi}$.

Policy evaluation is the bottleneck. Each evaluation round must sweep repeatedly over every state until the value function converges to $V^{\pi}$. For large state spaces this is expensive.

### The Key Insight

> [!tip] Core Idea
> We do **not** need to wait for $V^{\pi}$ to fully converge before we improve the policy. Even a single sweep of the Bellman equation already moves values in the right direction. If we improve immediately after just **one** sweep, we still converge to the optimal value function -- and we save all those inner-loop sweeps.

This is **value iteration**: policy evaluation truncated to a single sweep, with the improvement step folded directly into the update.

### Equivalent Viewpoint -- The Bellman Optimality Equation as an Update Rule

Instead of thinking "truncated policy iteration," you can equivalently think of value iteration as turning the Bellman optimality equation into an iterative update:

$$V_{k+1}(s) \;\leftarrow\; \max_a \sum_{s',r} p(s',r \mid s,a)\bigl[r + \gamma\, V_k(s')\bigr]$$

At every step we are asking: "If the current value estimates $V_k$ were correct for future states, what is the best action and resulting value at state $s$?" Repeating this drives $V_k \to V^*$.

### A Small Concrete Example (Warm-Up)

Consider a two-state MDP before we tackle the full algorithm.

- **States**: $\{s_1, s_2\}$, with $s_2$ terminal.
- **Actions at $s_1$**: $\{a\}$ (only one action).
- **Transition**: $p(s_2, r=+5 \mid s_1, a) = 1$.
- **Discount**: $\gamma = 0.9$.

Start with $V_0(s_1) = 0$.

| Iteration | Update | $V(s_1)$ |
|-----------|--------|-----------|
| 0 | -- | 0 |
| 1 | $\max_a [5 + 0.9 \cdot 0] = 5$ | 5 |

Only one action, one transition, so convergence is immediate. The optimal policy is trivially $\pi^*(s_1) = a$. This toy case shows the mechanics; a richer example appears in Section 6.

---

## 3. Analogies

> [!abstract] Analogy 1 -- GPS Recalculation
> Policy iteration is like computing a full route plan, driving the whole route, then replanning from scratch. Value iteration is like a GPS that recalculates the best next turn after every single block -- it never finishes a "full" plan but it still gets you to the destination optimally.

> [!abstract] Analogy 2 -- Exam Preparation
> Policy iteration: study an entire textbook cover to cover, then redo all problems, then repeat the whole textbook. Value iteration: after reading just one chapter, immediately solve problems from that chapter and move on. You cycle through the material faster, even if each pass is shallower.

> [!abstract] Analogy 3 -- Auction Bidding
> Imagine bidders updating their maximum bid one at a time. Each bidder looks at the current highest bids of neighbours and raises theirs to the best possible. After enough rounds, bids stabilise at their true values. The "max" operation in value iteration mirrors each bidder choosing the best action (bid).

---

## 4. Bellman Optimality Equations

> [!danger] MUST MEMORIZE -- All Four Bellman Optimality Equations
> These are the backbone of value iteration and appear directly on exams.

### Equation 1 -- Optimal State-Value Function

$$V^*(s) = \max_a \sum_{s',r} p(s',r \mid s,a)\bigl[r + \gamma\, V^*(s')\bigr]$$

### Equation 2 -- Optimal Action-Value Function

$$Q^*(s,a) = \sum_{s',r} p(s',r \mid s,a)\bigl[r + \gamma\, \max_{a'} Q^*(s',a')\bigr]$$

### Equation 3 -- Linking $V^*$ and $Q^*$ (V from Q)

$$V^*(s) = \max_a\; Q^*(s,a)$$

### Equation 4 -- Linking $Q^*$ and $V^*$ (Q from V)

$$Q^*(s,a) = \sum_{s',r} p(s',r \mid s,a)\bigl[r + \gamma\, V^*(s')\bigr]$$

### Variable Definitions

| Symbol | Meaning |
|--------|---------|
| $s$ | Current state |
| $a$ | Action taken in state $s$ |
| $s'$ | Successor (next) state |
| $r$ | Reward received on transition |
| $p(s',r \mid s,a)$ | Transition-reward probability: probability of reaching $s'$ with reward $r$ when taking action $a$ in state $s$ |
| $\gamma$ | Discount factor, $0 \le \gamma < 1$ (or $\gamma = 1$ for episodic tasks with guaranteed termination) |
| $V^*(s)$ | Optimal state-value function -- expected return starting from $s$ and acting optimally thereafter |
| $Q^*(s,a)$ | Optimal action-value function -- expected return starting from $s$, taking $a$, and acting optimally thereafter |
| $\max_a$ | Maximisation over all actions available in $s$ |

### How $V^*$ and $Q^*$ Relate

The relationship forms a cycle:

$$V^*(s) = \max_a\; Q^*(s,a)$$

$$Q^*(s,a) = \sum_{s',r} p(s',r \mid s,a)\bigl[r + \gamma\, V^*(s')\bigr]$$

Substituting the second into the first gives Equation 1. Substituting the first into the second gives Equation 2. Knowing any one of $V^*$ or $Q^*$ is enough to recover the other and the optimal policy.

---

## 5. Value Iteration Algorithm

### Pseudocode

> [!note] Algorithm -- Value Iteration (Sutton & Barto, Chapter 4)
> ```
> Algorithm: Value Iteration
> ─────────────────────────────────────────
> Input:  MDP (S, A, p, gamma), threshold theta > 0
> Output: Approximate optimal value function V ≈ V*
>         Deterministic optimal policy pi ≈ pi*
>
> 1.  Initialize V(s) arbitrarily for all s in S
>     Set V(terminal) = 0
>
> 2.  Repeat:
> 3.      delta <- 0
> 4.      For each s in S:
> 5.          v <- V(s)                                    // save old value
> 6.          V(s) <- max_a  sum_{s',r} p(s',r|s,a) [r + gamma * V(s')]
> 7.          delta <- max(delta, |v - V(s)|)              // track largest change
> 8.      Until delta < theta                              // convergence check
>
> 9.  Output deterministic policy:
> 10.     For each s in S:
> 11.         pi(s) <- argmax_a  sum_{s',r} p(s',r|s,a) [r + gamma * V(s')]
> ```

### Line-by-Line Explanation

| Line | What It Does |
|------|--------------|
| 1 | Arbitrary initialisation (often all zeros). Terminal states must be zero because no future reward is possible. |
| 2 | Outer loop -- keeps sweeping until values stabilise. |
| 3 | Reset the convergence tracker at the start of each full sweep. |
| 4 | Iterate over every non-terminal state. |
| 5 | Save the current value so we can measure how much it changed. |
| 6 | **The core update.** For each action, compute the expected return using current estimates, then take the **max** over actions. This line simultaneously does evaluation (the expectation) and improvement (the max). |
| 7 | Track the biggest value change across all states in this sweep. |
| 8 | If the biggest change is smaller than threshold $\theta$, we declare convergence. |
| 9--11 | **Policy extraction.** After the value function has converged, derive the greedy policy. For each state, pick the action that maximises the expected return under the converged $V$. |

> [!warning] Important
> Policy extraction happens **after** convergence, not during. During the loop (lines 2--8) there is no explicit policy -- only values are updated. This is a key difference from policy iteration, which maintains and alternates between an explicit policy and a value function.

---

## 6. Hand-Traced Example

### MDP Definition

A 3-state MDP with states $\{s_1, s_2, s_3\}$ where $s_3$ is terminal.

**Actions and transitions:**

| State | Action | Next State | Probability | Reward |
|-------|--------|------------|-------------|--------|
| $s_1$ | $a_1$ (go-right) | $s_2$ | 1.0 | +2 |
| $s_1$ | $a_2$ (jump) | $s_3$ | 1.0 | +6 |
| $s_2$ | $a_1$ (go-right) | $s_3$ | 1.0 | +10 |
| $s_2$ | $a_2$ (go-left) | $s_1$ | 1.0 | +1 |

**Discount factor:** $\gamma = 0.9$

**Threshold:** $\theta = 0.01$

**Terminal state:** $V(s_3) = 0$ always.

### Iteration-by-Iteration Trace

**Initialisation (k = 0):**

| State | $V_0$ |
|-------|-------|
| $s_1$ | 0 |
| $s_2$ | 0 |
| $s_3$ | 0 |

---

**Iteration k = 1:**

Update $s_1$:

$$V(s_1) \leftarrow \max\bigl\{\underbrace{2 + 0.9 \cdot V_0(s_2)}_{a_1: 2 + 0 = 2},\;\underbrace{6 + 0.9 \cdot V_0(s_3)}_{a_2: 6 + 0 = 6}\bigr\} = 6$$

Update $s_2$ (using in-place $V(s_1)=6$ from above):

$$V(s_2) \leftarrow \max\bigl\{\underbrace{10 + 0.9 \cdot V_0(s_3)}_{a_1: 10 + 0 = 10},\;\underbrace{1 + 0.9 \cdot V(s_1)}_{a_2: 1 + 5.4 = 6.4}\bigr\} = 10$$

$\delta = \max(|0-6|, |0-10|) = 10$. Not converged.

| State | $V_1$ |
|-------|-------|
| $s_1$ | 6 |
| $s_2$ | 10 |
| $s_3$ | 0 |

---

**Iteration k = 2:**

Update $s_1$:

$$V(s_1) \leftarrow \max\bigl\{2 + 0.9 \cdot 10,\;6 + 0.9 \cdot 0\bigr\} = \max\{11, 6\} = 11$$

Update $s_2$ (using in-place $V(s_1) = 11$):

$$V(s_2) \leftarrow \max\bigl\{10 + 0,\;1 + 0.9 \cdot 11\bigr\} = \max\{10, 10.9\} = 10.9$$

$\delta = \max(|6-11|, |10-10.9|) = 5$. Not converged.

| State | $V_2$ |
|-------|-------|
| $s_1$ | 11 |
| $s_2$ | 10.9 |
| $s_3$ | 0 |

---

**Iteration k = 3:**

Update $s_1$:

$$V(s_1) \leftarrow \max\{2 + 0.9 \cdot 10.9,\;6\} = \max\{11.81, 6\} = 11.81$$

Update $s_2$ (using in-place $V(s_1) = 11.81$):

$$V(s_2) \leftarrow \max\{10,\;1 + 0.9 \cdot 11.81\} = \max\{10, 11.629\} = 11.629$$

$\delta = \max(|11 - 11.81|, |10.9 - 11.629|) = 0.81$. Not converged.

| State | $V_3$ |
|-------|-------|
| $s_1$ | 11.81 |
| $s_2$ | 11.629 |
| $s_3$ | 0 |

---

**Iteration k = 4:**

Update $s_1$:

$$V(s_1) \leftarrow \max\{2 + 0.9 \cdot 11.629,\;6\} = \max\{12.466, 6\} = 12.466$$

Update $s_2$:

$$V(s_2) \leftarrow \max\{10,\;1 + 0.9 \cdot 12.466\} = \max\{10, 12.219\} = 12.219$$

$\delta = \max(|11.81 - 12.466|, |11.629 - 12.219|) = 0.656$. Not converged.

| State | $V_4$ |
|-------|-------|
| $s_1$ | 12.466 |
| $s_2$ | 12.219 |
| $s_3$ | 0 |

> [!info] Convergence Behaviour
> The values keep growing but the **changes** ($\delta$) shrink geometrically (roughly by a factor of $\gamma = 0.9$ each iteration). After enough iterations $\delta$ will drop below $\theta = 0.01$. The true optimal values for this MDP (obtained by solving the Bellman optimality equations exactly) are:
>
> $$V^*(s_2) = \frac{1}{1 - 0.81}\left(\text{from the recurrence}\right)$$
>
> Solving the system:
> - $V^*(s_1) = \max\{2 + 0.9\,V^*(s_2),\; 6\}$
> - $V^*(s_2) = \max\{10,\; 1 + 0.9\,V^*(s_1)\}$
>
> Assuming best actions are $a_1$ at $s_1$ and $a_2$ at $s_2$ (the pattern from iteration 2 onward):
> - $V^*(s_1) = 2 + 0.9\,V^*(s_2)$
> - $V^*(s_2) = 1 + 0.9\,V^*(s_1)$
>
> Substituting: $V^*(s_1) = 2 + 0.9(1 + 0.9\,V^*(s_1)) = 2.9 + 0.81\,V^*(s_1)$
>
> $V^*(s_1) = 2.9 / 0.19 \approx 15.26$
>
> $V^*(s_2) = 1 + 0.9 \times 15.26 \approx 14.74$

### Extracted Optimal Policy

After convergence:

$$\pi^*(s_1) = \arg\max\{2 + 0.9 \cdot V^*(s_2),\;6\} = a_1\;\text{(go-right)}$$

$$\pi^*(s_2) = \arg\max\{10,\;1 + 0.9 \cdot V^*(s_1)\} = a_2\;\text{(go-left)}$$

> [!success] Intuition Check
> The optimal policy creates a loop: $s_1 \to s_2 \to s_1 \to s_2 \to \ldots$, collecting rewards of $+2$ and $+1$ each cycle. With $\gamma = 0.9$ this infinite stream of discounted rewards ($2 + 0.9 + 0.81 \times 2 + \ldots$) is worth more than the one-shot $+6$ or $+10$ to the terminal state. The algorithm correctly discovers that **staying in the loop is more valuable than exiting**.

---

## 7. Value Iteration vs Policy Iteration Comparison

| Aspect | Policy Iteration | Value Iteration |
|--------|-----------------|-----------------|
| **Update rule** | Bellman **expectation** equation (for fixed $\pi$) | Bellman **optimality** equation (with max) |
| **Per iteration** | Full policy evaluation (many sweeps) + policy improvement | Single sweep with max over actions |
| **Convergence type** | Finite steps (policy space is finite, strict improvement each step) | Asymptotic (approaches $V^*$ to within $\theta$) |
| **Policy representation** | Explicit policy maintained throughout | No explicit policy until the end |
| **Policy extraction** | After every improvement step | Only once, after value convergence |
| **Computational cost per iteration** | Higher (full evaluation is $O(|S|^2|A|)$ per sweep $\times$ many sweeps, or $O(|S|^3)$ if solved exactly) | Lower (one sweep: $O(|S|^2|A|)$) |
| **Total iterations to converge** | Fewer (typically very few policy changes) | More (value changes are gradual) |
| **Total wall-clock time** | Can be faster for small $|S|$ (fewer outer iterations) | Often faster for large $|S|$ (cheaper iterations) |
| **Better suited for** | Small state spaces; when exact evaluation is affordable | Large state spaces; when you want simplicity |
| **Relationship** | General case (evaluation until convergence) | Special case of truncated PI (evaluation for exactly 1 sweep) |

> [!tip] Exam Insight
> A common exam question asks: "Is value iteration a special case of policy iteration?" The answer is **yes** -- it is policy iteration with the evaluation phase truncated to a single sweep. Generalized Policy Iteration (GPI) is the umbrella framework that covers both.

---

## 8. Convergence Properties

### Why Value Iteration Converges

> [!important] Contraction Mapping Theorem
> Define the **Bellman optimality operator** $T$ as:
>
> $$(TV)(s) = \max_a \sum_{s',r} p(s',r \mid s,a)\bigl[r + \gamma\, V(s')\bigr]$$
>
> For $\gamma < 1$, $T$ is a **contraction mapping** in the max-norm:
>
> $$\|TV_1 - TV_2\|_\infty \;\le\; \gamma \,\|V_1 - V_2\|_\infty$$
>
> By the Banach Fixed Point Theorem, $T$ has a unique fixed point ($V^*$), and repeatedly applying $T$ from any starting $V_0$ converges to $V^*$.

### Key Convergence Facts

1. **Any initialisation works.** $V_0$ can be all zeros, random values, or anything else. Convergence is guaranteed.
2. **Rate of convergence.** After $k$ iterations, the error satisfies:

$$\|V_k - V^*\|_\infty \;\le\; \gamma^k \,\|V_0 - V^*\|_\infty$$

   Larger $\gamma$ (closer to 1) means slower convergence.

3. **Stopping criterion.** When $\delta < \theta$, the current $V$ satisfies:

$$\|V - V^*\|_\infty \;\le\; \frac{\theta\,\gamma}{1 - \gamma}$$

   This bound comes from the geometric series of remaining contractions.

4. **$\gamma = 1$ (undiscounted).** Convergence is not guaranteed for continuing tasks. For episodic tasks with guaranteed termination, convergence still holds.

---

## 9. Key Formulas

> [!danger] MUST MEMORIZE -- Value Iteration Update
> $$V_{k+1}(s) = \max_a \sum_{s',r} p(s',r \mid s,a)\bigl[r + \gamma\, V_k(s')\bigr]$$
>
> - $V_{k+1}(s)$: updated value of state $s$ at iteration $k+1$
> - $\max_a$: choose the action that maximises the expression
> - $p(s',r \mid s,a)$: dynamics of the MDP
> - $r$: immediate reward
> - $\gamma$: discount factor
> - $V_k(s')$: value of successor state from the previous iteration

> [!danger] MUST MEMORIZE -- Policy Extraction
> $$\pi^*(s) = \arg\max_a \sum_{s',r} p(s',r \mid s,a)\bigl[r + \gamma\, V^*(s')\bigr]$$
>
> - $\pi^*(s)$: optimal action in state $s$
> - $\arg\max_a$: the action that achieves the maximum (not the maximum value itself)
> - Uses the converged $V^*$ from value iteration

> [!danger] MUST MEMORIZE -- Contraction Bound
> $$\|TV_1 - TV_2\|_\infty \le \gamma\,\|V_1 - V_2\|_\infty$$
>
> - $T$: Bellman optimality operator
> - $\|\cdot\|_\infty$: max-norm (largest absolute element)
> - $\gamma$: discount factor; the contraction factor

> [!danger] MUST MEMORIZE -- Error After $k$ Iterations
> $$\|V_k - V^*\|_\infty \le \gamma^k\,\|V_0 - V^*\|_\infty$$

---

## 10. Derivations

### Derivation 1: Value Iteration from Truncated Policy Iteration

**Starting point:** Policy iteration with iterative policy evaluation.

Policy evaluation for policy $\pi$ performs repeated sweeps:

$$V_{k+1}^{\pi}(s) = \sum_a \pi(a \mid s)\sum_{s',r} p(s',r \mid s,a)\bigl[r + \gamma\, V_k^{\pi}(s')\bigr]$$

until convergence, then policy improvement sets:

$$\pi'(s) = \arg\max_a \sum_{s',r} p(s',r \mid s,a)\bigl[r + \gamma\, V^{\pi}(s')\bigr]$$

**Truncation step:** Instead of running evaluation to convergence, perform exactly **one** sweep:

$$V_1^{\pi}(s) = \sum_a \pi(a \mid s)\sum_{s',r} p(s',r \mid s,a)\bigl[r + \gamma\, V_0(s')\bigr]$$

Then immediately improve. But if we are going to improve right away, the evaluation under $\pi$ and improvement via $\max$ can be **fused into a single step**:

$$V_{k+1}(s) = \max_a \sum_{s',r} p(s',r \mid s,a)\bigl[r + \gamma\, V_k(s')\bigr]$$

The $\sum_a \pi(a|s)(\ldots)$ from evaluation and the $\arg\max_a$ from improvement collapse into a single $\max_a$, because the greedy policy puts all weight on the maximising action.

> [!success] Result
> Value iteration is exactly policy iteration with the evaluation phase truncated to one sweep, with evaluation and improvement merged into a single update.

### Derivation 2: The Update Rule from the Bellman Optimality Equation

The Bellman optimality equation states that $V^*$ satisfies:

$$V^*(s) = \max_a \sum_{s',r} p(s',r \mid s,a)\bigl[r + \gamma\, V^*(s')\bigr]$$

This is a system of $|S|$ nonlinear equations (nonlinear because of the $\max$). Solving it directly is generally hard.

**Fixed-point iteration approach:** Replace $V^*$ on the left with $V_{k+1}$ and $V^*$ on the right with the current estimate $V_k$:

$$V_{k+1}(s) = \max_a \sum_{s',r} p(s',r \mid s,a)\bigl[r + \gamma\, V_k(s')\bigr]$$

This is a standard fixed-point iteration. The contraction property of the Bellman optimality operator (Section 8) guarantees that this iteration converges to the fixed point $V^*$.

---

## 11. Synchronous vs Asynchronous DP

### Synchronous Updates

In the standard (synchronous) version:

- Every state is updated exactly once per sweep.
- All updates in a given sweep use values from the **same** iteration.
- Implementation requires **two arrays**: $V_{\text{old}}$ (read from) and $V_{\text{new}}$ (write to). After the sweep, $V_{\text{new}}$ becomes $V_{\text{old}}$.

### In-Place Updates

A common practical variant:

- Use a **single array** for $V$.
- When updating $V(s)$, successor states $s'$ that were already updated in this sweep use their **new** values; those not yet updated use their old values.
- The result depends on the **ordering** of state updates.
- Often converges faster in practice because information propagates within a sweep.
- The hand-traced example in Section 6 used in-place updates (notice $V(s_2)$ used the freshly updated $V(s_1)$).

> [!note] Convergence Guarantee
> In-place value iteration still converges to $V^*$ regardless of update ordering, as long as every state continues to be updated (no state is permanently neglected).

### Asynchronous Dynamic Programming

More general than in-place updates. Key idea: states can be updated in **any order, at any frequency**, as long as all states continue to be updated over time.

**Variants include:**

1. **Real-time DP:** Only update states that the agent actually visits during interaction. Focuses computation on relevant parts of the state space.

2. **Prioritized sweeping:** Maintain a priority queue. After updating a state whose value changed significantly, give high priority to its **predecessor** states (states that transition into it). Update the highest-priority state next.

> [!tip] Why Asynchronous Matters
> For MDPs with millions of states, synchronous sweeps are impractical. Asynchronous methods let you focus computation where it matters most -- states the agent is likely to visit or states whose values are changing rapidly.

3. **State-subset updates:** Only update a selected subset of states each sweep. Useful when some states are known to be irrelevant.

---

## 12. Complexity Analysis of DP Methods

| Method | Cost Per Sweep | Iterations (Typical) | Notes |
|--------|---------------|---------------------|-------|
| **Policy Evaluation** (iterative) | $O(|S|^2 \cdot |A|)$ | Until $V^{\pi}$ converges | Inner loop of policy iteration |
| **Policy Evaluation** (exact/linear algebra) | $O(|S|^3)$ | 1 (direct solve) | Solve linear system $V = R^{\pi} + \gamma P^{\pi} V$ |
| **Policy Iteration** | $O(|S|^2 \cdot |A| + |S|^3)$ per outer iteration | $O(|A|^{|S|})$ worst case, but usually very few | Each outer iteration: full evaluation + improvement |
| **Value Iteration** | $O(|S|^2 \cdot |A|)$ | Depends on $\theta$ and $\gamma$; roughly $O\!\left(\frac{\log(1/\theta)}{1 - \gamma}\right)$ | Single sweep per iteration |

### Breakdown of the $O(|S|^2 \cdot |A|)$ per-sweep cost:

- For each of the $|S|$ states: examine each of $|A|$ actions.
- For each action: sum over at most $|S|$ successor states.
- Total: $|S| \times |A| \times |S| = O(|S|^2 \cdot |A|)$.

> [!warning] Curse of Dimensionality
> All DP methods suffer from the curse of dimensionality. If the state is described by $d$ variables each taking $n$ values, then $|S| = n^d$ and the per-sweep cost grows exponentially with $d$. This motivates approximate methods (function approximation, Monte Carlo, TD learning).

---

## 13. Common Mistakes

> [!warning] Common Mistakes -- Avoid These on the Exam

**Mistake 1: Confusing the Bellman expectation equation with the Bellman optimality equation.**
- Expectation equation: $V^{\pi}(s) = \sum_a \pi(a|s) \sum_{s',r} p(s',r|s,a)[r + \gamma V^{\pi}(s')]$ -- averages over policy.
- Optimality equation: $V^*(s) = \max_a \sum_{s',r} p(s',r|s,a)[r + \gamma V^*(s')]$ -- takes max over actions.
- Value iteration uses the **optimality** equation. Policy evaluation uses the **expectation** equation.

**Mistake 2: Extracting the policy during the value iteration loop.**
- Value iteration does NOT maintain an explicit policy during its loop. The policy is extracted **only after** the value function converges.

**Mistake 3: Forgetting to set $V(\text{terminal}) = 0$.**
- Terminal states must always have value zero. Failing to enforce this leads to incorrect value propagation.

**Mistake 4: Using $V_{k+1}(s')$ instead of $V_k(s')$ in synchronous updates.**
- In synchronous (two-array) updates, successor values come from the **old** array. In in-place updates, this distinction does not apply.

**Mistake 5: Believing value iteration always converges faster than policy iteration.**
- Value iteration has cheaper iterations but needs more of them. Policy iteration can converge in very few outer iterations. Neither is universally faster; it depends on the MDP.

**Mistake 6: Thinking $\gamma = 1$ always prevents convergence.**
- For **episodic** tasks with guaranteed termination, $\gamma = 1$ is fine. It is **continuing** (non-terminating) tasks with $\gamma = 1$ where convergence breaks down.

---

## 14. Self-Check Questions

> [!question]- Q1: Why is the max operator in value iteration's update rule equivalent to doing policy improvement?
> The max over actions selects the greedy action with respect to the current value estimates. This is exactly what policy improvement does -- it picks the action that maximises the expected return under the current value function. Folding the max into the update combines evaluation (one step) and improvement (greedy selection) into a single operation.

> [!question]- Q2: If you initialise all values to +1000, will value iteration still converge to $V^*$?
> Yes. The contraction mapping property guarantees convergence from **any** initialisation. The Bellman optimality operator is a $\gamma$-contraction, so the distance to $V^*$ shrinks by a factor of $\gamma$ each iteration regardless of the starting point. It may just take more iterations than starting from zero.

> [!question]- Q3: In the hand-traced example, the optimal policy creates a loop rather than going to the terminal state. Under what condition would the agent prefer to exit?
> If $\gamma$ were small enough, the discounting would make the infinite stream of small rewards worth less than the one-time exit reward. Specifically, if $\gamma$ is low enough that $\frac{2 + 0.9\gamma}{1 - \gamma^2} < 6$ (for $s_1$) and similar for $s_2$, the agent would prefer to exit. Intuitively, a very impatient agent (low $\gamma$) grabs the immediate big reward.

> [!question]- Q4: What is the relationship between the convergence threshold $\theta$ and the actual error $\|V - V^*\|_\infty$?
> When value iteration stops with $\delta < \theta$, the actual error is bounded by $\frac{\theta \gamma}{1 - \gamma}$. So the true error can be larger than $\theta$ itself, especially when $\gamma$ is close to 1. To guarantee the error is below some target $\epsilon$, set $\theta = \frac{\epsilon(1-\gamma)}{\gamma}$.

> [!question]- Q5: Can you run value iteration without knowing the transition probabilities $p(s',r|s,a)$?
> No. Value iteration is a **model-based** method -- it requires full knowledge of the MDP dynamics. For model-free settings (where you only have sample transitions), you need methods like Monte Carlo ([[04_monte_carlo_prediction]], [[05_monte_carlo_control]]) or Temporal Difference learning.

> [!question]- Q6: What happens to the number of iterations needed if you double $\gamma$ from 0.45 to 0.9?
> Convergence slows dramatically. The error decays as $\gamma^k$, so to reach a given precision you need roughly $k \propto \frac{1}{\log(1/\gamma)}$ iterations. As $\gamma \to 1$, $\log(1/\gamma) \to 0$ and the required iterations grow without bound. Doubling $\gamma$ from 0.45 to 0.9 can easily multiply the iteration count by an order of magnitude.

> [!question]- Q7: In what sense is value iteration a special case of Generalized Policy Iteration (GPI)?
> GPI is the general idea of interleaving policy evaluation and policy improvement in any proportion. Policy iteration does full evaluation then full improvement. Value iteration does minimal evaluation (one sweep) then implicit improvement (the max). Both are points on the GPI spectrum. Any scheme that alternates some evaluation with some improvement, and does not neglect either, will converge to $V^*$ and $\pi^*$.

---

## 15. Concept Links

| Concept | Link | Relationship |
|---------|------|-------------|
| Dynamic Programming foundations | [[01_dynamic_programming]] | Value iteration is a DP method; requires understanding of iterative policy evaluation |
| Policy Iteration | [[02_policy_iteration]] | Value iteration is the truncated version; compare and contrast extensively |
| Monte Carlo Prediction | [[04_monte_carlo_prediction]] | Model-free alternative to DP for estimating value functions |
| Monte Carlo Control | [[05_monte_carlo_control]] | Model-free alternative to DP for finding optimal policies |
| Importance Sampling | [[06_importance_sampling]] | Technique used in off-policy MC methods; not directly related to VI but part of the same exam |
| Bellman Equations | [[01_dynamic_programming]] | Value iteration is derived directly from the Bellman optimality equation |
| Generalized Policy Iteration | [[02_policy_iteration]] | GPI is the unifying framework; VI and PI are both instances of GPI |

> [!abstract] Summary
> Value iteration simplifies policy iteration by truncating evaluation to one sweep and folding improvement into the update via the $\max$ operator. It converges to $V^*$ from any initialisation due to the contraction mapping property of the Bellman optimality operator. The algorithm is straightforward to implement, easy to trace by hand, and foundational for understanding more advanced RL methods.
