---
type: topic
topic: monte-carlo-control
module: 3
exam_weight: high
prerequisites: [[04_monte_carlo_prediction]], [[02_policy_iteration]]
tags: [rl, cat2, monte-carlo, control, exploring-starts, epsilon-greedy, on-policy, off-policy]
---

# Monte Carlo Control

> [!warning] Source Slides Unavailable
> The original slides (MODULE3 3 Monte Carlo Control.pptx) were corrupted and could not be recovered. This guide is reconstructed from Sutton & Barto Chapter 5 and standard RL curriculum. It is written to be self-contained -- treat it as your primary reference for this topic.

---

## 1. Learning Objectives

After studying this topic, you should be able to:

1. **Explain why** MC control requires action-value functions $Q(s,a)$ rather than state-value functions $V(s)$, and connect this to the model-free setting.
2. **Describe the exploration problem** in MC control and articulate why greedy policy improvement alone is insufficient.
3. **Write and trace** the Monte Carlo ES (Exploring Starts) algorithm, including its convergence assumptions.
4. **Write and trace** the on-policy (epsilon-greedy) MC control algorithm, and explain what class of policies it converges to.
5. **Write and trace** the off-policy MC control algorithm using weighted importance sampling, and explain why episodes are processed backward and why we break early.
6. **Compare and contrast** all three MC control methods on exploration strategy, optimality guarantees, variance, and practical applicability.
7. **Apply** the epsilon-greedy policy improvement theorem to prove that the updated policy is at least as good as the current one.
8. **Identify** when to use on-policy vs. off-policy methods and the trade-offs involved.

---

## 2. Ground-Up Explanation

### The Story So Far

In [[04_monte_carlo_prediction]], we learned how to **estimate** $V^\pi(s)$ or $Q^\pi(s,a)$ for a given fixed policy $\pi$ by averaging sample returns from episodes. That solves the **prediction** problem.

But prediction is only half the story. What we really want is the **control** problem: find the **optimal** policy $\pi^*$.

### The Big Idea: GPI with Monte Carlo Evaluation

Recall from [[02_policy_iteration]] the framework of **Generalized Policy Iteration (GPI)**:

$$\pi_0 \xrightarrow{E} Q^{\pi_0} \xrightarrow{I} \pi_1 \xrightarrow{E} Q^{\pi_1} \xrightarrow{I} \pi_2 \xrightarrow{E} \cdots \xrightarrow{I} \pi^* \xrightarrow{E} Q^*$$

where $E$ = **evaluation** (estimate the value function) and $I$ = **improvement** (make the policy greedy w.r.t. the value function).

In DP, we used iterative policy evaluation for the $E$ step. In MC control, we replace that with **Monte Carlo evaluation** -- averaging returns from sampled episodes. The $I$ step (greedy improvement) remains the same idea, but we face two new challenges.

### Challenge 1: We Need Q, Not V

In DP, the improvement step was:

$$\pi'(s) = \arg\max_a \sum_{s', r} p(s', r \mid s, a)\big[r + \gamma V^\pi(s')\big]$$

This **requires the model** $p(s', r \mid s, a)$. Without it, knowing $V(s)$ is useless for choosing actions -- you cannot look ahead one step.

**Solution**: estimate **action-value** functions $Q^\pi(s,a)$ instead. Then improvement becomes:

$$\pi'(s) = \arg\max_a Q^\pi(s,a)$$

No model needed. This is the fundamental reason MC control works with $Q$ rather than $V$.

### Challenge 2: Exploration

If we always act greedily w.r.t. our current $Q$ estimate, we may **never visit** certain state-action pairs. If $(s,a)$ is never visited, $Q(s,a)$ is never updated, and we can never discover that $a$ might actually be the best action in state $s$.

**Solution**: we need mechanisms to ensure **continued exploration** of all state-action pairs. Three approaches:
1. **Exploring starts** -- assume every $(s,a)$ pair can be the starting point of an episode (unrealistic but theoretically clean).
2. **Epsilon-soft policies** -- always maintain a nonzero probability of choosing every action (on-policy).
3. **Separate behavior policy** -- use one policy to generate data, learn about another (off-policy).

### Building Up Step by Step

```
MC Prediction (V^pi)
    |
    v
MC Prediction for Q^pi  (track state-action returns)
    |
    v
MC Control with Exploring Starts  (GPI + exploring starts)
    |
    v
On-Policy MC Control  (GPI + epsilon-greedy, no exploring starts needed)
    |
    v
Off-Policy MC Control  (GPI + importance sampling, separate behavior policy)
```

Each step removes an assumption or limitation of the previous one, making the method more practical.

---

## 3. Analogies

> [!tip] Analogy 1 -- The Restaurant Explorer
> Imagine you move to a new city and want to find the best restaurant (optimal policy). **MC Prediction** is like rating only the restaurants you already go to. **MC Control** is like actively deciding which restaurants to try. **Exploring starts** is like being randomly teleported to a restaurant each evening. **Epsilon-greedy** is like going to your current favourite 90% of the time but trying a random place 10% of the time. **Off-policy** is like reading your adventurous friend's reviews (behavior policy) while building your own personal ranking (target policy).

> [!tip] Analogy 2 -- GPI as Two Competing Forces
> Think of GPI as two people holding a rope. One person (evaluation) keeps pulling the value function toward the true values for the current policy. The other person (improvement) keeps pulling the policy toward greediness w.r.t. the current values. They are pulling in different directions, but the point of equilibrium -- where neither person can pull further -- is the optimal policy and its true value function.

> [!tip] Analogy 3 -- Exploration vs. Exploitation as Research vs. Production
> A company that only exploits its best-known product never discovers breakthroughs (no exploration). A company that only does research never ships anything (no exploitation). Epsilon-greedy is like spending 90% of budget on production and 10% on R&D.

---

## 4. Why Action Values Q(s,a)?

This is a critical conceptual point that often appears on exams.

### With a Model (DP Setting)

Given $V^\pi(s)$ and the model $p(s',r \mid s,a)$, we can do policy improvement:

$$\pi'(s) = \arg\max_a \sum_{s',r} p(s', r \mid s, a)\big[r + \gamma V^\pi(s')\big]$$

The model lets us "look ahead" one step from state $s$ under each possible action $a$ and evaluate where we land.

### Without a Model (MC Setting)

We do **not** have $p(s',r \mid s,a)$. So the expression above is impossible to compute.

But if we have $Q^\pi(s,a)$, improvement is trivial:

$$\pi'(s) = \arg\max_a Q^\pi(s,a)$$

> [!important] Key Insight
> Action-value functions encode the result of taking each action **within themselves**. No model is needed to pick the best action -- just take the $\arg\max$ over $Q$ values.

### Modifying MC Prediction for Q

We simply change what we track. Instead of averaging returns starting from state $s$, we average returns starting from **state-action pair** $(s,a)$:

- Visit $(s,a)$ means the agent is in state $s$ and takes action $a$ at some time step $t$.
- The return from that point: $G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \cdots$
- **First-visit MC for Q**: average the return from the **first** time $(s,a)$ is visited in each episode.
- **Every-visit MC for Q**: average the return from **every** time $(s,a)$ is visited.

Both converge to $Q^\pi(s,a)$ as the number of episodes goes to infinity.

> [!warning] Exam Alert
> If asked "why does MC control use Q instead of V?", the answer is: **without a model of the environment, V(s) alone cannot determine which action is best. Q(s,a) directly associates values with actions, making model-free policy improvement possible.**

---

## 5. The Exploration Problem

### Why Exploration Matters

Suppose we have some initial estimate $Q(s,a)$ and form a greedy policy:

$$\pi(s) = \arg\max_a Q(s,a)$$

This policy is **deterministic**. It always picks the same action in each state. If our initial $Q$ estimates happen to be wrong (and they will be, since they start arbitrary), the greedy policy will never try alternatives. The $(s,a)$ pairs it skips will never get updated, so the agent may **permanently** miss the optimal action.

### Formal Requirement

For MC methods to converge to the correct $Q^\pi$, we need:

> Every state-action pair $(s,a)$ must be visited infinitely often in the limit.

This is the **exploration condition**. Without it, some $Q$ values will be estimated from zero samples and remain at their arbitrary initial values.

### Two Families of Solutions

| Approach | How it Ensures Exploration | Practical? |
|----------|---------------------------|-----------|
| **Exploring starts** | Every episode starts from a random $(s,a)$ | No -- cannot control starting conditions in most real environments |
| **Epsilon-soft policies** | Every action has probability $\geq \frac{\epsilon}{\lvert A(s) \rvert}$ in every state | Yes -- exploration is built into the policy |

A third approach, **off-policy learning**, separates exploration from the policy being learned -- explored in Section 8.

---

## 6. Monte Carlo Control with Exploring Starts (MC ES)

### The Algorithm

This is the simplest MC control method. It directly implements GPI: alternate between MC evaluation and greedy improvement, relying on exploring starts to guarantee exploration.

> [!abstract] MC ES -- Complete Pseudocode
> ```
> Initialize:
>     Q(s,a) <- arbitrary, for all s in S, a in A(s)
>     pi(s) <- arbitrary, for all s in S
>     Returns(s,a) <- empty list, for all s, a
>
> Repeat forever (for each episode):
>     1. Choose S_0 in S and A_0 in A(S_0) each with nonzero probability
>        (exploring starts)
>     2. Generate an episode starting from S_0, A_0, following pi:
>        S_0, A_0, R_1, S_1, A_1, R_2, ..., S_{T-1}, A_{T-1}, R_T
>     3. G <- 0
>     4. For t = T-1, T-2, ..., 0:
>            G <- gamma * G + R_{t+1}
>            Unless (S_t, A_t) appears in (S_0,A_0),...,(S_{t-1},A_{t-1}):
>                Append G to Returns(S_t, A_t)
>                Q(S_t, A_t) <- average(Returns(S_t, A_t))
>                pi(S_t) <- argmax_a Q(S_t, a)
> ```

### Line-by-Line Explanation

**Initialization**: $Q(s,a)$ is set to arbitrary values (often zero). The policy $\pi$ can also be arbitrary (e.g., random). An empty list is prepared for each $(s,a)$ pair to collect returns.

**Step 1 -- Exploring Starts**: Before each episode, we randomly select a starting state $S_0$ and starting action $A_0$. Every $(s,a)$ pair must have nonzero probability of being selected. This is the key assumption that guarantees exploration.

**Step 2 -- Episode Generation**: From $(S_0, A_0)$, the agent follows the current policy $\pi$ until the episode terminates. The first action is $A_0$ (forced), but all subsequent actions come from $\pi$.

**Step 3 -- Initialize Return**: We process the episode **backward** (from the terminal step to the start), accumulating the discounted return.

**Step 4 -- Update Loop** (for each time step, going backward):
- **Compute return**: $G \leftarrow \gamma G + R_{t+1}$ accumulates the discounted sum of future rewards.
- **First-visit check**: We only update if this is the **first** time $(S_t, A_t)$ appears in the episode (first-visit MC). This avoids double-counting.
- **Evaluation**: Append the return $G$ to the list for $(S_t, A_t)$, then update $Q(S_t, A_t)$ to be the average of all collected returns.
- **Improvement**: Immediately update $\pi(S_t)$ to be greedy w.r.t. the new $Q$ values. This is the policy improvement step, done **within** the same episode processing (not after a separate evaluation phase).

> [!note] Interleaved Evaluation and Improvement
> Notice that evaluation and improvement happen for each state in each episode, rather than waiting for Q to fully converge before improving. This is the GPI idea -- both processes run simultaneously and still converge.

### The Exploring Starts Assumption

The assumption requires that every $(s,a)$ pair has a nonzero probability of being selected as the starting pair of an episode. This ensures that, over infinite episodes, every pair is visited infinitely often.

> [!warning] Why Exploring Starts is Impractical
> In most real-world problems, you cannot choose the starting state freely. A robot cannot teleport to arbitrary positions. A game cannot start from an arbitrary board configuration. An autonomous car cannot begin at a random location on the road. Exploring starts is a theoretical tool, not a practical one.

### Convergence

> [!success] Convergence Guarantee
> Under the exploring starts assumption, MC ES converges to $Q^*$ and $\pi^*$ (the optimal action-value function and optimal policy) as the number of episodes approaches infinity.

The proof relies on:
1. The exploring starts condition ensuring all $(s,a)$ pairs are visited infinitely often.
2. The policy improvement theorem guaranteeing that greedy improvement never makes the policy worse.
3. There are finitely many deterministic policies, so the sequence of policies must converge.

### Hand-Traced Example

Consider a simple MDP with 2 states and 2 actions, $\gamma = 1$ (undiscounted):

```
States: {A, B}    Actions: {left, right}
Transitions (deterministic):
  A, left  -> A, reward = +1  (stays in A)
  A, right -> B, reward = +5  (moves to B)
  B, left  -> A, reward = 0   (moves to A)
  B, right -> B, reward = +2  (stays in B)
Episodes terminate after 3 steps.
```

**Initial Q (arbitrary):**

| | left | right |
|---|------|-------|
| A | 0 | 0 |
| B | 0 | 0 |

**Initial policy (arbitrary):** $\pi(A) = \text{left},\ \pi(B) = \text{left}$

**Episode 1**: Exploring starts selects $(A, \text{right})$.
- $t=0$: $S_0=A, A_0=\text{right}, R_1=5, S_1=B$
- $t=1$: $A_1=\pi(B)=\text{left}, R_2=0, S_2=A$
- $t=2$: $A_2=\pi(A)=\text{left}, R_3=1$. Episode ends.

Process backward:
- $t=2$: $G = 0 + 1 = 1$. First visit of $(A, \text{left})$. $Q(A,\text{left})=1$. $\pi(A)=\arg\max\{1, 0\}=\text{left}$.
- $t=1$: $G = 1 \cdot 1 + 0 = 1$. First visit of $(B, \text{left})$. $Q(B,\text{left})=1$. $\pi(B)=\arg\max\{1, 0\}=\text{left}$.
- $t=0$: $G = 1 \cdot 1 + 5 = 6$. First visit of $(A, \text{right})$. $Q(A,\text{right})=6$. $\pi(A)=\arg\max\{1, 6\}=\text{right}$.

**Updated Q:**

| | left | right |
|---|------|-------|
| A | 1 | 6 |
| B | 1 | 0 |

**Updated policy:** $\pi(A) = \text{right},\ \pi(B) = \text{left}$

After more episodes (especially one starting from $(B, \text{right})$), $Q(B, \text{right})$ would be updated and the policy would converge. The key point: exploring starts forces us to try $(A, \text{right})$ in Episode 1, which we would have missed with the initial greedy policy.

---

## 7. On-Policy MC Control (Epsilon-Greedy)

### Motivation

To remove the exploring starts assumption, we build exploration **into the policy itself**. The policy is no longer deterministic -- it is **stochastic**, always assigning some probability to every action.

### On-Policy vs. Off-Policy

> [!info] On-Policy Definition
> **On-policy** methods evaluate and improve the **same** policy that is used to generate episodes. The agent learns about the policy it is currently following.

### Epsilon-Greedy Policy

Given current action-value estimates $Q(s,a)$ and a parameter $\epsilon \in (0, 1]$:

$$\pi(a \mid s) = \begin{cases} 1 - \epsilon + \dfrac{\epsilon}{|A(s)|} & \text{if } a = \arg\max_{a'} Q(s, a') \\[10pt] \dfrac{\epsilon}{|A(s)|} & \text{if } a \neq \arg\max_{a'} Q(s, a') \end{cases}$$

Where $|A(s)|$ is the number of available actions in state $s$.

**Properties:**
- The greedy action gets the lion's share of probability: $1 - \epsilon + \frac{\epsilon}{|A(s)|}$.
- Every non-greedy action gets a small probability: $\frac{\epsilon}{|A(s)|}$.
- Every action has probability $\geq \frac{\epsilon}{|A(s)|} > 0$, so all actions are tried eventually.
- When $\epsilon = 0$, this reduces to a purely greedy policy.
- When $\epsilon = 1$, this is a uniformly random policy.

> [!info] Epsilon-Soft Policy
> A policy is **epsilon-soft** if $\pi(a \mid s) \geq \frac{\epsilon}{|A(s)|}$ for all $s$ and $a$. Epsilon-greedy is the most common example, but any policy satisfying this lower bound qualifies. Among all epsilon-soft policies, epsilon-greedy is closest to the true greedy policy.

### The Algorithm

> [!abstract] On-Policy MC Control -- Complete Pseudocode
> ```
> Initialize:
>     Q(s,a) <- arbitrary, for all s in S, a in A(s)
>     Returns(s,a) <- empty list, for all s, a
>     Choose epsilon in (0, 1]
>     pi <- epsilon-greedy policy w.r.t. Q
>
> Repeat forever (for each episode):
>     1. Generate episode following pi:
>        S_0, A_0, R_1, S_1, A_1, R_2, ..., S_{T-1}, A_{T-1}, R_T
>     2. G <- 0
>     3. For t = T-1, T-2, ..., 0:
>            G <- gamma * G + R_{t+1}
>            Unless (S_t, A_t) appears in (S_0,A_0),...,(S_{t-1},A_{t-1}):
>                Append G to Returns(S_t, A_t)
>                Q(S_t, A_t) <- average(Returns(S_t, A_t))
>                A* <- argmax_a Q(S_t, a)
>                For all a in A(S_t):
>                    If a = A*:
>                        pi(a | S_t) <- 1 - epsilon + epsilon / |A(S_t)|
>                    Else:
>                        pi(a | S_t) <- epsilon / |A(S_t)|
> ```

### Step-by-Step Explanation

**Initialization**: Same as MC ES, but now $\pi$ is epsilon-greedy from the start. No exploring starts needed.

**Step 1 -- Episode Generation**: The agent follows the epsilon-greedy policy $\pi$. Because every action has nonzero probability, all $(s,a)$ pairs will eventually be visited (given enough episodes and assuming all states are reachable).

**Steps 2--3 -- Backward Return Computation and Update**: Identical to MC ES in structure. The only difference is the improvement step: instead of setting $\pi(s) = \arg\max_a Q(s,a)$ (deterministic), we set $\pi$ to be epsilon-greedy w.r.t. the new $Q$ values.

### The Epsilon-Greedy Policy Improvement Theorem

> [!important] Theorem (Policy Improvement for Epsilon-Soft Policies)
> Let $\pi$ be any epsilon-soft policy, and let $\pi'$ be the epsilon-greedy policy w.r.t. $Q^\pi$. Then for all states $s$:
> $$V^{\pi'}(s) \geq V^\pi(s)$$

**Proof sketch**: For any epsilon-soft policy $\pi$ and state $s$:

$$Q^\pi(s, \pi'(s)) = \sum_a \pi'(a \mid s)\, Q^\pi(s,a)$$

The epsilon-greedy policy $\pi'$ places maximum probability on the action with highest $Q^\pi(s,a)$ while remaining epsilon-soft. Since it shifts probability **toward** the best action compared to any other epsilon-soft policy, the weighted sum of $Q$ values can only increase or stay the same. By the policy improvement theorem, $V^{\pi'}(s) \geq V^{\pi}(s)$ for all $s$.

### What Does On-Policy MC Converge To?

> [!warning] Critical Subtlety
> On-policy MC control converges to the **best epsilon-soft policy**, NOT the overall optimal policy $\pi^*$.
>
> The best epsilon-soft policy is optimal **among policies that explore with probability epsilon**. It is generally suboptimal compared to the true optimal (deterministic) policy because it is forced to take random actions $\epsilon$ fraction of the time.

In practice, one can **decay** $\epsilon$ over time (e.g., $\epsilon_k = 1/k$). As $\epsilon \to 0$, the epsilon-greedy policy approaches the true optimal policy. However, the theoretical convergence guarantee is for **fixed** $\epsilon$.

### Exploration vs. Exploitation Trade-off

| $\epsilon$ value | Exploration | Exploitation | Consequence |
|:---:|:---:|:---:|:---|
| Large (e.g., 0.5) | High | Low | Learns about many actions but follows a poor policy |
| Small (e.g., 0.01) | Low | High | Exploits current knowledge but may miss better actions |
| Typical (e.g., 0.1) | Moderate | Moderate | Reasonable balance for most problems |
| Decaying | Starts high, decreases | Starts low, increases | Explores early, exploits later (common in practice) |

---

## 8. Off-Policy MC Control

### Motivation

On-policy methods have a fundamental compromise: the policy they learn about is the **same** policy that generates data, so it must remain exploratory. This means the learned policy is the best epsilon-soft policy, not the truly optimal policy.

**Off-policy** methods break this compromise by using **two** policies:

| Policy | Name | Role |
|--------|------|------|
| $\pi$ | **Target policy** | The policy we want to learn about and optimize. Can be deterministic/greedy. |
| $b$ | **Behavior policy** | The policy used to generate episodes. Must be exploratory. |

> [!info] Off-Policy Advantage
> The target policy $\pi$ can be fully greedy (optimal) while the behavior policy $b$ handles all exploration. We get the best of both worlds: optimal policy learning with sufficient exploration.

### Importance Sampling Requirement

Since episodes are generated by $b$ but we want to evaluate $\pi$, we need to correct for the difference in distributions. This is done via **importance sampling** (see [[06_importance_sampling]] for full treatment).

The **importance sampling ratio** for a trajectory from time $t$ to the end of the episode $T-1$ is:

$$\rho_{t:T-1} = \prod_{k=t}^{T-1} \frac{\pi(A_k \mid S_k)}{b(A_k \mid S_k)}$$

### Coverage Requirement

> [!danger] Coverage Assumption
> The behavior policy $b$ must **cover** the target policy $\pi$:
> $$\pi(a \mid s) > 0 \implies b(a \mid s) > 0 \quad \text{for all } s, a$$
> If $\pi$ would ever take an action that $b$ never takes, we can never observe data about that action, and the importance sampling ratio would involve division by zero.

Since $\pi$ is typically deterministic and greedy, coverage simply means $b$ must assign nonzero probability to every action -- i.e., $b$ must be a soft policy (e.g., epsilon-greedy).

### The Algorithm

The off-policy MC control algorithm uses **incremental weighted importance sampling** for efficiency and lower variance.

> [!abstract] Off-Policy MC Control -- Complete Pseudocode
> ```
> Initialize:
>     Q(s,a) <- arbitrary, for all s in S, a in A(s)
>     C(s,a) <- 0, for all s, a     (cumulative importance sampling weights)
>     pi(s) <- argmax_a Q(s,a), for all s   (target policy, deterministic greedy)
>
> Repeat forever (for each episode):
>     1. b <- any soft policy covering pi (e.g., epsilon-greedy w.r.t. Q)
>     2. Generate episode using b:
>        S_0, A_0, R_1, S_1, A_1, R_2, ..., S_{T-1}, A_{T-1}, R_T
>     3. G <- 0
>     4. W <- 1
>     5. For t = T-1, T-2, ..., 0:
>            G <- gamma * G + R_{t+1}
>            C(S_t, A_t) <- C(S_t, A_t) + W
>            Q(S_t, A_t) <- Q(S_t, A_t) + (W / C(S_t, A_t)) * (G - Q(S_t, A_t))
>            pi(S_t) <- argmax_a Q(S_t, a)
>            If A_t != pi(S_t): break      (*** early exit ***)
>            W <- W * (1 / b(A_t | S_t))
> ```

### Line-by-Line Explanation

**Initialization**:
- $Q(s,a)$: arbitrary initial action-value estimates.
- $C(s,a)$: cumulative sum of importance sampling weights for each $(s,a)$ pair. Starts at 0.
- $\pi(s)$: target policy, initialized as greedy w.r.t. $Q$. This is **deterministic**.

**Step 1 -- Choose Behavior Policy**: Any soft (exploratory) policy that covers $\pi$. It can change between episodes. A common choice is epsilon-greedy w.r.t. the current $Q$.

**Step 2 -- Generate Episode**: The episode is generated entirely by the **behavior** policy $b$, not the target policy $\pi$.

**Steps 3--4 -- Initialize**: $G$ accumulates the return (backward from terminal step). $W$ accumulates the importance sampling weight.

**Step 5 -- Backward Processing Loop**:

- **Return accumulation**: $G \leftarrow \gamma G + R_{t+1}$ -- standard backward return computation.

- **Weight accumulation**: $C(S_t, A_t) \leftarrow C(S_t, A_t) + W$ -- adds the current importance weight to the running total for this $(s,a)$ pair.

- **Incremental Q update**:
$$Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \frac{W}{C(S_t, A_t)}\big(G - Q(S_t, A_t)\big)$$
This is an incremental weighted average update. The fraction $\frac{W}{C(S_t, A_t)}$ acts as a step size that correctly weights this return relative to all previous returns for $(S_t, A_t)$.

- **Policy improvement**: $\pi(S_t) \leftarrow \arg\max_a Q(S_t, a)$ -- update target policy to be greedy w.r.t. new $Q$.

- **Early exit check**: If $A_t \neq \pi(S_t)$, we **break** out of the loop and move to the next episode. (Explained below.)

- **Weight update**: $W \leftarrow W \cdot \frac{1}{b(A_t \mid S_t)}$. Since $\pi$ is deterministic and $A_t = \pi(S_t)$ at this point, $\pi(A_t \mid S_t) = 1$, so the ratio $\frac{\pi(A_t \mid S_t)}{b(A_t \mid S_t)} = \frac{1}{b(A_t \mid S_t)}$.

### Why Do We Break When $A_t \neq \pi(S_t)$?

> [!important] The Early Exit Explained
> The target policy $\pi$ is deterministic. If the action taken by the behavior policy at time $t$ is **not** the action $\pi$ would have taken, then $\pi(A_t \mid S_t) = 0$. The importance sampling ratio becomes:
> $$\frac{\pi(A_t \mid S_t)}{b(A_t \mid S_t)} = \frac{0}{b(A_t \mid S_t)} = 0$$
> Once $W = 0$, all subsequent (earlier) time steps would have $W = 0$ too, contributing nothing to the updates. So we can safely stop processing this episode.

This means only the **tail** of the episode (from the last time step backward until the first disagreement with $\pi$) contributes to learning. Many episodes are discarded entirely or contribute very little. This is a major source of inefficiency.

### Advantages and Disadvantages

> [!success] Advantages
> - Learns the **truly optimal** policy (not just the best epsilon-soft policy).
> - The behavior policy can be anything exploratory -- even a human demonstrator or a random policy.
> - Separates the concerns of exploration (behavior policy) and optimization (target policy).

> [!danger] Disadvantages
> - **High variance**: importance sampling weights can be very large (product of many ratios), causing high variance in $Q$ updates.
> - **Slow convergence**: many episodes may be discarded due to the early exit (tail-only learning).
> - **Requires coverage**: the behavior policy must take every action that the target policy would take.
> - More complex to implement than on-policy methods.

---

## 9. Comparison Table

| Aspect | MC ES | On-Policy ($\epsilon$-greedy) | Off-Policy |
|:-------|:------|:------------------------------|:-----------|
| **Exploration mechanism** | Exploring starts (random initial $(s,a)$) | $\epsilon$-greedy built into policy | Separate behavior policy $b$ |
| **Policy learned** | Optimal $\pi^*$ | Best $\epsilon$-soft policy | Optimal $\pi^*$ |
| **Requires model?** | No | No | No |
| **Requires IS?** | No | No | Yes (importance sampling) |
| **Practical?** | No (need random starts) | Yes | Yes (but slow convergence) |
| **Convergence guarantee** | To $\pi^*$ (with exploring starts) | To best $\epsilon$-soft policy | To $\pi^*$ (with coverage) |
| **Variance** | Low | Low | High (due to IS weights) |
| **Implementation complexity** | Simple | Simple | Moderate |
| **Single policy or two?** | One policy | One policy | Two policies ($\pi$ and $b$) |
| **Exploration-exploitation tradeoff** | N/A (starts handle it) | Controlled by $\epsilon$ | Fully separated |

> [!tip] Exam Strategy
> If asked "which method should you use?":
> - **MC ES**: only in theoretical/simulation settings where you can control the start state.
> - **On-policy**: when you need a simple, practical method and can tolerate a near-optimal (not optimal) policy.
> - **Off-policy**: when you need the truly optimal policy and have data from another policy (e.g., historical data, human demonstrations).

---

## 10. Key Formulas

> [!danger] MUST MEMORIZE -- Epsilon-Greedy Action Probabilities
> $$\pi(a \mid s) = \begin{cases} 1 - \epsilon + \dfrac{\epsilon}{|A(s)|} & \text{if } a = a^* = \arg\max_{a'} Q(s,a') \\[8pt] \dfrac{\epsilon}{|A(s)|} & \text{otherwise} \end{cases}$$
> - $\epsilon$: exploration parameter, $0 < \epsilon \leq 1$
> - $|A(s)|$: number of available actions in state $s$
> - $a^*$: greedy action under current $Q$ estimates
> - The probabilities sum to 1: $(1 - \epsilon + \frac{\epsilon}{|A(s)|}) + (|A(s)| - 1)\frac{\epsilon}{|A(s)|} = 1$

> [!danger] MUST MEMORIZE -- Return (Backward Accumulation)
> $$G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \cdots = R_{t+1} + \gamma G_{t+1}$$
> Computed backward: initialize $G \leftarrow 0$ at the terminal step, then $G \leftarrow \gamma G + R_{t+1}$ at each step.

> [!danger] MUST MEMORIZE -- MC Update for Q
> $$Q(s,a) \leftarrow \text{average}\big(\text{Returns}(s,a)\big)$$
> Incremental form:
> $$Q(s,a) \leftarrow Q(s,a) + \frac{1}{N(s,a)}\big(G - Q(s,a)\big)$$
> where $N(s,a)$ is the visit count.

> [!danger] MUST MEMORIZE -- Importance Sampling Ratio
> $$\rho_{t:T-1} = \prod_{k=t}^{T-1} \frac{\pi(A_k \mid S_k)}{b(A_k \mid S_k)}$$
> - $\pi$: target policy
> - $b$: behavior policy
> - Product runs from time $t$ to the end of the episode

> [!important] Off-Policy Incremental Weighted Update
> $$C(s,a) \leftarrow C(s,a) + W$$
> $$Q(s,a) \leftarrow Q(s,a) + \frac{W}{C(s,a)}\big(G - Q(s,a)\big)$$
> where $W$ is the cumulative importance sampling weight for the trajectory tail.

> [!important] Model-Free Policy Improvement
> $$\pi'(s) = \arg\max_a Q(s,a)$$
> Compare with model-based (DP) improvement:
> $$\pi'(s) = \arg\max_a \sum_{s',r} p(s',r \mid s,a)\big[r + \gamma V(s')\big]$$

> [!info] Verification: Epsilon-Greedy Probabilities Sum to 1
> $$\underbrace{\left(1 - \epsilon + \frac{\epsilon}{|A|}\right)}_{\text{greedy action}} + \underbrace{(|A| - 1) \cdot \frac{\epsilon}{|A|}}_{\text{non-greedy actions}} = 1 - \epsilon + \frac{\epsilon}{|A|} + \epsilon - \frac{\epsilon}{|A|} = 1 \checkmark$$

---

## 11. Common Mistakes

> [!warning] Common Mistake 1 -- Using V Instead of Q
> Students sometimes write MC control algorithms using $V(s)$ instead of $Q(s,a)$. Remember: without a model, $V(s)$ cannot be used for policy improvement. **MC control always uses $Q(s,a)$.**

> [!warning] Common Mistake 2 -- Forgetting the First-Visit Check
> In first-visit MC, you must only update $Q(s,a)$ for the **first** occurrence of $(s,a)$ in the episode. A common error is updating for every occurrence (which is every-visit MC -- a valid but different algorithm).

> [!warning] Common Mistake 3 -- Confusing On-Policy Convergence
> On-policy MC control converges to the **best epsilon-soft policy**, not the optimal policy. Many students incorrectly claim it converges to $\pi^*$. The optimal policy is deterministic; an epsilon-soft policy always has randomness.

> [!warning] Common Mistake 4 -- Importance Sampling Ratio Direction
> The ratio is $\frac{\pi(a \mid s)}{b(a \mid s)}$, NOT $\frac{b(a \mid s)}{\pi(a \mid s)}$. Target policy on top, behavior policy on bottom.

> [!warning] Common Mistake 5 -- Forgetting the Break in Off-Policy MC
> When $A_t \neq \pi(S_t)$ in off-policy MC control, you must **break** the inner loop. The importance sampling weight becomes zero, making all further updates pointless. Forgetting this does not cause incorrect results (zero weight means zero update), but understanding **why** we break is important for exam explanations.

> [!warning] Common Mistake 6 -- Thinking Exploring Starts is Practical
> MC ES is a theoretical algorithm. In exams, do not suggest exploring starts as a solution for real-world problems. Use epsilon-greedy or off-policy methods instead.

> [!warning] Common Mistake 7 -- Mixing Up Behavior and Target Policies
> In off-policy methods: the **behavior** policy $b$ generates episodes (exploratory), and the **target** policy $\pi$ is being learned (can be greedy). Do not reverse these.

---

## 12. Self-Check Questions

> [!question]- Q1: Why does MC control use $Q(s,a)$ instead of $V(s)$?
> Because without a model of the environment's dynamics $p(s',r \mid s,a)$, we cannot compute which action leads to the highest expected value from $V(s)$ alone. With $Q(s,a)$, we can directly take $\arg\max_a Q(s,a)$ without needing the model.

> [!question]- Q2: In on-policy MC control with $\epsilon = 0.2$ and $|A(s)| = 4$, what is the probability of selecting the greedy action? A non-greedy action?
> Greedy action: $1 - 0.2 + \frac{0.2}{4} = 0.8 + 0.05 = 0.85$.
> Each non-greedy action: $\frac{0.2}{4} = 0.05$.
> Check: $0.85 + 3 \times 0.05 = 0.85 + 0.15 = 1.0$. Correct.

> [!question]- Q3: What does on-policy MC control converge to, and why is it not the optimal policy?
> It converges to the **best epsilon-soft policy** -- the best policy that still takes every action with probability at least $\frac{\epsilon}{|A(s)|}$. This is not the optimal policy because the optimal policy is generally deterministic, but an epsilon-soft policy must always maintain some exploration probability.

> [!question]- Q4: In off-policy MC control, why do we process episodes backward and break when $A_t \neq \pi(S_t)$?
> We process backward to accumulate returns and importance weights from the tail of the episode. We break when $A_t \neq \pi(S_t)$ because the target policy $\pi$ is deterministic -- if the behavior policy took a different action than $\pi$ would have, the importance sampling ratio $\frac{\pi(A_t|S_t)}{b(A_t|S_t)} = 0$, making the weight $W = 0$ for all earlier time steps. No further updates would have any effect.

> [!question]- Q5: What is the coverage requirement in off-policy learning, and why is it necessary?
> Coverage requires that $\pi(a \mid s) > 0 \implies b(a \mid s) > 0$ for all $s, a$. In other words, the behavior policy must take every action that the target policy might take. Without this, there would be state-action pairs that $\pi$ considers but $b$ never visits, making it impossible to estimate their values. Mathematically, it prevents division by zero in the importance sampling ratio.

> [!question]- Q6: Compare the variance of on-policy and off-policy MC methods. Why does off-policy have higher variance?
> Off-policy MC uses importance sampling to correct for the mismatch between behavior and target policies. The importance sampling weights are products of ratios $\frac{\pi(A_k|S_k)}{b(A_k|S_k)}$ over potentially many time steps. These products can become very large or very small, causing high variance in the value estimates. On-policy methods do not need importance sampling because the data-generating policy and the policy being evaluated are the same, resulting in lower variance.

> [!question]- Q7: In MC ES, why do we update the policy inside the backward loop (for each state in the episode) rather than after processing the entire episode?
> This is the GPI (Generalized Policy Iteration) idea in action. We interleave evaluation and improvement at the finest grain possible. Each $(s,a)$ update immediately improves $Q$, and the policy is immediately made greedy w.r.t. the new $Q$. This does not cause problems because policy improvement is guaranteed to not make the policy worse (by the policy improvement theorem), and in practice it speeds convergence.

> [!question]- Q8: Suppose you are building an RL agent for a card game where episodes always start from a fixed initial deal. Can you use MC ES? What would you use instead?
> No, MC ES requires that every state-action pair can be the starting point of an episode. In a card game with a fixed initial deal, you cannot control the starting state. You should use **on-policy MC control** (epsilon-greedy) if you want simplicity, or **off-policy MC control** if you want to learn the truly optimal policy.

---

## 13. Concept Links

**Prerequisites (should be solid before studying this topic):**
- [[04_monte_carlo_prediction]] -- MC evaluation of $V^\pi$ and $Q^\pi$; first-visit vs. every-visit; episode generation.
- [[02_policy_iteration]] -- GPI framework; policy evaluation + policy improvement cycle; policy improvement theorem.
- [[01_dynamic_programming]] -- Bellman equations; iterative policy evaluation; why DP needs a model.

**Concepts Used Within This Topic:**
- **Generalized Policy Iteration (GPI)** -- the overarching framework that MC control instantiates. See [[02_policy_iteration]].
- **First-visit vs. Every-visit MC** -- the evaluation subroutine inside MC control. See [[04_monte_carlo_prediction]].
- **Importance Sampling** -- required for off-policy MC control. See [[06_importance_sampling]].

**Topics That Build on This:**
- [[06_importance_sampling]] -- deeper treatment of ordinary vs. weighted IS, variance analysis.
- Temporal-Difference (TD) methods -- replace MC evaluation with bootstrapping (TD(0), SARSA, Q-learning). MC control is the conceptual precursor to TD control.
- SARSA and Q-learning -- the on-policy and off-policy TD control methods, respectively. They are the TD analogues of on-policy and off-policy MC control.

**Key Contrasts:**
| This Topic | Contrast With | Key Difference |
|:-----------|:-------------|:---------------|
| MC Control (model-free) | DP Control ([[02_policy_iteration]]) | MC samples episodes; DP uses known model |
| MC Control (full returns) | TD Control (future topic) | MC waits until episode ends; TD updates after one step (bootstrapping) |
| On-policy MC | Off-policy MC | Same policy for data and learning vs. separate policies |
| MC for Q | MC for V ([[04_monte_carlo_prediction]]) | Q enables model-free improvement; V does not |

---

> [!abstract] Summary
> Monte Carlo control applies the GPI framework in a model-free setting by estimating **action-value functions** $Q(s,a)$ from sampled episodes and improving the policy greedily. The central challenge is **exploration**: three solutions exist (exploring starts, epsilon-greedy on-policy, and off-policy with importance sampling), each with distinct trade-offs between practicality, optimality, and variance. For the exam, be prepared to write all three algorithms from memory, explain why $Q$ is used instead of $V$, and analyze the convergence properties and limitations of each method.
