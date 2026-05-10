# RL Fundamentals

**Source**: Module 1 (Module1.pdf), Slides 10--19 | **Coverage**: Introduction, ML Paradigms, RL Characteristics, MDP Terms

---

## Learning Objectives

After completing this section, you should be able to:

- Distinguish between supervised learning, unsupervised learning, and reinforcement learning in terms of data, feedback, and goals
- Explain why reinforcement learning is considered a hybrid approach and how it mimics human learning
- List and define the five core MDP terms: agent, environment, state, action, reward
- Identify the two most important distinguishing features of RL (trial-and-error search and delayed rewards)
- Describe at least three real-world applications of RL
- Model a given real-world scenario as an RL problem by specifying agent, environment, states, actions, rewards, and policy (a high-priority exam skill)

---

## Ground-Up Explanation

### Introduction to Machine Learning Paradigms

Machine learning (ML) is a branch of artificial intelligence where systems learn patterns from data rather than being explicitly programmed. There are three major paradigms of machine learning, each defined by the type of data they use, the feedback mechanism available, and the goal they try to achieve.

The three paradigms are:

1. **Supervised Learning**
2. **Unsupervised Learning**
3. **Reinforcement Learning**

Understanding how they differ is essential, because RL borrows characteristics from both supervised and unsupervised learning while being fundamentally distinct from either.

---

### Supervised Learning

**Supervised learning** uses **labelled data** for training. Each training example comes with an input and a corresponding correct output (the "label"). The model learns a mapping from inputs to outputs by receiving **feedback** -- it checks whether its prediction matches the label and adjusts accordingly.

**Key characteristics:**

- Uses labelled data for training
- Model requires feedback to train (checks if predictions are correct)
- Output is predicted by the model
- The model is trained so it can predict the output when new, unseen data is presented
- Considered "Not AI" in the slides (in contrast to unsupervised learning)

**Common algorithms:**

| Algorithm | Type |
|-----------|------|
| Linear Regression | Regression |
| Logistic Regression | Classification |
| Support Vector Machines (SVMs) | Classification |
| Decision Trees | Classification / Regression |
| Bayesian Logic | Probabilistic Classification |

**Example:** Given thousands of images of cats and dogs, each labelled "cat" or "dog," a supervised model learns to classify new images it has never seen before.

---

### Unsupervised Learning

**Unsupervised learning** works with **unlabelled data**. There is **no feedback mechanism** telling the model whether it is right or wrong. Instead, the model must discover **hidden patterns** within the data on its own.

**Key characteristics:**

- Uses unlabelled data for training
- No feedback mechanism
- Hidden lying patterns in the data are learnt
- Main goal is to find the hidden patterns in the input dataset
- Considered "True AI" in the slides

**Common algorithms:**

| Algorithm | Purpose |
|-----------|---------|
| Clustering (e.g., K-Means) | Group similar data points |
| KNN (K-Nearest Neighbours) | Find similar items based on proximity |
| Apriori Algorithm | Discover association rules in transaction data |

**Example:** Given customer purchase data with no labels, an unsupervised algorithm groups customers into clusters based on buying behaviour, without being told what the groups should be.

---

### Reinforcement Learning -- The Hybrid Approach

**Reinforcement learning (RL)** does not fit neatly into either category. It is a **hybrid machine learning process** that shares traits with both:

- Like supervised learning, RL **uses feedback** to train the model.
- Like unsupervised learning, RL **does not use labelled data**.

Instead of learning from a pre-built dataset of correct answers, an RL agent learns through **trial and error**. It takes actions in an environment, receives numerical rewards (feedback), and gradually discovers which actions lead to the best outcomes.

> **Key Insight:** RL mimics human learning patterns. Just as a child learns to walk by trying different movements and experiencing the consequences (falling down vs. staying upright), an RL agent learns by interacting with its environment and observing rewards.

**Summary comparison:**

| Feature | Supervised Learning | Unsupervised Learning | Reinforcement Learning |
|---------|--------------------|-----------------------|------------------------|
| Data | Labelled | Unlabelled | No labels; generated through interaction |
| Feedback | Yes (correct labels) | No | Yes (numerical reward) |
| Goal | Predict output | Find hidden patterns | Maximize cumulative reward |
| Learning method | Learn from examples | Discover structure | Trial and error |
| Considered | Not AI | True AI | Hybrid |

---

### Pavlov's Conditioning -- The Biological Analogy for RL

The slides draw a direct analogy between RL and **classical conditioning**, discovered by **Ivan Petrovich Pavlov (1849--1936)**, a Russian physiologist.

**Pavlov's experiment:**

1. An unconditioned stimulus (food) naturally produces a response (salivating)
2. A new conditioned stimulus (ringing of a bell) is paired repeatedly with food
3. Eventually, the bell alone produces salivation -- the dog has **learned** to associate the bell with food

This is analogous to RL: the agent learns to associate certain actions (the "bell") with certain rewards (the "food") through repeated interaction. The agent is not told in advance which action leads to which reward -- it must discover this through experience, just as Pavlov's dog learned through repeated pairing.

---

### RL Characteristics -- Formal Description

The slides define RL through several key characteristics:

1. **Learning from interaction** -- this is the foundational idea of RL
2. **Goal-directed learning** -- RL is goal-directed learning from interaction
3. **State-action mapping** -- RL is about learning what to do (which **action** to take) in a particular situation (which **state** the environment is in)
4. **Reward maximization** -- the agent maps actions to states by **maximizing a numerical reward**
5. **Formalized as MDP** -- the RL problem is formalized as a **Markov Decision Process (MDP)**. MDPs frame the problem of learning from interaction to achieve a goal.

> **CRITICAL CONCEPT**
>
> Trial-and-error search and delayed rewards are the **two most important distinguishing features** of reinforcement learning. These two properties set RL apart from all other forms of machine learning.

**Trial-and-error search:** The learner is not told which action to take in a given situation. It must **discover** which actions yield the most reward by trying them (exploring).

**Delayed rewards:** Actions may not only affect the immediate reward but also the next situation and, through that, **all subsequent rewards**. The consequence of an action may not be felt until many steps later.

---

### RL Applications

The course material highlights three landmark applications of RL:

**1. Inverted Helicopter Flight**
An RL agent learned to fly a helicopter in inverted (upside-down) orientation -- a feat that is extremely difficult to program manually because the physics of helicopter flight are complex and nonlinear. The agent learned through trial and error in simulation.

**2. Atari Games**
DeepMind's RL agent (DQN) learned to play Atari 2600 games (such as Breakout and Pong) at a superhuman level, receiving only the raw pixel screen as input and the game score as the reward signal. No game-specific knowledge was provided.

**3. Learning to Walk**
RL agents have been trained to control simulated robots to walk, run, and navigate terrain. The agent discovers gait patterns through trial and error, receiving positive reward for forward movement and negative reward for falling.

---

### MDP Terms -- The Core Vocabulary

The Markov Decision Process (MDP) provides the formal framework for RL problems. Five terms form the foundation:

| Term | Definition |
|------|-----------|
| **Agent** | The learner and decision maker. It is the entity that takes actions and receives rewards. |
| **Environment** | The thing the agent interacts with. Everything outside the agent that responds to its actions. |
| **State** | The situation of the environment at a given time. It captures all relevant information about the current configuration. |
| **Action** | The steps the agent performs on the environment. Actions alter the state of the environment. |
| **Reward** | The numerical acknowledgment received by the agent for the action performed, from the environment. It is a scalar signal indicating how good or bad the action was. |

> **Figure: The RL Interaction Loop**
>
> ```
> +-------+    action (A_t)     +-----------+
> |       | -----------------> |           |
> | Agent |                    |Environment|
> |       | <----------------- |           |
> +-------+  state (S_t),      +-----------+
>            reward (R_t)
> ```
>
> At each time step `t`:
> 1. The agent observes the current state `S_t`
> 2. The agent selects an action `A_t`
> 3. The environment transitions to a new state `S_{t+1}`
> 4. The environment returns a reward `R_{t+1}` to the agent
> 5. The cycle repeats

---

### Two Distinguishing Features of RL (Expanded)

These two features are worth memorizing explicitly, as the slides emphasize them:

**1. Trial-and-error search:**
- The agent takes actions to maximize the numerical reward signal
- The learner is **not told** which action to take in a given situation
- It must **discover** which actions yield the most reward by trying them (exploring)

**2. Delayed rewards:**
- Actions may affect not only the **immediate** reward but also the **next situation** and, through that, all **subsequent** rewards
- This means the agent must consider long-term consequences, not just immediate payoff

---

## Analogies

**The Restaurant Analogy for ML Paradigms:**

Think of learning to cook a new cuisine.

- **Supervised learning** is like having a cookbook with exact recipes (labelled data). You follow the recipe (input), and you know exactly what the dish should taste like (label). If it does not match, you adjust.

- **Unsupervised learning** is like being given a pantry full of unlabelled ingredients from an unfamiliar culture. You have no recipes. You experiment, group similar ingredients together, and discover flavour combinations on your own.

- **Reinforcement learning** is like being placed in a kitchen with a food critic (the environment). You have no recipes (no labelled data), but after each dish you cook (action), the critic gives you a score from 1 to 10 (reward). Over many attempts (trial and error), you learn which ingredient combinations and techniques (policy) produce the highest scores. Sometimes a technique that seems bad now (e.g., marinating overnight) only pays off the next day (delayed reward).

**The Maze Analogy for MDP Terms:**

Imagine a mouse (agent) navigating a maze (environment). Each junction in the maze is a state. At each junction, the mouse can go left, right, or straight (actions). Some paths lead to cheese (positive reward), others to dead ends (zero reward), and one leads to a trap (negative reward). The mouse has no map -- it must explore the maze through trial and error and remember which paths led to cheese.

---

## Key Formulas

This section covers introductory concepts, so there are no complex formulas. The key "formula" is the **RL interaction loop**, which can be expressed as:

$$
S_t \xrightarrow{A_t} (R_{t+1}, S_{t+1})
$$

> **Where:**
> - $S_t$ = state of the environment at time step $t$
> - $A_t$ = action taken by the agent at time step $t$
> - $R_{t+1}$ = reward received from the environment after the action
> - $S_{t+1}$ = new state of the environment after the action

The trajectory of an RL agent over time is:

$$
S_0, A_0, R_1, S_1, A_1, R_2, S_2, A_2, \ldots
$$

This trajectory notation appears in the later "Full RL" slides and is useful to remember.

---

## Worked Examples

### Example 1: Modelling a Self-Driving Car as an RL Problem

> **Problem (Past Paper style, 10 marks):** A self-driving car aims to navigate safely and makes real-time decisions such as accelerating, braking, and changing lanes. Examine whether Reinforcement Learning can be used for solving this problem. If yes, explain how RL can be applied, including the formulation of states, actions, rewards, and policy. If not, justify why another learning method would be more suitable.

**Solution:**

Yes, Reinforcement Learning is well-suited for this problem because:
- The car must make sequential decisions in a dynamic environment
- There is no single "correct" label for each driving situation (unlike supervised learning)
- The car learns from interaction with the road environment through trial and error
- Rewards are delayed -- a lane change decision now affects safety seconds later

**RL Formulation:**

| MDP Component | Self-Driving Car Mapping |
|---------------|------------------------|
| **Agent** | The self-driving car's decision-making system (the AI controller) |
| **Environment** | The road, including other vehicles, pedestrians, traffic signals, lane markings, weather conditions |
| **States** | Current speed, position on road, distance to nearby vehicles, traffic light status, lane position, sensor readings (LiDAR, camera) |
| **Actions** | Accelerate, brake, turn left, turn right, change lane left, change lane right, maintain speed |
| **Rewards** | +ve reward for: safe driving, reaching destination, maintaining speed limit, staying in lane. -ve reward for: collision, running red light, harsh braking, going off-road. Large -ve reward for accidents. |
| **Policy** | The learned mapping from the current driving situation (state) to the best driving action. For example: "When a vehicle ahead is braking and distance is less than 10m, apply brakes." |

**Why not other methods?**
- Supervised learning would require labelled data for every possible driving scenario, which is impractical to collect exhaustively
- Unsupervised learning has no feedback mechanism and cannot optimize for safety
- RL is ideal because the car can learn through simulation (trial and error) with clear reward signals for safe vs. unsafe behaviour

---

### Example 2: Modelling Advertisement Selection as an RL Problem

> **Problem (Past Paper style, 10 marks):** A company selects its advertisements based on feedback received from users, such as likes and dislikes. Explain how this advertisement selection problem can be modelled using Reinforcement Learning by identifying the agent, environment, actions, and rewards. Explain the role of rewards in reinforcement learning and discuss how user feedback enables the system to improve advertisement selection.

**Solution:**

**RL Formulation:**

| MDP Component | Advertisement Selection Mapping |
|---------------|-------------------------------|
| **Agent** | The advertisement recommendation system (the algorithm deciding which ad to show) |
| **Environment** | The user population and the platform through which ads are displayed |
| **States** | User profile information (age, browsing history, past ad interactions, time of day, device type, current page content) |
| **Actions** | Select which advertisement to display to the user from the available ad inventory |
| **Rewards** | +ve reward for: user clicks the ad, user likes/engages with the ad, user makes a purchase. -ve reward for: user skips the ad, user dislikes the ad, user installs ad blocker. The magnitude of reward can vary (a purchase is worth more than a click). |
| **Policy** | The learned strategy mapping user state to the best ad to display. For example: "For users aged 18-25 browsing sports content in the evening, show sportswear ads." |

**Role of rewards:**
- Rewards define the goal of the RL problem -- they tell the agent what is good (user engagement) and what is bad (user annoyance)
- The reward signal is the **primary basis for altering the policy**. If showing a particular ad to a particular user segment results in low engagement (low reward), the policy updates to try a different ad for that segment
- Rewards are **immediate** (click/no-click) but also have **delayed** effects -- showing too many irrelevant ads may cause a user to leave the platform entirely, which is a long-term negative consequence

**Why RL is suitable:**
- User preferences are not fully known in advance (no complete labelled dataset)
- The system must balance **exploration** (trying new ads to discover preferences) with **exploitation** (showing ads known to perform well)
- This is precisely the exploration-exploitation trade-off that RL is designed to handle

---

### Example 3: Real-Time Application Examples (SL, UL, RL)

> **Problem (Past Paper 2, Q5c, 3 marks):** Provide one real-time application example for supervised, unsupervised, and reinforcement learning.

**Solution:**

| Paradigm | Real-Time Application | Explanation |
|----------|----------------------|-------------|
| **Supervised Learning** | Email spam detection | The system is trained on a labelled dataset of emails marked "spam" or "not spam." It learns patterns (certain keywords, sender addresses) to classify new incoming emails. |
| **Unsupervised Learning** | Customer segmentation in retail | Given unlabelled customer transaction data, clustering algorithms group customers into segments (e.g., frequent buyers, bargain hunters, seasonal shoppers) without predefined labels. |
| **Reinforcement Learning** | Robot navigation in a warehouse | A robot learns to navigate a warehouse to pick and deliver packages. It receives positive rewards for successful deliveries and negative rewards for collisions or delays. No pre-programmed path is given. |

---

## Common Mistakes

- **Confusing RL with supervised learning because both use feedback.** The critical difference is that supervised learning has labelled data (the "correct answer" is given for each input), while RL only receives a scalar reward signal that indicates how good an action was -- not what the correct action should have been.

- **Saying RL is unsupervised learning because it has no labels.** While RL does not use labels, it does use a reward signal (feedback), which unsupervised learning does not have. RL is a distinct paradigm, not a subset of unsupervised learning.

- **Confusing state with environment.** The environment is the entire external system; the state is a snapshot of the environment's situation at a particular moment. The environment persists; states change over time.

- **Confusing reward with value.** Reward is the immediate numerical signal received after an action. Value (covered in the next file) is the expected total accumulated reward from a state going forward. A state might have low immediate reward but high value if it leads to a rewarding path.

- **Forgetting delayed rewards when modelling RL problems.** In exam questions asking you to model a scenario as RL, students often only describe immediate rewards. Always mention that actions can have long-term consequences (delayed rewards) and explain how the policy should account for this.

- **Omitting the policy in RL modelling questions.** Past papers ask for agent, environment, states, actions, rewards, **and policy**. Do not forget to describe what the learned mapping would look like.

- **Listing KNN as supervised learning.** The slides list KNN under unsupervised learning algorithms. Be consistent with the course material in the exam, even if other textbooks classify KNN differently.

---

## Self-Check Questions

<details>
<summary>Q1: What are the three main paradigms of machine learning, and what is the key distinguishing factor for each?</summary>

**Answer:**
1. **Supervised Learning** -- uses labelled data and feedback; goal is to predict output for new inputs
2. **Unsupervised Learning** -- uses unlabelled data with no feedback; goal is to find hidden patterns in data
3. **Reinforcement Learning** -- uses feedback (reward) but no labelled data; goal is to maximize cumulative reward through trial and error

The key distinguishing factors are: (a) whether labelled data is used, (b) whether feedback is provided, and (c) the nature of the learning goal.

</details>

<details>
<summary>Q2: Why is RL called a "hybrid" machine learning process?</summary>

**Answer:** RL is called hybrid because it borrows characteristics from both supervised and unsupervised learning. Like supervised learning, it uses feedback to train (the reward signal). Like unsupervised learning, it does not use labelled data. It combines these aspects with its unique trial-and-error approach.

</details>

<details>
<summary>Q3: What are the two most important distinguishing features of RL?</summary>

**Answer:** Trial-and-error search and delayed rewards. The agent must discover which actions yield the most reward by trying them (it is not told the correct action). Actions affect not only immediate rewards but also future states and all subsequent rewards.

</details>

<details>
<summary>Q4: Define all five MDP terms.</summary>

**Answer:**
- **Agent**: The learner and decision maker
- **Environment**: The thing the agent interacts with; everything external to the agent
- **State**: The situation of the environment at a given time
- **Action**: The steps the agent performs on the environment; actions alter the state
- **Reward**: The numerical acknowledgment received by the agent from the environment for the action performed

</details>

<details>
<summary>Q5: How does Pavlov's conditioning relate to reinforcement learning?</summary>

**Answer:** In Pavlov's experiment, a dog learned to associate a neutral stimulus (bell) with an unconditioned stimulus (food) through repeated pairing, eventually producing a conditioned response (salivating at the bell alone). Similarly, in RL, an agent learns to associate certain actions with certain rewards through repeated interaction with the environment. Neither the dog nor the RL agent is told the "correct" response in advance -- both learn through experience and feedback.

</details>

<details>
<summary>Q6: Model a music streaming platform that recommends playlists as an RL problem. Identify agent, environment, states, actions, and rewards.</summary>

**Answer:**
- **Agent**: The playlist recommendation algorithm
- **Environment**: The user and the music streaming platform
- **States**: User's listening history, current mood/time of day, genre preferences, skip rate, device type
- **Actions**: Recommend one of several playlists (e.g., Yaman, Bhairav, Todi -- as in past paper Q2)
- **Rewards**: Number of minutes the user listens to the recommended playlist (longer listening = higher reward; skipping = low/negative reward)
- **Policy**: The learned strategy that maps user state to the best playlist recommendation

</details>

<details>
<summary>Q7: Name three algorithms used in supervised learning and three used in unsupervised learning, as listed in the course material.</summary>

**Answer:**
- **Supervised Learning**: Linear regression, logistic regression, SVMs (also: decision trees, Bayesian logic)
- **Unsupervised Learning**: Clustering, KNN, Apriori algorithm

</details>

---

## Exam Focus (from Past Papers)

### How This Topic Has Been Examined

This is a **high-priority exam topic**. Both available past papers (Set 2 AN and Set 4 FN, dated 05/02/2026) include a Question 1 worth **10 marks** that tests the ability to model a real-world scenario as an RL problem.

| Paper | Question | Marks | What Was Asked |
|-------|----------|-------|----------------|
| Paper 1 (Set 2, AN) | Q1(a) | 5 M | Model a self-driving car as RL: identify states, actions, rewards, policy. Justify why RL over other methods. |
| Paper 1 (Set 2, AN) | Q1(b) | 5 M | Explain exploration-exploitation trade-off and why both are critical for learning an optimal policy. |
| Paper 2 (Set 4, FN) | Q1(a) | 5 M | Model advertisement selection as RL: identify agent, environment, actions, rewards. |
| Paper 2 (Set 4, FN) | Q1(b) | 5 M | Role of rewards in RL; how user feedback improves ad selection. |
| Paper 1 (Set 2, AN) | Q5c (partial) | -- | Given value functions for two policies, compare them (related topic). |
| Paper 2 (Set 4, FN) | Q5c (partial) | 3 M | Provide one real-time application example for SL, UL, and RL. |

### Key Patterns

1. **Always expect a modelling question (Q1, 10 marks).** You will be given a real-world scenario and asked to formulate it as an RL problem. You must identify: agent, environment, states, actions, rewards, and policy.

2. **Justify why RL is suitable.** The question often asks you to explain why RL is appropriate (or why another method is not). Use the comparison table: no labelled data available, feedback exists through interaction, sequential decision-making, delayed consequences.

3. **The exploration-exploitation trade-off** frequently appears alongside fundamentals (Paper 1, Q1b). While it is covered in more detail in the next file, be prepared to explain it here: the agent must explore new actions to discover better rewards but also exploit known good actions. Pursuing only one leads to failure.

4. **Real-time application examples** for all three paradigms have been asked (Paper 2, Q5c). Prepare one clear example for each.

### Likely Variations

- A different real-world scenario (e.g., traffic signal control, game playing, stock trading, robot arm manipulation)
- Same question structure: "Model X as RL. Identify agent, environment, states, actions, rewards, and policy."
- May ask you to also describe what the optimal policy would look like
- May combine with asking you to compare RL with SL and UL for the given problem

### Exam Answer Template for RL Modelling Questions

When answering a 10-mark RL modelling question, structure your answer as follows:

1. **State that RL is applicable** and briefly justify (1-2 sentences)
2. **Identify each MDP component** in a clear table or list format:
   - Agent
   - Environment
   - States (list at least 3-4 concrete state variables)
   - Actions (list at least 3-4 specific actions)
   - Rewards (describe both positive and negative rewards with examples)
   - Policy (describe what the learned mapping would look like with a concrete example)
3. **Explain why RL is preferred** over SL and UL (2-3 sentences)
4. **Mention delayed rewards** and give a concrete example from the scenario

---

## Concept Links

- **Next**: [Elements of RL](./02_elements_of_rl.md) -- covers policy, value function, model, and the exploration vs. exploitation trade-off in detail
- **Related**: [Bandit Problem](./03_bandit_problem.md) -- the simplest RL setting (single state), where exploration vs. exploitation is the central challenge
- **Formula reference**: [Formula Sheet](./08_formula_sheet.md) -- all equations organized by topic
- **Practice**: [Worked Problems](./07_worked_problems.md) -- past paper solutions for RL modelling questions
