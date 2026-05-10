# Past Paper Analysis -- Reinforcement Learning CAT-1

**Course**: CSE4037 -- Reinforcement Learning
**University**: VIT-AP University
**Instructor**: Dr. D. John Pradeep
**Exam**: CAT-1 (Closed Book, 90 minutes, 50 marks)
**Coverage**: Modules 1 and 2
**Papers Analysed**: 2 (both dated 05/02/2026)

---

## 1. Frequency Table

The table below counts how many of the 2 papers contain at least one question (or sub-question) on each topic. A score of **2/2** means the topic appeared in every paper analysed.

| # | Topic | Paper 1 (Set 2, AN) | Paper 2 (Set 4, FN) | Frequency (out of 2) |
|---|-------|:-------------------:|:-------------------:|:--------------------:|
| 1 | RL application modelling (agent, environment, states, actions, rewards, policy) | Q1(a) | Q1 | **2/2** |
| 2 | Softmax algorithm -- numerical computation on MAB data table | Q2(a) | Q2(a) | **2/2** |
| 3 | Beta (temperature) parameter -- effect on exploration vs exploitation | Q2(b) | Q2(a),(b) | **2/2** |
| 4 | Contraction mapping -- definition, verification, iterative convergence | Q3(b) | Q3(b) | **2/2** |
| 5 | Banach Fixed Point Theorem (BFPT) and convergence of Bellman operator | Q3(a) | Q3(a) | **2/2** |
| 6 | Exploration vs exploitation trade-off (conceptual) | Q1(b) | Q2(b) | **2/2** |
| 7 | Fixed-point problem -- definition, mathematical formulation, relation to RL | Q3(a) partial | Q4 | **2/2** |
| 8 | Immediate RL vs Full RL -- definitions, return, difficulty | Q4 | -- | 1/2 |
| 9 | Cauchy sequence and convergence | Q4 | Q4 partial | **2/2** |
| 10 | PAC optimality -- definition, equation, sample complexity | Q5(a) | -- | 1/2 |
| 11 | UCB -- Upper Confidence Bound | Q5(a) | -- | 1/2 |
| 12 | Greedy vs epsilon-greedy comparison | Q5(b) | -- | 1/2 |
| 13 | L-infinity norm computation on value functions | Q5(c) | -- | 1/2 |
| 14 | Bellman expectation operator ($T^\pi$) and policy evaluation as fixed point | -- | Q3(a) | 1/2 |
| 15 | Business/practical perspective on beta selection (on-boarding vs high-confidence) | -- | Q2(b) | 1/2 |
| 16 | Existence and uniqueness via BFPT (full proof sketch) | -- | Q4 | 1/2 |

---

## 2. High-Priority Topics

These topics appeared in **every paper** (2/2). They are virtually guaranteed to appear again.

### Tier 1 -- Appears in every paper (2/2)

| Priority | Topic | Typical Marks | Typical Question Style |
|:--------:|-------|:------------:|------------------------|
| 1 | **Softmax numerical computation on MAB** | 6--10 | Given iteration table with actions and rewards, apply Softmax formula to compute selection probabilities for next iteration |
| 2 | **Beta parameter analysis** | 4--6 | Compare two beta values (e.g. beta=1 vs beta=100, or beta=5 vs beta=100) and discuss effect on exploration/exploitation |
| 3 | **RL application modelling** | 5--10 | Given a real-world scenario, identify agent/environment/states/actions/rewards/policy |
| 4 | **Contraction mapping -- verify and iterate** | 5--10 | Given a function, prove it is (or is not) a contraction; find contraction constant; perform iterative convergence from a starting point |
| 5 | **BFPT and Bellman convergence** | 5--10 | Explain how BFPT guarantees convergence of Bellman operator; describe the role of contraction mapping in proving optimality |
| 6 | **Exploration vs exploitation** | 3--5 | Discuss why balancing exploration and exploitation is critical for learning an optimal policy |
| 7 | **Fixed-point problem** | 5--10 | Define fixed-point problem mathematically; relate to RL (value function as fixed point of Bellman operator) |
| 8 | **Cauchy sequence** | 3--5 | Define Cauchy sequence; explain convergence; connect to BFPT proof |

> **Key insight**: Every single paper has a Softmax numerical problem worth 6+ marks. This is the single most predictable question. You must be able to compute $Q_t(a)$ for each arm from a data table, apply the Boltzmann formula, and calculate probabilities. Practise this until it is mechanical.

### Tier 2 -- Appears in 1/2 papers (likely to rotate)

| Topic | Appeared In | Notes |
|-------|:-----------:|-------|
| Immediate RL vs Full RL | Paper 1 | Definitions, return formulations, why Full RL is harder |
| PAC optimality | Paper 1 | $(\\epsilon, \\delta)$-PAC definition, sample complexity formula |
| UCB | Paper 1 | Usually paired with PAC in a comparison question |
| Greedy vs epsilon-greedy | Paper 1 | Short conceptual comparison (3 marks) |
| L-infinity norm computation | Paper 1 | Given two value function vectors, compute max absolute difference |
| Bellman expectation operator ($T^\pi$) | Paper 2 | Policy evaluation as finding fixed point of $T^\pi$ |
| Business perspective on beta | Paper 2 | Practical reasoning: low beta for exploitation (high-confidence), high beta for exploration (on-boarding) |
| BFPT full proof (uniqueness + existence) | Paper 2 | Proof by contradiction for uniqueness; Cauchy sequence argument for existence |

> **Key insight**: Tier 2 topics rotate between sets. The examiner uses different sets for AN and FN sessions. Prepare all Tier 2 topics -- you cannot predict which set you will receive.

---

## 3. Question Style Patterns

### Exam Structure

Both papers follow an identical structure:

| Feature | Observation |
|---------|-------------|
| Total marks | 50 |
| Number of questions | 5 (Paper 1) or 4 (Paper 2) |
| Marks per question | 10 each |
| Sub-parts | Most questions have (a) and (b) sub-parts, typically split 5+5 or 6+4 |
| Time | 90 minutes |
| Type codes used | E (Evaluate/Examine), A (Apply/Analyse), T (Think/Compare) |
| Module tags | Each question is tagged with Module 1, Module 2, or both |

### Examiner Preferences (Dr. D. John Pradeep)

| Pattern | Evidence |
|---------|----------|
| **Real-world scenario modelling** is always Q1 | Both papers open with a scenario (self-driving car, ad recommendation) requiring RL formulation |
| **Softmax numerical problem** is always Q2 | Both papers have a full data-table Softmax computation as Q2 |
| **BFPT / Contraction mapping** is always Q3 | Both papers place the mathematical convergence theory at Q3 |
| **Conceptual definitions** occupy Q4 | Immediate vs Full RL, or Fixed-point problem with BFPT proof |
| **Mixed short-answer / comparison** appears as Q5 (when present) | PAC vs UCB, greedy vs epsilon-greedy, L-infinity norm -- all in one question |
| Sub-questions tend to escalate: *define then compute* or *describe then prove* | e.g., Q3(a) asks for the concept, Q3(b) asks for a worked verification |
| Marks split favours computation | 6M for Softmax calculation, 4M for beta discussion |
| Negative rewards appear in data tables | Paper 1 includes rewards of -5, -2, -3 -- students must handle negative $Q_t(a)$ in the Softmax exponent |
| The examiner names specific theorems | "Banach's theorem", "Cauchy's sequence", "Bellman expectation operator" -- use the exact names in your answers |

> **Key insight**: The question ordering is not random. The examiner follows a fixed template: Q1 = scenario modelling, Q2 = numerical MAB, Q3 = BFPT/contraction, Q4 = definitions, Q5 = comparisons. Prepare in this order for maximum efficiency.

---

## 4. Recurring Question Templates

Below are the specific question formats that have appeared. Questions marked with a star are near-identical across papers.

### Template 1: RL Application Modelling (Q1, 10 marks)

**Format**: A real-world scenario is described. You must:
1. Examine whether RL can be applied and justify why (2--3 marks)
2. Formulate: states, actions, rewards, policy (5--7 marks)
3. Explain role of rewards and feedback loop (2--3 marks)

**Past instances**:
- Paper 1: Self-driving car
- Paper 2: Online ad recommendation based on user likes/dislikes

**Preparation**: Practise modelling at least 3--4 diverse scenarios (robotics, recommendation systems, game playing, resource allocation). Always include: agent identity, environment boundary, state representation, action space (discrete), reward signal design, and a one-line policy description.

---

### Template 2: Softmax Numerical Computation (Q2, 10 marks)

**Format**: A data table is given with columns for iteration number, action selected, and reward received. You must:
1. Compute $Q_t(a)$ for each arm using the sample average:

$Q_t(a) = \frac{\sum_{i=1}^{t} \mathbf{1}(a_i = a) \cdot R_i}{\sum_{i=1}^{t} \mathbf{1}(a_i = a)}$

2. Apply the Softmax (Boltzmann) selection formula:

$P(a_t = a) = \frac{e^{Q_t(a)/\beta}}{\sum_{b=1}^{n} e^{Q_t(b)/\beta}}$

3. Calculate the probability of selecting each arm at the *next* iteration (6 marks)
4. Compare two beta values and discuss their effect (4 marks)

**Past instances**:
- Paper 1: 3-arm MAB (A, B, C), 15 iterations, asked for 16th iteration probabilities with beta comparison (beta=5 vs beta=100)
- Paper 2: 3-arm MAB (Yaman, Bhairav, Todi), 10 iterations, asked for 11th day with beta comparison (beta=1 vs beta=100)

> **Key insight**: The number of arms is always 3. The number of iterations ranges from 10 to 15. Expect negative rewards in the data table. Always show the $Q_t(a)$ computation step before plugging into the Softmax formula.

---

### Template 3: Contraction Mapping Verification (Q3(b), 5 marks)

**Format**: One or two functions are given. You must:
1. Check the contraction condition: $d(f(x_1), f(x_2)) \leq \gamma \cdot d(x_1, x_2)$ for some $\gamma \in [0, 1)$
2. Find the contraction constant $\gamma$ (Lipschitz constant)
3. Identify which function is/is not a contraction
4. Find the fixed point analytically (solve $f(x) = x$)
5. Perform iterative computation from a given starting point to demonstrate convergence

**Past instances**:
- Paper 1: $T_1(x) = 0.9x + 1$ and $T_2(x) = 1.2x^2 + 3$ -- identify which is a contraction
- Paper 2: $f(x) = 0.25 \sin^2(x)$, $x_0 = 0.71$, perform 5 iterations

**Related examples from lecture slides**:
- $f(x) = (x + 3)/4$ on $X = [0, 2]$ (worked example in Module 2)
- $f(x) = 0.5 \sin(x)$ starting from $x_0 = 0.2$ (listed as previous exam question in slides)
- $f(x) = 0.25 \cos^2(x)$ starting from $x_0 = 0.2$ (listed as previous exam question in slides)

---

### Template 4: BFPT and Bellman Convergence (Q3(a), 5 marks)

**Format**: Explain the theoretical chain:
1. Define contraction mapping mathematically (2 marks)
2. State Banach Fixed Point Theorem (1--2 marks)
3. Explain how the Bellman optimality operator $B$ is a contraction in $(R^{|S|}, L_\infty)$ (2--3 marks)
4. Conclude: repeated application of $B$ converges to unique $V^*$, from which $\pi^*$ can be derived

**Variant (Paper 2)**: Frame as policy evaluation -- $T^\pi$ is the Bellman expectation operator, and finding $V^\pi$ is a fixed-point problem. Banach's theorem guarantees convergence because $T^\pi$ is a contraction with factor $\gamma$.

---

### Template 5: Immediate RL vs Full RL / Fixed-Point Definitions (Q4, 10 marks)

**Format A (Paper 1)**:
- Define Immediate RL (bandit setting: no state transitions, single-step rewards)
- Define Full RL (sequential decision-making with states, transitions, cumulative returns)
- Explain how return differs (immediate reward vs discounted cumulative return $G_t$)
- Why Full RL is harder (credit assignment, delayed rewards, state space explosion)
- Explain Cauchy sequence convergence

**Format B (Paper 2)**:
- Define fixed-point problem with mathematical justification: $f(x) = x$
- Relate to RL: value function $V$ is the fixed point of Bellman operator $T$
- Discuss existence and uniqueness via BFPT (complete metric space + contraction implies unique fixed point)

---

### Template 6: Short Comparison Questions (Q5, 10 marks split into 3 parts)

Only appeared in Paper 1. Combines multiple small topics:

| Sub-part | Topic | Marks |
|----------|-------|:-----:|
| (a) | Compare PAC optimality and UCB with equations | 3 |
| (b) | Greedy vs epsilon-greedy in RL context | 3 |
| (c) | L-infinity norm computation given two value function vectors | 4 |

**L-infinity norm computation format**:

Given $V_{\pi_1}(s) = [v_1, v_2, \ldots, v_n]$ and $V_{\pi_2}(s) = [w_1, w_2, \ldots, w_n]$, compute:

$\|V_1 - V_2\|_\infty = \max_s |V_{\pi_1}(s) - V_{\pi_2}(s)|$

---

## 5. Topics from Course Material Never Tested in CAT-1

The following topics appear in the Module 1 and Module 2 lecture slides but have **not** been directly tested in either past paper. They are lower priority for CAT-1 but should not be ignored entirely.

| Topic | Where in Slides | Why It May Not Have Been Tested | Risk of Appearing |
|-------|-----------------|--------------------------------|:-----------------:|
| Supervised vs Unsupervised vs RL comparison | Module 1, pp. 10--12 | Too basic; assumed prerequisite knowledge | Low |
| Pavlov's conditioning and RL analogy | Module 1, p. 16 | Motivational content, not examinable depth | Very Low |
| RL applications (Atari, helicopter, walking) | Module 1, pp. 13--15 | Covered implicitly in Q1 scenario modelling | Low |
| Temporal difference update formula | Module 1, p. 26 | Belongs more to Module 3 territory | Low |
| Formal MAB definition (probability distribution notation) | Module 1, p. 28 | Tested indirectly via Softmax computation | Low |
| Asymptotic correctness | Module 1, p. 30 | Appears in "notions for solving bandits" list but never asked standalone | Medium |
| Regret optimality (definition, log(T) bound) | Module 1, pp. 31--32 | Same as above; could appear as a short-answer | Medium |
| Metric space properties (4 axioms: identity, non-negativity, symmetry, triangle inequality) | Module 2, pp. 9--10 | Supporting concept for BFPT; could appear as a define-and-list question | Medium |
| Complete metric space (standalone definition) | Module 2, p. 13 | Usually embedded in BFPT explanation, not asked separately | Low |
| BFPT full proof -- existence part (triangular inequality chain, geometric series bound) | Module 2, pp. 24--27 | Lengthy derivation; only Paper 2 hints at "discuss existence and uniqueness" | Medium |
| Bellman optimality proof steps (inequality introduction, removing sigma) | Module 2, pp. 31--32 | The detailed proof steps of showing $B$ is a contraction; could be asked as "prove that Bellman operator is a contraction" | Medium |
| MDP dynamics $p(s', r \mid s, a)$ and Markov property formal definition | Module 1, pp. 52--53 | Could appear as a short definition question | Medium |
| Returns: three notions ($G_t$ sum, discounted, averaged) | Module 1, p. 51 | Partially tested via Immediate vs Full RL; the averaged return formula not specifically asked | Low |
| Optimal value functions and optimal policy definitions | Module 1, pp. 56--57 | Foundational but tested implicitly through BFPT questions | Low |
| Value function -- recursive relationship (Bellman equation derivation) | Module 1, p. 55 | Core concept but hasn't been a standalone question yet | Medium |
| Policy Gradient (mentioned in Module 1 syllabus) | Module 1 syllabus | Listed in syllabus but no slides provided; unlikely for CAT-1 | Very Low |

> **Key insight**: "Regret optimality", "Asymptotic correctness", and "Metric space axioms" are medium-risk topics that have not appeared yet but are clearly taught in the slides. A 3-mark short-answer question on any of these is plausible.

---

## 6. Predicted Questions for the Upcoming CAT-1

Based on the patterns, frequency analysis, and the examiner's demonstrated preferences, the following questions are predicted for the next CAT-1 exam.

### Prediction 1 (Very High Confidence): RL Application Modelling

**Predicted Question**: A new real-world scenario will be presented (e.g., a robot navigating a warehouse, a stock trading agent, a medical treatment recommender, or a traffic signal controller). You will be asked to:
- Examine whether RL is suitable for the problem
- Formulate states, actions, rewards, and policy
- Explain the role of the reward signal in guiding learning

**Reasoning**: This has appeared as Q1 in both papers with different scenarios. The examiner values the ability to map RL concepts to diverse applications. Expect 10 marks, split 5+5.

**Preparation**: Write out RL formulations for at least 4 scenarios not already used (self-driving car and ad recommendation are used). Good candidates:
- Game-playing agent (e.g., chess, Go)
- Inventory management / supply chain
- Personalized education / tutoring system
- Energy grid management

---

### Prediction 2 (Very High Confidence): Softmax Numerical Problem on MAB

**Predicted Question**: A data table with 10--15 iterations for a 3-arm bandit will be provided. You will need to:
- Compute $Q_t(a)$ for each arm at the end of the table
- Apply the Softmax formula with a given beta to find selection probabilities for the next iteration
- Compare two beta values and their effect

**Reasoning**: This is the most predictable question in the exam. It has appeared in identical format in both papers. The only variation is the specific numbers, arm labels, and beta values.

**Preparation**: Practise the full computation at least 3 times with different data tables. Key pitfalls to avoid:
- Forgetting to handle negative rewards when computing $Q_t(a)$
- Arithmetic errors in the exponent $Q_t(a)/\beta$
- Not showing the intermediate $Q_t(a)$ step (marks are awarded for working)

---

### Prediction 3 (Very High Confidence): Contraction Mapping Verification

**Predicted Question**: One or two functions will be given. You must:
- Show whether each is a contraction mapping (find the Lipschitz constant via the derivative: $|f'(x)| \leq \gamma < 1$)
- Find the fixed point by solving $f(x) = x$
- Iterate from a given starting point (typically 3--5 iterations) to demonstrate convergence

**Reasoning**: Both papers include this. The examiner draws from a pool of trigonometric and linear functions.

**Functions likely to appear** (based on lecture slide examples and past papers):
- $f(x) = 0.5 \sin(x)$ (mentioned in slides as previous exam question)
- $f(x) = 0.25 \cos^2(x)$ (mentioned in slides as previous exam question)
- $f(x) = (x + c)/k$ for some constants (lecture worked example)
- $f(x) = a \cdot \sin^2(x)$ or $f(x) = a \cdot \cos(x)$ for $a < 1$
- A non-contraction like $f(x) = 1.2x^2 + 3$ to test the negative case

---

### Prediction 4 (High Confidence): BFPT and Bellman Convergence Theory

**Predicted Question**: One of two variants:

*Variant A*: Describe contraction mapping mathematically. Explain how the Bellman optimality operator is a contraction. Use BFPT to prove that a unique optimal value function $V^*$ exists.

*Variant B*: Explain policy evaluation as finding the fixed point of the Bellman expectation operator $T^\pi$. How does Banach's theorem guarantee convergence?

**Reasoning**: Both variants have appeared (one per paper). The examiner may combine them or rotate.

---

### Prediction 5 (High Confidence): Fixed-Point Problem or Immediate vs Full RL

**Predicted Question**: One of two options:

*Option A*: Define the fixed-point problem. Give its mathematical form. Relate it to the RL domain (value function as fixed point of Bellman operator). Discuss existence and uniqueness via BFPT.

*Option B*: Define Immediate RL and Full RL. How does the return differ? Why is Full RL harder? Explain how Cauchy's sequence convergence is relevant.

**Reasoning**: These two question types have alternated between papers. Both are 10-mark definition-heavy questions.

---

### Prediction 6 (Medium Confidence): Short Comparison / Computation Mix

**Predicted Question**: A question with 2--3 sub-parts combining:
- PAC optimality vs UCB (with equations)
- Greedy vs epsilon-greedy (conceptual)
- L-infinity norm computation on value function vectors
- Possibly: Regret optimality definition (not yet tested but in slides)
- Possibly: Metric space axioms (not yet tested but in slides)

**Reasoning**: This format appeared only in Paper 1 (Set 2) as Q5. It may reappear if the paper has 5 questions, or it may be absorbed into other questions.

---

### Prediction 7 (Medium Confidence): Business/Practical Interpretation of Beta

**Predicted Question**: Given a Softmax-based system (e.g., recommendation, ad selection), discuss which beta value to use during:
- On-boarding / cold-start phase (high beta for exploration)
- Mature / high-confidence phase (low beta for exploitation)

**Reasoning**: Appeared in Paper 2. This connects the mathematical framework to practical decision-making, which aligns with course outcomes CO2 and CO6.

---

### Summary of Predictions

| # | Predicted Topic | Confidence | Expected Marks | Preparation Priority |
|---|----------------|:----------:|:--------------:|:--------------------:|
| 1 | RL application modelling (new scenario) | Very High | 10 | Must prepare |
| 2 | Softmax numerical computation on 3-arm MAB | Very High | 6--10 | Must prepare |
| 3 | Contraction mapping verification + iteration | Very High | 5--10 | Must prepare |
| 4 | BFPT and Bellman convergence explanation | High | 5--10 | Must prepare |
| 5 | Fixed-point problem or Immediate vs Full RL | High | 10 | Must prepare |
| 6 | Short comparisons (PAC/UCB, greedy/epsilon-greedy, L-inf norm) | Medium | 3--10 | Should prepare |
| 7 | Business interpretation of beta parameter | Medium | 4 | Should prepare |

> **Final recommendation**: If time is limited, allocate study effort in this order: (1) Softmax numerical computation -- drill this until it is automatic, (2) Contraction mapping verification with iteration, (3) RL scenario modelling -- prepare 4 templates, (4) BFPT theory and Bellman convergence chain, (5) Definitions (fixed-point, Immediate vs Full RL, Cauchy sequence), (6) Short comparison topics. Together, items 1--5 cover a minimum of 40 out of 50 marks on any plausible paper.
