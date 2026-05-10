# Formula Sheet -- Reinforcement Learning CAT-1

**Purpose**: Comprehensive reference of every formula, definition, and identity needed for the exam
**Usage**: Quick look-up during revision; pair with worked examples in earlier modules
**Coverage**: Modules 1--2 (RL Fundamentals, Bandits, Mathematical Foundations, Contraction Mapping, Bellman Equations)

---

## 1. Frequently Examined Formulas (Past Paper Favourites)

The formulas in this section have appeared in **every past paper analysed** (2/2). They are virtually guaranteed to appear again. Memorise these first.

---

### 1.1 Softmax (Boltzmann) Action Selection

> **PAST PAPER FAVOURITE** -- This formula has appeared in **2/2** past papers.
> Always tested as a numerical computation problem worth 6--10 marks.

> **CRITICAL EQUATION -- Boltzmann Softmax**
>
> $
> P(a_t = a) = \frac{e^{Q_t(a) / \beta}}{\sum_{b=1}^{n} e^{Q_t(b) / \beta}}
> $

> **Where:**
> - $P(a_t = a)$ = probability of selecting action $a$ at time $t$
> - $Q_t(a)$ = estimated value of arm $a$ at time $t$ (average of rewards received from arm $a$ so far)
> - $\beta$ = temperature parameter (positive real number)
> - $n$ = total number of arms (actions)
> - The summation in the denominator runs over **all** arms $b = 1, 2, \ldots, n$

---

### 1.2 Contraction Mapping Condition

> **PAST PAPER FAVOURITE** -- This formula has appeared in **2/2** past papers.
> Tested as: "prove that $f$ is a contraction" or "find the contraction constant."

> **CRITICAL EQUATION -- Contraction Mapping**
>
> $
> d\big(f(x_1),\; f(x_2)\big) \leq \gamma \cdot d(x_1, x_2) \quad \text{for all } x_1, x_2 \in X
> $

> **Where:**
> - $f: X \to X$ = a mapping on the metric space $(X, d)$
> - $d$ = the metric (distance function) on $X$
> - $\gamma \in [0, 1)$ = the **contraction constant** (also called Lipschitz constant); must be strictly less than 1
> - $x_1, x_2$ = any two points in $X$

---

### 1.3 Bellman Optimality Operator

> **PAST PAPER FAVOURITE** -- This formula has appeared in **2/2** past papers.
> Tested as: "state the Bellman optimality operator" and "show that it is a contraction."

> **CRITICAL EQUATION -- Bellman Optimality Operator**
>
> $
> BV(s) = \max_{a} \left[ R_s^a + \gamma \sum_{s' \in S} P_{ss'}^a \, V(s') \right]
> $

> **Where:**
> - $BV(s)$ = the result of applying the Bellman operator $B$ to value function $V$ at state $s$
> - $R_s^a$ = expected immediate reward for taking action $a$ in state $s$
> - $\gamma \in [0, 1)$ = discount factor
> - $P_{ss'}^a$ = transition probability from state $s$ to state $s'$ under action $a$
> - $V(s')$ = value of successor state $s'$
> - $S$ = the set of all states

---

### 1.4 L-infinity Norm

> **PAST PAPER FAVOURITE** -- This formula has appeared in **2/2** past papers.
> Tested as: "compute the L-infinity norm of the difference between two value functions."

> **CRITICAL EQUATION -- L-infinity (Max) Norm**
>
> $
> \|X\|_\infty = \max_{i} |X_i|
> $

For value functions specifically:

$
\|V\|_\infty = \max_{s \in S} |V(s)|
$

> **Where:**
> - $X$ = a vector (or function represented as a vector)
> - $X_i$ = the $i$-th component of $X$
> - $|X_i|$ = absolute value of the $i$-th component
> - The norm equals the **maximum absolute value** across all components

When computing the distance between two value functions:

$
\|V_1 - V_2\|_\infty = \max_{s \in S} |V_1(s) - V_2(s)|
$

---

### 1.5 Policy Comparison (Partial Ordering)

> **PAST PAPER FAVOURITE** -- This formula has appeared in **2/2** past papers.
> Tested as: "when can we say one policy is better than another?"

> **CRITICAL EQUATION -- Policy Ordering**
>
> $
> \pi_1 \geq \pi_2 \quad \text{if and only if} \quad V^{\pi_1}(s) \geq V^{\pi_2}(s) \quad \text{for all } s \in S
> $

> **Where:**
> - $\pi_1, \pi_2$ = two policies
> - $V^{\pi}(s)$ = value of state $s$ under policy $\pi$
> - $S$ = the set of all states
> - The comparison must hold for **every** state, not just some

---

### 1.6 Bellman Contraction Result

> **PAST PAPER FAVOURITE** -- This formula has appeared in **2/2** past papers.
> Tested as: "prove that the Bellman operator is a contraction in the L-infinity norm."

> **CRITICAL EQUATION -- Bellman Operator Contraction**
>
> $
> \|BV_1 - BV_2\|_\infty \leq \gamma \cdot \|V_1 - V_2\|_\infty
> $

> **Where:**
> - $B$ = the Bellman optimality operator
> - $V_1, V_2$ = any two value functions in $\mathbb{R}^{|S|}$
> - $\gamma \in [0, 1)$ = discount factor (acts as the contraction constant)
> - $\|\cdot\|_\infty$ = L-infinity norm (max absolute difference across states)
> - This result means $B$ is a contraction mapping with constant $\gamma$ on the complete metric space $(\mathbb{R}^{|S|}, \|\cdot\|_\infty)$

---

## 2. Reinforcement Learning Basics

### 2.1 Action Value

$
Q(a) = E[r \mid a]
$

> **Where:**
> - $Q(a)$ = true value of action $a$
> - $E[r \mid a]$ = expected reward given that action $a$ is selected

### 2.2 Optimal Value

$
V^* = \max_a Q(a) = Q(a^*)
$

> **Where:**
> - $V^*$ = optimal value (value of the best action)
> - $a^* = \arg\max_a Q(a)$ = the optimal action

### 2.3 Temporal Difference (TD) Update

$
V(S_t) \leftarrow V(S_t) + \alpha \Big[ V(S_{t+1}) - V(S_t) \Big]
$

> **Where:**
> - $V(S_t)$ = estimated value of the current state
> - $V(S_{t+1})$ = estimated value of the next state
> - $\alpha \in (0, 1]$ = learning rate (step size)
> - $V(S_{t+1}) - V(S_t)$ = TD error (difference between successive estimates)

### 2.4 Discounted Return

$
G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \cdots = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}
$

> **Where:**
> - $G_t$ = return (total discounted reward) from time step $t$
> - $R_{t+k+1}$ = reward received $k+1$ steps after time $t$
> - $\gamma \in [0, 1)$ = discount factor

---

## 3. Multi-Armed Bandit

### 3.1 Action Value Estimate

$
Q_t(a) = \frac{\text{Sum of rewards when } a \text{ was chosen}}{\text{Number of times } a \text{ was chosen}} = \frac{\sum_{i=1}^{t} \mathbf{1}_{(a_i = a)} \cdot R_i}{\sum_{i=1}^{t} \mathbf{1}_{(a_i = a)}}
$

> **Where:**
> - $Q_t(a)$ = estimated value of action $a$ at time $t$
> - $\mathbf{1}_{(a_i = a)}$ = indicator function; equals 1 if action $a$ was chosen at step $i$, 0 otherwise
> - $R_i$ = reward received at step $i$

### 3.2 MAB Objective

$
\text{Maximize } \; E\left[\sum_{t=1}^{T} R_t\right]
$

> **Where:**
> - $R_t$ = reward at time $t$
> - $T$ = total number of time steps (horizon)

### 3.3 Greedy Action Selection

$
a_t = \arg\max_a \; Q_t(a)
$

Pure exploitation -- always selects the arm with the highest current estimate.

### 3.4 Epsilon-Greedy Action Selection

$
a_t = \begin{cases} \arg\max_a Q_t(a) & \text{with probability } (1 - \epsilon) \\ \text{uniform random from } A & \text{with probability } \epsilon \end{cases}
$

> **Where:**
> - $\epsilon \in (0, 1)$ = exploration rate
> - With probability $(1 - \epsilon)$: **exploit** (choose best-known action)
> - With probability $\epsilon$: **explore** (choose any action uniformly at random)

### 3.5 Intuitive Softmax

$
P(a_t = a) = \frac{Q_t(a)}{\sum_{b=1}^{n} Q_t(b)}
$

> **Where:**
> - Probabilities are directly proportional to estimated values
> - **Problem:** fails when $Q_t(a)$ can be negative (produces invalid probabilities)

### 3.6 Boltzmann (Gibbs) Softmax

$
P(a_t = a) = \frac{e^{Q_t(a) / \beta}}{\sum_{b=1}^{n} e^{Q_t(b) / \beta}}
$

> **Where:**
> - $Q_t(a)$ = estimated value of action $a$ at time $t$
> - $\beta$ = temperature parameter (positive real number)
> - $n$ = total number of arms

| $\beta$ Value | Behaviour | Interpretation |
|---------------|-----------|----------------|
| Very high ($\beta \to \infty$) | All actions get approximately equal probability | Maximum exploration (uniform / random) |
| Very low ($\beta \to 0^+$) | Best action gets probability approaching 1 | Maximum exploitation (greedy) |
| Moderate $\beta$ | Probabilities weighted by $Q_t$ values with spread | Balanced exploration-exploitation |

### 3.7 UCB -- Upper Confidence Bound

$
A_t = \arg\max_a \left( Q_t(a) + c \sqrt{\frac{2 \ln n}{N_t(a)}} \right)
$

> **Where:**
> - $Q_t(a)$ = estimated value of action $a$ at time $t$
> - $c$ = exploration constant
> - $n$ = total number of time steps so far
> - $N_t(a)$ = number of times action $a$ has been selected
> - $c \sqrt{\frac{2 \ln n}{N_t(a)}}$ = exploration bonus (upper confidence bound)

---

## 4. Regret

### 4.1 Instantaneous Regret

$
l_t = E\big[V^* - Q(A_t)\big]
$

> **Where:**
> - $l_t$ = expected regret at step $t$
> - $V^* = \max_a Q(a)$ = value of the optimal action
> - $Q(A_t)$ = value of the action actually chosen at time $t$

### 4.2 Total Regret

$
L_T = \sum_{t=1}^{T} l_t = \sum_{t=1}^{T} E\big[V^* - Q(A_t)\big]
$

> **Where:**
> - $L_T$ = cumulative regret over $T$ time steps
> - Minimising total regret is equivalent to maximising expected cumulative reward

### 4.3 Fundamental Lower Bound

Regret cannot diminish faster than $\log(T)$. Every bandit algorithm must incur at least logarithmic regret.

---

## 5. PAC Optimality

### 5.1 PAC Guarantee

$
P\big(q^*(a) > q^*(a^*) - \epsilon\big) \geq (1 - \delta)
$

> **Where:**
> - $\epsilon$ = accuracy parameter (how close to optimal)
> - $\delta$ = confidence parameter (probability of failure)
> - $q^*(a)$ = true value of the returned arm $a$
> - $q^*(a^*)$ = true value of the best arm
> - An algorithm is $(\epsilon, \delta)$-PAC if it satisfies this inequality

### 5.2 Epsilon-Optimal Policy

$
V^\pi(s) \geq V^*(s) - \epsilon \quad \text{for all states } s
$

> **Where:**
> - $V^\pi(s)$ = value of state $s$ under policy $\pi$
> - $V^*(s)$ = optimal value of state $s$
> - A policy is $\epsilon$-optimal if it is within $\epsilon$ of optimal at every state

### 5.3 Non-Epsilon-Optimal Step

$
V^{\pi_t}(s_t) < V^*(s_t) - \epsilon
$

> **Where:**
> - $\pi_t$ = the policy used at time $t$
> - $s_t$ = the state visited at time $t$
> - A step is non-$\epsilon$-optimal if the policy's value falls more than $\epsilon$ below optimal at the current state

### 5.4 PAC Sample Complexity Bound

$
N = O\left(\frac{|S||A|}{\epsilon^2 (1 - \gamma)^3} \cdot \log\frac{|S||A|}{\delta}\right)
$

> **Where (interpretation -- important per slides):**
> - $\epsilon$ = **accuracy** -- smaller $\epsilon$ means more iterations needed
> - $\delta$ = **confidence** -- smaller $\delta$ means more iterations needed
> - $|S||A|$ = **problem size** -- number of states times number of actions
> - $(1 - \gamma)$ = **planning horizon** -- as $\gamma \to 1$, required iterations increase sharply
> - $N$ = PAC bound on the number of non-$\epsilon$-optimal steps

---

## 6. Fixed Point

### 6.1 Fixed Point Definition

$
f(x^*) = x^*
$

> **Where:**
> - $x^*$ = the fixed point of function $f$
> - Applying $f$ to $x^*$ returns $x^*$ unchanged

### 6.2 Iterative Solution

$
x^* = \lim_{n \to \infty} f^n(x_0)
$

> **Where:**
> - $f^n$ = $f$ applied $n$ times (function composition, not exponentiation)
> - $x_0$ = any starting guess
> - Convergence is guaranteed when $f$ is a contraction on a complete metric space

### 6.3 Conversion to Root Finding

$
g(x) = f(x) - x = 0
$

> **Where:**
> - $f(x^*) = x^*$ is equivalent to $g(x^*) = 0$
> - The two formulations are mathematically interchangeable

---

## 7. Metric Space Properties

A metric space $(X, d)$ requires the distance function $d$ to satisfy all four properties:

| # | Property | Statement | Intuition |
|---|----------|-----------|-----------|
| 1 | Identity of indiscernibles | $d(x, x) = 0$ | Distance from any point to itself is zero |
| 2 | Non-negativity (positivity) | $d(x, y) > 0$ for $x \neq y$ | Distinct points always have positive distance |
| 3 | Symmetry | $d(x, y) = d(y, x)$ | Distance from A to B equals distance from B to A |
| 4 | Triangle inequality | $d(x, z) \leq d(x, y) + d(y, z)$ | A direct path is never longer than a detour |

---

## 8. Cauchy Sequence

### 8.1 Definition

$
d(x_a, x_b) < \varepsilon \quad \text{for all } a, b > N
$

> **Where:**
> - $(x_1, x_2, \ldots)$ = a sequence of elements in metric space $(X, d)$
> - $\varepsilon > 0$ = any tolerance (no matter how small)
> - $N$ = a cutoff index that exists for every choice of $\varepsilon$
> - Beyond index $N$, every pair of terms is within $\varepsilon$ of each other

### 8.2 Complete Metric Space

> **Definition.** A metric space $(X, d)$ is **complete** if every Cauchy sequence of elements in $X$ converges to a limit that is also an element of $X$.

| Space | Complete? | Reason |
|-------|:---------:|--------|
| $\mathbb{R}$ (real numbers) | Yes | No "holes" -- every Cauchy sequence of reals converges to a real |
| $\mathbb{Q}$ (rationals) | No | Cauchy sequences can converge to irrationals (e.g., $\sqrt{2}$) which are not in $\mathbb{Q}$ |
| $\mathbb{R}^{|S|}$ with $\|\cdot\|_\infty$ | Yes | The metric space used for Bellman operator analysis |

---

## 9. Contraction Mapping

### 9.1 Contraction Condition

$
d\big(f(x_1),\; f(x_2)\big) \leq \gamma \cdot d(x_1, x_2) \quad \text{for all } x_1, x_2 \in X, \quad \gamma \in [0, 1)
$

> **Where:**
> - $\gamma$ = contraction constant (Lipschitz constant); must be strictly less than 1
> - The function "shrinks" distances between any two points by at least a factor of $\gamma$

### 9.2 Key Distinctions

| $\gamma$ Value | Classification |
|:--------------:|----------------|
| $\gamma \in [0, 1)$ | **Contraction mapping** -- distances strictly shrink |
| $\gamma = 1$ | **Short mapping** (non-expansive) -- distances do not increase, but not a contraction |
| $\gamma > 1$ | **Expansive mapping** -- distances grow |

### 9.3 Derivative Test for Differentiable Functions

$
\text{If } |f'(x)| \leq k < 1 \text{ for all } x \in X, \text{ then } f \text{ is a contraction with constant } k
$

> **Where:**
> - $f'(x)$ = derivative of $f$ at $x$
> - $k$ = the supremum of $|f'(x)|$ over the domain
> - This provides a practical method to verify the contraction property and find the constant

---

## 10. Banach Fixed Point Theorem (BFPT)

### 10.1 Statement

> **Banach Fixed Point Theorem.**
> If $(X, d)$ is a **complete metric space** and $f: X \to X$ is a **contraction mapping** (with constant $\gamma \in [0, 1)$), then:
>
> 1. $f$ has a **unique** fixed point $x^*$ such that $f(x^*) = x^*$
> 2. For any starting point $x_0 \in X$, the iterative sequence $f^n(x_0) \to x^*$ as $n \to \infty$

### 10.2 Convergence Bound

$
d(x_m, x_n) \leq \frac{\gamma^n}{1 - \gamma} \cdot d\big(f(x_0), x_0\big)
$

> **Where:**
> - $x_m, x_n$ = iterates at steps $m$ and $n$ (with $m > n$)
> - $\gamma$ = contraction constant
> - $x_0$ = initial starting point
> - $d(f(x_0), x_0)$ = distance moved in the very first iteration
> - The bound decreases exponentially with $n$ since $\gamma < 1$

### 10.3 Prerequisites Checklist for Applying BFPT

| Requirement | What to Verify |
|-------------|----------------|
| Complete metric space | Identify $(X, d)$ and confirm completeness |
| $f$ maps $X$ to $X$ | Confirm the function's range is within its domain |
| $f$ is a contraction | Show $d(f(x_1), f(x_2)) \leq \gamma \cdot d(x_1, x_2)$ with $\gamma < 1$ |

---

## 11. Bellman Equations

### 11.1 Bellman Optimality Operator

$
BV(s) = \max_{a} \left[ R_s^a + \gamma \sum_{s' \in S} P_{ss'}^a \, V(s') \right]
$

> **Where:**
> - $B$ = Bellman optimality operator
> - $V(s)$ = value function evaluated at state $s$
> - $R_s^a$ = expected immediate reward for action $a$ in state $s$
> - $\gamma$ = discount factor
> - $P_{ss'}^a$ = probability of transitioning from $s$ to $s'$ under action $a$
> - $\sum_{s'} P_{ss'}^a = 1$ for all $s, a$ (probabilities sum to 1)

### 11.2 Bellman Expectation Operator

$
T^\pi V(s) = \sum_{a} \pi(a \mid s) \left[ R_s^a + \gamma \sum_{s'} P_{ss'}^a \, V(s') \right]
$

> **Where:**
> - $T^\pi$ = Bellman expectation operator under policy $\pi$
> - $\pi(a \mid s)$ = probability of taking action $a$ in state $s$ under policy $\pi$
> - This operator averages over actions according to the policy (unlike the optimality operator which takes the max)

### 11.3 Metric Space for Bellman Analysis

| Component | Specification |
|-----------|---------------|
| Set $X$ | $\mathbb{R}^{|S|}$ (vectors of real numbers, one per state) |
| Metric $d$ | $d(V_1, V_2) = \|V_1 - V_2\|_\infty = \max_{s \in S} |V_1(s) - V_2(s)|$ |
| Complete? | Yes -- $\mathbb{R}^{|S|}$ with the infinity norm is a complete metric space |

### 11.4 Bellman Contraction

$
\|BV_1 - BV_2\|_\infty \leq \gamma \cdot \|V_1 - V_2\|_\infty
$

> **Where:**
> - The Bellman operator $B$ is a contraction with constant $\gamma$ (the discount factor)
> - Since $\gamma < 1$ and the space is complete, BFPT guarantees a unique fixed point $V^*$ such that $BV^* = V^*$
> - Value iteration converges to $V^*$ from any initial $V_0$

---

## 12. Sign Conventions and Parameter Reference

| Symbol | Name | Range | Effect |
|--------|------|-------|--------|
| $\gamma$ | Discount factor | $[0, 1)$ | Closer to 1 = long-sighted (values future rewards); closer to 0 = short-sighted (values immediate rewards) |
| $\alpha$ | Learning rate | $(0, 1]$ | Step size for TD updates; larger = faster but noisier updates |
| $\beta$ | Temperature | $(0, \infty)$ | Higher = more exploration (uniform); lower = more exploitation (greedy) |
| $\epsilon$ | Exploration rate | $(0, 1)$ | Higher = more exploration in epsilon-greedy |

### Key Constraints to Remember

- Transition probabilities always sum to 1: $\sum_{s'} P_{ss'}^a = 1$ for all $s, a$
- Discount factor must be strictly less than 1 for contraction: $\gamma < 1$
- Probabilities from softmax always sum to 1: $\sum_{a} P(a_t = a) = 1$

---

## 13. Pre-Submission Checklist

Use this checklist before submitting any exam answer that involves these formulas.

- [ ] Check units and dimensions in all calculations
- [ ] Verify $\gamma < 1$ when claiming contraction
- [ ] When computing the L-infinity norm, take the **maximum** of **absolute** differences
- [ ] In softmax, ensure the denominator sums over **all** arms (not just a subset)
- [ ] For contraction proof, show $|f'(x)| < 1$ for all $x$ in the domain, or use the definition directly
- [ ] When comparing policies, check **all** states, not just some
- [ ] In iterative convergence, show the sequence approaching the fixed point (not just one step)
- [ ] In PAC bounds, confirm the roles of $\epsilon$ (accuracy) and $\delta$ (confidence) are not swapped
- [ ] When writing the Bellman operator, include **both** the immediate reward $R_s^a$ **and** the discounted future $\gamma \sum P_{ss'}^a V(s')$
- [ ] For regret calculations, remember $l_t = E[V^* - Q(A_t)]$ uses the **true** values, not estimates

---

## Quick-Reference Index

| Formula | Section | Exam Frequency |
|---------|:-------:|:--------------:|
| Boltzmann Softmax | 1.1, 3.6 | **2/2** |
| Contraction Mapping Condition | 1.2, 9.1 | **2/2** |
| Bellman Optimality Operator | 1.3, 11.1 | **2/2** |
| L-infinity Norm | 1.4, 11.3 | **2/2** |
| Policy Comparison | 1.5 | **2/2** |
| Bellman Contraction Result | 1.6, 11.4 | **2/2** |
| Action Value Estimate $Q_t(a)$ | 3.1 | **2/2** |
| Epsilon-Greedy | 3.4 | 1/2 |
| Total Regret | 4.2 | 1/2 |
| PAC Guarantee | 5.1 | 1/2 |
| PAC Sample Complexity | 5.4 | 1/2 |
| BFPT Statement | 10.1 | **2/2** |
| Banach Convergence Bound | 10.2 | 1/2 |
| Bellman Expectation Operator $T^\pi$ | 11.2 | 1/2 |
| UCB | 3.7 | 1/2 |
