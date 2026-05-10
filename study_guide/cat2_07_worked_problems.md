---
type: problems
tags: [rl, cat2, worked-problems]
---

# Worked Problems - RL CAT-2

This file contains ALL worked problems from the source material plus additional practice problems. Every problem has step-by-step solutions.

---

## Dynamic Programming Problems

### Problem 1: Iterative Policy Evaluation on 4x4 Gridworld

**Concepts Used**: [[01_dynamic_programming#Policy Evaluation]], [[cat2_08_formula_sheet#Bellman Equations]]

> [!info] Problem Setup
> A 4x4 gridworld has 16 states (numbered 0--15). States 0 and 15 are terminal. The agent follows a uniform random policy (each of 4 actions -- up, down, left, right -- has probability 0.25). Reward $= -1$ for every transition. $\gamma = 1$. Actions that take the agent off the grid leave the state unchanged.

**Formulas Used**: [[cat2_08_formula_sheet#Dynamic Programming Update Rules]]

$$V_{k+1}(s) = \sum_a \pi(a|s) \sum_{s',r} p(s',r|s,a)\bigl[r + \gamma\, V_k(s')\bigr]$$

> [!example] Step-by-step solution

**Initialize** all $V_0(s) = 0$.

---

**Iteration 1 ($k=0 \to k=1$):**

For state 1 (top row, second from left):

| Action | Next State | $V_0(\text{next})$ | Contribution |
|--------|-----------|---------------------|-------------|
| Up | 1 (off grid) | 0 | $0.25(-1 + 0) = -0.25$ |
| Down | 5 | 0 | $0.25(-1 + 0) = -0.25$ |
| Left | 0 (terminal) | 0 | $0.25(-1 + 0) = -0.25$ |
| Right | 2 | 0 | $0.25(-1 + 0) = -0.25$ |

$$V_1(1) = -0.25 \times 4 = -1.0$$

By symmetry, all non-terminal states get $V_1(s) = -1.0$ in iteration 1, since every action yields reward $-1$ and all current values are 0.

Grid after $k=1$:

```
 0.0  -1.0  -1.0  -1.0
-1.0  -1.0  -1.0  -1.0
-1.0  -1.0  -1.0  -1.0
-1.0  -1.0  -1.0   0.0
```

---

**Iteration 2 ($k=1 \to k=2$):**

For state 1:

| Action | Next State | $V_1(\text{next})$ | Contribution |
|--------|-----------|---------------------|-------------|
| Up | 1 (off grid) | $-1.0$ | $0.25(-1 + (-1)) = -0.50$ |
| Down | 5 | $-1.0$ | $0.25(-1 + (-1)) = -0.50$ |
| Left | 0 (terminal) | $0$ | $0.25(-1 + 0) = -0.25$ |
| Right | 2 | $-1.0$ | $0.25(-1 + (-1)) = -0.50$ |

$$V_2(1) = -0.50 - 0.50 - 0.25 - 0.50 = -1.75$$

For state 5 (second row, second column -- no adjacent terminals):

| Action | Next State | $V_1(\text{next})$ | Contribution |
|--------|-----------|---------------------|-------------|
| Up | 1 | $-1.0$ | $0.25(-1 + (-1)) = -0.50$ |
| Down | 9 | $-1.0$ | $0.25(-1 + (-1)) = -0.50$ |
| Left | 4 | $-1.0$ | $0.25(-1 + (-1)) = -0.50$ |
| Right | 6 | $-1.0$ | $0.25(-1 + (-1)) = -0.50$ |

$$V_2(5) = -2.0$$

> [!tip] Exam Tip
> Corner and edge states adjacent to terminals get smaller magnitudes because one of their neighbor values is 0 (the terminal). Interior states see all $-1$ neighbors and accumulate faster.

Grid after $k=2$:

```
 0.0  -1.75  -2.0  -2.0
-1.75  -2.0  -2.0  -2.0
-2.0  -2.0  -2.0  -1.75
-2.0  -2.0  -1.75   0.0
```

---

**Iteration 3 ($k=2 \to k=3$):**

For state 1:

| Action | Next State | $V_2(\text{next})$ | Contribution |
|--------|-----------|---------------------|-------------|
| Up | 1 | $-1.75$ | $0.25(-1 + (-1.75)) = -0.6875$ |
| Down | 5 | $-2.0$ | $0.25(-1 + (-2.0)) = -0.75$ |
| Left | 0 | $0$ | $0.25(-1 + 0) = -0.25$ |
| Right | 2 | $-2.0$ | $0.25(-1 + (-2.0)) = -0.75$ |

$$V_3(1) = -0.6875 - 0.75 - 0.25 - 0.75 = -2.4375$$

Grid after $k=3$:

```
  0.0   -2.44  -2.94  -3.0
-2.44   -2.88  -3.0   -2.94
-2.94   -3.0   -2.88  -2.44
-3.0   -2.94  -2.44    0.0
```

The values continue to grow more negative. Final converged values ($k \to \infty$):

```
  0   -14  -20  -22
-14   -18  -20  -20
-20   -20  -18  -14
-22   -20  -14    0
```

> [!success] Key Observation
> States far from terminals have more negative values. The pattern is symmetric about the diagonal connecting state 0 and state 15.

> [!warning] Common Pitfall
> Do not forget that off-grid actions leave the agent in the same state. The agent still receives $r = -1$ for an off-grid action, it just does not move. Many students miss the self-loop contribution.

---

### Problem 2: Policy Iteration on a Simple MDP

**Concepts Used**: [[02_policy_iteration]], [[cat2_08_formula_sheet#Dynamic Programming Update Rules]]

> [!info] Problem Setup
> States: $\{s_1, s_2\}$, Terminal state: $s_T$
> Actions: $\{a_1, a_2\}$
> Transitions:
> - From $s_1$: $a_1 \to s_2$ (reward 5), $a_2 \to s_T$ (reward 10)
> - From $s_2$: $a_1 \to s_1$ (reward $-1$), $a_2 \to s_T$ (reward 2)
>
> $\gamma = 0.9$

**Initial policy**: $\pi_0(s_1) = a_1$, $\pi_0(s_2) = a_1$

> [!example] Step 1 -- Policy Evaluation for $\pi_0$

Under $\pi_0$: $s_1 \to s_2$ (r=5), $s_2 \to s_1$ (r=$-1$), cycles forever.

Set up the system of equations:

$$V^{\pi_0}(s_1) = 5 + 0.9 \cdot V^{\pi_0}(s_2)$$

$$V^{\pi_0}(s_2) = -1 + 0.9 \cdot V^{\pi_0}(s_1)$$

Substitute the second into the first:

$$V(s_1) = 5 + 0.9\bigl(-1 + 0.9 \cdot V(s_1)\bigr)$$

$$V(s_1) = 5 - 0.9 + 0.81 \cdot V(s_1)$$

$$0.19 \cdot V(s_1) = 4.1$$

$$V^{\pi_0}(s_1) = \frac{4.1}{0.19} = 21.58$$

$$V^{\pi_0}(s_2) = -1 + 0.9 \times 21.58 = 18.42$$

> [!example] Step 2 -- Policy Improvement

For $s_1$:

$$Q(s_1, a_1) = 5 + 0.9 \cdot V(s_2) = 5 + 0.9 \times 18.42 = 21.58$$

$$Q(s_1, a_2) = 10 + 0.9 \cdot V(s_T) = 10 + 0 = 10$$

$\pi_1(s_1) = a_1$ since $Q(s_1, a_1) = 21.58 > Q(s_1, a_2) = 10$.

For $s_2$:

$$Q(s_2, a_1) = -1 + 0.9 \cdot V(s_1) = -1 + 0.9 \times 21.58 = 18.42$$

$$Q(s_2, a_2) = 2 + 0.9 \cdot V(s_T) = 2 + 0 = 2$$

$\pi_1(s_2) = a_1$ since $Q(s_2, a_1) = 18.42 > Q(s_2, a_2) = 2$.

Policy unchanged: $\pi_1 = \pi_0$. Policy iteration converges in one round.

> [!success] Answer
> Optimal policy: $\pi^*(s_1) = a_1$, $\pi^*(s_2) = a_1$
> Optimal values: $V^*(s_1) = 21.58$, $V^*(s_2) = 18.42$

> [!warning] Common Pitfall
> When the terminal state is reached, its value is always 0. Do not forget $V(s_T) = 0$ in the Q-value computation for actions that transition to the terminal.

---

### Problem 3: Value Iteration

**Concepts Used**: [[03_value_iteration]], [[cat2_08_formula_sheet#Dynamic Programming Update Rules]]

> [!info] Problem Setup
> Same MDP as Problem 2. Apply value iteration.
> $$V_{k+1}(s) = \max_a \sum_{s',r} p(s',r|s,a)\bigl[r + \gamma\, V_k(s')\bigr]$$

Initialize $V_0(s_1) = 0$, $V_0(s_2) = 0$.

> [!example] Iteration-by-iteration computation

**Iteration 1:**

$$V_1(s_1) = \max\{5 + 0.9 \times 0,\; 10 + 0.9 \times 0\} = \max\{5, 10\} = 10$$

$$V_1(s_2) = \max\{-1 + 0.9 \times 0,\; 2 + 0.9 \times 0\} = \max\{-1, 2\} = 2$$

**Iteration 2:**

$$V_2(s_1) = \max\{5 + 0.9 \times 2,\; 10 + 0.9 \times 0\} = \max\{6.8,\; 10\} = 10$$

$$V_2(s_2) = \max\{-1 + 0.9 \times 10,\; 2 + 0.9 \times 0\} = \max\{8,\; 2\} = 8$$

**Iteration 3:**

$$V_3(s_1) = \max\{5 + 0.9 \times 8,\; 10\} = \max\{12.2,\; 10\} = 12.2$$

$$V_3(s_2) = \max\{-1 + 0.9 \times 10,\; 2\} = \max\{8,\; 2\} = 8$$

**Iteration 4:**

$$V_4(s_1) = \max\{5 + 0.9 \times 8,\; 10\} = \max\{12.2,\; 10\} = 12.2$$

$$V_4(s_2) = \max\{-1 + 0.9 \times 12.2,\; 2\} = \max\{9.98,\; 2\} = 9.98$$

**Iteration 5:**

$$V_5(s_1) = \max\{5 + 0.9 \times 9.98,\; 10\} = \max\{13.982,\; 10\} = 13.982$$

$$V_5(s_2) = \max\{-1 + 0.9 \times 12.2,\; 2\} = \max\{9.98,\; 2\} = 9.98$$

**Iteration 6:**

$$V_6(s_1) = \max\{5 + 0.9 \times 9.98,\; 10\} = \max\{13.982,\; 10\} = 13.982$$

$$V_6(s_2) = \max\{-1 + 0.9 \times 13.982,\; 2\} = \max\{11.584,\; 2\} = 11.584$$

**Summary Table:**

| $k$ | $V(s_1)$ | $V(s_2)$ | $\delta$ |
|-----|-----------|-----------|----------|
| 0 | 0 | 0 | -- |
| 1 | 10 | 2 | 10 |
| 2 | 10 | 8 | 6 |
| 3 | 12.2 | 8 | 2.2 |
| 4 | 12.2 | 9.98 | 1.98 |
| 5 | 13.982 | 9.98 | 1.782 |
| 6 | 13.982 | 11.584 | 1.604 |
| $\vdots$ | $\vdots$ | $\vdots$ | $\vdots$ |
| $\infty$ | 21.58 | 18.42 | 0 |

> [!tip] Exam Tip
> Notice how value iteration alternates which state "catches up." The values oscillate as improvements propagate back and forth between states. Policy iteration solved the same problem in a single evaluation + improvement step.

**Extract policy at convergence:**

$$\pi^*(s_1) = a_1 \quad\text{since}\quad 5 + 0.9 \times 18.42 = 21.58 > 10$$

$$\pi^*(s_2) = a_1 \quad\text{since}\quad -1 + 0.9 \times 21.58 = 18.42 > 2$$

> [!success] Answer
> Same result as policy iteration: $V^*(s_1) = 21.58$, $V^*(s_2) = 18.42$, $\pi^*(s_1) = a_1$, $\pi^*(s_2) = a_1$.

---

## Monte Carlo Problems

### Problem 4: First-Visit vs Every-Visit MC (Single State)

**Concepts Used**: [[04_monte_carlo_prediction#First-Visit Monte Carlo Prediction]]

> [!info] Problem Setup
> MDP with a single nonterminal state $s$, a single action. At each step the agent transitions back to $s$ with probability $p$ or to the terminal with probability $1-p$. Reward $= +1$ on all transitions. $\gamma = 1$.
> One episode lasts 10 steps (return = 10).

> [!example] First-Visit MC
> The state $s$ is visited once at the start (first visit only).
> $$V(s) = \frac{10}{1} = 10$$

> [!example] Every-Visit MC
> The state $s$ is visited 10 times. The return starting from each visit:
>
> | Visit | Remaining rewards | $G$ |
> |-------|-------------------|-----|
> | 1 | 10 | 10 |
> | 2 | 9 | 9 |
> | 3 | 8 | 8 |
> | 4 | 7 | 7 |
> | 5 | 6 | 6 |
> | 6 | 5 | 5 |
> | 7 | 4 | 4 |
> | 8 | 3 | 3 |
> | 9 | 2 | 2 |
> | 10 | 1 | 1 |
>
> $$V(s) = \frac{10 + 9 + 8 + 7 + 6 + 5 + 4 + 3 + 2 + 1}{10} = \frac{55}{10} = 5.5$$

> [!success] Answer
> First-visit: $V(s) = 10$
> Every-visit: $V(s) = 5.5$

> [!warning] Common Pitfall
> Every-visit MC counts ALL visits to a state within a single episode. The returns from later visits are smaller, pulling the average down. This is why first-visit and every-visit give different estimates from the same data.

---

### Problem 5: MC with States A and B

**Concepts Used**: [[04_monte_carlo_prediction]]

> [!info] Problem Setup
> Two episodes with states $A$ and $B$:
> - Episode 1: $A \xrightarrow{+3} A \xrightarrow{+2} B \xrightarrow{-4} A \xrightarrow{+4} B \xrightarrow{-3} \text{terminate}$
> - Episode 2: $B \xrightarrow{-2} A \xrightarrow{+3} B \xrightarrow{-3} \text{terminate}$
>
> $\gamma = 1$ (undiscounted).

> [!example] First-Visit MC

**State $A$:**
- Episode 1: First visit at step 0. $G = 3 + 2 + (-4) + 4 + (-3) = 2$
- Episode 2: First visit at step 1. $G = 3 + (-3) = 0$

$$V(A) = \frac{2 + 0}{2} = 1.0$$

**State $B$:**
- Episode 1: First visit at step 2. $G = -4 + 4 + (-3) = -3$
- Episode 2: First visit at step 0. $G = -2 + 3 + (-3) = -2$

$$V(B) = \frac{-3 + (-2)}{2} = -2.5$$

> [!example] Every-Visit MC

**State $A$:**

| Episode | Step | Return $G$ |
|---------|------|-----------|
| 1 | 0 | $3+2-4+4-3 = 2$ |
| 1 | 1 | $2-4+4-3 = -1$ |
| 1 | 3 | $4-3 = 1$ |
| 2 | 1 | $3-3 = 0$ |

$$V(A) = \frac{2 + (-1) + 1 + 0}{4} = \frac{2}{4} = 0.5$$

**State $B$:**

| Episode | Step | Return $G$ |
|---------|------|-----------|
| 1 | 2 | $-4+4-3 = -3$ |
| 1 | 4 | $-3$ |
| 2 | 0 | $-2+3-3 = -2$ |
| 2 | 2 | $-3$ |

$$V(B) = \frac{-3 + (-3) + (-2) + (-3)}{4} = \frac{-11}{4} = -2.75$$

> [!success] Answer
> **First-Visit:** $V(A) = 1.0$, $V(B) = -2.5$
> **Every-Visit:** $V(A) = 0.5$, $V(B) = -2.75$

> [!tip] Exam Tip
> When computing every-visit returns, list out every occurrence of each state across all episodes. A systematic table like the ones above prevents missed visits.

---

### Problem 6: Five States, Four Episodes

**Concepts Used**: [[04_monte_carlo_prediction]]

> [!info] Problem Setup
> Five states $S_0$--$S_4$, terminal state $S_T$. Four episodes ($\gamma = 1$):
>
> **E1:** $S_0 \xrightarrow{3} S_4 \xrightarrow{1} S_0 \xrightarrow{2} S_2 \xrightarrow{-1} S_1 \xrightarrow{5} S_2 \xrightarrow{4} S_T$
>
> **E2:** $S_1 \xrightarrow{3} S_3 \xrightarrow{1} S_0 \xrightarrow{2} S_2 \xrightarrow{5} S_T$
>
> **E3:** $S_2 \xrightarrow{-2} S_1 \xrightarrow{2} S_3 \xrightarrow{3} S_4 \xrightarrow{1} S_1 \xrightarrow{2} S_T$
>
> **E4:** $S_4 \xrightarrow{3} S_0 \xrightarrow{1} S_2 \xrightarrow{3} S_0 \xrightarrow{-1} S_2 \xrightarrow{2} S_1 \xrightarrow{1} S_T$

#### Part A: First-Visit MC

> [!example] First-Visit computation for each state

**$S_0$:**

| Episode | First appears at step | Return $G$ |
|---------|----------------------|-----------|
| E1 | 0 | $3+1+2-1+5+4 = 14$ |
| E2 | 2 | $2+5 = 7$ |
| E3 | not visited | -- |
| E4 | 1 | $1+3-1+2+1 = 6$ |

$$V(S_0) = \frac{14 + 7 + 6}{3} = \frac{27}{3} = 9.0$$

**$S_1$:**

| Episode | First appears at step | Return $G$ |
|---------|----------------------|-----------|
| E1 | 4 | $5+4 = 9$ |
| E2 | 0 | $3+1+2+5 = 11$ |
| E3 | 1 | $2+3+1+2 = 8$ |
| E4 | 5 | $1$ |

$$V(S_1) = \frac{9 + 11 + 8 + 1}{4} = \frac{29}{4} = 7.25$$

**$S_2$:**

| Episode | First appears at step | Return $G$ |
|---------|----------------------|-----------|
| E1 | 3 | $-1+5+4 = 8$ |
| E2 | 3 | $5$ |
| E3 | 0 | $-2+2+3+1+2 = 6$ |
| E4 | 2 | $3-1+2+1 = 5$ |

$$V(S_2) = \frac{8 + 5 + 6 + 5}{4} = \frac{24}{4} = 6.0$$

**$S_3$:**

| Episode | First appears at step | Return $G$ |
|---------|----------------------|-----------|
| E1 | not visited | -- |
| E2 | 1 | $1+2+5 = 8$ |
| E3 | 2 | $3+1+2 = 6$ |
| E4 | not visited | -- |

$$V(S_3) = \frac{8 + 6}{2} = \frac{14}{2} = 7.0$$

**$S_4$:**

| Episode | First appears at step | Return $G$ |
|---------|----------------------|-----------|
| E1 | 1 | $1+2-1+5+4 = 11$ |
| E2 | not visited | -- |
| E3 | 3 | $1+2 = 3$ |
| E4 | 0 | $3+1+3-1+2+1 = 9$ |

$$V(S_4) = \frac{11 + 3 + 9}{3} = \frac{23}{3} \approx 7.67$$

> [!success] Answer (First-Visit MC)
> $V(S_0) = 9.0$, $V(S_1) = 7.25$, $V(S_2) = 6.0$, $V(S_3) = 7.0$, $V(S_4) \approx 7.67$

---

#### Part B: Every-Visit MC

> [!example] Every-Visit computation for each state

**$S_0$:**

| Episode | Step | Return $G$ |
|---------|------|-----------|
| E1 | 0 | $3+1+2-1+5+4 = 14$ |
| E1 | 2 | $2-1+5+4 = 10$ |
| E2 | 2 | $2+5 = 7$ |
| E4 | 1 | $1+3-1+2+1 = 6$ |
| E4 | 3 | $-1+2+1 = 2$ |

$$V(S_0) = \frac{14 + 10 + 7 + 6 + 2}{5} = \frac{39}{5} = 7.8$$

**$S_1$:**

| Episode | Step | Return $G$ |
|---------|------|-----------|
| E1 | 4 | $5+4 = 9$ |
| E2 | 0 | $3+1+2+5 = 11$ |
| E3 | 1 | $2+3+1+2 = 8$ |
| E3 | 4 | $2$ |
| E4 | 5 | $1$ |

$$V(S_1) = \frac{9 + 11 + 8 + 2 + 1}{5} = \frac{31}{5} = 6.2$$

**$S_2$:**

| Episode | Step | Return $G$ |
|---------|------|-----------|
| E1 | 3 | $-1+5+4 = 8$ |
| E1 | 5 | $4$ |
| E2 | 3 | $5$ |
| E3 | 0 | $-2+2+3+1+2 = 6$ |
| E4 | 2 | $3-1+2+1 = 5$ |
| E4 | 4 | $2+1 = 3$ |

$$V(S_2) = \frac{8 + 4 + 5 + 6 + 5 + 3}{6} = \frac{31}{6} \approx 5.17$$

**$S_3$:**

| Episode | Step | Return $G$ |
|---------|------|-----------|
| E2 | 1 | $1+2+5 = 8$ |
| E3 | 2 | $3+1+2 = 6$ |

$$V(S_3) = \frac{8 + 6}{2} = 7.0$$

(No repeated visits to $S_3$ in any episode, so every-visit equals first-visit here.)

**$S_4$:**

| Episode | Step | Return $G$ |
|---------|------|-----------|
| E1 | 1 | $1+2-1+5+4 = 11$ |
| E3 | 3 | $1+2 = 3$ |
| E4 | 0 | $3+1+3-1+2+1 = 9$ |

$$V(S_4) = \frac{11 + 3 + 9}{3} = \frac{23}{3} \approx 7.67$$

(No repeated visits to $S_4$ in any episode, so every-visit equals first-visit here.)

> [!success] Answer (Every-Visit MC)
> $V(S_0) = 7.8$, $V(S_1) = 6.2$, $V(S_2) \approx 5.17$, $V(S_3) = 7.0$, $V(S_4) \approx 7.67$

> [!info] Comparison Table
>
> | State | First-Visit | Every-Visit |
> |-------|------------|------------|
> | $S_0$ | 9.0 | 7.8 |
> | $S_1$ | 7.25 | 6.2 |
> | $S_2$ | 6.0 | 5.17 |
> | $S_3$ | 7.0 | 7.0 |
> | $S_4$ | 7.67 | 7.67 |
>
> States with repeated intra-episode visits ($S_0$, $S_1$, $S_2$) show different first-visit and every-visit estimates. States visited at most once per episode ($S_3$, $S_4$) have identical estimates.

> [!warning] Common Pitfall
> When listing visits for every-visit MC, scan each episode from start to finish. Every time the state label appears, that is a separate visit. Do not skip later occurrences -- that is the whole point of every-visit.

---

### Problem 7: Three States, Three Episodes

**Concepts Used**: [[04_monte_carlo_prediction]]

> [!info] Problem Setup
> Agent always goes right. (State, Reward) pairs per episode:
> - Episode 1: $(1,1) \to (2,2) \to (1,3) \to (3,4)$
> - Episode 2: $(1,2) \to (1,3) \to (2,1) \to (2,4) \to (3,2)$
> - Episode 3: $(1,1) \to (2,1) \to (2,4) \to (2,3) \to (3,2) \to (3,6)$
>
> $\gamma = 1$ (undiscounted).
> Interpretation: at the state shown, the agent receives the reward shown, then transitions to the next state. The episode terminates after the last entry.

> [!example] First-Visit MC

**State 1:**

| Episode | First at step | Rewards from that point | $G$ |
|---------|--------------|------------------------|-----|
| E1 | 0 | $1+2+3+4$ | 10 |
| E2 | 0 | $2+3+1+4+2$ | 12 |
| E3 | 0 | $1+1+4+3+2+6$ | 17 |

$$V(1) = \frac{10+12+17}{3} = \frac{39}{3} = 13.0$$

**State 2:**

| Episode | First at step | Rewards from that point | $G$ |
|---------|--------------|------------------------|-----|
| E1 | 1 | $2+3+4$ | 9 |
| E2 | 2 | $1+4+2$ | 7 |
| E3 | 1 | $1+4+3+2+6$ | 16 |

$$V(2) = \frac{9+7+16}{3} = \frac{32}{3} \approx 10.67$$

**State 3:**

| Episode | First at step | Rewards from that point | $G$ |
|---------|--------------|------------------------|-----|
| E1 | 3 | $4$ | 4 |
| E2 | 4 | $2$ | 2 |
| E3 | 4 | $2+6$ | 8 |

$$V(3) = \frac{4+2+8}{3} = \frac{14}{3} \approx 4.67$$

> [!success] Answer (First-Visit MC)
> $V(1) = 13.0$, $V(2) \approx 10.67$, $V(3) \approx 4.67$

> [!tip] Exam Tip
> When episodes are given as (state, reward) pairs, the return from a visit is the sum of all rewards from that step onward to the end of the episode. Carefully index from the correct starting position.

---

## Importance Sampling Problems

### Problem 8: Statistical Importance Sampling

**Concepts Used**: [[06_importance_sampling#Statistical Foundation]]

> [!info] Problem Setup
> Estimate $E_p[f(X)]$ where:
> - $p(x) = \mathcal{N}(0,1)$
> - $q(x) = \mathcal{N}(1,1)$
> - $f(x) = e^{-x^2}$
>
> We draw samples from $q$ and use IS to estimate the expectation under $p$.

**Formula:** [[cat2_08_formula_sheet#Bellman Equations]]

$$E_p[f(X)] = E_q\!\left[\frac{p(X)}{q(X)}\, f(X)\right] \approx \frac{1}{N}\sum_{i=1}^{N} w(x_i)\, f(x_i)$$

where $x_i \sim q$ and $w(x_i) = \dfrac{p(x_i)}{q(x_i)}$.

> [!example] Step 1 -- Derive the importance weight

$$w(x) = \frac{p(x)}{q(x)} = \frac{\frac{1}{\sqrt{2\pi}}\exp\!\bigl(-\tfrac{x^2}{2}\bigr)}{\frac{1}{\sqrt{2\pi}}\exp\!\bigl(-\tfrac{(x-1)^2}{2}\bigr)}$$

$$w(x) = \exp\!\left(-\frac{x^2}{2} + \frac{(x-1)^2}{2}\right)$$

Expand $(x-1)^2 = x^2 - 2x + 1$:

$$w(x) = \exp\!\left(\frac{-x^2 + x^2 - 2x + 1}{2}\right) = \exp\!\left(\frac{-2x+1}{2}\right) = e^{-x + 1/2}$$

> [!example] Step 2 -- Draw $N=5$ samples from $q(x) = \mathcal{N}(1,1)$

Samples: $x = \{0.5,\ 1.2,\ 0.8,\ 1.5,\ 2.0\}$

> [!example] Step 3 -- Compute weight and product for each sample

$$w(x_i) = e^{-x_i + 0.5}$$

| $x_i$ | $f(x_i) = e^{-x_i^2}$ | $w(x_i) = e^{-x_i+0.5}$ | $w(x_i) \cdot f(x_i)$ |
|--------|----------------------|--------------------------|----------------------|
| 0.5 | $e^{-0.25} = 0.7788$ | $e^{0} = 1.0000$ | 0.7788 |
| 1.2 | $e^{-1.44} = 0.2369$ | $e^{-0.7} = 0.4966$ | 0.1176 |
| 0.8 | $e^{-0.64} = 0.5273$ | $e^{-0.3} = 0.7408$ | 0.3907 |
| 1.5 | $e^{-2.25} = 0.1054$ | $e^{-1.0} = 0.3679$ | 0.0388 |
| 2.0 | $e^{-4.0} = 0.0183$ | $e^{-1.5} = 0.2231$ | 0.0041 |

> [!example] Step 4 -- Compute estimate

$$\sum_{i=1}^{5} w(x_i)\, f(x_i) = 0.7788 + 0.1176 + 0.3907 + 0.0388 + 0.0041 = 1.330$$

$$\hat{E}_p[f(X)] = \frac{1}{5} \times 1.330 = 0.266$$

> [!success] Answer
> $E_p[f(X)] \approx 0.266$ (with these 5 samples).
> The true value is $E_p[e^{-X^2}] = \frac{1}{\sqrt{3}} \approx 0.577$. More samples would improve the estimate.

> [!tip] Exam Tip
> The key formula for the IS weight between two Gaussians $\mathcal{N}(\mu_1, \sigma^2)$ and $\mathcal{N}(\mu_2, \sigma^2)$ with equal variance simplifies nicely. Always expand the exponent algebra carefully.

> [!warning] Common Pitfall
> Make sure the weight is $w = p/q$, not $q/p$. The numerator is always the distribution you want to estimate under (the target), and the denominator is the distribution you actually sample from (the proposal/behavior).

---

### Problem 9: RL Importance Sampling

**Concepts Used**: [[06_importance_sampling#Importance Sampling in RL]]

> [!info] Problem Setup
> One episode: $S_0 = s_1,\ A_0 = a_1,\ R_1 = 2,\ S_1 = s_2,\ A_1 = a_2,\ R_2 = 5$
>
> Behavior policy $b$: $b(a_1|s_1) = 0.4$, $b(a_2|s_2) = 0.3$
> Target policy $\pi$: $\pi(a_1|s_1) = 0.6$, $\pi(a_2|s_2) = 0.5$
> $\gamma = 0.9$

> [!example] Step 1 -- Compute return

$$G = R_1 + \gamma R_2 = 2 + 0.9 \times 5 = 2 + 4.5 = 6.5$$

> [!example] Step 2 -- Compute IS ratio

The importance sampling ratio is the product of policy ratios over all time steps:

$$\rho_{0:T-1} = \prod_{t=0}^{T-1} \frac{\pi(A_t|S_t)}{b(A_t|S_t)}$$

$$\rho = \frac{\pi(a_1|s_1)}{b(a_1|s_1)} \times \frac{\pi(a_2|s_2)}{b(a_2|s_2)} = \frac{0.6}{0.4} \times \frac{0.5}{0.3} = 1.5 \times 1.667 = 2.5$$

> [!example] Step 3 -- Off-policy return estimate

$$\hat{V}(s_1) = \rho \times G = 2.5 \times 6.5 = 16.25$$

> [!success] Answer
> IS ratio $\rho = 2.5$, Estimated return under target policy $\hat{V}(s_1) = 16.25$.

> [!warning] Common Pitfall
> The IS ratio is a **product** over all time steps, not a sum. Missing one factor gives a completely wrong answer. Also, the ratio involves only the actions actually taken -- not all possible actions.

---

### Problem 10: Ordinary vs Weighted IS Comparison

**Concepts Used**: [[06_importance_sampling#Ordinary Importance Sampling]], [[06_importance_sampling#Weighted Importance Sampling]]

> [!info] Problem Setup
> We want to estimate $V^\pi(s)$. Three episodes generated by behavior policy $b$, all starting at state $s$:
>
> | Episode | Return $G_i$ | IS Ratio $\rho_i$ |
> |---------|-------------|-------------------|
> | 1 | 4 | 2.0 |
> | 2 | 6 | 0.5 |
> | 3 | 3 | 1.5 |

> [!example] Ordinary Importance Sampling

Ordinary IS divides by the number of episodes $n$:

$$V_{\text{ordinary}}(s) = \frac{1}{n}\sum_{i=1}^{n} \rho_i\, G_i$$

$$= \frac{1}{3}\bigl(2.0 \times 4 + 0.5 \times 6 + 1.5 \times 3\bigr)$$

$$= \frac{1}{3}\bigl(8 + 3 + 4.5\bigr) = \frac{15.5}{3} \approx 5.167$$

> [!example] Weighted Importance Sampling

Weighted IS normalizes by the sum of weights instead:

$$V_{\text{weighted}}(s) = \frac{\sum_{i=1}^{n} \rho_i\, G_i}{\sum_{i=1}^{n} \rho_i}$$

$$= \frac{2.0 \times 4 + 0.5 \times 6 + 1.5 \times 3}{2.0 + 0.5 + 1.5}$$

$$= \frac{8 + 3 + 4.5}{4.0} = \frac{15.5}{4.0} = 3.875$$

> [!success] Answer
> **Ordinary IS:** $V(s) \approx 5.167$
> **Weighted IS:** $V(s) = 3.875$

> [!info] Key Differences
> - **Ordinary IS** is **unbiased** but has **higher variance** (can produce estimates outside the range of observed returns).
> - **Weighted IS** is **biased** (bias decreases with more samples) but has **lower variance** (the estimate is always within the range of observed returns).
> - In practice, weighted IS is generally preferred because the variance reduction outweighs the small bias.

> [!tip] Exam Tip
> Quick check: weighted IS always produces an estimate that is a convex combination of the returns $G_i$ (since the normalized weights sum to 1). If your weighted IS answer falls outside $[\min(G_i), \max(G_i)]$, you made an error. Ordinary IS has no such constraint.

---

## Quick Reference: Problem-to-Concept Map

| Problem | Topic | Method | Key Concept |
|---------|-------|--------|-------------|
| 1 | [[01_dynamic_programming]] | Iterative Policy Evaluation | Bellman expectation backup |
| 2 | [[02_policy_iteration]] | Policy Iteration | Evaluate then improve |
| 3 | [[03_value_iteration]] | Value Iteration | Bellman optimality backup |
| 4 | [[04_monte_carlo_prediction]] | First-Visit vs Every-Visit | Return counting |
| 5 | [[04_monte_carlo_prediction]] | First-Visit vs Every-Visit | Multi-state episodes |
| 6 | [[04_monte_carlo_prediction]] | First-Visit and Every-Visit | 5-state full walkthrough |
| 7 | [[04_monte_carlo_prediction]] | First-Visit MC | (State, Reward) pair format |
| 8 | [[06_importance_sampling]] | Statistical IS | Gaussian weight derivation |
| 9 | [[06_importance_sampling]] | RL IS | Trajectory ratio |
| 10 | [[06_importance_sampling]] | Ordinary vs Weighted IS | Bias-variance tradeoff |
