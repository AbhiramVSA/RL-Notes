# Worked Problems -- Reinforcement Learning CAT-1

**Purpose:** Complete worked solutions for every past paper question and every source material problem.
**Usage:** Work through these under timed conditions after completing Phases 1--6 of the [Study Roadmap](./00_roadmap.md).

---

## Past Paper Questions

### Paper 1 (Set 2, Session AN, 05/02/2026)

---

#### Paper 1 -- Q1(a): RL Application Modelling -- Self-Driving Car [5 Marks]

> **Question.** A self-driving car aims to navigate safely and makes real-time decisions such as accelerating, braking and changing lanes. Examine whether RL can be used for solving this problem. If yes, explain how RL can be applied including formulation of states, actions, rewards, and policy. If not, justify why another learning method would be more suitable.

**Concepts Used:** [RL Fundamentals -- MDP Terms](./01_rl_fundamentals.md), [RL Fundamentals -- RL Application Modelling](./01_rl_fundamentals.md)

**Formulas Used:** None (conceptual question). Refer to the RL interaction loop in [Formula Sheet](./08_formula_sheet.md).

**Step-by-step solution:**

**Step 1 -- Justify that RL is suitable.**

Yes, Reinforcement Learning is well-suited for this problem because:

- The car must make **sequential decisions** in a dynamic, uncertain environment.
- There is no pre-existing dataset of correct labels for every possible driving situation (ruling out pure supervised learning).
- The car learns through **trial-and-error** interaction with the road environment.
- Rewards are **delayed** -- a lane change decision now affects safety several seconds later.

These two properties -- trial-and-error search and delayed rewards -- are the **two most important distinguishing features** of RL.

**Step 2 -- Formulate the MDP components.**

| MDP Component | Self-Driving Car Mapping |
|---------------|--------------------------|
| **Agent** | The self-driving car's AI decision-making system |
| **Environment** | The road, other vehicles, pedestrians, traffic signals, weather conditions |
| **States** | Current speed, position on road, lane, distance to nearby vehicles, traffic light status (red/green/yellow), sensor readings |
| **Actions** | Accelerate, brake, change lane left, change lane right, maintain speed |
| **Rewards** | +ve for safe driving, reaching destination, obeying traffic rules; -ve for collisions, traffic violations, harsh braking |
| **Policy** | Mapping from the current driving situation (state) to the best driving action. Example: "When a vehicle ahead is braking and distance < 10 m, apply brakes." |

**Step 3 -- Why not other methods?**

- Supervised learning requires labelled examples for every scenario, which is impractical to collect exhaustively for all driving situations.
- Unsupervised learning has no feedback mechanism and cannot optimise for safety.
- RL is ideal because the car can learn in simulation through trial and error with clear reward signals for safe vs. unsafe behaviour.

> **Final Answer.** RL is applicable. The agent is the car's AI system. The environment is the road and surrounding traffic. States capture speed, position, lane, distances, and traffic signals. Actions are accelerate, brake, change lane, and maintain speed. Rewards are positive for safe driving and goal progress, negative for collisions and violations. The policy maps each driving state to the best action. RL suits this problem because it involves sequential decisions, delayed rewards, and trial-and-error learning in a dynamic environment.

---

#### Paper 1 -- Q1(b): Exploration-Exploitation Trade-off [5 Marks]

> **Question.** Explain exploration-exploitation trade-off. Discuss why balancing exploration and exploitation is critical for learning an optimal policy.

**Concepts Used:** [Elements of RL -- Exploration vs Exploitation](./02_elements_of_rl.md), [Bandit Problem -- Greedy, Epsilon-Greedy, Softmax, UCB](./03_bandit_problem.md)

**Formulas Used:** None (conceptual). Epsilon-greedy and Softmax selection formulas are in [Formula Sheet](./08_formula_sheet.md).

**Step-by-step solution:**

**Step 1 -- Define each term.**

- **Exploration:** Trying new or less-tried actions to discover which ones yield the highest reward. The agent gathers information about the environment.
- **Exploitation:** Choosing actions already known to give good rewards based on past experience. The agent capitalises on existing knowledge.

**Step 2 -- Explain the dilemma.**

The agent cannot pursue both at the same time. In any given step, it either tries something new (explore) or uses what it knows (exploit).

- **Exclusively exploiting** means the agent always picks the currently best-known action. It will never discover potentially better actions and may converge to a **suboptimal policy**.
- **Exclusively exploring** means the agent always tries random actions. It never leverages known good actions and **wastes time** on actions already known to be poor.

**Step 3 -- Why balance is critical for optimal policy.**

1. Without exploration, the agent may converge to a suboptimal policy because it never discovers better actions.
2. Without exploitation, the agent wastes time and accumulates low reward because it never uses what it has learned.
3. An optimal policy requires sufficient knowledge of the environment, which only comes from exploration. But an optimal policy must also maximise reward, which requires exploitation.
4. Early in learning, the agent should explore more to build knowledge. Later, it should exploit more to maximise reward.

**Step 4 -- Methods to achieve balance.**

| Method | Mechanism |
|--------|-----------|
| Epsilon-greedy | With probability $\varepsilon$, select a random action (explore); with probability $1 - \varepsilon$, select $\arg\max Q_t(a)$ (exploit) |
| Softmax (Boltzmann) | Select actions with probability proportional to $e^{Q_t(a)/\beta}$; higher-valued actions get higher probability but all actions have nonzero chance |
| UCB (Upper Confidence Bound) | Add a bonus for uncertainty; arms that have been tried less get a higher upper bound, encouraging exploration |

> **Final Answer.** Exploration means trying new actions to discover better rewards; exploitation means choosing known good actions. The trade-off is critical because exclusively exploiting leads to suboptimal policies (never discovering better actions), while exclusively exploring wastes time on poor actions. An optimal policy requires both: exploration to build sufficient knowledge of the environment, and exploitation to maximise accumulated reward. Methods such as epsilon-greedy, softmax, and UCB provide mechanisms to balance these competing needs.

---

#### Paper 1 -- Q2(a): Softmax Numerical Computation -- 3-Arm MAB, 15 Iterations [6 Marks]

> **Question.** Apply Softmax action selection formula to calculate the probability of selecting each arm at the 16th iteration, given the following data table.

| Iteration | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|-----------|---|---|---|---|---|---|---|---|---|----|----|----|----|----|------|
| Action    | A | C | B | A | C | B | C | A | B | C  | A  | B  | B  | C  | C |
| Reward    | 4 | 2 | 5 | 3 | 1 | 4 |-5 | 2 | 3 | 4  |-5  |-2  |-3  | 2  | 4 |

**Concepts Used:** [Bandit Problem -- Softmax (Boltzmann) Action Selection](./03_bandit_problem.md)

**Formulas Used:**

Sample-average action value:

$
Q_t(a) = \frac{\sum_{i=1}^{t} \mathbf{1}(a_i = a) \cdot R_i}{\sum_{i=1}^{t} \mathbf{1}(a_i = a)}
$

Boltzmann softmax selection probability:

$
P(a_t = a) = \frac{e^{Q_t(a)/\beta}}{\sum_{b=1}^{n} e^{Q_t(b)/\beta}}
$

See [Formula Sheet](./08_formula_sheet.md) for full notation.

**Step-by-step solution (beta = 5):**

**Step 1 -- Count selections and sum rewards per arm.**

| Arm | Iterations Selected | Rewards | Count | Sum of Rewards | $Q_t(a)$ |
|-----|---------------------|---------|-------|----------------|-----------|
| A | 1, 4, 8, 11 | 4, 3, 2, -5 | 4 | 4 | 4/4 = 1.0 |
| B | 3, 6, 9, 12, 13 | 5, 4, 3, -2, -3 | 5 | 7 | 7/5 = 1.4 |
| C | 2, 5, 7, 10, 14, 15 | 2, 1, -5, 4, 2, 4 | 6 | 8 | 8/6 = 1.333 |

**Verification:** Total selections = 4 + 5 + 6 = 15 (matches 15 iterations).

**Step 2 -- Compute the exponents $Q_t(a)/\beta$ for $\beta = 5$.**

$
Q_A / \beta = 1.0 / 5 = 0.2
$

$
Q_B / \beta = 1.4 / 5 = 0.28
$

$
Q_C / \beta = 1.333 / 5 = 0.2667
$

**Step 3 -- Compute $e^{Q_t(a)/\beta}$ for each arm.**

$
e^{0.2} = 1.2214
$

$
e^{0.28} = 1.3231
$

$
e^{0.2667} = 1.3056
$

**Step 4 -- Compute the denominator (normalising constant).**

$
Z = e^{0.2} + e^{0.28} + e^{0.2667} = 1.2214 + 1.3231 + 1.3056 = 3.8501
$

**Step 5 -- Compute the Softmax probability of each arm.**

$
P(A) = \frac{e^{Q_A/\beta}}{Z} = \frac{1.2214}{3.8501} = 0.3173
$

$
P(B) = \frac{e^{Q_B/\beta}}{Z} = \frac{1.3231}{3.8501} = 0.3437
$

$
P(C) = \frac{e^{Q_C/\beta}}{Z} = \frac{1.3056}{3.8501} = 0.3391
$

**Verification:** $P(A) + P(B) + P(C) = 0.3173 + 0.3437 + 0.3391 = 1.0001 \approx 1.0$ (rounding).

> **Final Answer.** At the 16th iteration with $\beta = 5$: $P(A) = 0.3173$, $P(B) = 0.3437$, $P(C) = 0.3391$. Arm B has the highest selection probability because it has the highest estimated value ($Q_B = 1.4$).

---

#### Paper 1 -- Q2(b): Beta Parameter Comparison (beta = 5 vs beta = 100) [4 Marks]

> **Question.** Compare the behaviour when beta = 5 versus beta = 100.

**Concepts Used:** [Bandit Problem -- Beta Parameter and Temperature Effects](./03_bandit_problem.md)

**Formulas Used:** Boltzmann softmax formula (same as Q2a). See [Formula Sheet](./08_formula_sheet.md).

**Step-by-step solution:**

**Step 1 -- Recompute for beta = 100 using the same Q values.**

$
Q_A / 100 = 1.0 / 100 = 0.01, \quad e^{0.01} = 1.01005
$

$
Q_B / 100 = 1.4 / 100 = 0.014, \quad e^{0.014} = 1.01410
$

$
Q_C / 100 = 1.333 / 100 = 0.01333, \quad e^{0.01333} = 1.01342
$

$
Z = 1.01005 + 1.01410 + 1.01342 = 3.03757
$

$
P(A) = 1.01005 / 3.03757 = 0.3325
$

$
P(B) = 1.01410 / 3.03757 = 0.3339
$

$
P(C) = 1.01342 / 3.03757 = 0.3336
$

**Step 2 -- Compare the two settings side by side.**

| Arm | $P$ at $\beta = 5$ | $P$ at $\beta = 100$ |
|-----|:-------------------:|:--------------------:|
| A | 0.3173 | 0.3325 |
| B | 0.3437 | 0.3339 |
| C | 0.3391 | 0.3336 |

**Step 3 -- Interpret.**

- **$\beta = 5$ (lower temperature):** Probabilities show meaningful differentiation between arms. Arm B (highest Q) gets the highest probability (0.3437). The agent **favours exploitation** -- it biases selection toward arms with higher estimated values.
- **$\beta = 100$ (higher temperature):** All probabilities are nearly equal ($\approx 1/3$ each). The agent treats all arms almost identically regardless of their Q values. The agent **favours exploration** -- it behaves nearly like uniform random selection.
- **General rule:** Lower $\beta$ leads to more exploitation (sharper distribution); higher $\beta$ leads to more exploration (flatter distribution). As $\beta \to \infty$, probabilities approach $1/n$ (uniform). As $\beta \to 0^+$, probability concentrates entirely on the arm with the highest Q (greedy).

> **Final Answer.** With $\beta = 5$, probabilities differentiate between arms (0.317, 0.344, 0.339) -- the agent is more exploitative, favouring higher-Q arms. With $\beta = 100$, probabilities are nearly uniform (0.333, 0.334, 0.334) -- the agent is highly exploratory. Lower beta emphasises exploitation; higher beta emphasises exploration.

---

#### Paper 1 -- Q3(a): Contraction Mapping and Bellman Convergence [5 Marks]

> **Question.** Mathematically describe contraction mapping. Establish the need for contraction mapping in proving convergence of the Bellman optimality operator.

**Concepts Used:** [Contraction Mapping](./05_contraction_and_bfpt.md), [Mathematical Foundations -- Complete Metric Space](./04_mathematical_foundations.md), [Bellman Operator](./06_bellman_and_convergence.md)

**Formulas Used:**

Contraction mapping condition:

$
d(f(x_1), f(x_2)) \leq \gamma \cdot d(x_1, x_2) \quad \text{for all } x_1, x_2 \in X, \text{ some } \gamma \in [0, 1)
$

Bellman optimality operator:

$
(BV)(s) = \max_a \left[ R_s^a + \gamma \sum_{s'} P_{ss'}^a V(s') \right]
$

Banach Fixed Point Theorem (BFPT):

$
\|BV_1 - BV_2\|_\infty \leq \gamma \|V_1 - V_2\|_\infty
$

See [Formula Sheet](./08_formula_sheet.md).

**Step-by-step solution:**

**Step 1 -- Define contraction mapping.**

A function $f$ on a metric space $(X, d)$ is a **contraction mapping** (or contraction) if there exists a constant $\gamma \in [0, 1)$ such that:

$
d(f(x_1), f(x_2)) \leq \gamma \cdot d(x_1, x_2) \quad \text{for all } x_1, x_2 \in X
$

The constant $\gamma$ is called the **contraction factor** (or Lipschitz constant). The key requirement is $\gamma < 1$, which ensures that applying the function **brings points closer together**.

**Step 2 -- State the Banach Fixed Point Theorem.**

If $(X, d)$ is a **complete metric space** and $f: X \to X$ is a contraction mapping, then:

1. $f$ has a **unique** fixed point $x^* \in X$ such that $f(x^*) = x^*$.
2. For any starting point $x_0 \in X$, the sequence $x_0, f(x_0), f^2(x_0), \ldots$ **converges** to $x^*$.

**Step 3 -- Establish the need for contraction in Bellman convergence.**

The Bellman optimality operator $B$ maps value functions to value functions:

$
(BV)(s) = \max_a \left[ R_s^a + \gamma \sum_{s'} P_{ss'}^a V(s') \right]
$

To prove that repeatedly applying $B$ converges to a unique optimal value function $V^*$, we need to invoke BFPT. This requires two conditions:

1. **Complete metric space:** The space of bounded value functions $(\mathbb{R}^{|S|}, \|\cdot\|_\infty)$ is complete (for finite MDPs, value functions are real-valued vectors and $\mathbb{R}^n$ with $L_\infty$ norm is complete).

2. **Contraction mapping:** We prove $B$ is a contraction with factor $\gamma$ (the discount factor):

$
\|BV_1 - BV_2\|_\infty \leq \gamma \|V_1 - V_2\|_\infty
$

Since $0 \leq \gamma < 1$, the Bellman operator is a contraction. By BFPT, a unique fixed point $V^* = BV^*$ exists, which is the **optimal value function**. The sequence $V_0, BV_0, B^2V_0, \ldots$ converges to $V^*$ regardless of starting point -- this is exactly **value iteration**.

> **Final Answer.** A contraction mapping satisfies $d(f(x_1), f(x_2)) \leq \gamma \cdot d(x_1, x_2)$ for some $\gamma \in [0,1)$. The Bellman operator $B$ is a contraction on the complete metric space of value functions with $L_\infty$ norm, with contraction factor equal to the discount factor $\gamma$. By the Banach Fixed Point Theorem, this guarantees: (1) a unique optimal value function $V^* = BV^*$ exists, and (2) repeated application of $B$ from any starting value function converges to $V^*$. Without the contraction property, neither existence, uniqueness, nor convergence would be guaranteed.

---

#### Paper 1 -- Q3(b): Identify Contraction and Find Fixed Point [5 Marks]

> **Question.** Given $T_1(x) = 0.9x + 1$ and $T_2(x) = 1.2x^2 + 3$, identify which is a contraction mapping and find the optimal value (fixed point).

**Concepts Used:** [Contraction Mapping -- Definition and Verification](./05_contraction_and_bfpt.md)

**Formulas Used:**

Contraction condition: $|f(x) - f(y)| \leq \gamma |x - y|$ for all $x, y$ with $\gamma < 1$.

Derivative test: If $|f'(x)| \leq \gamma < 1$ for all $x$, then $f$ is a contraction with factor $\gamma$.

Fixed point: Solve $f(x^*) = x^*$.

See [Formula Sheet](./08_formula_sheet.md).

**Step-by-step solution:**

**Step 1 -- Check $T_1(x) = 0.9x + 1$.**

$
|T_1(x) - T_1(y)| = |(0.9x + 1) - (0.9y + 1)| = |0.9x - 0.9y| = 0.9|x - y|
$

Since $0.9 < 1$, $T_1$ **is a contraction** with contraction constant $k = 0.9$.

**Step 2 -- Check $T_2(x) = 1.2x^2 + 3$.**

$
|T_2(x) - T_2(y)| = |1.2x^2 - 1.2y^2| = 1.2|x^2 - y^2| = 1.2|x + y| \cdot |x - y|
$

The factor $1.2|x + y|$ can exceed 1 for $|x + y| > 1/1.2 \approx 0.833$. Therefore $T_2$ is **not a contraction** in general (the Lipschitz constant is unbounded).

**Step 3 -- Find the fixed point of $T_1$.**

Solve $T_1(x^*) = x^*$:

$
0.9x^* + 1 = x^*
$

$
1 = x^* - 0.9x^* = 0.1x^*
$

$
x^* = \frac{1}{0.1} = 10
$

**Step 4 -- Verify by iteration (starting from $x_0 = 0$).**

| $n$ | $x_n$ | $T_1(x_n) = x_{n+1}$ |
|-----|--------|-----------------------|
| 0 | 0.000 | 0.9(0) + 1 = 1.000 |
| 1 | 1.000 | 0.9(1) + 1 = 1.900 |
| 2 | 1.900 | 0.9(1.9) + 1 = 2.710 |
| 3 | 2.710 | 0.9(2.71) + 1 = 3.439 |
| 4 | 3.439 | 0.9(3.439) + 1 = 4.095 |

The sequence is increasing toward $x^* = 10$, confirming convergence.

> **Final Answer.** $T_1(x) = 0.9x + 1$ is a contraction with constant $k = 0.9$. $T_2(x) = 1.2x^2 + 3$ is not a contraction (factor $1.2|x+y|$ exceeds 1). The fixed point (optimal value) of $T_1$ is $x^* = 10$, found by solving $0.9x + 1 = x$.

---

#### Paper 1 -- Q4: Immediate RL vs Full RL, Return, Cauchy Sequence [5 + 5 Marks]

> **Question.** Define Immediate RL and Full RL. How does return differ? Why is Full RL harder? How is Cauchy's sequence convergent?

**Concepts Used:** [Elements of RL -- Immediate RL vs Full RL](./02_elements_of_rl.md), [Elements of RL -- Returns](./02_elements_of_rl.md), [Mathematical Foundations -- Cauchy Sequence](./04_mathematical_foundations.md)

**Formulas Used:**

Discounted return: $G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \cdots = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}$

Cauchy condition: For every $\varepsilon > 0$, there exists $N$ such that $d(x_a, x_b) < \varepsilon$ for all $a, b > N$.

See [Formula Sheet](./08_formula_sheet.md).

**Step-by-step solution:**

**Step 1 -- Define Immediate RL.**

Immediate RL covers **single-step** decision problems. The canonical example is the **multi-armed bandit** (MAB). The agent takes one action and receives an immediate reward. There are no sequential state transitions -- the agent's action does not affect any future state.

- Return in Immediate RL = the **immediate reward** $R_t$.
- Goal: find the single action with the highest expected immediate reward.

**Step 2 -- Define Full RL.**

Full RL covers **sequential** decision problems. The agent follows a trajectory:

$
S_0, A_0, R_1, S_1, A_1, R_2, S_2, A_2, \ldots
$

Each action potentially alters the state of the environment, thereby affecting all future rewards. In a finite MDP, $S$, $A$, and $R$ all have finite numbers of elements, and $R_t$, $S_t$ are random variables with well-defined probability distributions.

- Return in Full RL = the **cumulative discounted sum**:

$
G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \cdots = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}
$

- Goal: find a policy $\pi$ that maximises the expected return from every state.

**Step 3 -- Why Full RL is harder.**

| Challenge | Explanation |
|-----------|-------------|
| Delayed rewards | Good actions may not show their benefit until many steps later |
| Credit assignment | When a reward finally arrives, the agent must determine which of its many past actions deserves credit (or blame) |
| State transitions depend on actions | Actions change the environment, creating a feedback loop between decisions and outcomes |
| Exponentially larger policy space | The policy must map every possible state to an action; with sequential states, the number of possible policies grows exponentially |

**Step 4 -- Cauchy sequence convergence.**

A sequence $\{x_n\}$ in a metric space $(X, d)$ is **Cauchy** if for every $\varepsilon > 0$, there exists $N$ such that:

$
d(x_a, x_b) < \varepsilon \quad \text{for all } a, b > N
$

In a **complete metric space**, every Cauchy sequence converges to a limit that belongs to the space. This is the defining property of completeness.

**Connection to RL and BFPT:** The sequence of value functions generated by repeatedly applying the Bellman operator is a Cauchy sequence (because $B$ is a contraction with factor $\gamma < 1$, the distance between successive iterates shrinks geometrically). Since the space of value functions $(\mathbb{R}^{|S|}, \|\cdot\|_\infty)$ is complete, this Cauchy sequence converges to the unique optimal value function $V^*$ within the space. This is precisely the argument used in the Banach Fixed Point Theorem.

> **Final Answer.** Immediate RL involves single-step decisions (e.g., MAB) where return equals the immediate reward. Full RL involves sequential decisions where return is the discounted cumulative sum $G_t = \sum \gamma^k R_{t+k+1}$. Full RL is harder due to delayed rewards, credit assignment, action-dependent state transitions, and exponentially larger policy spaces. A Cauchy sequence has the property that its terms become arbitrarily close to each other; in a complete metric space, every Cauchy sequence converges. This guarantees the value iteration sequence converges to $V^*$ via BFPT.

---

#### Paper 1 -- Q5(a): PAC Optimality vs UCB [3 Marks]

> **Question.** Compare PAC optimality and UCB.

**Concepts Used:** [Bandit Problem -- PAC Optimality, UCB](./03_bandit_problem.md)

**Formulas Used:**

PAC condition: $P(q^*(a) > q^*(a^*) - \varepsilon) \geq 1 - \delta$

PAC sample complexity: $N = O\!\left(\frac{|S||A|}{\varepsilon^2(1-\gamma)^3} \cdot \log\frac{|S||A|}{\delta}\right)$

UCB action selection: $a_t = \arg\max_a \left[ Q_t(a) + c\sqrt{\frac{\ln t}{N_t(a)}} \right]$

See [Formula Sheet](./08_formula_sheet.md).

**Step-by-step solution:**

| Aspect | PAC Optimality | UCB |
|--------|---------------|-----|
| **Type** | Theoretical framework / criterion | Practical action-selection algorithm |
| **Focus** | "How many samples are needed to find a near-optimal policy?" | "Which arm should I pull next?" |
| **Core idea** | Provides a statistical guarantee: with probability $\geq 1-\delta$, the selected action is within $\varepsilon$ of optimal | Selects the action with the highest upper confidence bound, adding a bonus for uncertainty |
| **Output** | A bound on sample complexity $N$ | A selection rule for each time step |
| **Exploration mechanism** | Implicit via sample complexity bound | Explicit via the $\sqrt{\ln t / N_t(a)}$ bonus term (optimism in the face of uncertainty) |

> **Final Answer.** PAC is a theoretical criterion providing statistical guarantees on sample complexity: $N = O(|S||A|/(\varepsilon^2(1-\gamma)^3) \cdot \log(|S||A|/\delta))$. UCB is a practical action-selection algorithm that balances exploration and exploitation by adding an uncertainty bonus. PAC answers "how many samples do I need?"; UCB answers "which arm do I pull now?"

---

#### Paper 1 -- Q5(b): Greedy vs Epsilon-Greedy [3 Marks]

> **Question.** Compare greedy and epsilon-greedy action selection in the RL context.

**Concepts Used:** [Bandit Problem -- Greedy and Epsilon-Greedy](./03_bandit_problem.md), [Elements of RL -- Exploration vs Exploitation](./02_elements_of_rl.md)

**Formulas Used:**

Greedy: $a_t = \arg\max_a Q_t(a)$

Epsilon-greedy:

$
a_t = \begin{cases} \arg\max_a Q_t(a) & \text{with probability } 1 - \varepsilon \\ \text{random action from } A & \text{with probability } \varepsilon \end{cases}
$

See [Formula Sheet](./08_formula_sheet.md).

**Step-by-step solution:**

| Aspect | Greedy | Epsilon-Greedy |
|--------|--------|----------------|
| **Selection rule** | Always select $\arg\max Q_t(a)$ | With probability $1-\varepsilon$ select $\arg\max Q_t(a)$; with probability $\varepsilon$ select random action |
| **Exploration** | None (pure exploitation) | Yes ($\varepsilon$ fraction of the time) |
| **Exploitation** | 100% of the time | $(1-\varepsilon)$ fraction of the time |
| **Risk** | Can get stuck on suboptimal actions permanently because it never tries alternatives | Explores enough to discover better actions over time |
| **Parameter** | None | $\varepsilon$ controls the exploration rate |

> **Final Answer.** Greedy always selects $\arg\max Q_t(a)$ -- pure exploitation with no exploration. It can permanently converge to suboptimal actions. Epsilon-greedy selects the greedy action with probability $1-\varepsilon$ and a random action with probability $\varepsilon$, ensuring the agent explores and can discover better actions. The parameter $\varepsilon$ controls the exploration-exploitation balance.

---

#### Paper 1 -- Q5(c): L-infinity Norm and Policy Comparison [4 Marks]

> **Question.** Given $V_{\pi_1}(s) = [0.75,\; 2.32,\; 1.9,\; 6.4]$ and $V_{\pi_2}(s) = [0.8,\; 2.32,\; 2,\; 6.41]$, compute $\|V_1 - V_2\|_\infty$. Which policy is better?

**Concepts Used:** [Mathematical Foundations -- Norms](./04_mathematical_foundations.md), [Elements of RL -- Policy Comparison](./02_elements_of_rl.md), [Bellman Convergence -- L-infinity Norm](./06_bellman_and_convergence.md)

**Formulas Used:**

$L_\infty$ norm: $\|V_1 - V_2\|_\infty = \max_s |V_{\pi_1}(s) - V_{\pi_2}(s)|$

Policy comparison: $\pi_1 \geq \pi_2$ if and only if $v_{\pi_1}(s) \geq v_{\pi_2}(s)$ for all $s$.

See [Formula Sheet](./08_formula_sheet.md).

**Step-by-step solution:**

**Step 1 -- Compute element-wise absolute differences.**

| State | $V_{\pi_1}(s)$ | $V_{\pi_2}(s)$ | $|V_{\pi_1}(s) - V_{\pi_2}(s)|$ |
|:-----:|:---------------:|:---------------:|:--------------------------------:|
| $s_1$ | 0.75 | 0.80 | 0.05 |
| $s_2$ | 2.32 | 2.32 | 0.00 |
| $s_3$ | 1.90 | 2.00 | 0.10 |
| $s_4$ | 6.40 | 6.41 | 0.01 |

**Step 2 -- Take the maximum.**

$
\|V_1 - V_2\|_\infty = \max(0.05,\; 0,\; 0.10,\; 0.01) = 0.10
$

**Step 3 -- Compare policies.**

Check whether $V_{\pi_2}(s) \geq V_{\pi_1}(s)$ for all states:

- $s_1$: $0.80 \geq 0.75$ -- holds
- $s_2$: $2.32 \geq 2.32$ -- holds (equal)
- $s_3$: $2.00 \geq 1.90$ -- holds
- $s_4$: $6.41 \geq 6.40$ -- holds

Since $V_{\pi_2}(s) \geq V_{\pi_1}(s)$ for all $s$, policy $\pi_2$ is at least as good as $\pi_1$.

> **Final Answer.** $\|V_1 - V_2\|_\infty = 0.10$ (the maximum absolute difference, occurring at state $s_3$). Since $V_{\pi_2}(s) \geq V_{\pi_1}(s)$ for every state, $\pi_2$ is the better (or at least as good) policy.

---

### Paper 2 (Set 4, Session FN, 05/02/2026)

---

#### Paper 2 -- Q1: RL Application Modelling -- Advertisement Selection [5 + 5 Marks]

> **Question.** A company selects its advertisements based on feedback received from users, such as likes and dislikes. Explain how this advertisement selection problem can be modelled using Reinforcement Learning by identifying the agent, environment, actions, and rewards. Explain the role of rewards in reinforcement learning and discuss how user feedback enables the system to improve advertisement selection.

**Concepts Used:** [RL Fundamentals -- MDP Terms and RL Application Modelling](./01_rl_fundamentals.md), [Elements of RL -- Reward](./02_elements_of_rl.md)

**Formulas Used:** None (conceptual question). See [Formula Sheet](./08_formula_sheet.md) for the RL interaction loop.

**Step-by-step solution:**

**Step 1 -- Formulate the MDP components.**

| MDP Component | Advertisement Selection Mapping |
|---------------|-------------------------------|
| **Agent** | The advertisement recommendation system (the algorithm selecting ads) |
| **Environment** | Users and their interactions on the platform |
| **States** | User profile (age, location), browsing history, time of day, previous ad interactions, current page content |
| **Actions** | Select which advertisement to display from the available inventory |
| **Rewards** | +ve for user clicks, likes, engagement, purchases; -ve for user dislikes, skips, ad-blocker installs |
| **Policy** | Learned strategy mapping user state to the best ad selection. Example: "For users aged 18--25 browsing sports content, show sportswear ads." |

**Step 2 -- Explain the role of rewards.**

Rewards define the **goal** of the RL problem -- they tell the agent what constitutes good behaviour (user engagement) and bad behaviour (user annoyance).

- Rewards are the **primary basis for altering the policy**. If showing a particular ad to a particular user segment results in low engagement (low reward), the policy updates to try a different ad.
- User feedback provides the reward signal: **likes = positive reward**, **dislikes = negative reward**.
- Rewards are **immediate** (click or no click) but also have **delayed effects** -- showing too many irrelevant ads may cause a user to leave the platform entirely (long-term negative consequence).
- Through repeated interaction, the reward signal enables the system to learn user preferences and improve its ad selection strategy over time.

**Step 3 -- How user feedback enables improvement.**

The system operates in a feedback loop:

1. Agent observes user state (profile, browsing history).
2. Agent selects an ad to display (action).
3. User responds -- click/like (positive reward) or skip/dislike (negative reward).
4. Agent updates its policy to favour ads that produced positive feedback for similar user states.
5. Over many iterations, the policy converges toward showing ads that maximise user engagement.

The system must balance **exploration** (trying new ads to discover preferences) with **exploitation** (showing ads known to perform well).

> **Final Answer.** The agent is the ad recommendation system; the environment is the user base; states capture user profiles and browsing context; actions are ad selections; rewards come from user feedback (likes = positive, dislikes = negative). Rewards define the RL goal and are the primary basis for policy improvement. Through repeated trial-and-error interaction with users, the reward signal enables the system to learn which ads to show which users, progressively improving ad selection over time.

---

#### Paper 2 -- Q2(a): Softmax Numerical Computation -- Music Streaming MAB [6 Marks]

> **Question.** A music streaming platform uses a 3-arm bandit (arms Y, T, B) for playlist recommendation. Given 10 iterations of data, apply the Softmax formula to compute the probability of selecting each arm on the 11th day with beta = 1 and beta = 100.

| Iteration | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|-----------|---|---|---|---|---|---|---|---|---|----|
| Action    | Y | T | B | Y | T | B | T | Y | B | T  |
| Reward    | 4 | 2 | 5 | 3 | 1 | 4 | 5 | 2 | 3 | 4  |

**Concepts Used:** [Bandit Problem -- Softmax (Boltzmann) Action Selection](./03_bandit_problem.md)

**Formulas Used:**

$Q_t(a) = \frac{\text{sum of rewards for arm } a}{\text{number of times arm } a \text{ was selected}}$

$P(a_t = a) = \frac{e^{Q_t(a)/\beta}}{\sum_{b=1}^{n} e^{Q_t(b)/\beta}}$

See [Formula Sheet](./08_formula_sheet.md).

**Step-by-step solution:**

**Step 1 -- Count selections and sum rewards per arm.**

| Arm | Iterations Selected | Rewards | Count | Sum of Rewards | $Q_t(a)$ |
|-----|---------------------|---------|-------|----------------|-----------|
| Y (Yaman) | 1, 4, 8 | 4, 3, 2 | 3 | 9 | 9/3 = 3.0 |
| T (Todi) | 2, 5, 7, 10 | 2, 1, 5, 4 | 4 | 12 | 12/4 = 3.0 |
| B (Bhairav) | 3, 6, 9 | 5, 4, 3 | 3 | 12 | 12/3 = 4.0 |

**Verification:** Total selections = 3 + 4 + 3 = 10 (matches 10 iterations).

**Step 2 -- Compute for $\beta = 1$.**

$
Q_Y / 1 = 3.0, \quad e^{3.0} = 20.0855
$

$
Q_T / 1 = 3.0, \quad e^{3.0} = 20.0855
$

$
Q_B / 1 = 4.0, \quad e^{4.0} = 54.5982
$

$
Z = 20.0855 + 20.0855 + 54.5982 = 94.7692
$

$
P(Y) = 20.0855 / 94.7692 = 0.2120
$

$
P(T) = 20.0855 / 94.7692 = 0.2120
$

$
P(B) = 54.5982 / 94.7692 = 0.5761
$

**Verification:** $0.2120 + 0.2120 + 0.5761 = 1.0001 \approx 1.0$ (rounding).

**Step 3 -- Compute for $\beta = 100$.**

$
Q_Y / 100 = 0.03, \quad e^{0.03} = 1.03045
$

$
Q_T / 100 = 0.03, \quad e^{0.03} = 1.03045
$

$
Q_B / 100 = 0.04, \quad e^{0.04} = 1.04081
$

$
Z = 1.03045 + 1.03045 + 1.04081 = 3.10171
$

$
P(Y) = 1.03045 / 3.10171 = 0.3323
$

$
P(T) = 1.03045 / 3.10171 = 0.3323
$

$
P(B) = 1.04081 / 3.10171 = 0.3356
$

**Verification:** $0.3323 + 0.3323 + 0.3356 = 1.0002 \approx 1.0$ (rounding).

**Step 4 -- Compare beta values.**

| Arm | $Q_t(a)$ | $P$ at $\beta = 1$ | $P$ at $\beta = 100$ |
|-----|:--------:|:-------------------:|:--------------------:|
| Y | 3.0 | 0.2120 | 0.3323 |
| T | 3.0 | 0.2120 | 0.3323 |
| B | 4.0 | 0.5761 | 0.3356 |

- **$\beta = 1$:** Strong preference for B (57.6%). Highly **exploitative** -- the agent strongly favours the highest-Q arm.
- **$\beta = 100$:** Nearly uniform (33.2%, 33.2%, 33.6%). Highly **exploratory** -- the agent treats all arms almost equally.

On the 11th day: with $\beta = 1$, the platform most likely recommends playlist B (Bhairav); with $\beta = 100$, the platform has nearly equal chance of recommending any of the three playlists.

> **Final Answer.** With $\beta = 1$: $P(Y) = 0.212$, $P(T) = 0.212$, $P(B) = 0.576$. With $\beta = 100$: $P(Y) = 0.332$, $P(T) = 0.332$, $P(B) = 0.336$. Low beta produces exploitative behaviour (strong B preference); high beta produces exploratory behaviour (near-uniform).

---

#### Paper 2 -- Q2(b): Business Perspective on Beta Selection [4 Marks]

> **Question.** From a business perspective, discuss when to use high vs low beta values.

**Concepts Used:** [Bandit Problem -- Beta Parameter and Temperature Effects](./03_bandit_problem.md), [Elements of RL -- Exploration vs Exploitation](./02_elements_of_rl.md)

**Formulas Used:** None (conceptual question).

**Step-by-step solution:**

| Business Phase | Recommended Beta | Behaviour | Rationale |
|----------------|:----------------:|-----------|-----------|
| **On-boarding / Cold Start** (new users) | High (e.g., 100) | Exploratory -- show diverse content to learn preferences | The platform has no data about the new user. It must explore widely to discover what the user likes. Showing the same content repeatedly without data would risk poor first impressions. |
| **High-Confidence Phase** (established users) | Low (e.g., 1) | Exploitative -- show content known to match preferences | The platform has accumulated sufficient data about the user's tastes. It should exploit this knowledge to maximise listening time (engagement) and user satisfaction. |

**Transition strategy:** Gradually decrease beta as the system gains confidence in user preferences. Start with high exploration and progressively shift toward exploitation.

> **Final Answer.** During on-boarding (new users, no data), use high beta for wide exploration to discover user preferences. After the platform has high confidence in user preferences, use low beta to exploit known favourites and maximise engagement. Gradually decrease beta as confidence grows.

---

#### Paper 2 -- Q3(a): Policy Evaluation as Fixed Point of Bellman Expectation Operator [5 + 5 Marks]

> **Question.** Describe policy evaluation as finding the fixed point of the Bellman expectation operator $T^\pi$. Explain how Banach's theorem guarantees convergence.

**Concepts Used:** [Contraction Mapping and BFPT](./05_contraction_and_bfpt.md), [Bellman Operator and Convergence](./06_bellman_and_convergence.md), [Mathematical Foundations -- Complete Metric Space](./04_mathematical_foundations.md)

**Formulas Used:**

Bellman expectation operator:

$
(T^\pi V)(s) = \sum_a \pi(a|s) \left[ R_s^a + \gamma \sum_{s'} P_{ss'}^a V(s') \right]
$

Contraction condition: $\|T^\pi V_1 - T^\pi V_2\|_\infty \leq \gamma \|V_1 - V_2\|_\infty$

See [Formula Sheet](./08_formula_sheet.md).

**Step-by-step solution:**

**Step 1 -- Define the policy evaluation problem.**

Policy evaluation seeks the value function $V^\pi$ for a given fixed policy $\pi$. The value function satisfies:

$
V^\pi(s) = \sum_a \pi(a|s) \left[ R_s^a + \gamma \sum_{s'} P_{ss'}^a V^\pi(s') \right]
$

This is a fixed-point equation: $V^\pi = T^\pi(V^\pi)$, where $T^\pi$ is the **Bellman expectation operator**.

**Step 2 -- Show $T^\pi$ is a contraction.**

For any two value functions $V_1$ and $V_2$:

$
\|T^\pi V_1 - T^\pi V_2\|_\infty \leq \gamma \|V_1 - V_2\|_\infty
$

This holds because:

- The expectation under $\pi$ and the transition probabilities $P_{ss'}^a$ sum to 1.
- The discount factor $\gamma$ multiplies the value function term.
- Taking the max over states preserves the bound.

Since $0 \leq \gamma < 1$, $T^\pi$ is a contraction with factor $\gamma$.

**Step 3 -- Apply Banach's Fixed Point Theorem.**

BFPT requires two conditions:

1. **Complete metric space:** The space of value functions $(\mathbb{R}^{|S|}, \|\cdot\|_\infty)$ is complete for finite MDPs. (Every Cauchy sequence of value function vectors converges to a value function in the same space.)

2. **Contraction mapping:** $T^\pi$ is a contraction with factor $\gamma$ (shown above).

By BFPT:

- A **unique** fixed point $V^\pi$ exists such that $T^\pi(V^\pi) = V^\pi$.
- The iterative sequence $V_0, T^\pi(V_0), (T^\pi)^2(V_0), \ldots$ **converges** to $V^\pi$ regardless of the starting value function $V_0$.

This iterative process is exactly **policy evaluation**: repeatedly apply $T^\pi$ until convergence.

> **Final Answer.** Policy evaluation finds $V^\pi$ satisfying $V^\pi = T^\pi(V^\pi)$, a fixed-point equation. The Bellman expectation operator $T^\pi$ is a contraction with factor $\gamma$ on the complete metric space $(\mathbb{R}^{|S|}, \|\cdot\|_\infty)$. By Banach's Fixed Point Theorem, this guarantees: (1) a unique $V^\pi$ exists, and (2) starting from any $V_0$ and repeatedly applying $T^\pi$ converges to $V^\pi$. Convergence is guaranteed because the iterative sequence is Cauchy (distance shrinks by factor $\gamma$ each step) and the space is complete.

---

#### Paper 2 -- Q3(b): Contraction Verification -- $f(x) = 0.25\sin^2(x)$, 5 Iterations [5 + 5 Marks]

> **Question.** Check whether $f(x) = 0.25\sin^2(x)$ is a contraction. Starting from $x_0 = 0.71$, perform 5 iterations.

**Concepts Used:** [Contraction Mapping -- Definition and Verification](./05_contraction_and_bfpt.md)

**Formulas Used:**

Derivative test: If $|f'(x)| \leq k < 1$ for all $x$, then $f$ is a contraction with constant $k$.

Mean Value Theorem: $|f(x) - f(y)| = |f'(c)| \cdot |x - y|$ for some $c$ between $x$ and $y$.

See [Formula Sheet](./08_formula_sheet.md).

**Step-by-step solution:**

**Step 1 -- Compute the derivative.**

$
f(x) = 0.25 \sin^2(x)
$

$
f'(x) = 0.25 \cdot 2\sin(x)\cos(x) = 0.25 \sin(2x)
$

**Step 2 -- Check the contraction condition.**

$
|f'(x)| = |0.25 \sin(2x)| \leq 0.25 \cdot 1 = 0.25 < 1 \quad \text{for all } x
$

Since $|\sin(2x)| \leq 1$ for all $x$, we have $|f'(x)| \leq 0.25 < 1$. By the Mean Value Theorem:

$
|f(x) - f(y)| \leq 0.25 |x - y|
$

Therefore $f$ **is a contraction** with contraction constant $k = 0.25$.

**Step 3 -- Perform 5 iterations from $x_0 = 0.71$.**

| $n$ | $x_n$ | $\sin(x_n)$ | $\sin^2(x_n)$ | $x_{n+1} = 0.25\sin^2(x_n)$ |
|-----|--------|-------------|---------------|-------------------------------|
| 0 | 0.71000 | 0.65183 | 0.42488 | 0.10622 |
| 1 | 0.10622 | 0.10602 | 0.01124 | 0.00281 |
| 2 | 0.00281 | 0.00281 | 0.00000789 | 0.00000197 |
| 3 | 0.00000197 | 0.00000197 | $\approx 0$ | $\approx 0$ |
| 4 | $\approx 0$ | $\approx 0$ | $\approx 0$ | $\approx 0$ |

**Step 4 -- Identify the fixed point.**

The fixed point satisfies $x^* = 0.25\sin^2(x^*)$.

At $x^* = 0$: $0.25\sin^2(0) = 0.25 \cdot 0 = 0 = x^*$. Confirmed.

**Verification:** Convergence is very rapid because the contraction constant $k = 0.25$ is small. After just 3 iterations, the sequence is effectively at the fixed point.

> **Final Answer.** $f(x) = 0.25\sin^2(x)$ is a contraction with constant $k = 0.25$ (since $|f'(x)| = |0.25\sin(2x)| \leq 0.25 < 1$). Starting from $x_0 = 0.71$: $x_1 = 0.1062$, $x_2 = 0.00281$, $x_3 \approx 0.00000197$, $x_4 \approx 0$, $x_5 \approx 0$. The fixed point is $x^* = 0$. Convergence is rapid due to the small contraction constant.

---

#### Paper 2 -- Q4: Fixed Point Problem, Relation to RL, Existence and Uniqueness via BFPT [10 Marks]

> **Question.** Define the fixed-point problem. Relate it to RL. Discuss existence and uniqueness via the Banach Fixed Point Theorem.

**Concepts Used:** [Mathematical Foundations -- Fixed Point Problem](./04_mathematical_foundations.md), [Contraction Mapping and BFPT](./05_contraction_and_bfpt.md), [Bellman Operator](./06_bellman_and_convergence.md)

**Formulas Used:**

Fixed point condition: $f(x^*) = x^*$

Bellman equation: $V^*(s) = \max_a [R_s^a + \gamma \sum_{s'} P_{ss'}^a V^*(s')]$, i.e., $V^* = BV^*$

Contraction condition: $d(f(x_1), f(x_2)) \leq \gamma \cdot d(x_1, x_2)$

See [Formula Sheet](./08_formula_sheet.md).

**Step-by-step solution:**

**Step 1 -- Define the fixed-point problem.**

A **fixed-point problem** asks: find $x^* \in X$ such that:

$
f(x^*) = x^*
$

The value $x^*$ does not change under application of $f$. This contrasts with root finding ($f(x) = 0$); any fixed-point problem can be converted to root finding via $g(x) = f(x) - x = 0$.

**Step 2 -- Relate to RL.**

The Bellman optimality equation for the optimal value function $V^*$ is:

$
V^*(s) = \max_a \left[ R_s^a + \gamma \sum_{s'} P_{ss'}^a V^*(s') \right]
$

This can be written compactly as $V^* = BV^*$, where $B$ is the **Bellman optimality operator**. Finding the optimal value function $V^*$ is therefore a **fixed-point problem**: we seek the value function that remains unchanged when the Bellman operator is applied.

Similarly, for policy evaluation, $V^\pi = T^\pi(V^\pi)$ is also a fixed-point problem.

**Step 3 -- Existence via BFPT.**

*Setup:* The space of bounded value functions with the $L_\infty$ norm, $(\mathbb{R}^{|S|}, \|\cdot\|_\infty)$, is a complete metric space (for finite MDPs).

*Cauchy sequence argument:*

Starting from any $V_0$, define $V_{n+1} = B(V_n)$. Since $B$ is a contraction with factor $\gamma$:

$
\|V_{n+1} - V_n\|_\infty = \|BV_n - BV_{n-1}\|_\infty \leq \gamma \|V_n - V_{n-1}\|_\infty \leq \gamma^n \|V_1 - V_0\|_\infty
$

For any $m > n$, by the triangle inequality and geometric series:

$
\|V_m - V_n\|_\infty \leq \frac{\gamma^n}{1 - \gamma} \|V_1 - V_0\|_\infty
$

As $n \to \infty$, $\gamma^n \to 0$, so $\|V_m - V_n\| \to 0$. The sequence $\{V_n\}$ is **Cauchy**.

Since the space is complete, the Cauchy sequence converges to some $V^* \in \mathbb{R}^{|S|}$.

Since $B$ is continuous (contractions are continuous), $V^* = \lim V_{n+1} = \lim B(V_n) = B(\lim V_n) = B(V^*)$.

Therefore $V^*$ is a fixed point of $B$: it **exists**.

**Step 4 -- Uniqueness via BFPT.**

Assume two fixed points $V_1^*$ and $V_2^*$ both satisfy $BV^* = V^*$. Then:

$
\|V_1^* - V_2^*\|_\infty = \|BV_1^* - BV_2^*\|_\infty \leq \gamma \|V_1^* - V_2^*\|_\infty
$

This gives $(1 - \gamma)\|V_1^* - V_2^*\|_\infty \leq 0$. Since $\gamma < 1$, we have $1 - \gamma > 0$, which forces:

$
\|V_1^* - V_2^*\|_\infty = 0
$

Therefore $V_1^* = V_2^*$. The fixed point is **unique**.

> **Final Answer.** A fixed-point problem seeks $x^*$ such that $f(x^*) = x^*$. In RL, the optimal value function $V^*$ is the fixed point of the Bellman operator: $V^* = BV^*$. Existence: The iterative sequence $V_{n+1} = BV_n$ is Cauchy (since $B$ is a contraction with factor $\gamma$, successive distances shrink geometrically). Since the value function space with $L_\infty$ norm is complete, this Cauchy sequence converges to $V^*$ in the space, so the fixed point exists. Uniqueness: If two fixed points existed, the contraction inequality $\|V_1^* - V_2^*\| \leq \gamma\|V_1^* - V_2^*\|$ with $\gamma < 1$ forces their distance to zero, so they must be identical.

---

## Source Material Problems

### Contraction Verification from Module 2 Lecture Slides

---

#### Source Problem 1: $f(x) = (x + 3)/4$ on $X = [0, 2]$

**Concepts Used:** [Contraction Mapping -- Definition and Verification](./05_contraction_and_bfpt.md), [Mathematical Foundations -- Iterative Convergence](./04_mathematical_foundations.md)

**Formulas Used:**

Contraction condition: $|f(x) - f(y)| \leq k|x - y|$ with $k < 1$.

Fixed point: $f(x^*) = x^*$.

**Step-by-step solution:**

**Step 1 -- Check the contraction condition.**

$
|f(x) - f(y)| = \left|\frac{x+3}{4} - \frac{y+3}{4}\right| = \frac{1}{4}|x - y|
$

Since $k = 1/4 = 0.25 < 1$, $f$ is a contraction with constant $k = 0.25$.

**Step 2 -- Find the fixed point algebraically.**

$
x^* = \frac{x^* + 3}{4} \implies 4x^* = x^* + 3 \implies 3x^* = 3 \implies x^* = 1
$

**Step 3 -- Verify by iteration from $x_0 = 0$.**

| $n$ | $x_n$ | $f(x_n) = (x_n + 3)/4$ |
|-----|--------|-------------------------|
| 0 | 0.0000 | 0.7500 |
| 1 | 0.7500 | 0.9375 |
| 2 | 0.9375 | 0.9844 |
| 3 | 0.9844 | 0.9961 |
| 4 | 0.9961 | 0.9990 |
| 5 | 0.9990 | 0.9998 |

The sequence converges rapidly to $x^* = 1$.

**Verification:** $f(1) = (1+3)/4 = 4/4 = 1 = x^*$. Confirmed.

> **Final Answer.** $f(x) = (x+3)/4$ is a contraction on $[0,2]$ with constant $k = 0.25$. The unique fixed point is $x^* = 1$.

---

#### Source Problem 2: $f(x) = 0.5\sin(x)$ -- Previous Exam Question from Slides

**Concepts Used:** [Contraction Mapping -- Derivative Test](./05_contraction_and_bfpt.md)

**Formulas Used:**

Derivative test: $|f'(x)| \leq k < 1$ implies contraction with constant $k$.

**Step-by-step solution:**

**Step 1 -- Compute the derivative and check contraction.**

$
f(x) = 0.5\sin(x)
$

$
f'(x) = 0.5\cos(x)
$

$
|f'(x)| = |0.5\cos(x)| \leq 0.5 \cdot 1 = 0.5 < 1 \quad \text{for all } x
$

Therefore $f$ is a contraction with constant $k = 0.5$.

**Step 2 -- Find the fixed point.**

At $x^* = 0$: $f(0) = 0.5\sin(0) = 0 = x^*$. So $x^* = 0$ is a fixed point.

**Step 3 -- Iterate from $x_0 = 0.2$.**

| $n$ | $x_n$ | $\sin(x_n)$ | $x_{n+1} = 0.5\sin(x_n)$ |
|-----|--------|-------------|---------------------------|
| 0 | 0.20000 | 0.19867 | 0.09934 |
| 1 | 0.09934 | 0.09917 | 0.04959 |
| 2 | 0.04959 | 0.04957 | 0.02479 |
| 3 | 0.02479 | 0.02479 | 0.01239 |
| 4 | 0.01239 | 0.01239 | 0.00620 |
| 5 | 0.00620 | 0.00620 | 0.00310 |

The sequence converges to $x^* = 0$. Each iterate is approximately half the previous one (consistent with $k = 0.5$).

**Verification:** The distance to the fixed point halves at each step: $0.2 \to 0.099 \to 0.050 \to 0.025 \to 0.012 \to 0.006$, confirming the contraction factor $k \approx 0.5$.

> **Final Answer.** $f(x) = 0.5\sin(x)$ is a contraction with $k = 0.5$ (since $|f'(x)| = |0.5\cos(x)| \leq 0.5 < 1$). The fixed point is $x^* = 0$. Iterating from $x_0 = 0.2$ converges to 0, with the distance halving at each step.

---

#### Source Problem 3: $f(x) = 0.25\cos^2(x)$ -- Previous Exam Question from Slides

**Concepts Used:** [Contraction Mapping -- Derivative Test](./05_contraction_and_bfpt.md)

**Formulas Used:**

$f'(x) = -0.25\sin(2x)$ (via chain rule: $\frac{d}{dx}\cos^2(x) = -2\cos(x)\sin(x) = -\sin(2x)$).

**Step-by-step solution:**

**Step 1 -- Compute the derivative and check contraction.**

$
f(x) = 0.25\cos^2(x)
$

$
f'(x) = 0.25 \cdot (-\sin(2x)) = -0.25\sin(2x)
$

$
|f'(x)| = |{-}0.25\sin(2x)| \leq 0.25 \cdot 1 = 0.25 < 1 \quad \text{for all } x
$

Therefore $f$ is a contraction with constant $k = 0.25$.

**Step 2 -- Find the fixed point.**

Solve $x^* = 0.25\cos^2(x^*)$. This equation has no closed-form solution, so we find it numerically via iteration.

**Step 3 -- Iterate from $x_0 = 0.2$.**

| $n$ | $x_n$ | $\cos(x_n)$ | $\cos^2(x_n)$ | $x_{n+1} = 0.25\cos^2(x_n)$ |
|-----|--------|-------------|---------------|-------------------------------|
| 0 | 0.20000 | 0.98007 | 0.96053 | 0.24013 |
| 1 | 0.24013 | 0.97124 | 0.94331 | 0.23583 |
| 2 | 0.23583 | 0.97228 | 0.94533 | 0.23633 |
| 3 | 0.23633 | 0.97216 | 0.94510 | 0.23628 |
| 4 | 0.23628 | 0.97217 | 0.94511 | 0.23628 |
| 5 | 0.23628 | 0.97217 | 0.94511 | 0.23628 |

The sequence converges to $x^* \approx 0.2363$.

**Verification:** $f(0.2363) = 0.25 \cdot \cos^2(0.2363) = 0.25 \cdot 0.9451 = 0.2363$. Confirmed.

> **Final Answer.** $f(x) = 0.25\cos^2(x)$ is a contraction with $k = 0.25$ (since $|f'(x)| = |0.25\sin(2x)| \leq 0.25 < 1$). Iterating from $x_0 = 0.2$: $x_1 = 0.2401$, $x_2 = 0.2358$, $x_3 = 0.2363$, $x_4 = 0.2363$, $x_5 = 0.2363$. The fixed point is $x^* \approx 0.2363$.

---

## Cross-Reference Index

| Problem Type | Past Paper Questions | Source Problems | Key Topic File |
|-------------|---------------------|-----------------|----------------|
| RL Application Modelling | P1-Q1(a), P2-Q1 | -- | [01_rl_fundamentals.md](./01_rl_fundamentals.md) |
| Exploration-Exploitation | P1-Q1(b), P2-Q2(b) | -- | [02_elements_of_rl.md](./02_elements_of_rl.md) |
| Softmax Computation | P1-Q2(a), P2-Q2(a) | -- | [03_bandit_problem.md](./03_bandit_problem.md) |
| Beta Parameter | P1-Q2(b), P2-Q2(a,b) | -- | [03_bandit_problem.md](./03_bandit_problem.md) |
| Contraction Mapping & BFPT | P1-Q3(a), P2-Q3(a), P2-Q4 | -- | [05_contraction_and_bfpt.md](./05_contraction_and_bfpt.md) |
| Contraction Verification & Iteration | P1-Q3(b), P2-Q3(b) | SP1, SP2, SP3 | [05_contraction_and_bfpt.md](./05_contraction_and_bfpt.md) |
| Immediate vs Full RL | P1-Q4 | -- | [02_elements_of_rl.md](./02_elements_of_rl.md) |
| Fixed Point & BFPT Proof | P2-Q4, P1-Q3(a) | -- | [04_mathematical_foundations.md](./04_mathematical_foundations.md) |
| PAC vs UCB | P1-Q5(a) | -- | [03_bandit_problem.md](./03_bandit_problem.md) |
| Greedy vs Epsilon-Greedy | P1-Q5(b) | -- | [03_bandit_problem.md](./03_bandit_problem.md) |
| L-infinity Norm & Policy Comparison | P1-Q5(c) | -- | [06_bellman_and_convergence.md](./06_bellman_and_convergence.md) |

---

*Next: [08_formula_sheet.md](./08_formula_sheet.md) -- All key formulas consolidated for quick revision.*
