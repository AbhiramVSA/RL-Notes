# Bellman Optimality Equation and Convergence Proof

---

## Learning Objectives

After completing this section, you will be able to:

- State the claim that every finite MDP has at least one optimal policy and explain why this matters
- Define policy comparison using value functions and the L-infinity norm
- Write the Bellman optimality operator and explain its recursive structure
- Set up the complete metric space $(R^{|S|}, \|\cdot\|_\infty)$ for value functions
- Prove step by step that the Bellman optimality operator is a contraction mapping with factor $\gamma$
- Apply the Banach Fixed Point Theorem to conclude that a unique optimal value function $V^*$ exists
- Compute the L-infinity norm between two value function vectors
- Explain how $V^*$ leads to an optimal policy $\pi^*$
- Describe what iterative methods (value iteration, policy iteration, Q-learning) do once the theory is established

---

## Ground-Up Explanation

### The Claim

The central question of this section is: **does an optimal policy always exist for an MDP?** It might seem obvious that there should be a "best way" to act, but this needs rigorous proof. There could, in principle, be an infinite number of policies, none of which dominates all others at every state.

The theorem we want to prove is:

> **Theorem (Existence of Optimal Policy):** For any finite MDP, there exists an optimal policy $\pi^*$ that is better than or equal to every other policy $\pi$.

In notation:

$
\pi^* \geq \pi \quad \text{for all } \pi
$

This is a strong claim. It says no matter how many policies you consider, there is always at least one that is universally best -- it achieves the highest (or tied-for-highest) value at every single state simultaneously.

---

### Policy Comparison

Before we can talk about an "optimal" policy, we need to define what it means for one policy to be better than another. The definition is:

$
\pi_1 \geq \pi_2 \quad \text{if and only if} \quad V_{\pi_1}(s) \geq V_{\pi_2}(s) \quad \text{for all } s \in S
$

> **Where:**
> - $\pi_1, \pi_2$ = two policies being compared
> - $V_{\pi}(s)$ = value of state $s$ under policy $\pi$
> - $S$ = the set of all states in the MDP

A policy is better if its value function is greater at **every** state, not just some states. This is a pointwise comparison -- you check every state individually, and the inequality must hold at all of them.

If $V_{\pi_1}(s_1) > V_{\pi_2}(s_1)$ but $V_{\pi_1}(s_2) < V_{\pi_2}(s_2)$, then neither policy is uniformly better than the other. The claim above says that the optimal policy $\pi^*$ avoids this situation -- it wins (or ties) at every state against every other policy.

---

### Strategy: Prove via Banach Fixed Point Theorem

How do we prove that such a $\pi^*$ exists? The strategy is:

1. Define the **Bellman optimality operator** $B$.
2. Show that $B$ operates on a **complete metric space**.
3. Prove that $B$ is a **contraction mapping** on that space.
4. Apply the **Banach Fixed Point Theorem (BFPT)**: since $B$ is a contraction on a complete metric space, it has a unique fixed point $V^*$.
5. From $V^*$, derive the optimal policy $\pi^*$.

This is the same BFPT machinery covered in the previous section, but now applied to a specific operator -- the Bellman optimality operator.

---

### The Bellman Optimality Operator

The **Bellman optimality operator** $B$ is defined as:

$
BV(s) = \max_a \left[ R_s^a + \gamma \sum_{s' \in S} P_{ss'}^a \cdot V(s') \right]
$

> **Where:**
> - $BV(s)$ = the result of applying operator $B$ to value function $V$, evaluated at state $s$
> - $\max_a$ = take the maximum over all available actions $a$
> - $R_s^a$ = expected immediate reward for taking action $a$ in state $s$
> - $\gamma$ = discount factor, $0 \leq \gamma < 1$
> - $P_{ss'}^a$ = probability of transitioning to state $s'$ given action $a$ in state $s$
> - $V(s')$ = current value estimate of the next state $s'$
> - $S$ = the set of all states

The operator works as follows: for each state $s$, it considers every possible action $a$, computes the expected one-step return (immediate reward plus discounted expected future value), and picks the action that gives the **maximum** value. This is what makes it the "optimality" operator -- it always selects the best action.

The operator $B$ is **recursive**. You start with some initial value function $V_0$ (even a random guess), apply $B$ to get $V_1 = BV_0$, then apply $B$ again to get $V_2 = BV_1$, and so on. This generates a sequence of value functions:

$
V_0, \quad V_1 = BV_0, \quad V_2 = BV_1 = B^2V_0, \quad V_3 = B^3V_0, \quad \ldots
$

The critical question is: **does this sequence converge to a unique limit?** If $B$ is a contraction mapping on a complete metric space, then by BFPT, the answer is yes -- the sequence converges to a unique fixed point $V^*$ satisfying $BV^* = V^*$.

---

### Setting Up the Metric Space

To apply BFPT, we need three things: a set $X$, a metric $d$, and the pair $(X, d)$ must be a **complete metric space**.

**The set $X$:**

Each value function $V$ assigns a real number to each state. If the MDP has $|S|$ states, then $V$ is a vector in $R^{|S|}$. So the set $X$ is:

$
X = R^{|S|}
$

Each element of $X$ is a value function -- a vector of $|S|$ real numbers, one per state.

**The metric $d$ (L-infinity norm):**

We measure the distance between two value functions $V_1$ and $V_2$ using the **L-infinity norm** (also called the supremum norm or max norm):

$
\|V_1 - V_2\|_\infty = \max_{s \in S} |V_1(s) - V_2(s)|
$

> **Where:**
> - $\|V_1 - V_2\|_\infty$ = the L-infinity distance between value functions $V_1$ and $V_2$
> - $\max_{s \in S}$ = take the maximum over all states $s$
> - $|V_1(s) - V_2(s)|$ = absolute difference of the value functions at state $s$

In words: the L-infinity distance between two value functions is the **largest element-wise absolute difference** across all states. It finds the single state where the two value functions disagree the most, and uses that as the distance.

More generally, for any vector $X$:

$
\|X\|_\infty = \max_{i \in \{1, 2, \ldots, |X|\}} |X_i|
$

**Completeness:**

For a finite MDP with finite rewards, the value of any state is a bounded real number (because the discounted sum of bounded rewards converges). The space $R^{|S|}$ with the L-infinity norm is a complete metric space -- every Cauchy sequence of value function vectors converges to a limit that is also a value function vector in $R^{|S|}$.

This gives us the complete metric space $(R^{|S|}, \|\cdot\|_\infty)$.

---

### Proving B is a Contraction

This is the core of the convergence proof. We need to show that for any two value functions $V_1$ and $V_2$:

$
\|BV_1 - BV_2\|_\infty \leq \gamma \cdot \|V_1 - V_2\|_\infty
$

where $0 \leq \gamma < 1$ is the discount factor.

The proof proceeds step by step. We begin by expanding the left-hand side.

**Step 1: Expand the definitions.**

$
\|BV_1 - BV_2\|_\infty = \left\| \max_a \left[ R_s^a + \gamma \sum_{s'} P_{ss'}^a V_1(s') \right] - \max_{a'} \left[ R_s^{a'} + \gamma \sum_{s'} P_{ss'}^{a'} V_2(s') \right] \right\|_\infty
$

Here, $a$ is the action that maximizes the expression for $V_1$, and $a'$ is the action that maximizes it for $V_2$. These could be different actions.

**Step 2: Replace the optimal action $a'$ with $a$ (introduces inequality).**

The key insight is: $\max_a f(a) - \max_{a'} g(a') \leq \max_a [f(a) - g(a)]$. This is because replacing the independently optimal $a'$ with the same $a$ used on the left side can only make the difference larger (or equal). This gives us an inequality:

$
\leq \left\| \max_a \left[ R_s^a + \gamma \sum_{s'} P_{ss'}^a V_1(s') - R_s^a - \gamma \sum_{s'} P_{ss'}^a V_2(s') \right] \right\|_\infty
$

> **Why this step works:** When we take $\max_a$ of the first term and $\max_{a'}$ of the second term, the two maxima might be achieved by different actions. By forcing both terms to use the same action $a$ and then taking the max of the difference, we are potentially overestimating the gap. The true difference (left side) is at most as large as this overestimate (right side).

**Step 3: Cancel the reward terms.**

The $R_s^a$ terms cancel because they appear with opposite signs:

$
= \left\| \max_a \left[ \gamma \sum_{s'} P_{ss'}^a V_1(s') - \gamma \sum_{s'} P_{ss'}^a V_2(s') \right] \right\|_\infty
$

Factor out $\gamma$:

$
= \gamma \cdot \left\| \max_a \sum_{s'} P_{ss'}^a \left[ V_1(s') - V_2(s') \right] \right\|_\infty
$

**Step 4: Remove the L-infinity norm by taking the maximum over $s'$.**

The L-infinity norm takes the maximum over all states $s$. Inside the expression, we have a weighted sum over $s'$. We can bound this by pulling the maximum outside:

$
\leq \gamma \cdot \max_{s} \max_a \sum_{s'} P_{ss'}^a \left| V_1(s') - V_2(s') \right|
$

**Step 5: Bound the difference by the L-infinity norm.**

The absolute difference $|V_1(s') - V_2(s')|$ at any particular $s'$ is at most the maximum difference across all states, which is $\|V_1 - V_2\|_\infty$. Factor this out of the sum:

$
\leq \gamma \cdot \|V_1 - V_2\|_\infty \cdot \max_{s} \max_a \sum_{s'} P_{ss'}^a
$

**Step 6: Use the fact that transition probabilities sum to 1.**

For any state $s$ and any action $a$, the transition probabilities over all possible next states sum to 1:

$
\sum_{s' \in S} P_{ss'}^a = 1
$

This is a fundamental property of probability distributions. Therefore:

$
\leq \gamma \cdot \|V_1 - V_2\|_\infty \cdot 1 = \gamma \cdot \|V_1 - V_2\|_\infty
$

We have shown:

$
\|BV_1 - BV_2\|_\infty \leq \gamma \cdot \|V_1 - V_2\|_\infty
$

Since $0 \leq \gamma < 1$, the operator $B$ is a **contraction mapping** with contraction factor $\gamma$.

---

### Key Steps Explained

The proof has three pivotal moves that deserve special attention:

| Step | What Happens | Why It Works |
|------|-------------|--------------|
| Step 2 | Replace the independently optimal action $a'$ with the same action $a$ used in the first term | $\max f - \max g \leq \max(f - g)$. Using the same action for both terms introduces an inequality because we are no longer using the best action for $V_2$ |
| Step 4 | Remove the L-infinity norm by resolving the max over states $s$ | The L-infinity norm is defined as the max over all states. We absorb this into the expression by writing $\max_s$ explicitly |
| Step 6 | Eliminate the summation $\sum_{s'} P_{ss'}^a$ | Transition probabilities form a valid probability distribution, so they sum to exactly 1 for every state-action pair. This removes the entire summation factor |

---

### Conclusion

Putting the full argument together:

1. **Complete metric space:** $(R^{|S|}, \|\cdot\|_\infty)$ is a complete metric space. Value functions are vectors of real numbers, and the L-infinity norm is a valid metric.

2. **Contraction:** The Bellman optimality operator $B$ is a contraction mapping with contraction factor $\gamma < 1$, as shown in the step-by-step proof above.

3. **BFPT:** By the Banach Fixed Point Theorem, since $B$ is a contraction on a complete metric space, there exists a **unique** fixed point $V^*$ such that $BV^* = V^*$. Moreover, starting from any initial value function $V_0$, the sequence $V_0, BV_0, B^2V_0, \ldots$ converges to $V^*$.

4. **Optimal policy:** From the optimal value function $V^*$, we can derive the optimal policy $\pi^*$ by selecting, at each state, the action that achieves the maximum in the Bellman optimality equation:

$
\pi^*(s) = \arg\max_a \left[ R_s^a + \gamma \sum_{s'} P_{ss'}^a V^*(s') \right]
$

5. **Therefore:** For any finite MDP, an optimal policy $\pi^*$ exists that is better than or equal to every other policy.

> **Key Insight:** The entire proof chain is: define the metric space, prove the operator is a contraction, invoke BFPT, conclude uniqueness of $V^*$, extract $\pi^*$. This chain is the backbone of why value iteration and policy iteration work.

---

### What Next: From Theory to Practice

The proof tells us that a unique $V^*$ exists and that we can reach it by repeatedly applying $B$. But in practice, computing $BV$ requires iterating over all states and all actions at each step, which is computationally expensive for large state spaces.

This motivates several **iterative methods** for finding $V^*$ (or approximating it):

| Method | Idea | How It Relates |
|--------|------|----------------|
| **Value Iteration** | Directly apply $B$ repeatedly: $V_{k+1} = BV_k$ until convergence | Exactly the BFPT iteration; guaranteed to converge by the contraction proof |
| **Policy Iteration** | Alternate between evaluating a policy (finding $V_\pi$) and improving it (finding a greedy policy w.r.t. $V_\pi$) | Uses the Bellman expectation operator for evaluation and the optimality operator for improvement |
| **Q-Learning** | A model-free temporal difference method that learns $Q(s,a)$ directly from experience | Does not require knowing $P_{ss'}^a$ or $R_s^a$; converges to $Q^*$ under certain conditions |
| **SARSA** | Another TD method, but on-policy (learns the value of the policy it is actually following) | Converges to $Q_\pi$ for the policy being executed |

These methods are covered in later modules. The convergence proof in this section provides the theoretical foundation that guarantees these methods are well-grounded.

---

## Analogies

**Value iteration as GPS recalculating a route.** Imagine you are driving and your GPS has an initial estimate of the best route (your initial $V_0$). At each intersection, the GPS recalculates by checking every possible road (every action), estimating the remaining travel time for each option (the Bellman equation), and picking the best one (the max). After recalculating enough times ($BV_0, B^2V_0, \ldots$), the GPS converges on the truly optimal route ($V^*$). The contraction property guarantees that each recalculation gets you closer to the true optimum -- the GPS never diverges or oscillates wildly. The discount factor $\gamma$ is like a preference for shorter routes: the further away a road segment is, the less it influences your current decision.

**L-infinity norm as "worst-case disagreement."** Suppose two weather forecasters each predict temperatures for 5 cities. Forecaster A says [20, 25, 18, 30, 22] and Forecaster B says [21, 25, 15, 30, 23]. The L-infinity distance between them is the city where they disagree the most: $|18 - 15| = 3$. It does not matter that they agree perfectly on some cities -- the L-infinity norm cares only about the worst case.

---

## Key Formulas

> **CRITICAL EQUATION**
>
> **Bellman Optimality Operator**
>
> $
> BV(s) = \max_a \left[ R_s^a + \gamma \sum_{s' \in S} P_{ss'}^a \cdot V(s') \right]
> $

> **Where:**
> - $B$ = Bellman optimality operator
> - $V(s)$ = value function at state $s$
> - $\max_a$ = maximize over all actions
> - $R_s^a$ = expected reward for action $a$ in state $s$
> - $\gamma$ = discount factor ($0 \leq \gamma < 1$)
> - $P_{ss'}^a$ = transition probability from $s$ to $s'$ under action $a$

---

> **CRITICAL EQUATION**
>
> **L-Infinity Norm**
>
> $
> \|X\|_\infty = \max_{i} |X_i|
> $

> **Where:**
> - $\|X\|_\infty$ = the L-infinity (max) norm of vector $X$
> - $X_i$ = the $i$-th component of $X$

---

> **CRITICAL EQUATION**
>
> **Contraction Result for the Bellman Operator**
>
> $
> \|BV_1 - BV_2\|_\infty \leq \gamma \cdot \|V_1 - V_2\|_\infty
> $

> **Where:**
> - $BV_1, BV_2$ = result of applying $B$ to value functions $V_1$ and $V_2$
> - $\gamma$ = discount factor (contraction constant)
> - $\|\cdot\|_\infty$ = L-infinity norm

---

**Policy Comparison:**

$
\pi_1 \geq \pi_2 \quad \text{if and only if} \quad V_{\pi_1}(s) \geq V_{\pi_2}(s) \quad \text{for all } s \in S
$

---

**Optimal Policy Extraction from $V^*$:**

$
\pi^*(s) = \arg\max_a \left[ R_s^a + \gamma \sum_{s'} P_{ss'}^a V^*(s') \right]
$

---

## Derivations

### Full Contraction Proof for the Bellman Optimality Operator

**Goal:** Show $\|BV_1 - BV_2\|_\infty \leq \gamma \cdot \|V_1 - V_2\|_\infty$.

**Starting point:**

$
\|BV_1 - BV_2\|_\infty = \left\| \max_a \left[ R_s^a + \gamma \sum_{s'} P_{ss'}^a V_1(s') \right] - \max_{a'} \left[ R_s^{a'} + \gamma \sum_{s'} P_{ss'}^{a'} V_2(s') \right] \right\|_\infty
$

**Step 1 -- Replace $a'$ with $a$:** Using the property $\max_x f(x) - \max_x g(x) \leq \max_x [f(x) - g(x)]$:

$
\leq \left\| \max_a \left[ R_s^a + \gamma \sum_{s'} P_{ss'}^a V_1(s') - R_s^a - \gamma \sum_{s'} P_{ss'}^a V_2(s') \right] \right\|_\infty
$

**Step 2 -- Cancel $R_s^a$ and factor $\gamma$:**

$
= \gamma \cdot \left\| \max_a \sum_{s'} P_{ss'}^a \left[ V_1(s') - V_2(s') \right] \right\|_\infty
$

**Step 3 -- Bound the weighted sum by the maximum difference:**

$
\leq \gamma \cdot \max_s \max_a \sum_{s'} P_{ss'}^a \left| V_1(s') - V_2(s') \right|
$

**Step 4 -- Factor out $\|V_1 - V_2\|_\infty$:** Since $|V_1(s') - V_2(s')| \leq \|V_1 - V_2\|_\infty$ for all $s'$:

$
\leq \gamma \cdot \|V_1 - V_2\|_\infty \cdot \max_s \max_a \sum_{s'} P_{ss'}^a
$

**Step 5 -- Transition probabilities sum to 1:**

$
\sum_{s'} P_{ss'}^a = 1 \quad \text{for all } s, a
$

Therefore:

$
\leq \gamma \cdot \|V_1 - V_2\|_\infty
$

**Conclusion:** $B$ is a contraction with factor $\gamma$. By BFPT on the complete metric space $(R^{|S|}, \|\cdot\|_\infty)$, a unique fixed point $V^* = BV^*$ exists.

---

## Worked Examples

### Example 1: Computing the L-Infinity Norm Between Two Value Functions

This matches the format from **Paper 1, Q5(c)**.

**Given:**

$
V_1 = [1.1, \; 2.4, \; 3.21, \; 4.2]
$

$
V_2 = [1.12, \; 2.4, \; 3.0, \; 4.19]
$

**Step 1:** Compute the element-wise absolute differences.

| State $s$ | $V_1(s)$ | $V_2(s)$ | $|V_1(s) - V_2(s)|$ |
|:---------:|:---------:|:---------:|:--------------------:|
| $s_1$ | 1.1 | 1.12 | $|1.1 - 1.12| = 0.02$ |
| $s_2$ | 2.4 | 2.4 | $|2.4 - 2.4| = 0.0$ |
| $s_3$ | 3.21 | 3.0 | $|3.21 - 3.0| = 0.21$ |
| $s_4$ | 4.2 | 4.19 | $|4.2 - 4.19| = 0.01$ |

**Step 2:** Take the maximum of all absolute differences.

$
\|V_1 - V_2\|_\infty = \max(0.02, \; 0.0, \; 0.21, \; 0.01) = 0.21
$

> **Answer:** $\|V_1 - V_2\|_\infty = 0.21$

The L-infinity distance is determined by state $s_3$, where the two value functions disagree the most.

---

### Example 2: Verifying the Contraction Property

Suppose after one application of the Bellman operator to $V_1$ and $V_2$, we obtain:

$
BV_1 = [5.0, \; 3.2, \; 7.1, \; 6.5]
$

$
BV_2 = [4.95, \; 3.18, \; 7.0, \; 6.48]
$

and the discount factor is $\gamma = 0.9$.

**Step 1:** Compute $\|BV_1 - BV_2\|_\infty$.

| State | $|BV_1(s) - BV_2(s)|$ |
|:-----:|:---------------------:|
| $s_1$ | $|5.0 - 4.95| = 0.05$ |
| $s_2$ | $|3.2 - 3.18| = 0.02$ |
| $s_3$ | $|7.1 - 7.0| = 0.10$ |
| $s_4$ | $|6.5 - 6.48| = 0.02$ |

$
\|BV_1 - BV_2\|_\infty = 0.10
$

**Step 2:** Compute $\gamma \cdot \|V_1 - V_2\|_\infty$ using $V_1$ and $V_2$ from Example 1.

$
\gamma \cdot \|V_1 - V_2\|_\infty = 0.9 \times 0.21 = 0.189
$

**Step 3:** Check the contraction condition.

$
\|BV_1 - BV_2\|_\infty = 0.10 \leq 0.189 = \gamma \cdot \|V_1 - V_2\|_\infty
$

> **Answer:** The contraction condition holds. The distance between the value functions decreased after applying $B$, confirming that $B$ is bringing them closer together.

---

## Common Mistakes

- **Forgetting the absolute value in the L-infinity norm.** The norm uses $|V_1(s) - V_2(s)|$, not $V_1(s) - V_2(s)$. Without the absolute value, negative differences could cancel positive ones and give incorrect results.

- **Confusing the contraction factor with the discount factor.** In this specific proof, the contraction factor happens to be $\gamma$ (the discount factor). But in general, a contraction mapping can have any contraction constant $c \in [0, 1)$. The coincidence here is specific to the Bellman operator.

- **Skipping the inequality step (Step 2).** Students often jump from the difference of two maxima to factoring out terms without explaining why the inequality holds. The step $\max f - \max g \leq \max(f - g)$ is essential and must be stated explicitly.

- **Claiming the proof works for $\gamma = 1$.** When $\gamma = 1$, the operator is not a contraction (it is non-expansive at best), and BFPT does not apply. Convergence guarantees require $\gamma < 1$ strictly.

- **Thinking value iteration gives the exact $V^*$ in finite steps.** BFPT guarantees convergence in the limit. In practice, we iterate until the change is below some threshold $\epsilon$, obtaining an approximation to $V^*$.

- **Forgetting that $\sum_{s'} P_{ss'}^a = 1$ is what makes Step 6 work.** Without this probability axiom, the summation factor would remain and the contraction would not hold with factor $\gamma$ alone.

- **Confusing the Bellman optimality operator with the Bellman expectation operator.** The optimality operator uses $\max_a$ (selects the best action). The expectation operator $T^\pi$ uses a fixed policy $\pi$ and takes an expectation over actions according to $\pi$. Both are contractions, but they answer different questions.

---

## Self-Check Questions

<details>
<summary>Q1: State the theorem about the existence of an optimal policy for finite MDPs.</summary>

**Answer:** For any finite MDP, there exists an optimal policy $\pi^*$ that is better than or equal to every other policy $\pi$. Formally, $\pi^* \geq \pi$ for all $\pi$, meaning $V_{\pi^*}(s) \geq V_{\pi}(s)$ for all states $s \in S$. The proof uses the Banach Fixed Point Theorem: the Bellman optimality operator is a contraction on the complete metric space $(R^{|S|}, \|\cdot\|_\infty)$, so it has a unique fixed point $V^*$, from which the optimal policy $\pi^*$ can be extracted.

</details>

<details>
<summary>Q2: What does the L-infinity norm measure when applied to the difference of two value functions?</summary>

**Answer:** The L-infinity norm $\|V_1 - V_2\|_\infty = \max_s |V_1(s) - V_2(s)|$ measures the worst-case disagreement between two value functions. It finds the single state where the two value functions differ the most in absolute terms and returns that maximum absolute difference. It does not average the differences; it reports only the largest one.

</details>

<details>
<summary>Q3: Why does replacing the optimal action $a'$ with $a$ in Step 2 introduce an inequality?</summary>

**Answer:** In the original expression, $\max_a f(a) - \max_{a'} g(a')$, the first max picks the best action for $f$ and the second max independently picks the best action for $g$. When we force both terms to use the same action $a$ and then take the max of the difference $\max_a [f(a) - g(a)]$, we are potentially overestimating, because the action that maximizes $f(a) - g(a)$ is not necessarily the action that minimizes $g$. Since $\max_{a'} g(a') \geq g(a)$ for any specific $a$, subtracting the max gives a smaller (or equal) result than subtracting a specific value. Hence, $\max f - \max g \leq \max(f - g)$.

</details>

<details>
<summary>Q4: Why is it important that the transition probabilities sum to 1 in the contraction proof?</summary>

**Answer:** In Step 5 of the proof, after factoring out $\|V_1 - V_2\|_\infty$, we are left with the factor $\sum_{s'} P_{ss'}^a$. Because transition probabilities form a valid probability distribution, this sum equals exactly 1 for every state-action pair. This eliminates the entire summation factor, leaving only $\gamma \cdot \|V_1 - V_2\|_\infty$. Without this property, the bound would include an additional multiplicative factor that could potentially exceed 1, breaking the contraction argument.

</details>

<details>
<summary>Q5: What is the difference between the Bellman optimality operator and the Bellman expectation operator?</summary>

**Answer:** The Bellman optimality operator $B$ uses $\max_a$ to select the best action at each state: $BV(s) = \max_a [R_s^a + \gamma \sum_{s'} P_{ss'}^a V(s')]$. Its fixed point is the optimal value function $V^*$. The Bellman expectation operator $T^\pi$ uses a fixed policy $\pi$ and weights actions by the policy's probabilities: $T^\pi V(s) = \sum_a \pi(a|s) [R_s^a + \gamma \sum_{s'} P_{ss'}^a V(s')]$. Its fixed point is $V_\pi$, the value function of policy $\pi$. Both are contractions with factor $\gamma$, but they serve different purposes: $B$ finds the optimal value function, while $T^\pi$ evaluates a given policy.

</details>

<details>
<summary>Q6: Given $V_1 = [3.5, 7.2, 1.0]$ and $V_2 = [3.4, 7.5, 1.1]$, compute $\|V_1 - V_2\|_\infty$.</summary>

**Answer:** Compute the element-wise absolute differences: $|3.5 - 3.4| = 0.1$, $|7.2 - 7.5| = 0.3$, $|1.0 - 1.1| = 0.1$. The L-infinity norm is the maximum: $\|V_1 - V_2\|_\infty = \max(0.1, 0.3, 0.1) = 0.3$. The largest disagreement is at state $s_2$.

</details>

<details>
<summary>Q7: After proving that $V^*$ exists, how do you obtain the optimal policy $\pi^*$?</summary>

**Answer:** Once $V^*$ is known, the optimal policy is obtained by acting greedily with respect to $V^*$. For each state $s$, choose the action $a$ that maximizes the expected one-step return: $\pi^*(s) = \arg\max_a [R_s^a + \gamma \sum_{s'} P_{ss'}^a V^*(s')]$. Since $V^*$ is the unique optimal value function, the policy derived this way is guaranteed to be optimal.

</details>

---

## Exam Focus

> **Paper 1, Q3(a) (5 marks): Establish the need for contraction in Bellman convergence.**
>
> This question asks you to explain why the contraction property is essential. Your answer should cover:
> - The goal: proving that a unique optimal value function $V^*$ exists
> - The Bellman optimality operator $B$ generates sequences of value functions
> - Without contraction, there is no guarantee the sequence converges or that the limit is unique
> - With contraction, BFPT guarantees both convergence and uniqueness
> - State the contraction condition: $\|BV_1 - BV_2\|_\infty \leq \gamma \|V_1 - V_2\|_\infty$
> - Conclude: from the unique $V^*$, we derive $\pi^*$, proving optimal policy existence

> **Paper 2, Q3(a): Policy evaluation as finding fixed point of Bellman expectation operator.**
>
> This variant asks about $T^\pi$ rather than $B$. Your answer should:
> - Define $T^\pi V(s) = \sum_a \pi(a|s) [R_s^a + \gamma \sum_{s'} P_{ss'}^a V(s')]$
> - State that $V_\pi$ is the fixed point of $T^\pi$: $T^\pi V_\pi = V_\pi$
> - Explain that $T^\pi$ is also a contraction with factor $\gamma$
> - By BFPT, the fixed point $V_\pi$ exists and is unique
> - This means iterative policy evaluation (repeatedly applying $T^\pi$) converges to the true value function of $\pi$

> **Paper 1, Q5(c) (4 marks): Compute $\|V_1 - V_2\|_\infty$ given two value function vectors.**
>
> This is a direct numerical computation. You must:
> - Write out the element-wise absolute differences in a table
> - Take the maximum of all differences
> - State the final answer clearly
> - See Worked Example 1 above for the exact format matching the past paper values

> **High-Value Exam Topic: The Full Proof Chain**
>
> Both papers test the theoretical chain that connects metric spaces to optimal policies. Be prepared to reproduce the full argument:
>
> 1. Define the metric space: $X = R^{|S|}$ with the L-infinity norm
> 2. Show completeness: finite MDP with bounded rewards gives bounded values in $R^{|S|}$
> 3. Prove $B$ is a contraction: the six-step proof showing $\|BV_1 - BV_2\|_\infty \leq \gamma \|V_1 - V_2\|_\infty$
> 4. Apply BFPT: unique fixed point $V^*$ exists
> 5. Extract $\pi^*$: act greedily with respect to $V^*$
> 6. Conclusion: optimal policy exists for any finite MDP
>
> This chain has appeared in some form in both papers and is the most theory-heavy examinable topic. Being able to write it out completely and explain each step is worth up to 10 marks.

---

## Concept Links

- **Previous topic:** [Contraction Mapping and BFPT](./05_contraction_and_bfpt.md) -- Covers the general theory of contraction mappings and the Banach Fixed Point Theorem, which is the mathematical engine behind this section
- **Related topic:** [Mathematical Foundations](./04_mathematical_foundations.md) -- Covers metric spaces, norms, Cauchy sequences, and complete metric spaces that underpin the proof setup
- **Related topic:** [Elements of RL](./02_elements_of_rl.md) -- Covers policy comparison, value functions, and the distinction between reward and value, all of which are used here
- **Next topic:** [Worked Problems](./07_worked_problems.md) -- Full worked solutions for past paper questions on this topic
- **Formula sheet:** [Formula Sheet](./08_formula_sheet.md) -- All key equations consolidated
