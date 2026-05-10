---
type: formula-sheet
tags: [rl, cat2, formulas]
---

# RL CAT-2 Formula Sheet

---

## RL Notation Reference Table

| Symbol | Meaning |
|--------|---------|
| $s, s'$ | Current and next state |
| $a$ | Action |
| $r, R_t$ | Reward |
| $\pi(a \mid s)$ | Policy: probability of action $a$ in state $s$ |
| $V^\pi(s)$ | State-value function under policy $\pi$ |
| $Q^\pi(s,a)$ | Action-value function under policy $\pi$ |
| $V^*(s)$ | Optimal state-value function |
| $Q^*(s,a)$ | Optimal action-value function |
| $G_t$ | Return from time $t$ |
| $\gamma$ | Discount factor ($0 \leq \gamma \leq 1$) |
| $p(s',r \mid s,a)$ | Transition probability |
| $\alpha$ | Learning rate / step size |
| $\epsilon$ | Exploration parameter |
| $\theta$ | Convergence threshold |
| $b(a \mid s)$ | Behavior policy |
| $\rho$ | Importance sampling ratio |

---

## Return Definition

$$G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \cdots = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}$$

> [!info] Variable Definitions
> - $G_t$: total discounted return starting from time step $t$
> - $R_{t+k+1}$: reward received $k+1$ steps after time $t$
> - $\gamma$: discount factor controlling how much future rewards are worth relative to immediate rewards
> - When $\gamma = 0$, only the immediate reward matters; when $\gamma = 1$, all future rewards are weighted equally

---

## Bellman Equations (All Four)

### 1. Bellman Expectation Equation for $V^\pi$

> [!warning] MUST MEMORIZE

$$V^\pi(s) = \sum_a \pi(a|s) \sum_{s',r} p(s',r|s,a)\Big[r + \gamma V^\pi(s')\Big]$$

> [!info] Variable Definitions
> - Outer sum: weighted average over all actions by the policy $\pi$
> - Inner sum: weighted average over all possible next states and rewards by transition dynamics
> - $r + \gamma V^\pi(s')$: immediate reward plus discounted future value

### 2. Bellman Expectation Equation for $Q^\pi$

> [!warning] MUST MEMORIZE

$$Q^\pi(s,a) = \sum_{s',r} p(s',r|s,a)\Big[r + \gamma \sum_{a'} \pi(a'|s') Q^\pi(s',a')\Big]$$

> [!info] Variable Definitions
> - Action $a$ is already chosen, so outer sum is over transitions only
> - Inner sum averages over next actions $a'$ chosen by policy $\pi$ at the next state $s'$

### 3. Bellman Optimality Equation for $V^*$

> [!warning] MUST MEMORIZE

$$V^*(s) = \max_a \sum_{s',r} p(s',r|s,a)\Big[r + \gamma V^*(s')\Big]$$

> [!info] Variable Definitions
> - $\max_a$: the optimal policy always picks the best action
> - $V^*(s)$: value of state $s$ under the optimal policy
> - No policy weighting needed -- the max replaces the sum over $\pi$

### 4. Bellman Optimality Equation for $Q^*$

> [!warning] MUST MEMORIZE

$$Q^*(s,a) = \sum_{s',r} p(s',r|s,a)\Big[r + \gamma \max_{a'} Q^*(s',a')\Big]$$

> [!info] Variable Definitions
> - $Q^*(s,a)$: value of taking action $a$ in state $s$ and acting optimally thereafter
> - $\max_{a'}$: at the next state, the optimal policy picks the best next action

> [!tip] Pattern Recognition
> - **Expectation equations** use $\sum_a \pi(a \mid s)$ -- average over policy
> - **Optimality equations** use $\max_a$ -- pick the best action
> - **V equations** sum/max over actions on the outside
> - **Q equations** have the action already fixed; sum/max appears inside for the next step

---

## Dynamic Programming Update Rules

### Iterative Policy Evaluation

$$V_{k+1}(s) = \sum_a \pi(a|s) \sum_{s',r} p(s',r|s,a)\Big[r + \gamma V_k(s')\Big]$$

> [!info] Variable Definitions
> - $V_k(s)$: estimate of value at iteration $k$
> - This is the Bellman expectation equation used as an iterative update
> - Sweep through all states, updating each using the previous iteration's values

### Value Iteration

$$V_{k+1}(s) = \max_a \sum_{s',r} p(s',r|s,a)\Big[r + \gamma V_k(s')\Big]$$

> [!info] Variable Definitions
> - This is the Bellman optimality equation used as an iterative update
> - Combines policy evaluation and improvement into a single step
> - Extract policy at the end via $\arg\max$

### Policy Improvement

$$\pi'(s) = \arg\max_a \sum_{s',r} p(s',r|s,a)\Big[r + \gamma V^\pi(s')\Big]$$

> [!info] Variable Definitions
> - $\pi'(s)$: the improved policy -- greedy with respect to $V^\pi$
> - If $\pi' = \pi$ (no change), the policy is already optimal

---

## Monte Carlo Estimation

### First-Visit MC Prediction

$$V(s) = \frac{1}{N(s)} \sum_{i=1}^{N(s)} G_i(s)$$

> [!info] Variable Definitions
> - $N(s)$: number of episodes in which state $s$ was visited (counting only the first visit per episode)
> - $G_i(s)$: return observed from the first visit to $s$ in episode $i$

### Incremental Update (Sample Average)

$$V(s) \leftarrow V(s) + \frac{1}{N(s)}\Big(G - V(s)\Big)$$

> [!info] Variable Definitions
> - $\frac{1}{N(s)}$: step size that decreases as more visits accumulate
> - $G - V(s)$: the MC error -- difference between observed return and current estimate

### Constant Step-Size Update

$$V(s) \leftarrow V(s) + \alpha\Big(G - V(s)\Big)$$

> [!info] Variable Definitions
> - $\alpha$: fixed learning rate (does not change with number of visits)
> - Gives more weight to recent returns -- useful for non-stationary problems
> - Effectively computes an exponentially weighted moving average

---

## Epsilon-Greedy Policy

$$\pi(a|s) = \begin{cases} 1 - \epsilon + \dfrac{\epsilon}{|A(s)|} & \text{if } a = \arg\max_a Q(s,a) \\[8pt] \dfrac{\epsilon}{|A(s)|} & \text{otherwise} \end{cases}$$

> [!info] Variable Definitions
> - $\epsilon$: probability of exploring (choosing a random action)
> - $\lvert A(s) \rvert$: number of available actions in state $s$
> - The greedy action gets probability $1 - \epsilon + \frac{\epsilon}{\lvert A(s) \rvert}$ (bulk of probability plus its share of the random portion)
> - Each non-greedy action gets probability $\frac{\epsilon}{\lvert A(s) \rvert}$
> - All probabilities sum to 1

---

## Importance Sampling

### IS Ratio (Single Episode)

$$\rho_{t:T-1} = \prod_{k=t}^{T-1} \frac{\pi(A_k|S_k)}{b(A_k|S_k)}$$

> [!info] Variable Definitions
> - $\pi$: target policy (the one we want to evaluate)
> - $b$: behavior policy (the one actually generating data)
> - $T$: terminal time step of the episode
> - The ratio corrects for the mismatch between the two policies
> - Only depends on policy probabilities, **not** on transition probabilities $p(s',r \mid s,a)$

### Ordinary Importance Sampling

$$V(s) = \frac{1}{|T(s)|} \sum_{t \in T(s)} \rho_{t:T(t)-1}\, G_t$$

> [!info] Variable Definitions
> - $T(s)$: set of all time steps where state $s$ is visited (across all episodes)
> - Simple average of importance-weighted returns
> - **Unbiased** but can have **high variance** (ratios can be very large)

### Weighted Importance Sampling

$$V(s) = \frac{\sum_{t \in T(s)} \rho_{t:T(t)-1}\, G_t}{\sum_{t \in T(s)} \rho_{t:T(t)-1}}$$

> [!info] Variable Definitions
> - Denominator normalizes by the sum of the weights
> - **Biased** (bias asymptotically vanishes) but **much lower variance**
> - Preferred in practice over ordinary IS

### Incremental Weighted IS Update

$$C_{n+1} = C_n + W_{n+1}$$

$$V_{n+1} = V_n + \frac{W_{n+1}}{C_{n+1}}\Big(G_{n+1} - V_n\Big)$$

> [!info] Variable Definitions
> - $C_n$: cumulative sum of weights after $n$ returns
> - $W_{n+1}$: importance sampling weight for the $(n+1)$-th return
> - This is the incremental form of weighted IS -- avoids storing all returns

---

## Key Algorithm Comparison Table

| Property | Policy Eval | Policy Iter | Value Iter | First-Visit MC | Every-Visit MC | MC ES | On-Policy MC | Off-Policy MC |
|----------|------------|------------|-----------|---------------|---------------|-------|-------------|--------------|
| Model? | Yes | Yes | Yes | No | No | No | No | No |
| Bootstrap? | Yes | Yes | Yes | No | No | No | No | No |
| Episodic? | No | No | No | Yes | Yes | Yes | Yes | Yes |
| On/Off | -- | -- | -- | On | On | On | On | Off |
| Finds optimal? | No (eval only) | Yes | Yes | No (eval only) | No (eval only) | Yes | Best eps-soft | Yes |

> [!tip] Reading the Table
> - **Model**: requires $p(s',r \mid s,a)$ -- the full dynamics
> - **Bootstrap**: updates estimates based on other estimates (not full returns)
> - **Episodic**: requires episodes to terminate
> - **On/Off**: on-policy learns about the policy it follows; off-policy learns about a different target policy

---

## Convergence Conditions

| Method | Converges when |
|--------|---------------|
| Policy Evaluation | $\delta = \max_s \lvert V_{k+1}(s) - V_k(s) \rvert < \theta$ |
| Policy Iteration | Policy is stable (no change after improvement step) |
| Value Iteration | $\delta = \max_s \lvert V_{k+1}(s) - V_k(s) \rvert < \theta$ |
| MC Prediction | $N(s) \to \infty$ for all $s$ (law of large numbers) |
| MC Control (ES) | All $(s,a)$ pairs visited infinitely often |

> [!info] Notes
> - $\theta$ is a small positive threshold chosen by the user
> - Policy iteration converges in a **finite** number of steps
> - Value iteration converges **asymptotically** (in the limit)
> - In practice, we stop value iteration when $\delta < \theta$

---

> [!abstract] See Also
> - [[cat2_09_quick_review]] for rapid-fire revision
> - [[07_off_policy_mc]] for detailed importance sampling coverage
> - [[06_monte_carlo_methods]] for MC algorithms in depth
> - [[04_dynamic_programming]] for DP algorithms in depth
