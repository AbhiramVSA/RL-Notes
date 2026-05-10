# Elements of Reinforcement Learning

---

## Learning Objectives

After completing this section, you will be able to:

- Define and distinguish the four main elements of an RL system: policy, reward signal, value function, and model of the environment
- Explain the critical difference between reward (immediate) and value (long-term)
- Describe the exploration vs exploitation dilemma and why neither can be pursued exclusively
- Differentiate between Immediate RL (bandits) and Full RL (sequential decisions)
- Write and interpret the Temporal Difference (TD) update rule
- Explain the concept of returns, including discounted returns
- Compare policies using value functions
- Distinguish model-based from model-free learning approaches

---

## Ground-Up Explanation

### Policy

A **policy** is the rule book that an RL agent has learned for how to behave at any given time. Formally, it is a mapping from the perceived state of the environment to the actions the agent should take when in that state. You can think of it as a lookup table or function that answers the question: "Given that the world looks like this, what should I do?"

The policy is the core of an RL agent. It is alone sufficient to completely determine the behavior of the agent. Everything else in the system -- rewards, value functions, models -- ultimately exists to help the agent find a better policy.

A policy can be deterministic, directly mapping each state to a single action, or stochastic, assigning a probability distribution over actions for each state. The stochastic form is written as:

$
\pi_t(a \mid s) \triangleq P[A_t = a \mid S_t = s]
$

> **Where:**
> - $\pi_t$ = the policy at time $t$
> - $a$ = an action from the action space $A$
> - $s$ = a state from the state space $S$
> - $P[\cdot]$ = probability

In most of this course, we deal with **stationary policies**, meaning the mapping does not change with time (i.e., the same state always produces the same action or action distribution, regardless of when the agent encounters it).

---

### Reward

The **reward signal** defines the goal of an RL problem. At each time step, the environment sends the RL agent a single number called the reward. The agent's sole objective is to maximize the total reward it receives over the long run.

Key properties of the reward signal:

- It defines what are good and bad events for the agent. A high reward means the action was beneficial; a low reward means it was not.
- Rewards are the **immediate and defining features** of the problems faced by the agent. They come directly from the environment and are outside the agent's direct control.
- The reward signal is the **primary basis for altering the policy**. If an action selected by the current policy is followed by low reward, the policy may be changed to select a different action in that situation in the future.
- Reward is a scalar function -- it is always a single number, not a vector.
- Rewards are bounded and frequent.

> **Key Insight:** The reward signal tells the agent what is good *right now*, in an immediate sense. It does not tell the agent what is good *in the long run*. That is the job of the value function.

---

### Value Function

While the reward indicates what is good in the immediate sense, the **value function** specifies what is good in the long run. The value of a state is the total amount of reward an agent can expect to accumulate over the future, starting from that state.

Values are assigned to states. A state might yield a low immediate reward but still have a high value because it is regularly followed by other states that yield high rewards. Conversely, a state might give a high immediate reward but have a low value because the states that follow it tend to give poor rewards.

Formally, the state-value function under a policy $\pi$ is:

$
v_\pi(s) = E_\pi[G_t \mid S_t = s]
$

> **Where:**
> - $v_\pi(s)$ = value of state $s$ under policy $\pi$
> - $E_\pi[\cdot]$ = expected value when following policy $\pi$
> - $G_t$ = the return (cumulative future reward) from time $t$ onward

There is also an **action-value function** $q_\pi(s, a)$, which gives the expected return of taking action $a$ in state $s$ and then following policy $\pi$ thereafter. This will become critical in later modules when we study Q-learning.

---

### Reward vs Value

This distinction is fundamental and is a common source of confusion.

| Aspect | Reward | Value |
|--------|--------|-------|
| **Time horizon** | Immediate (single time step) | Long-term (cumulative future) |
| **Source** | Given directly by the environment | Estimated and re-estimated by the agent |
| **Assigned to** | A state-action-transition event | A state (or state-action pair) |
| **Role** | Defines what is good/bad right now | Defines what is good/bad in the long run |
| **Certainty** | Directly observed | Must be learned from experience |
| **Primary use** | Provides the raw signal | Guides action selection and policy improvement |

> **Key Insight:** Without rewards, there could be no values. But without values, the agent cannot make decisions that account for future consequences. Rewards are the raw data; values are the processed intelligence derived from that data.

In practice, the most important decisions an RL agent makes are based on value judgments, not immediate rewards. The agent seeks states of highest value, not highest immediate reward, because those states produce the greatest total reward over the long run.

---

### Model of the Environment

A **model of the environment** is something that mimics the behavior of the environment. Given a current state and an action, the model can predict the resulting next state and the reward associated with that transition.

Models are used for **planning** -- deciding on a course of action by considering possible future situations before they are actually experienced.

This gives rise to two fundamental categories of RL methods:

| Approach | Description | Example |
|----------|-------------|---------|
| **Model-based** | The agent has (or learns) a model of the environment and uses it to plan ahead | Dynamic programming, Dyna |
| **Model-free** | No model is available; the agent must learn the environment's behavior purely through trial and error | Q-learning, SARSA, Monte Carlo |

Model-free methods are simpler but may require more interaction with the environment. Model-based methods can be more sample-efficient but require the model to be accurate.

---

### Immediate RL vs Full RL

This is a critical distinction in the course and a frequently examined topic.

**Immediate RL** deals with single-step decision problems. The canonical example is the **multi-armed bandit** problem. In Immediate RL:

- The agent selects a single action and receives a single reward.
- The action does not affect any future state -- there is no notion of sequential states.
- The agent's goal is simply to find the action with the highest expected reward.
- The problem reduces to estimating the value of each action independently.

**Full RL** deals with sequential decision problems where actions affect future states. In Full RL:

- The agent follows a trajectory: $S_0, A_0, R_1, S_1, A_1, R_2, S_2, A_2, \ldots$
- Each action potentially alters the state of the environment, thereby affecting all future rewards.
- The agent must consider not just immediate reward but the entire stream of future rewards.
- In a finite MDP, $S$, $A$, and $R$ all have finite numbers of elements.
- $R_t$ and $S_t$ are random variables with well-defined probability distributions.

Full RL is significantly harder than Immediate RL because of two challenges:

1. **Delayed rewards** -- An action taken now may not produce its consequences until many time steps later.
2. **Credit assignment** -- When a good (or bad) outcome finally occurs, the agent must figure out which of its many past actions deserves credit (or blame).

> **Key Insight:** The bandit problem is Immediate RL -- a simplified version of the full RL problem where there is only one state and actions do not influence future situations. Full RL adds the sequential dimension, making it far more complex.

---

### Returns

The **return** is the concept that formalizes "total future reward." It is what the agent ultimately wants to maximize.

**Simple cumulative return** (for episodic tasks with a terminal state):

$
G_t = R_{t+1} + R_{t+2} + R_{t+3} + \cdots + R_T
$

> **Where:**
> - $G_t$ = return from time step $t$
> - $R_{t+k}$ = reward received $k$ steps into the future
> - $T$ = time step at which the episode ends (e.g., end of a chess game)

**Discounted return** (for continuing tasks or when future rewards are worth less):

$
G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \cdots = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}
$

> **Where:**
> - $\gamma$ = discount factor, $0 \leq \gamma < 1$

The discount factor $\gamma$ captures the idea that reward received now is more valuable than reward received in the future. When $\gamma$ is close to 0, the agent is "myopic" and cares mostly about immediate reward. When $\gamma$ is close to 1, the agent is "far-sighted" and weighs future rewards almost as heavily as immediate ones.

**Averaged return** (less common, mentioned in the slides):

$
G_t = \frac{1}{N}(R_{t+1} + R_{t+2} + R_{t+3} + \cdots + R_{t+N})
$

---

### Exploration vs Exploitation

This is one of the most fundamental dilemmas in reinforcement learning.

- **Exploration**: The agent tries new or less-tried actions to discover which ones yield the highest reward. This is necessary because the agent starts with no knowledge and must learn about its environment.
- **Exploitation**: The agent selects actions that it has already found to produce good rewards, based on past experience. This is necessary to actually accumulate high reward.

The dilemma arises because exploration and exploitation **cannot be exclusively pursued without failing at the task**:

- If the agent only exploits (always picks the currently best-known action), it will never discover potentially better actions. It gets stuck with a possibly sub-optimal choice.
- If the agent only explores (always tries random actions), it never capitalizes on what it has already learned. It wastes time on actions already known to be poor.

The agent must strike a balance. Various methods for managing this trade-off are covered in later topics, including epsilon-greedy, softmax action selection, and UCB (Upper Confidence Bound).

> **Warning:** Continuously pursuing only one strategy (pure exploration or pure exploitation) leads to failure. This is a point the slides emphasize explicitly.

---

### Temporal Difference Update

The **Temporal Difference (TD) update** is a method for learning value function estimates from experience. Instead of waiting until the end of an episode to update, TD methods update their estimates based on the difference between predictions at successive time steps.

The TD(0) update rule for the state-value function is:

$
V(S_t) \leftarrow V(S_t) + \alpha \left[ V(S_{t+1}) - V(S_t) \right]
$

> **Where:**
> - $V(S_t)$ = current estimate of the value of state $S_t$
> - $V(S_{t+1})$ = current estimate of the value of the next state $S_{t+1}$
> - $\alpha$ = step-size parameter (learning rate), $0 < \alpha \leq 1$
> - $V(S_{t+1}) - V(S_t)$ = the **temporal difference error**

The idea is straightforward: after transitioning from state $S_t$ to state $S_{t+1}$, the agent updates its estimate of $V(S_t)$ by nudging it in the direction of $V(S_{t+1})$. If the next state turns out to be more valuable than expected, the current state's value is revised upward. If less valuable, it is revised downward.

> **Key Insight:** The name "temporal difference" comes from the fact that the update is based on the difference between the agent's value estimates at two successive points in time.

---

## Analogies

**Policy as a GPS navigation app.** Just as a GPS tells you "turn left here, go straight there" based on your current location, the policy tells the agent what action to take based on the current state. The GPS does not need to understand the full map -- it just needs to know the correct instruction for each location. Similarly, the policy alone is sufficient to determine the agent's behavior.

**Reward vs Value as daily pay vs career earnings.** Imagine choosing between two jobs. Job A pays you a large bonus today (high immediate reward) but has no growth prospects. Job B pays modestly today (low immediate reward) but leads to a career with massive future earnings. The reward is today's paycheck. The value is the total career earnings you can expect from this point forward. A wise agent (like a wise person) makes decisions based on value, not just immediate reward.

**Exploration vs Exploitation as choosing restaurants.** You know a restaurant you like (exploit), but there might be an even better one you have not tried (explore). If you always go to the same restaurant, you might miss a better one. If you always try random new places, you spend many nights eating mediocre food at places you already know are not great. The best strategy is a mix: mostly go to your favorite, but occasionally try somewhere new.

**TD Update as adjusting expectations mid-journey.** Suppose you estimate a road trip will take 5 hours. After 1 hour, you notice traffic is lighter than expected and revise your estimate to 4.5 hours. You did not wait until you arrived to update your estimate -- you updated it based on new information encountered along the way. This is exactly what TD learning does with value estimates.

---

## Key Formulas

> **CRITICAL EQUATION**
>
> **Temporal Difference Update**
>
> $
> V(S_t) \leftarrow V(S_t) + \alpha \left[ V(S_{t+1}) - V(S_t) \right]
> $

> **Where:**
> - $V(S_t)$ = current estimate of the value of state $S_t$
> - $\alpha$ = learning rate (step size)
> - $V(S_{t+1}) - V(S_t)$ = temporal difference error

---

> **CRITICAL EQUATION**
>
> **Policy Comparison**
>
> $
> \pi_1 \geq \pi_2 \quad \text{if and only if} \quad v_{\pi_1}(s) \geq v_{\pi_2}(s) \quad \text{for all } s \in S
> $

> **Where:**
> - $\pi_1, \pi_2$ = two policies being compared
> - $v_{\pi}(s)$ = value of state $s$ under policy $\pi$
> - $S$ = the set of all states

---

**Discounted Return:**

$
G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}
$

> **Where:**
> - $G_t$ = return from time step $t$
> - $\gamma$ = discount factor, $0 \leq \gamma < 1$
> - $R_{t+k+1}$ = reward received $k+1$ steps from time $t$

---

**Stochastic Policy:**

$
\pi_t(a \mid s) = P[A_t = a \mid S_t = s]
$

---

## Worked Examples

### Example 1: Interpreting the TD Update

Suppose the agent is in state $S_t$ with current value estimate $V(S_t) = 3.0$, and it transitions to state $S_{t+1}$ with current value estimate $V(S_{t+1}) = 5.0$. The learning rate is $\alpha = 0.1$.

**Step 1:** Compute the temporal difference error.

$
\text{TD error} = V(S_{t+1}) - V(S_t) = 5.0 - 3.0 = 2.0
$

**Step 2:** Apply the update rule.

$
V(S_t) \leftarrow V(S_t) + \alpha \cdot \text{TD error} = 3.0 + 0.1 \times 2.0 = 3.0 + 0.2 = 3.2
$

> **Answer:** The new estimate is $V(S_t) = 3.2$. The value of $S_t$ was nudged upward because the next state turned out to be more valuable than the current estimate of $S_t$.

---

### Example 2: Computing Discounted Return

An agent receives the following reward sequence starting from time $t$: $R_{t+1} = 2$, $R_{t+2} = 3$, $R_{t+3} = 1$, and the episode ends. The discount factor is $\gamma = 0.9$.

**Step 1:** Write out the discounted return formula.

$
G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3}
$

**Step 2:** Substitute values.

$
G_t = 2 + 0.9 \times 3 + 0.9^2 \times 1 = 2 + 2.7 + 0.81 = 5.51
$

> **Answer:** $G_t = 5.51$

---

### Example 3: Comparing Two Policies

Consider an environment with three states $S = \{s_1, s_2, s_3\}$ and two policies $\pi_1$ and $\pi_2$ with the following value functions:

| State | $v_{\pi_1}(s)$ | $v_{\pi_2}(s)$ |
|-------|:--------:|:--------:|
| $s_1$ | 4.0 | 3.5 |
| $s_2$ | 2.5 | 2.5 |
| $s_3$ | 6.0 | 5.8 |

**Step 1:** Check whether $v_{\pi_1}(s) \geq v_{\pi_2}(s)$ for all $s \in S$.

- $s_1$: $4.0 \geq 3.5$ -- holds
- $s_2$: $2.5 \geq 2.5$ -- holds (equality counts)
- $s_3$: $6.0 \geq 5.8$ -- holds

**Step 2:** Since the inequality holds for every state, we conclude:

> **Answer:** $\pi_1 \geq \pi_2$. Policy $\pi_1$ is at least as good as policy $\pi_2$.

---

## Common Mistakes

- **Confusing reward with value.** Reward is a single number received at one time step from the environment. Value is the expected cumulative total of all future rewards from a state. A state with low immediate reward can still have high value.

- **Thinking the agent controls the reward.** The reward is generated by the environment, not the agent. The agent can only influence which actions it takes, not what reward any given action produces.

- **Assuming exploration is wasteful.** Students sometimes think a greedy-only strategy is best because it always picks the highest-known action. In reality, without exploration, the agent may never discover the truly optimal action.

- **Treating Immediate RL and Full RL as the same problem.** The bandit problem (Immediate RL) has no sequential state transitions. Full RL has trajectories of states, actions, and rewards. The techniques and challenges are fundamentally different.

- **Forgetting that the TD update uses estimates, not true values.** Both $V(S_t)$ and $V(S_{t+1})$ are estimates. The update bootstraps -- it uses one estimate to improve another. This is powerful but introduces bias.

- **Setting the discount factor $\gamma = 1$ in infinite-horizon problems.** When $\gamma = 1$ and the task never ends, the return $G_t$ can diverge to infinity. The discount factor must be strictly less than 1 for infinite-horizon tasks to keep the return finite.

- **Confusing policy with value function.** The policy says what to do (action selection). The value function says how good a state is (evaluation). They are related but distinct.

---

## Self-Check Questions

<details>
<summary>Q1: What is the fundamental difference between reward and value in RL?</summary>

**Answer:** Reward is the immediate, single-step feedback from the environment -- a scalar number received at each time step. Value is the expected total cumulative reward the agent can accumulate from a state over the entire future. Reward tells the agent what is good right now; value tells the agent what is good in the long run. Values are estimated by the agent, while rewards are given by the environment.

</details>

<details>
<summary>Q2: Why can an agent not pursue only exploitation without failing?</summary>

**Answer:** If the agent only exploits (always selects the action with the highest known value), it never tries alternative actions that might actually be better. The agent's initial estimates may be inaccurate, and without exploring, it will get stuck with a sub-optimal action forever. The agent might miss the truly best action simply because it never tried it.

</details>

<details>
<summary>Q3: What distinguishes Immediate RL from Full RL?</summary>

**Answer:** Immediate RL deals with single-step decisions where the action does not affect future states. The bandit problem is the canonical example. Full RL deals with sequential decision-making where actions affect future states, forming trajectories $S_0, A_0, R_1, S_1, A_1, R_2, \ldots$. Full RL is harder because of delayed rewards and the credit assignment problem -- figuring out which past actions are responsible for current outcomes.

</details>

<details>
<summary>Q4: In the TD update rule, what does the term $V(S_{t+1}) - V(S_t)$ represent?</summary>

**Answer:** It represents the temporal difference error -- the difference between the estimated value of the next state and the estimated value of the current state. If this difference is positive, it means the next state is estimated to be more valuable than the current state, so the current state's estimate is revised upward. If negative, the current state's estimate is revised downward. The update adjusts the estimate based on the difference between predictions at two successive time steps.

</details>

<details>
<summary>Q5: What is the role of the discount factor $\gamma$ in the return?</summary>

**Answer:** The discount factor $\gamma$ ($0 \leq \gamma < 1$) determines how much the agent values future rewards relative to immediate rewards. A reward received $k$ steps in the future is weighted by $\gamma^k$. When $\gamma$ is close to 0, the agent is myopic and cares mostly about immediate reward. When $\gamma$ is close to 1, the agent is far-sighted and values future rewards nearly as much as present ones. Mathematically, $\gamma < 1$ also ensures that the infinite sum of discounted rewards converges to a finite value.

</details>

<details>
<summary>Q6: How do you determine whether policy $\pi_1$ is better than or equal to policy $\pi_2$?</summary>

**Answer:** Policy $\pi_1 \geq \pi_2$ if and only if $v_{\pi_1}(s) \geq v_{\pi_2}(s)$ for all states $s \in S$. That is, $\pi_1$ must produce equal or higher value at every single state in the environment. If even one state has a lower value under $\pi_1$, then $\pi_1$ is not considered uniformly better.

</details>

<details>
<summary>Q7: What is the difference between model-based and model-free RL?</summary>

**Answer:** In model-based RL, the agent has (or learns) a model that can predict the next state and reward given a current state and action. This model is used for planning -- evaluating potential future actions before taking them. In model-free RL, no such model is available. The agent must learn purely through direct trial-and-error interaction with the environment, without being able to simulate or predict what will happen before acting.

</details>

---

## Exam Focus

> **Paper 1, Q4 (10 marks):** Define Immediate RL vs Full RL.
>
> This is a definition-and-comparison question. You should:
> - Define Immediate RL as single-step decision-making (bandit problem), where actions do not affect future states
> - Define Full RL as sequential decision-making with trajectories $S_0, A_0, R_1, S_1, A_1, R_2, \ldots$
> - Explain that Full RL is harder because of delayed rewards and the credit assignment problem
> - Mention that in finite MDP (Full RL), $S$, $A$, $R$ are all finite and $R_t$, $S_t$ are random variables with well-defined probability distributions
> - Give a concrete example for each (e.g., slot machine for Immediate RL, robot navigation for Full RL)

> **Paper 1, Q1(b): Exploration-Exploitation.**
>
> Expect a question asking you to explain the exploration-exploitation dilemma. Cover:
> - Definition of exploration (trying new actions to discover better rewards)
> - Definition of exploitation (selecting known good actions to maximize reward)
> - Why neither can be pursued exclusively (leads to failure)
> - Mention that this is a distinguishing feature of RL not found in supervised/unsupervised learning

> **Paper 2, Q1: Role of Rewards.**
>
> Likely asks you to explain what rewards are and their role in RL. Cover:
> - Reward defines the goal of the RL problem
> - Single scalar number at each time step, sent by the environment
> - Agent maximizes total reward over the long run
> - Primary basis for altering the policy
> - Reward is immediate; value function is the long-term counterpart
> - Reward is out of the agent's direct control

**Likely question variations based on past paper patterns:**
- "Define policy, value function, and model of the environment" (define-and-explain format, likely 10 marks)
- "Explain the difference between reward and value function with an example" (comparison format)
- "Write the TD update rule and explain each term" (formula + explanation format)
- "What is the significance of the discount factor in the return formula?" (conceptual)

---

## Concept Links

- **Previous topic:** [RL Fundamentals](./01_rl_fundamentals.md) -- Covers the basics of RL, supervised vs unsupervised learning, MDP terms (agent, environment, state, action, reward)
- **Next topic:** [Bandit Problem](./03_bandit_problem.md) -- Applies Immediate RL concepts; covers greedy, epsilon-greedy, softmax, UCB methods for exploration vs exploitation
- **Related topic:** [Bellman Equation and Convergence](./06_bellman_and_convergence.md) -- Uses the value function and policy comparison concepts to prove optimal policy existence
- **Formula sheet:** [Formula Sheet](./08_formula_sheet.md) -- All key equations consolidated
