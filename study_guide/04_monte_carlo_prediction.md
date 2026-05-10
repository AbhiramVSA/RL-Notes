---
type: topic
topic: monte-carlo-prediction
module: 3
exam_weight: high
prerequisites: [[01_dynamic_programming]]
tags: [rl, cat2, monte-carlo, prediction, first-visit, every-visit]
---

# Monte Carlo Prediction

## Learning Objectives

After studying this topic, you should be able to:

- Explain why Monte Carlo methods exist and what problem they solve that Dynamic Programming cannot
- Distinguish between model-based (DP) and model-free (MC) approaches to policy evaluation
- Define what makes a task episodic and why MC requires episodes to terminate
- Implement First-Visit MC Prediction and trace through its execution on a given set of episodes
- Implement Every-Visit MC Prediction and explain how it differs from First-Visit
- Compute state-value estimates by hand using both First-Visit and Every-Visit methods given episode data
- Derive and apply the incremental mean update formula for efficient MC value estimation
- Explain why MC does not bootstrap and what consequences this has for bias and variance
- Compare and contrast MC Prediction with DP-based policy evaluation across multiple dimensions

---

## Ground-Up Explanation

### The Fundamental Problem: What If We Have No Model?

In Dynamic Programming, we had full access to the environment's dynamics -- the transition probabilities $p(s', r \mid s, a)$. We used those to compute value functions via the Bellman equations. But in most real-world problems, we do not have a model of the environment. We do not know the transition probabilities. We do not know the reward function. All we can do is interact with the environment and observe what happens.

This is precisely where Monte Carlo methods enter the picture. MC methods learn directly from episodes of experience, requiring no prior knowledge of MDP transitions whatsoever. The agent simply acts in the environment, collects sequences of states, actions, and rewards, and uses those raw experiences to estimate value functions.

### The Episodic Requirement

Monte Carlo methods can only be applied to **episodic MDPs** -- tasks that eventually terminate. Why? Because MC methods rely on computing the **return** (total discounted cumulative reward) from a state, and the return can only be calculated once the episode is over. We do not update value estimates after every action (as in DP). We update after every complete episode.

> [!important] Episodic Constraint
> An episode **must terminate** before we can calculate any returns. MC is not applicable to continuing (non-terminating) tasks without modification.

### What Is a Return?

The return $G_t$ is the total discounted reward from time step $t$ onward:

$$G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \cdots = \sum_{k=0}^{T-t-1} \gamma^k R_{t+k+1}$$

where $T$ is the terminal time step and $\gamma \in [0, 1]$ is the discount factor.

### The Core Intuition: Just Average the Returns

The value of a state under a policy $\pi$ is defined as the expected return starting from that state:

$$v_\pi(s) = \mathbb{E}_\pi[G_t \mid S_t = s]$$

Monte Carlo prediction estimates this expected value in the simplest possible way: **play many episodes, observe the returns from each state, and average them**. By the law of large numbers, as the number of visits grows, the sample average converges to the true expected value.

$$V_\pi(s) = \frac{1}{N} \sum_{i=1}^{N} G_{i,s}$$

where $N$ is the number of times state $s$ was visited and $G_{i,s}$ is the return observed after the $i$-th visit to $s$.

This is learning from raw experience. No model. No Bellman equations. No matrix inversions. Just sampling and averaging.

---

## Analogies

> [!tip] Restaurant Rating Analogy
> Imagine you want to know how good a restaurant is (its "value"). With the DP approach, you would need a complete model: the menu, the chef's skill ratings, ingredient quality scores, and a formula to combine them. With the MC approach, you simply eat there multiple times, record your satisfaction after each visit, and average those scores. You need no knowledge of the kitchen -- just repeated experience. The more visits you make, the more accurate your average rating becomes. However, you must finish the entire meal (the episode must terminate) before you can rate it.

---

## Key Concepts

### Model-Free Learning

MC methods require only **experience** -- sample sequences of states, actions, and rewards from actual interaction with the environment. There is no need to know $p(s', r \mid s, a)$. This is what makes MC a **model-free** method. Learning from actual experience requires no prior knowledge of environment dynamics, yet can still attain optimal behavior.

### Episodic Requirement

MC methods work by averaging complete returns. Since a return is a sum from the current time step to the end of the episode, the episode must have a definite end. Every episode must terminate in a finite number of steps.

### Returns vs Rewards

> [!warning] Do Not Confuse Returns and Rewards
> - A **reward** $R_t$ is the immediate scalar signal received at a single time step.
> - A **return** $G_t$ is the cumulative discounted sum of all future rewards from time $t$ to the end of the episode.
> - MC methods average **returns**, not individual rewards.

In MC, the random component is the return (or equivalently, the reward sequence that produces it). Different episodes yield different returns from the same state because the trajectory that unfolds is stochastic.

### Sample Averages Converge to Expected Values

By the **law of large numbers**, as the number of samples $N \to \infty$:

$$\frac{1}{N} \sum_{i=1}^{N} G_{i,s} \xrightarrow{} \mathbb{E}_\pi[G_t \mid S_t = s] = v_\pi(s)$$

More visits to a state means the average converges closer to the true value.

### No Bootstrapping

> [!abstract] What Is Bootstrapping?
> **Bootstrapping** means using estimates of other states' values to compute the value of the current state. In DP, the Bellman equation updates $V(s)$ using $V(s')$ for successor states -- that is bootstrapping.

MC is one of the few methods that does **not** bootstrap. The value estimate for a state is computed entirely from observed returns -- it does not depend on the value estimates of any other state. This has two consequences:

1. **Reduced bias**: No error propagation from inaccurate estimates of other states
2. **Slower convergence**: Cannot leverage structure across states to speed up learning

---

## First-Visit Monte Carlo Prediction

### Pseudocode

```
Initialize:
    V(s) arbitrarily for all s in S
    Returns(s) = empty list for all s in S

Repeat forever (for each episode):
    Generate an episode using policy pi:
        S_0, A_0, R_1, S_1, A_1, R_2, ..., S_{T-1}, A_{T-1}, R_T

    For each state s appearing in the episode:
        G = return following the FIRST occurrence of s in this episode
        Append G to Returns(s)
        V(s) = average(Returns(s))
```

### Line-by-Line Explanation

| Line | Explanation |
|------|-------------|
| `V(s) arbitrarily` | Initialize value estimates to any value (e.g., zero). These will be corrected by experience. |
| `Returns(s) = empty list` | For each state, maintain a list that will accumulate observed returns across episodes. |
| `Generate an episode using pi` | Follow the current policy from start to termination, recording the full trajectory. |
| `For each state s appearing in the episode` | Iterate over each unique state that was visited in this episode. |
| `G = return following FIRST occurrence of s` | Find the first time step $t$ where $S_t = s$. Compute $G_t = R_{t+1} + \gamma R_{t+2} + \cdots + \gamma^{T-t-1} R_T$. Ignore all later visits to $s$ in this episode. |
| `Append G to Returns(s)` | Add this return to the running list for state $s$. Each episode contributes at most one entry per state. |
| `V(s) = average(Returns(s))` | Recompute the value estimate as the mean of all returns ever observed for $s$. |

### Properties

- **Unbiased estimator**: Each return $G_{i,s}$ is an unbiased sample of $v_\pi(s)$, so the sample mean is an unbiased estimator.
- **Convergence**: By the law of large numbers, $V(s) \to v_\pi(s)$ as the number of first visits to $s$ goes to infinity.
- **Each episode contributes at most one return per state**, regardless of how many times that state is visited within the episode.

---

## Every-Visit Monte Carlo Prediction

### Pseudocode

```
Initialize:
    V(s) arbitrarily for all s in S
    Returns(s) = empty list for all s in S

Repeat forever (for each episode):
    Generate an episode using policy pi:
        S_0, A_0, R_1, S_1, A_1, R_2, ..., S_{T-1}, A_{T-1}, R_T

    For each state s appearing in the episode:
        For EVERY time step t where S_t = s:
            G = return following this occurrence of s
            Append G to Returns(s)
            V(s) = average(Returns(s))
```

### Properties

- **Also converges** to $v_\pi(s)$ as visits increase, though the convergence characteristics differ.
- In a single episode, a state visited $k$ times contributes $k$ returns (one per visit).
- Every-visit MC may have **different bias/variance characteristics** compared to first-visit.

### Comparison: First-Visit vs Every-Visit

| Aspect | First-Visit MC | Every-Visit MC |
|--------|---------------|----------------|
| Which visits count? | Only the first visit to $s$ per episode | Every visit to $s$ per episode |
| Returns per episode per state | At most 1 | Can be multiple |
| Bias | Unbiased | May be slightly biased (within-episode correlation) |
| Variance | Generally higher per-episode | Generally lower (more samples) |
| Convergence | Converges to $v_\pi(s)$ | Also converges to $v_\pi(s)$ |
| Implementation | Must track if state already seen in episode | Simpler -- process every occurrence |
| Data efficiency | Uses less data per episode | Uses more data per episode |

---

## Worked Examples

### Example 1: Single Nonterminal State (Slides 10--11)

> [!example] Setup
> An MDP has a **single nonterminal state** $s$ with a single action. On each step, the agent transitions back to $s$ with probability $p$, or to the terminal state with probability $1 - p$. The reward is $+1$ on every transition. The discount factor is $\gamma = 1$.

**One observed episode lasts 10 steps**: the agent visits $s$ ten times, receiving reward $+1$ each time, then terminates.

The trajectory is:

$$s \xrightarrow{+1} s \xrightarrow{+1} s \xrightarrow{+1} s \xrightarrow{+1} s \xrightarrow{+1} s \xrightarrow{+1} s \xrightarrow{+1} s \xrightarrow{+1} s \xrightarrow{+1} s \xrightarrow{+1} \text{Terminal}$$

**First-Visit MC**:
- The first (and only counted) visit to $s$ is at time $t = 0$.
- $G_0 = 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 = 10$
- $V(s) = \frac{10}{1} = 10$

**Every-Visit MC**:
- State $s$ is visited at $t = 0, 1, 2, \ldots, 9$.
- Returns from each visit:
  - $t=0$: $G_0 = 10$
  - $t=1$: $G_1 = 9$
  - $t=2$: $G_2 = 8$
  - $t=3$: $G_3 = 7$
  - $t=4$: $G_4 = 6$
  - $t=5$: $G_5 = 5$
  - $t=6$: $G_6 = 4$
  - $t=7$: $G_7 = 3$
  - $t=8$: $G_8 = 2$
  - $t=9$: $G_9 = 1$
- $V(s) = \frac{10 + 9 + 8 + 7 + 6 + 5 + 4 + 3 + 2 + 1}{10} = \frac{55}{10} = 5.5$

> [!note] Observation
> First-visit gives $V(s) = 10$, every-visit gives $V(s) = 5.5$. Both converge to the true value with many more episodes. The true value is $v_\pi(s) = \frac{1}{1-p}$ (the expected number of steps times reward $+1$), so the true answer depends on $p$.

---

### Example 2: States A and B with 2 Episodes (Slides 13--15)

> [!example] Setup
> An environment has 2 nonterminal states: **A** and **B**. Two episodes are observed. Assume $\gamma = 1$.

![[m3_2_s14_img5.png|Episode traces for states A and B]]

**Episode 1**: $A \xrightarrow{+3} A \xrightarrow{+2} B \xrightarrow{-4} A \xrightarrow{+4} B \xrightarrow{-3} \text{Terminal}$

**Episode 2**: $B \xrightarrow{-2} A \xrightarrow{+3} B \xrightarrow{-3} \text{Terminal}$

#### First-Visit MC

For first-visit, we only consider the **first time** each state appears in each episode.

**State A**:
- Episode 1: First visit to A is at $t=0$. Return = $+3 +2 -4 +4 -3 = 2$
- Episode 2: First visit to A is at $t=1$. Return = $+3 -3 = 0$
- $V(A) = \frac{2 + 0}{2} = 1$

**State B**:
- Episode 1: First visit to B is at $t=2$. Return = $-4 +4 -3 = -3$
- Episode 2: First visit to B is at $t=0$. Return = $-2 +3 -3 = -2$
- $V(B) = \frac{-3 + (-2)}{2} = \frac{-5}{2} = -2.5$

#### Every-Visit MC

For every-visit, we count **every occurrence** of each state.

**State A** (visited 4 times total):

| Episode | Time step | Return from this visit |
|---------|-----------|----------------------|
| 1 | $t=0$ | $+3+2-4+4-3 = 2$ |
| 1 | $t=1$ | $+2-4+4-3 = -1$ |
| 1 | $t=3$ | $+4-3 = 1$ |
| 2 | $t=1$ | $+3-3 = 0$ |

$$V(A) = \frac{2 + (-1) + 1 + 0}{4} = \frac{2}{4} = 0.5$$

**State B** (visited 4 times total):

| Episode | Time step | Return from this visit |
|---------|-----------|----------------------|
| 1 | $t=2$ | $-4+4-3 = -3$ |
| 1 | $t=4$ | $-3$ |
| 2 | $t=0$ | $-2+3-3 = -2$ |
| 2 | $t=2$ | $-3$ |

$$V(B) = \frac{-3 + (-3) + (-2) + (-3)}{4} = \frac{-11}{4} = -2.75$$

> [!success] Summary of Example 2
> | State | First-Visit | Every-Visit |
> |-------|------------|-------------|
> | A | $1.0$ | $0.5$ |
> | B | $-2.5$ | $-2.75$ |

---

### Example 3: Five States, Four Episodes (Slide 16)

> [!example] Setup
> Five nonterminal states $S_0, S_1, S_2, S_3, S_4$. Four episodes observed. Assume $\gamma = 1$. The notation $S_i \xrightarrow{r} S_j$ means transitioning from $S_i$ to $S_j$ with reward $r$. $S_T$ denotes the terminal state.

![[m3_2_s16_img7.png|Episode traces for 5-state example]]

**Episode 1**: $S_0 \xrightarrow{3} S_4 \xrightarrow{1} S_0 \xrightarrow{2} S_2 \xrightarrow{-1} S_1 \xrightarrow{5} S_2 \xrightarrow{4} S_T$

**Episode 2**: $S_1 \xrightarrow{3} S_3 \xrightarrow{1} S_0 \xrightarrow{2} S_2 \xrightarrow{5} S_T$

**Episode 3**: $S_2 \xrightarrow{-2} S_1 \xrightarrow{2} S_3 \xrightarrow{3} S_4 \xrightarrow{1} S_1 \xrightarrow{2} S_T$

**Episode 4**: $S_4 \xrightarrow{3} S_0 \xrightarrow{1} S_2 \xrightarrow{3} S_0 \xrightarrow{-1} S_2 \xrightarrow{2} S_1 \xrightarrow{1} S_T$

#### First-Visit MC Calculations

For each state, identify the **first** occurrence in each episode and compute the return from that point to the end.

**State $S_0$**:

| Episode | First visit at step | Remaining rewards | Return |
|---------|-------------------|-------------------|--------|
| E1 | $t=0$ | $3, 1, 2, -1, 5, 4$ | $3+1+2-1+5+4 = 14$ |
| E2 | $t=2$ | $2, 5$ | $2+5 = 7$ |
| E3 | not visited | -- | -- |
| E4 | $t=1$ | $1, 3, -1, 2, 1$ | $1+3-1+2+1 = 6$ |

$$V(S_0) = \frac{14 + 7 + 6}{3} = \frac{27}{3} = 9$$

**State $S_1$**:

| Episode | First visit at step | Remaining rewards | Return |
|---------|-------------------|-------------------|--------|
| E1 | $t=4$ | $5, 4$ | $5+4 = 9$ |
| E2 | $t=0$ | $3, 1, 2, 5$ | $3+1+2+5 = 11$ |
| E3 | $t=1$ | $2, 3, 1, 2$ | $2+3+1+2 = 8$ |
| E4 | $t=5$ | $1$ | $1$ |

$$V(S_1) = \frac{9 + 11 + 8 + 1}{4} = \frac{29}{4} = 7.25$$

**State $S_2$**:

| Episode | First visit at step | Remaining rewards | Return |
|---------|-------------------|-------------------|--------|
| E1 | $t=3$ | $-1, 5, 4$ | $-1+5+4 = 8$ |
| E2 | $t=3$ | $5$ | $5$ |
| E3 | $t=0$ | $-2, 2, 3, 1, 2$ | $-2+2+3+1+2 = 6$ |
| E4 | $t=2$ | $3, -1, 2, 1$ | $3-1+2+1 = 5$ |

$$V(S_2) = \frac{8 + 5 + 6 + 5}{4} = \frac{24}{4} = 6$$

**State $S_3$**:

| Episode | First visit at step | Remaining rewards | Return |
|---------|-------------------|-------------------|--------|
| E1 | not visited | -- | -- |
| E2 | $t=1$ | $1, 2, 5$ | $1+2+5 = 8$ |
| E3 | $t=2$ | $3, 1, 2$ | $3+1+2 = 6$ |
| E4 | not visited | -- | -- |

$$V(S_3) = \frac{8 + 6}{2} = \frac{14}{2} = 7$$

**State $S_4$**:

| Episode | First visit at step | Remaining rewards | Return |
|---------|-------------------|-------------------|--------|
| E1 | $t=1$ | $1, 2, -1, 5, 4$ | $1+2-1+5+4 = 11$ |
| E2 | not visited | -- | -- |
| E3 | $t=3$ | $1, 2$ | $1+2 = 3$ |
| E4 | $t=0$ | $3, 1, 3, -1, 2, 1$ | $3+1+3-1+2+1 = 9$ |

$$V(S_4) = \frac{11 + 3 + 9}{3} = \frac{23}{3} \approx 7.67$$

> [!success] First-Visit MC Results for Example 3
> | State | $V(s)$ |
> |-------|--------|
> | $S_0$ | $9.0$ |
> | $S_1$ | $7.25$ |
> | $S_2$ | $6.0$ |
> | $S_3$ | $7.0$ |
> | $S_4$ | $\approx 7.67$ |

#### Every-Visit MC Calculations

Now we count **every** occurrence of each state.

**State $S_0$** (5 visits total):

| Episode | Step | Return |
|---------|------|--------|
| E1 | $t=0$ | $3+1+2-1+5+4 = 14$ |
| E1 | $t=2$ | $2-1+5+4 = 10$ |
| E2 | $t=2$ | $2+5 = 7$ |
| E4 | $t=1$ | $1+3-1+2+1 = 6$ |
| E4 | $t=3$ | $-1+2+1 = 2$ |

$$V(S_0) = \frac{14 + 10 + 7 + 6 + 2}{5} = \frac{39}{5} = 7.8$$

**State $S_1$** (5 visits total):

| Episode | Step | Return |
|---------|------|--------|
| E1 | $t=4$ | $5+4 = 9$ |
| E2 | $t=0$ | $3+1+2+5 = 11$ |
| E3 | $t=1$ | $2+3+1+2 = 8$ |
| E3 | $t=4$ | $2$ |
| E4 | $t=5$ | $1$ |

$$V(S_1) = \frac{9 + 11 + 8 + 2 + 1}{5} = \frac{31}{5} = 6.2$$

**State $S_2$** (6 visits total):

| Episode | Step | Return |
|---------|------|--------|
| E1 | $t=3$ | $-1+5+4 = 8$ |
| E1 | $t=5$ | $4$ |
| E2 | $t=3$ | $5$ |
| E3 | $t=0$ | $-2+2+3+1+2 = 6$ |
| E4 | $t=2$ | $3-1+2+1 = 5$ |
| E4 | $t=4$ | $2+1 = 3$ |

$$V(S_2) = \frac{8 + 4 + 5 + 6 + 5 + 3}{6} = \frac{31}{6} \approx 5.17$$

**State $S_3$** (2 visits total -- same as first-visit since $S_3$ appears at most once per episode):

$$V(S_3) = \frac{8 + 6}{2} = 7$$

**State $S_4$** (3 visits total -- same as first-visit since $S_4$ appears at most once per episode):

$$V(S_4) = \frac{11 + 3 + 9}{3} \approx 7.67$$

> [!success] Every-Visit MC Results for Example 3
> | State | First-Visit $V(s)$ | Every-Visit $V(s)$ |
> |-------|--------------------|--------------------|
> | $S_0$ | $9.0$ | $7.8$ |
> | $S_1$ | $7.25$ | $6.2$ |
> | $S_2$ | $6.0$ | $\approx 5.17$ |
> | $S_3$ | $7.0$ | $7.0$ |
> | $S_4$ | $\approx 7.67$ | $\approx 7.67$ |

---

### Example 4: Three States, Three Episodes (Slide 17)

> [!example] Setup
> Three nonterminal states: **1**, **2**, **3**. The agent always goes right. The notation $(s, r)$ indicates being in state $s$ and receiving reward $r$ on the transition to the next state. Assume $\gamma = 1$.

**Episode 1**: $(1, 1) \to (2, 2) \to (1, 3) \to (3, 4)$

Interpreting this as: State 1, reward 1, State 2, reward 2, State 1, reward 3, State 3, reward 4, Terminal.

Trajectory: $S_0=1 \xrightarrow{1} S_1=2 \xrightarrow{2} S_2=1 \xrightarrow{3} S_3=3 \xrightarrow{4} \text{Terminal}$

**Episode 2**: $(1, 2) \to (1, 3) \to (2, 1) \to (2, 4) \to (3, 2)$

Trajectory: $S_0=1 \xrightarrow{2} S_1=1 \xrightarrow{3} S_2=2 \xrightarrow{1} S_3=2 \xrightarrow{4} S_4=3 \xrightarrow{2} \text{Terminal}$

**Episode 3**: $(1, 1) \to (2, 1) \to (2, 4) \to (2, 3) \to (3, 2) \to (3, 6)$

Trajectory: $S_0=1 \xrightarrow{1} S_1=2 \xrightarrow{1} S_2=2 \xrightarrow{4} S_3=2 \xrightarrow{3} S_4=3 \xrightarrow{2} S_5=3 \xrightarrow{6} \text{Terminal}$

#### First-Visit MC

**State 1**:
- E1: First at $t=0$, return = $1+2+3+4 = 10$
- E2: First at $t=0$, return = $2+3+1+4+2 = 12$
- E3: First at $t=0$, return = $1+1+4+3+2+6 = 17$

$$V(1) = \frac{10+12+17}{3} = \frac{39}{3} = 13$$

**State 2**:
- E1: First at $t=1$, return = $2+3+4 = 9$
- E2: First at $t=2$, return = $1+4+2 = 7$
- E3: First at $t=1$, return = $1+4+3+2+6 = 16$

$$V(2) = \frac{9+7+16}{3} = \frac{32}{3} \approx 10.67$$

**State 3**:
- E1: First at $t=3$, return = $4$
- E2: First at $t=4$, return = $2$
- E3: First at $t=4$, return = $2+6 = 8$

$$V(3) = \frac{4+2+8}{3} = \frac{14}{3} \approx 4.67$$

#### Every-Visit MC

**State 1** (4 visits):

| Episode | Step | Return |
|---------|------|--------|
| E1 | $t=0$ | $1+2+3+4 = 10$ |
| E1 | $t=2$ | $3+4 = 7$ |
| E2 | $t=0$ | $2+3+1+4+2 = 12$ |
| E2 | $t=1$ | $3+1+4+2 = 10$ |

$$V(1) = \frac{10+7+12+10}{4} = \frac{39}{4} = 9.75$$

**State 2** (6 visits):

| Episode | Step | Return |
|---------|------|--------|
| E1 | $t=1$ | $2+3+4 = 9$ |
| E2 | $t=2$ | $1+4+2 = 7$ |
| E2 | $t=3$ | $4+2 = 6$ |
| E3 | $t=1$ | $1+4+3+2+6 = 16$ |
| E3 | $t=2$ | $4+3+2+6 = 15$ |
| E3 | $t=3$ | $3+2+6 = 11$ |

$$V(2) = \frac{9+7+6+16+15+11}{6} = \frac{64}{6} \approx 10.67$$

**State 3** (4 visits):

| Episode | Step | Return |
|---------|------|--------|
| E1 | $t=3$ | $4$ |
| E2 | $t=4$ | $2$ |
| E3 | $t=4$ | $2+6 = 8$ |
| E3 | $t=5$ | $6$ |

$$V(3) = \frac{4+2+8+6}{4} = \frac{20}{4} = 5$$

> [!success] Summary of Example 4
> | State | First-Visit $V(s)$ | Every-Visit $V(s)$ |
> |-------|--------------------|--------------------|
> | 1 | $13.0$ | $9.75$ |
> | 2 | $\approx 10.67$ | $\approx 10.67$ |
> | 3 | $\approx 4.67$ | $5.0$ |

---

## Incremental Mean Update

Maintaining a list of all returns and recomputing the average each time is memory-inefficient. Instead, we can update the mean **incrementally**.

### Derivation

Given a running mean $\mu_n$ after $n$ samples and a new sample $x_{n+1}$:

$$\mu_{n+1} = \frac{1}{n+1} \sum_{i=1}^{n+1} x_i = \frac{1}{n+1} \left( n \cdot \mu_n + x_{n+1} \right) = \mu_n + \frac{1}{n+1}(x_{n+1} - \mu_n)$$

### Applied to MC Prediction

After observing the $N$-th return $G$ for state $s$:

$$V(s) \leftarrow V(s) + \frac{1}{N(s)}\Big(G - V(s)\Big)$$

where $N(s)$ is the total count of visits to state $s$ so far.

> [!info] Intuition
> The update rule says: adjust the old estimate toward the new observation. The term $(G - V(s))$ is the **error** between what we observed and what we estimated. We move a fraction $\frac{1}{N}$ of this error into our estimate.

### Constant Step-Size Variant

In non-stationary environments (where the underlying value may change over time), we can replace $\frac{1}{N(s)}$ with a constant step size $\alpha \in (0, 1]$:

$$V(s) \leftarrow V(s) + \alpha \Big(G - V(s)\Big)$$

This gives more weight to recent returns and allows the estimate to track a changing environment. With constant $\alpha$:
- Recent returns have exponentially more influence than older returns
- The estimate never fully converges but remains responsive to change
- Choosing $\alpha$ involves a bias-variance tradeoff: larger $\alpha$ tracks faster but is noisier

### Incremental Update Pseudocode

```
Initialize V(s) = 0, N(s) = 0 for all s

Repeat forever (for each episode):
    Generate episode using pi
    For each state s with return G (first-visit or every-visit):
        N(s) = N(s) + 1
        V(s) = V(s) + (1/N(s)) * (G - V(s))
```

---

## MC vs DP Comparison

| Aspect | Dynamic Programming | Monte Carlo |
|--------|-------------------|-------------|
| **Model required?** | Yes -- needs full knowledge of $p(s', r \mid s, a)$ | No -- learns from experience only |
| **Bootstrapping?** | Yes -- updates use estimates of successor states | No -- updates use complete actual returns |
| **Episode required?** | No -- can work with continuing tasks | Yes -- must wait for episode termination |
| **Update timing** | After each step (or sweep) | After each complete episode |
| **Bias** | May have bias from value initialization and bootstrapping | Unbiased (first-visit); slightly biased (every-visit) |
| **Variance** | Lower -- averages over all possible next states | Higher -- depends on single sampled trajectory |
| **Computational cost per update** | Requires sweep over all states or known transitions | Only updates states visited in the episode |
| **Handles large state spaces** | Poorly -- full sweeps become expensive | Better -- focuses on visited states |
| **Sensitivity to initial values** | High -- bootstrapping propagates initialization errors | Low -- returns are independent of initialization |

---

## Common Mistakes

> [!warning] Common Mistakes to Avoid
>
> **1. Confusing rewards and returns.** The return $G_t$ is the cumulative discounted sum from step $t$ to the end. Do not use a single reward $R_t$ where a return $G_t$ is needed.
>
> **2. Forgetting the episodic requirement.** MC cannot be applied to non-terminating tasks. If your MDP does not have terminal states, MC prediction does not apply directly.
>
> **3. Mixing up first-visit and every-visit counting.** In first-visit MC, if state $s$ appears at $t=2$ and $t=5$, you only compute the return from $t=2$. In every-visit MC, you compute returns from both $t=2$ and $t=5$.
>
> **4. Computing returns incorrectly.** The return from step $t$ includes all rewards from $R_{t+1}$ onward (not from $R_t$). In the notation $S_t \xrightarrow{r} S_{t+1}$, the reward $r$ is $R_{t+1}$ and is included in $G_t$.
>
> **5. Forgetting the discount factor.** When $\gamma < 1$, each successive reward must be multiplied by an additional power of $\gamma$. Many exam errors come from assuming $\gamma = 1$ when it is not.
>
> **6. Updating values before the episode ends.** MC requires the full episode to compute returns. You cannot update $V(s)$ mid-episode.
>
> **7. Thinking MC bootstraps.** MC does NOT use other value estimates to compute its updates. Each return is computed entirely from observed rewards.

---

## Self-Check Questions

> [!question]- Why can't Monte Carlo methods be applied to continuing (non-episodic) tasks?
> Because MC computes returns $G_t = R_{t+1} + \gamma R_{t+2} + \cdots$ all the way to the terminal state. If there is no terminal state, the return is an infinite sum that cannot be computed from a finite amount of experience. We must wait for the episode to end to know the return.

> [!question]- In First-Visit MC, if state $s$ appears 5 times in one episode and we run 3 episodes, how many returns are in $\text{Returns}(s)$?
> At most 3 -- one per episode (only the first visit counts in each episode). If $s$ does not appear in some episode, that episode contributes nothing. So the answer is between 0 and 3.

> [!question]- Why is First-Visit MC an unbiased estimator of $v_\pi(s)$ while Every-Visit MC may have slight bias?
> In first-visit MC, each return is an independent, identically distributed sample of $v_\pi(s)$, since each episode contributes one return starting from the first visit to $s$. In every-visit MC, multiple returns from the same episode are correlated (they share parts of the same trajectory), which can introduce slight bias in finite samples. However, both are asymptotically consistent.

> [!question]- What does "no bootstrapping" mean in the context of MC, and what are its consequences?
> No bootstrapping means the value estimate of a state does NOT depend on the value estimates of other states. MC computes returns entirely from observed rewards, not from $V(s')$ of successor states. This reduces bias (no error propagation from inaccurate estimates of other states) but makes convergence slower (cannot leverage structural relationships between states).

> [!question]- Given an episode $S_0 \to S_1 \to S_0 \to S_2 \to \text{Terminal}$ with rewards $+2, +3, -1, +4$ and $\gamma = 1$, what are the first-visit returns for $S_0$, $S_1$, and $S_2$?
> - $S_0$ first appears at $t=0$: $G_0 = 2 + 3 - 1 + 4 = 8$
> - $S_1$ first appears at $t=1$: $G_1 = 3 - 1 + 4 = 6$
> - $S_2$ first appears at $t=3$: $G_3 = 4$
>
> The second visit to $S_0$ at $t=2$ is ignored in first-visit MC. For every-visit, $S_0$ would also get a return of $-1 + 4 = 3$ from $t=2$.

> [!question]- How does the incremental update $V(s) \leftarrow V(s) + \alpha(G - V(s))$ differ from the exact sample average when $\alpha$ is constant?
> With constant $\alpha$, recent returns receive exponentially more weight than older returns, effectively creating a weighted (recency-biased) average. The exact sample average uses $\frac{1}{N}$ which decreases over time, weighting all returns equally. Constant $\alpha$ is useful in non-stationary environments where the true value may change, but it means the estimate never fully converges -- it keeps fluctuating around the true value.

---

## Concept Links

- **Prerequisite**: [[01_dynamic_programming]] -- DP provides the model-based counterpart to MC; understanding Bellman equations and policy evaluation via DP clarifies what MC achieves without a model
- **Next topic**: [[05_monte_carlo_control]] -- extends MC prediction to the control problem (finding optimal policies, not just evaluating them)
- **Related**: [[06_importance_sampling]] -- technique for using episodes generated under one policy to evaluate a different policy in MC
- **Reference**: [[cat2_08_formula_sheet]] -- quick lookup for MC update formulas, return definitions, and comparison tables
