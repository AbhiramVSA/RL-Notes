# 03 -- The Multi-Armed Bandit Problem

**Module**: 1 (slides 27--48) | **Priority**: P1 | **Exam Weight**: HIGH -- appears in both past papers

---

## Learning Objectives

After studying this section, you should be able to:

- Define the multi-armed bandit problem and its formal mathematical specification
- Distinguish between asymptotic correctness, regret optimality, and PAC optimality as criteria for solving bandit problems
- Explain the greedy action selection method and its limitations
- Explain epsilon-greedy action selection and its limitations
- Derive the Boltzmann (Gibbs) softmax formula from the intuitive softmax formula
- Compute action-selection probabilities using the Boltzmann softmax formula given a data table of iterations, actions, and rewards
- Analyze the effect of the temperature parameter beta on exploration vs. exploitation
- Describe the UCB approach at a high level and contrast it with PAC optimality

---

## Ground-Up Explanation

### 2.1 What Is the Bandit Problem?

The word **bandit** refers to a slot machine in a casino. A single slot machine has one lever (one arm) you pull to gamble -- this is a **one-armed bandit**. The name comes from the idea that the machine "robs" you of your money over time.

Now imagine you are standing in front of a row of slot machines, each with its own lever. Each machine pays out according to its own hidden probability distribution -- some are generous, some are stingy, and you do not know which is which. The **Multi-Armed Bandit (MAB)** problem is the name for this scenario. "Multi-Armed" is a playful way of saying "Many One-Armed Bandits."

Your **goal** is to figure out which arm (action) gives you the maximum payback. In formal notation, you want to find $q^*(a^*)$ -- the true value of the best action.

The core tension is the **exploration-exploitation trade-off**: should you keep pulling the arm that has given you the best payoff so far (exploit), or should you try other arms to see if they might be even better (explore)?

### 2.2 Formal Definition

A multi-armed bandit (MAB) comprises:

1. **A finite set of Actions** $A$ (also called **arms**).
2. Each action $a \in A$ is associated with a **probability distribution** $R^a$ over the real numbers $\mathbb{R}$, **unknown to the agent**, defined as:

$
R^a(r) = P(r \mid a) \quad \text{for all } r \in \mathbb{R}
$

3. A time-indexed sequence of **agent-selected actions** $A_t \in A$ for time steps $t = 1, 2, 3, \ldots$ and a time-indexed sequence of **environment-generated rewards** $R_t \in \mathbb{R}$ for time steps $t = 1, 2, 3, \ldots$ with $R_t$ randomly drawn from the distribution $R^{A_t}$.

4. The **goal** of the agent is to maximize the expected cumulative reward:

> **CRITICAL EQUATION -- MAB Objective**
>
> $
> \text{Maximize } \; E\left[\sum_{t=1}^{T} R_t\right]
> $

> **Where:**
> - $A$ = finite set of available actions (arms)
> - $R^a$ = unknown reward distribution for arm $a$
> - $A_t$ = action selected by the agent at time $t$
> - $R_t$ = reward received at time $t$, drawn from $R^{A_t}$
> - $T$ = total number of time steps (horizon)

**Key observation:** The agent does not know the reward distributions $R^a$. It must learn about them through interaction -- by pulling arms and observing the rewards it receives.

### 2.3 Notions for Solving the Bandit Problem

The slides present three theoretical criteria for evaluating bandit-solving algorithms, plus practical methods. The three criteria are:

#### 2.3.1 Asymptotic Correctness -- The Problem of Correctness

As the number of time steps $t \to \infty$, the algorithm **guarantees** that the arm with the highest pay-off is eventually selected. In other words, the estimated action value $q^*(a)$ computed by the algorithm ultimately converges to $q^*(a^*)$, the value of the truly best arm.

Convergence is of **high priority** in this notion. The concern is not about how fast you get there, but whether you will get there at all given infinite time.

#### 2.3.2 Regret Optimality -- The Problem of Convergence

This notion quantifies the **cost of learning**. While the agent is exploring (trying different arms to learn their values), it is not always picking the best arm. The loss incurred during this learning period is called **regret**.

Define the following quantities:

- **Action value**: $Q(a) = E[r \mid a]$ -- the expected reward from arm $a$.
- **Optimal value**: $V^* = \max_a Q(a) = Q(a^*)$ -- the expected reward from the best arm.
- **Instantaneous regret**: $l_t = E[V^* - Q(A_t)]$ -- the expected gap between the optimal arm and the arm actually chosen at time $t$.
- **Total regret** over $T$ time steps:

> **CRITICAL EQUATION -- Total Regret**
>
> $
> L_T = \sum_{t=1}^{T} l_t
> $

**Key insight:** Minimizing total regret is equivalent to maximizing expected cumulative rewards. The two objectives are two sides of the same coin.

**Fundamental lower bound:** No algorithm can make regret diminish faster than $\log(T)$. This means every algorithm must incur at least logarithmic regret -- you cannot avoid the cost of learning entirely.

Regret-optimal solutions exploit more aggressively to achieve steeper reduction in the regret curve.

#### 2.3.3 PAC Optimality / Complexity -- The Problem of Sample Complexity

**PAC** stands for **Probably Approximately Correct**. The idea is: it is highly probable that the arm $a$ returned by the algorithm gives a value $q^*(a)$ that is approximately close to the true optimum $q^*(a^*)$.

Formally, an algorithm is $(\epsilon, \delta)$-PAC if:

> **CRITICAL EQUATION -- PAC Guarantee**
>
> $
> P\big(q^*(a) > q^*(a^*) - \epsilon\big) \geq (1 - \delta)
> $

Given any number of arms, the optimality guarantee holds if the number of samples drawn is large enough. The natural question is: given $(\epsilon, \delta)$, what is the **smallest number of samples** needed to guarantee PAC?

The answer is the **sample complexity** bound:

$
N = O\left(\frac{|S||A|}{\epsilon^2 (1 - \gamma)^3} \cdot \log\frac{|S||A|}{\delta}\right)
$

> **Where (interpretation -- important per slides):**
> - $\epsilon$ = **accuracy** -- how close to optimal we require (smaller $\epsilon$ means more iterations needed)
> - $\delta$ = **confidence** -- how sure we want to be (smaller $\delta$ means more iterations needed)
> - $|S||A|$ = **problem size** -- number of states times number of actions
> - $(1 - \gamma)$ = **planning horizon** -- as $\gamma \to 1$, required iterations increase sharply
> - $N$ = PAC bound on the number of non-$\epsilon$-optimal steps

**Summary of the three notions (from slide 48):**

| Notion | Concerned With |
|--------|---------------|
| Asymptotic correctness | Correctness -- will we find the best arm? |
| Regret optimality | Convergence -- how much do we lose while learning? |
| PAC optimality | Sample complexity -- how many samples do we need? |

### 2.4 Value Function Based Methods

In these methods, the true action value $q^*$ is unknown, so we form an **estimate** called $Q_t$.

#### 2.4.1 Greedy Action Selection

We estimate the value of each action by averaging the rewards received whenever that action was chosen:

$
Q_t(a) = \frac{\text{Sum of rewards received when } a \text{ was chosen}}{\text{Number of times } a \text{ was chosen}} = \frac{\sum_{i=1}^{t} \mathbf{1}_{(a_i = a)} \cdot R_i}{\sum_{i=1}^{t} \mathbf{1}_{(a_i = a)}}
$

> **Where:**
> - $Q_t(a)$ = estimated value of action $a$ at time $t$
> - $\mathbf{1}_{(a_i = a)}$ = indicator function, equals 1 if action $a$ was chosen at step $i$, 0 otherwise
> - $R_i$ = reward received at step $i$

The greedy rule then selects the action with the highest estimated value:

$
a_t = \arg\max_a \; Q_t(a) \quad \text{(pure exploitation)}
$

**Problem:** The greedy method is **purely exploitative**. It never explores. Once it finds an arm that looks good early on, it keeps pulling that arm forever and never discovers potentially better arms. Being exploitative will always lead to non-exploration of the best states.

#### 2.4.2 Epsilon-Greedy Action Selection

Epsilon-greedy adds a small amount of forced exploration:

> **CRITICAL EQUATION -- Epsilon-Greedy Rule**
>
> $
> a_t = \begin{cases} \arg\max_a Q_t(a) & \text{with probability } (1 - \epsilon) \\ \text{uniform random from } A & \text{with probability } \epsilon \end{cases}
> $

> **Where:**
> - $\epsilon \in (0, 1)$ = exploration rate
> - With probability $(1 - \epsilon)$: exploit (choose the best-known action)
> - With probability $\epsilon$: explore (choose any action uniformly at random)

**Limitations of epsilon-greedy (from slides):**

1. **Does not address the problem of unwanted states** -- exploration is random and undirected, so the agent may waste time on clearly bad arms.
2. **The greedy part selects based on the minutest differences** -- even if two arms have nearly identical estimated values (say 2.001 vs. 2.000), the greedy part always picks the one with the slightly higher estimate. This makes the method sensitive to noise.

### 2.5 Softmax Action Selection

Softmax addresses the limitations of epsilon-greedy by making the selection probability **proportional to the estimated value** of each arm.

#### 2.5.1 Intuitive Softmax

The simplest idea is to set each action's selection probability proportional to its estimated value:

$
P(a_t = a) = \frac{Q_t(a)}{\sum_{b=1}^{n} Q_t(b)}
$

**Problem:** Rewards can be negative (different signs / weightages in the rewarding process). If $Q_t(a)$ is negative, this formula produces negative probabilities, which are not valid. Probabilities must lie in $[0, 1]$.

#### 2.5.2 Boltzmann / Gibbs Softmax

To fix the negativity problem, we exponentiate the estimates. The exponential function $e^x$ is always positive for any real $x$:

> **CRITICAL EQUATION -- Boltzmann Softmax**
>
> $
> P(a_t = a) = \frac{e^{Q_t(a) / \beta}}{\sum_{b=1}^{n} e^{Q_t(b) / \beta}}
> $

> **Where:**
> - $P(a_t = a)$ = probability of selecting action $a$ at time $t$
> - $Q_t(a)$ = estimated value of action $a$ (average reward so far)
> - $\beta$ = **temperature parameter** (positive real number)
> - $n$ = total number of arms (actions)

**The temperature parameter $\beta$ controls the exploration-exploitation balance:**

| $\beta$ Value | Behavior | Interpretation |
|---------------|----------|----------------|
| Very high ($\beta \to \infty$) | All actions get approximately **equal probability** | Maximum exploration (random) |
| Very low ($\beta \to 0^+$) | The action with the highest $Q_t$ gets probability approaching 1 | Maximum exploitation (greedy) |
| Moderate $\beta$ | Probabilities are weighted by $Q_t$ values with some spread | Balanced exploration-exploitation |

**Why this works:** When $\beta$ is very large, $Q_t(a)/\beta \approx 0$ for all $a$, so $e^{Q_t(a)/\beta} \approx 1$ for all arms, giving uniform probabilities. When $\beta$ is very small, $Q_t(a)/\beta$ becomes very large for the best arm and very negative for worse arms, so the exponential concentrates all probability on the best arm.

**Cooling:** Since the method explores with probability related to $\beta$, there is a possibility that the solution oscillates around $q^*$. To avoid this, we can "cool" the exploration (reduce $\beta$ over time, analogous to cooling $\epsilon$ proportional to $1/t$). However, cooling takes a longer period for convergence -- a balance is needed.

### 2.6 UCB -- Upper Confidence Bound

**UCB (Upper Confidence Bound)** is another approach for solving the bandit problem. It uses the **uncertainty** in the action-value estimates to drive exploration.

The UCB action selection rule is:

$
A_t = \arg\max_a \left( Q_t(a) + c \sqrt{\frac{2 \ln n}{N_t(a)}} \right)
$

> **Where:**
> - $Q_t(a)$ = estimated value of action $a$ at time $t$
> - $c$ = exploration constant
> - $n$ = total number of time steps so far
> - $N_t(a)$ = number of times action $a$ has been selected
> - The square root term is the **exploration bonus** (upper confidence bound)

**Algorithm:**
1. Play each arm at least once.
2. Then, in a loop: play the arm $A_t$ that maximizes the sum of the estimated value plus the confidence bound.

**How UCB works:**
- If an arm has been played many times, $N_t(a)$ is large, so the exploration bonus is small -- we are confident in our estimate.
- If an arm has been played few times, $N_t(a)$ is small, so the exploration bonus is large -- we are uncertain and should explore it.
- UCB explores more to systematically reduce uncertainty, but its exploration reduces over time as all arms get sampled.

---

## Analogies

**The Casino Floor Analogy:** Imagine you walk into a casino with a row of 5 slot machines. You have a fixed budget of 100 tokens. Each machine has a different (hidden) payout rate. The greedy strategy is like finding a machine that pays out on your first try and then playing it exclusively for all 100 tokens -- you might miss the jackpot machine two spots over. Epsilon-greedy is like mostly playing your favourite machine but randomly trying a different one every 10th token. Softmax is like adjusting how often you try each machine based on how well it has paid so far -- you still try the low-paying machines occasionally, but you spend more tokens on the ones that look promising. UCB is like a careful gambler who specifically seeks out machines they have not tried much, reasoning: "I do not know enough about that machine, so it might be great."

**Temperature Analogy for $\beta$:** Think of $\beta$ as the "temperature" of a gas. At high temperature, molecules bounce around randomly (exploration -- all actions are equally likely). At low temperature, molecules settle into the lowest energy state (exploitation -- the best action dominates). This is exactly the analogy from statistical mechanics that gives the Boltzmann distribution its name.

---

## Key Formulas

### MAB Objective

$
\text{Maximize } \; E\left[\sum_{t=1}^{T} R_t\right]
$

> **Where:** $R_t$ = reward at time $t$, $T$ = horizon length.

### Reward Distribution

$
R^a(r) = P(r \mid a) \quad \text{for all } r \in \mathbb{R}
$

### Action Value Estimate

$
Q_t(a) = \frac{\sum_{i=1}^{t} \mathbf{1}_{(a_i = a)} \cdot R_i}{\sum_{i=1}^{t} \mathbf{1}_{(a_i = a)}}
$

> **Where:** numerator = total reward from arm $a$; denominator = count of times arm $a$ was pulled.

### Greedy Selection

$
a_t = \arg\max_a \; Q_t(a)
$

### Epsilon-Greedy Selection

$
a_t = \begin{cases} \arg\max_a Q_t(a) & \text{with probability } (1 - \epsilon) \\ \text{uniform random from } A & \text{with probability } \epsilon \end{cases}
$

### Intuitive Softmax

$
P(a_t = a) = \frac{Q_t(a)}{\sum_{b=1}^{n} Q_t(b)}
$

### Boltzmann / Gibbs Softmax

$
P(a_t = a) = \frac{e^{Q_t(a) / \beta}}{\sum_{b=1}^{n} e^{Q_t(b) / \beta}}
$

> **Where:** $\beta$ = temperature parameter. High $\beta$ = exploration (uniform). Low $\beta$ = exploitation (greedy).

### Regret

$
l_t = E[V^* - Q(A_t)] \qquad L_T = \sum_{t=1}^{T} l_t
$

> **Where:** $V^* = \max_a Q(a)$, $l_t$ = instantaneous regret, $L_T$ = total regret.

### PAC Guarantee

$
P\big(q^*(a) > q^*(a^*) - \epsilon\big) \geq (1 - \delta)
$

### PAC Sample Complexity

$
N = O\left(\frac{|S||A|}{\epsilon^2 (1 - \gamma)^3} \cdot \log\frac{|S||A|}{\delta}\right)
$

### UCB Action Selection

$
A_t = \arg\max_a \left( Q_t(a) + c \sqrt{\frac{2 \ln n}{N_t(a)}} \right)
$

---

## Derivations

### How Greedy Leads to Epsilon-Greedy Leads to Softmax

This progression represents increasingly sophisticated approaches to the exploration-exploitation trade-off.

**Step 1: Greedy -- Pure Exploitation**

Start with the simplest idea: always pick the arm with the highest estimated value.

$
a_t = \arg\max_a \; Q_t(a)
$

Problem: This never explores. If arm 2 happened to give a high reward on its first pull purely by chance, the greedy agent locks onto arm 2 forever, even if arm 3 is actually better on average.

**Step 2: Epsilon-Greedy -- Adding Random Exploration**

Fix the "never explores" problem by forcing exploration with probability $\epsilon$:

$
P(a_t = a) = \begin{cases} (1 - \epsilon) + \frac{\epsilon}{|A|} & \text{if } a = \arg\max_a Q_t(a) \\ \frac{\epsilon}{|A|} & \text{otherwise} \end{cases}
$

Now every arm has at least a $\frac{\epsilon}{|A|}$ chance of being selected. When $\epsilon = 0$, this reduces to pure greedy.

Problem: Exploration is **undirected**. An arm with $Q_t = 0.1$ gets the same exploration probability as an arm with $Q_t = 4.9$. Also, the greedy part selects based on the minutest differences.

**Step 3: Intuitive Softmax -- Proportional Exploration**

Make exploration smarter by making selection probability proportional to estimated value:

$
P(a_t = a) = \frac{Q_t(a)}{\sum_{b=1}^{n} Q_t(b)}
$

Now better arms get explored more. This assigns zero probability to unwanted states (arms with $Q_t = 0$).

Problem: If $Q_t(a)$ is negative for any arm, we get negative probabilities. Probabilities must be non-negative.

**Step 4: Boltzmann Softmax -- Fixing Negativity with Exponentiation**

Apply the exponential function to guarantee all values are positive, and introduce a temperature parameter $\beta$ to control the sharpness of the distribution:

$
P(a_t = a) = \frac{e^{Q_t(a) / \beta}}{\sum_{b=1}^{n} e^{Q_t(b) / \beta}}
$

Since $e^x > 0$ for all real $x$, every probability is guaranteed to be positive. The denominator normalizes the probabilities to sum to 1. The parameter $\beta$ gives a tunable knob between exploration and exploitation.

This is the final form used in practice and asked about in exams.

---

## Worked Examples

### Example 1: Softmax Probability Calculation from a Data Table (Exam Style)

This example mirrors the exact format of the 10-mark questions from both past papers.

**Problem:** A multi-armed bandit problem has 3 arms (A, B, C). The following data table shows 15 iterations of interaction:

| Iteration | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|-----------|---|---|---|---|---|---|---|---|---|----|----|----|----|----|----|
| Action    | A | C | B | A | C | B | C | A | B | C  | A  | B  | B  | C  | C  |
| Reward    | 4 | 2 | 5 | 3 | 1 | 4 | -5 | 2 | 3 | -5 | -2 | -3 | 2 | 4 | 4 |

(a) Apply the Boltzmann softmax formula to calculate the probability of selecting each arm for the 16th iteration.

(b) Compare how the choice of $\beta = 5$ and $\beta = 100$ affects exploration and exploitation across the 15 iterations.

---

**Solution Part (a): Computing $Q_t(a)$ for each arm after 15 iterations**

**Step 1: Identify which iterations belong to each arm and their rewards.**

**Arm A:** Pulled at iterations 1, 4, 8, 11.

| Iteration | Reward |
|-----------|--------|
| 1 | 4 |
| 4 | 3 |
| 8 | 2 |
| 11 | -2 |

Count of pulls: $N(A) = 4$

Sum of rewards: $4 + 3 + 2 + (-2) = 7$

$
Q_{15}(A) = \frac{7}{4} = 1.75
$

**Arm B:** Pulled at iterations 3, 6, 9, 12, 13.

| Iteration | Reward |
|-----------|--------|
| 3 | 5 |
| 6 | 4 |
| 9 | 3 |
| 12 | -3 |
| 13 | 2 |

Count of pulls: $N(B) = 5$

Sum of rewards: $5 + 4 + 3 + (-3) + 2 = 11$

$
Q_{15}(B) = \frac{11}{5} = 2.2
$

**Arm C:** Pulled at iterations 2, 5, 7, 10, 14, 15.

| Iteration | Reward |
|-----------|--------|
| 2 | 2 |
| 5 | 1 |
| 7 | -5 |
| 10 | -5 |
| 14 | 4 |
| 15 | 4 |

Count of pulls: $N(C) = 6$

Sum of rewards: $2 + 1 + (-5) + (-5) + 4 + 4 = 1$

$
Q_{15}(C) = \frac{1}{6} \approx 0.1667
$

**Summary of action values:**

| Arm | Times Pulled | Total Reward | $Q_{15}$ |
|-----|-------------|-------------|----------|
| A | 4 | 7 | 1.75 |
| B | 5 | 11 | 2.2 |
| C | 6 | 1 | 0.1667 |

**Step 2: Apply the Boltzmann softmax formula with $\beta = 5$.**

$
P(a_t = a) = \frac{e^{Q_t(a)/\beta}}{\sum_{b \in \{A,B,C\}} e^{Q_t(b)/\beta}}
$

Compute the exponents:

$
\frac{Q_{15}(A)}{\beta} = \frac{1.75}{5} = 0.35 \qquad \Rightarrow \qquad e^{0.35} = 1.4191
$

$
\frac{Q_{15}(B)}{\beta} = \frac{2.2}{5} = 0.44 \qquad \Rightarrow \qquad e^{0.44} = 1.5527
$

$
\frac{Q_{15}(C)}{\beta} = \frac{0.1667}{5} = 0.03333 \qquad \Rightarrow \qquad e^{0.03333} = 1.0339
$

Compute the denominator (normalizing constant):

$
Z = e^{0.35} + e^{0.44} + e^{0.03333} = 1.4191 + 1.5527 + 1.0339 = 4.0057
$

Compute each probability:

$
P(A) = \frac{1.4191}{4.0057} = 0.3543 \approx 35.43\%
$

$
P(B) = \frac{1.5527}{4.0057} = 0.3876 \approx 38.76\%
$

$
P(C) = \frac{1.0339}{4.0057} = 0.2581 \approx 25.81\%
$

**Verification:** $0.3543 + 0.3876 + 0.2581 = 1.0000$ (probabilities sum to 1).

> **Answer ($\beta = 5$):**
>
> | Arm | $Q_{15}$ | $e^{Q/\beta}$ | $P(\text{arm})$ |
> |-----|----------|----------------|-----------------|
> | A | 1.75 | 1.4191 | 0.3543 (35.4%) |
> | B | 2.2 | 1.5527 | 0.3876 (38.8%) |
> | C | 0.1667 | 1.0339 | 0.2581 (25.8%) |

---

**Solution Part (b): Effect of $\beta = 5$ vs. $\beta = 100$**

We already computed for $\beta = 5$. Now compute for $\beta = 100$:

$
\frac{Q_{15}(A)}{\beta} = \frac{1.75}{100} = 0.0175 \qquad \Rightarrow \qquad e^{0.0175} = 1.01765
$

$
\frac{Q_{15}(B)}{\beta} = \frac{2.2}{100} = 0.022 \qquad \Rightarrow \qquad e^{0.022} = 1.02224
$

$
\frac{Q_{15}(C)}{\beta} = \frac{0.1667}{100} = 0.001667 \qquad \Rightarrow \qquad e^{0.001667} = 1.00167
$

$
Z = 1.01765 + 1.02224 + 1.00167 = 3.04156
$

$
P(A) = \frac{1.01765}{3.04156} = 0.33459 \approx 33.46\%
$

$
P(B) = \frac{1.02224}{3.04156} = 0.33610 \approx 33.61\%
$

$
P(C) = \frac{1.00167}{3.04156} = 0.32932 \approx 32.93\%
$

**Comparison table:**

| Arm | $Q_{15}$ | $P$ at $\beta = 5$ | $P$ at $\beta = 100$ |
|-----|----------|---------------------|----------------------|
| A | 1.75 | 35.43% | 33.46% |
| B | 2.2 | 38.76% | 33.61% |
| C | 0.1667 | 25.81% | 32.93% |

**Discussion:**

- **At $\beta = 100$ (high temperature):** The probabilities are nearly uniform (approximately 33.3% each). Even though arm B has the highest estimated value and arm C has the lowest, they are selected with almost the same probability. This is **maximum exploration** -- the agent treats all arms nearly equally and continues to gather information about all of them. This is useful during the **initial on-boarding phase** when the agent has little data and needs to learn about all arms.

- **At $\beta = 5$ (lower temperature):** The probabilities show clear differentiation. Arm B (highest $Q_t$) gets the most probability (38.8%), arm A gets intermediate probability (35.4%), and arm C (lowest $Q_t$) gets the least (25.8%). This is more **exploitative** -- the agent favors arms that have performed well while still giving some chance to inferior arms.

- **At $\beta \to 0^+$ (very low temperature):** The probabilities would approach $P(B) \to 1$ and $P(A), P(C) \to 0$, becoming **pure greedy** exploitation.

- **Practical recommendation:** Use high $\beta$ early (explore broadly), then decrease $\beta$ over time (exploit what you have learned). This is called "cooling" or "annealing."

---

### Example 2: Verifying the Effect of Extreme Beta Values

Given $Q_t(A) = 3$, $Q_t(B) = 1$, $Q_t(C) = 2$ with 3 arms.

**Case 1: $\beta = 0.1$ (very low -- exploitation)**

$
e^{3/0.1} = e^{30} \approx 1.069 \times 10^{13}
$

$
e^{1/0.1} = e^{10} \approx 2.203 \times 10^{4}
$

$
e^{2/0.1} = e^{20} \approx 4.851 \times 10^{8}
$

$
Z = e^{30} + e^{10} + e^{20} \approx 1.069 \times 10^{13}
$

$
P(A) \approx \frac{1.069 \times 10^{13}}{1.069 \times 10^{13}} \approx 1.0 \qquad P(B) \approx 0 \qquad P(C) \approx 0
$

The best arm (A) gets essentially all the probability. This is greedy behavior.

**Case 2: $\beta = 1000$ (very high -- exploration)**

$
e^{3/1000} = e^{0.003} \approx 1.003 \qquad e^{1/1000} = e^{0.001} \approx 1.001 \qquad e^{2/1000} = e^{0.002} \approx 1.002
$

$
Z = 1.003 + 1.001 + 1.002 = 3.006
$

$
P(A) = \frac{1.003}{3.006} \approx 0.3337 \qquad P(B) \approx 0.3330 \qquad P(C) \approx 0.3334
$

All arms are selected with nearly equal probability (about 33.3%). This is random exploration.

---

## Common Mistakes

- **Sign errors in softmax computation:** When computing $Q_t(a)/\beta$, students sometimes forget to include negative rewards in the sum. A reward of $-5$ must be added (not subtracted again) when computing the total reward. For example, rewards of $4, -5, 2$ sum to $4 + (-5) + 2 = 1$, not $4 - (-5) + 2 = 11$.

- **Forgetting to track per-arm counts:** The denominator of $Q_t(a)$ is the number of times arm $a$ specifically was pulled, NOT the total number of iterations. If arm A was pulled 4 times out of 15 iterations, $N(A) = 4$, not 15.

- **Beta interpretation reversed:** High $\beta$ means **more exploration** (random, uniform probabilities). Low $\beta$ means **more exploitation** (greedy, concentrated on the best arm). Students commonly get this backwards. Memory aid: think of high temperature = hot = molecules bouncing randomly = exploration.

- **Dividing by $\beta$, not multiplying:** The formula is $e^{Q_t(a) / \beta}$ -- you divide $Q_t$ by $\beta$. Some students accidentally write $e^{Q_t(a) \cdot \beta}$, which inverts the effect of $\beta$.

- **Not verifying probabilities sum to 1:** After computing all probabilities, always check they sum to 1.0 (or very close due to rounding). If they do not, there is a calculation error.

- **Confusing the intuitive softmax with Boltzmann softmax:** The exam always asks for the Boltzmann (exponential) version, not the simple ratio version. If you write $P(a) = Q_t(a) / \sum Q_t(b)$ without exponentiation, you will lose marks.

- **Forgetting the $\beta$ in the exponent:** Writing $e^{Q_t(a)}$ instead of $e^{Q_t(a)/\beta}$. The temperature parameter is essential to the formula.

---

## Self-Check Questions

<details>
<summary>Q1: What does the term "multi-armed bandit" literally refer to?</summary>

**Answer:** It refers to multiple slot machines (one-armed bandits) in a casino. Each "arm" is a lever on a slot machine. The "multi-armed" part means there are many machines to choose from, and the agent must figure out which one gives the best payoff.

</details>

<details>
<summary>Q2: Why is the greedy approach insufficient for solving the bandit problem?</summary>

**Answer:** The greedy approach always selects the arm with the highest estimated value and never explores other arms. This means it can get stuck on a suboptimal arm that happened to give a good reward early on by chance, while never discovering the truly best arm. It is purely exploitative with zero exploration.

</details>

<details>
<summary>Q3: What are the two limitations of epsilon-greedy mentioned in the slides?</summary>

**Answer:** (1) It does not address the problem of unwanted states -- exploration is completely random, so it wastes exploration steps on arms that are clearly bad. (2) The greedy part selects based on the minutest differences -- even a tiny, noise-driven gap between two arm estimates causes one to always be preferred over the other during exploitation.

</details>

<details>
<summary>Q4: Why do we use exponentiation in the Boltzmann softmax instead of the simple ratio?</summary>

**Answer:** The simple ratio $P(a) = Q_t(a) / \sum Q_t(b)$ can produce negative probabilities when some $Q_t(a)$ values are negative (due to negative rewards). The exponential function $e^x$ is always positive for any real input, so $e^{Q_t(a)/\beta}$ is always positive, guaranteeing valid probabilities.

</details>

<details>
<summary>Q5: If beta = 0.01, what behavior do you expect from the Boltzmann softmax?</summary>

**Answer:** With $\beta = 0.01$ (very low temperature), the softmax becomes nearly greedy. The arm with the highest $Q_t$ value will get a probability very close to 1, and all other arms will get probabilities very close to 0. This is pure exploitation.

</details>

<details>
<summary>Q6: What is the fundamental lower bound on regret, and what does it mean?</summary>

**Answer:** No algorithm can make regret diminish faster than $\log(T)$, where $T$ is the number of time steps. This means that every learning algorithm must incur some loss due to exploration -- you cannot learn for free. The best you can do is logarithmic total regret.

</details>

<details>
<summary>Q7: In the PAC sample complexity formula, what happens as gamma approaches 1?</summary>

**Answer:** As $\gamma \to 1$, the term $(1 - \gamma)^3$ in the denominator approaches 0, causing the required number of samples $N$ to increase sharply (approach infinity). This reflects the fact that when the planning horizon is very long (high $\gamma$), the agent needs far more samples to achieve the same accuracy guarantee.

</details>

<details>
<summary>Q8: Given Q_t(A) = 3 and Q_t(B) = 3 with beta = 5, what are the softmax probabilities?</summary>

**Answer:** Since $Q_t(A) = Q_t(B)$, we get $e^{3/5} = e^{0.6}$ for both arms. The probabilities are: $P(A) = e^{0.6} / (e^{0.6} + e^{0.6}) = 1/2 = 0.5$ and $P(B) = 0.5$. When two arms have equal estimated values, softmax assigns them equal probabilities regardless of $\beta$.

</details>

<details>
<summary>Q9: How does UCB differ from softmax in its approach to exploration?</summary>

**Answer:** Softmax assigns exploration probability proportional to the estimated action value (better arms get more probability). UCB assigns exploration based on **uncertainty** -- arms that have been sampled fewer times get a larger exploration bonus, regardless of their estimated value. UCB systematically targets the arms it knows least about, while softmax targets the arms it thinks are best.

</details>

<details>
<summary>Q10: What is the relationship between minimizing total regret and maximizing expected cumulative rewards?</summary>

**Answer:** They are equivalent. Total regret $L_T = \sum_{t=1}^{T} E[V^* - Q(A_t)]$. Minimizing this is the same as maximizing $\sum_{t=1}^{T} E[Q(A_t)]$, which is the expected cumulative reward. The difference $V^* \cdot T - L_T$ gives the expected cumulative reward (up to a constant).

</details>

---

## Exam Focus

> **CRITICAL TOPIC: This topic appears in BOTH past papers as a mandatory 10-mark question.**

### How This Topic Has Been Examined

**Paper 1 (Set 2, Session AN) -- Question 2 [10 marks]:**

"How can the Softmax algorithm be applied to solve a multi-armed bandit problem with 3 arms over 15 iterations, using the provided data?"

A data table is given with 15 iterations showing Action (A, B, or C) and Reward for each iteration.

- Part (a) [6 marks]: Apply the Softmax action selection formula to calculate the probability of selecting each arm for the 16th iteration.
- Part (b) [4 marks]: Compare how the choice of $\beta = 5$ and $\beta = 100$ affects exploration and exploitation across the 15 iterations.

**Paper 2 (Set 4, Session FN) -- Question 2 [10 marks, split 6+4]:**

"A music streaming platform wants to recommend one of three raags (Yaman(Y), Bhairav(B), Todi(T)) based playlists to a new user each day in order to maximize listening time. Each playlist corresponds to an arm in a multi-armed bandit problem."

A data table is given with 10 iterations showing Action (Y, B, or T) and Reward (minutes).

- Part (a): Compare how the choice of $\beta = 1$ versus $\beta = 100$ affects the exploration-exploitation trade-off and the selection of playlist on the 11th day.
- Part (b): From a business perspective, explain which value of $\beta$ would be more suitable during the initial on-boarding phase, and after the platform has high confidence in user preferences.

**Paper 2 (Set 4) -- also asks in Question 5b:**

"Discuss the difference between greedy and epsilon-greedy algorithms used in the context of RL."

**Paper 1 (Set 2) -- Question 5a [3 marks]:**

"Compare and contrast PAC optimality and UCB with relevant equations."

### What You Must Be Able to Do

1. **Given a data table of iterations, actions, and rewards**, compute $Q_t(a)$ for each arm by:
   - Identifying which iterations correspond to each arm
   - Summing the rewards for each arm
   - Dividing by the number of times each arm was pulled

2. **Apply the Boltzmann softmax formula** with a given $\beta$ value:
   - Compute $Q_t(a)/\beta$ for each arm
   - Compute $e^{Q_t(a)/\beta}$ for each arm
   - Sum the exponentials (denominator)
   - Divide each exponential by the sum to get probabilities
   - Verify probabilities sum to 1

3. **Repeat with a different $\beta$ value** and compare:
   - Show that high $\beta$ produces nearly uniform probabilities (exploration)
   - Show that low $\beta$ produces concentrated probabilities (exploitation)
   - Recommend which $\beta$ is appropriate for different scenarios (early learning vs. confident exploitation)

4. **Explain the greedy-to-epsilon-greedy-to-softmax progression** and the limitations of each.

5. **Compare PAC optimality and UCB** with their respective equations.

### Likely Exam Variations

- The number of arms may change (3 arms is standard, but 4 or 5 arms are possible)
- The number of iterations may change (10 or 15 iterations are typical)
- Different $\beta$ values may be asked (common pairs: 1 vs. 100, 5 vs. 100, 0.1 vs. 10)
- The data table may include negative rewards -- be prepared to handle them
- An application framing may be added (e.g., music recommendation, ad selection, casino scenario)
- You may be asked to recommend a $\beta$ value for a business scenario

---

## Concept Links

- **Prerequisite**: [Exploration vs. Exploitation Trade-off](./02_elements_of_rl.md) -- the bandit problem is the simplest setting where this trade-off arises
- **Prerequisite**: [Elements of RL -- Policy, Value function](./02_elements_of_rl.md) -- $Q_t(a)$ is an estimate of the action-value function
- **Forward link**: [Bellman Equation and Value Iteration](./06_bellman_and_convergence.md) -- the bandit problem is "immediate RL" (single state); full RL extends this to multiple states using the Bellman equation
- **Formula reference**: [Formula Sheet -- Softmax and Bandit Formulas](./08_formula_sheet.md)
- **Worked problems**: [Worked Problems -- Past Paper Softmax Questions](./07_worked_problems.md)
