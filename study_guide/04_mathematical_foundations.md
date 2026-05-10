# Module 4 -- Mathematical Foundations for RL

**Prerequisites:** Basic algebra, comfort with sequences and limits
**Builds toward:** [05_contraction_and_bfpt.md](./05_contraction_and_bfpt.md), [06_bellman_and_convergence.md](./06_bellman_and_convergence.md)
**Exam relevance:** Paper 1 Q4 (5M), Paper 2 Q4 (10M)

---

## 1. Learning Objectives

By the end of this module you should be able to:

| # | Objective | Bloom's Level |
|---|-----------|---------------|
| 1 | Define a fixed point problem and distinguish it from root finding | Understand |
| 2 | Explain the iterative method for solving fixed point problems and state the convergence result | Understand |
| 3 | State the four properties of a metric and give an example of a metric space | Remember |
| 4 | Define a Cauchy sequence and explain its intuition | Understand |
| 5 | Define a complete metric space and explain why completeness matters | Understand |
| 6 | Connect these foundations to the Banach Fixed Point Theorem (covered next module) | Apply |

---

## 2. Ground-Up Explanation

### 2.1 Fixed Point Problem

In standard mathematics, much of our effort goes toward solving equations of the form:

$
f(x) = 0
$

This is called **root finding** -- we look for a value of $x$ that makes the function equal to zero.

A **fixed point problem** asks a different question. Instead of finding where the function hits zero, we ask: where does applying the function leave the input unchanged?

> **Definition -- Fixed Point.**
> A value $x^*$ is a fixed point of a function $f$ if and only if:
>
> $
> f(x^*) = x^*
> $
>
> In words: plugging $x^*$ into $f$ gives back $x^*$ itself. The point does not move under the function.

**Why should we care in RL?** The Bellman equation, which is at the heart of reinforcement learning, is a fixed point equation. The optimal value function $V^*$ is defined as the fixed point of the Bellman operator $B$. That is, $B(V^*) = V^*$. Everything in Modules 5 and 6 depends on this idea.

**Relationship to root finding.** Any fixed point problem can be rewritten as a root-finding problem. Define a helper function:

$
g(x) = f(x) - x
$

Then $f(x^*) = x^*$ is equivalent to $g(x^*) = 0$. The two formulations are mathematically interchangeable, but the fixed point form is more natural for iterative algorithms -- which is exactly what RL uses.

---

### 2.2 Solving Fixed Point Problems by Iteration

The beauty of fixed point problems is that they suggest their own solution method: just keep applying the function.

**Algorithm:**

1. Pick any starting guess $x_0$ (can be random or arbitrary).
2. Compute $x_1 = f(x_0)$.
3. Compute $x_2 = f(x_1) = f(f(x_0))$.
4. Continue: $x_{n+1} = f(x_n)$.
5. Repeat infinitely (or until the values stop changing appreciably).

If the function has the right properties (specifically, if it is a **contraction** on a **complete metric space** -- see Modules 5 and 6), this sequence converges to the fixed point regardless of where you started.

> **Key Result -- Iterative Convergence.**
>
> $
> x^* = \lim_{n \to \infty} f^n(x_0)
> $
>
> where $f^n$ means "$f$ applied $n$ times" (function composition, not exponentiation).

**Why does $x^*$ satisfy $f(x^*) = x^*$?** Here is the formal justification:

$
f(x^*) = f\!\left(\lim_{n \to \infty} f^n(x_0)\right) = \lim_{n \to \infty} f\!\left(f^n(x_0)\right) = \lim_{n \to \infty} f^{n+1}(x_0) = x^*
$

Step by step:

1. We substitute the definition $x^* = \lim_{n \to \infty} f^n(x_0)$.
2. We pull $f$ inside the limit (valid when $f$ is continuous).
3. We recognize that $f(f^n(x_0)) = f^{n+1}(x_0)$.
4. The limit of $f^{n+1}(x_0)$ as $n \to \infty$ is the same as the limit of $f^n(x_0)$ as $n \to \infty$, which is $x^*$.

Therefore $f(x^*) = x^*$, confirming that the iterative limit is indeed a fixed point.

---

### 2.3 Metric Space

Before we can talk rigorously about convergence, we need a way to measure "distance" between objects. This is what a metric space provides.

> **Definition -- Metric Space.**
> A metric space is a pair $(X, d)$ where:
> - $X$ is a set (of points, vectors, functions, etc.)
> - $d: X \times X \to \mathbb{R}$ is a **metric** (distance function)
>
> The metric $d$ must satisfy the following four properties for all $x, y, z \in X$:

| # | Property | Statement | Intuition |
|---|----------|-----------|-----------|
| 1 | Identity of indiscernibles | $d(x, x) = 0$ | The distance from any point to itself is zero |
| 2 | Non-negativity (positivity) | $d(x, y) > 0$ for $x \neq y$ | Distinct points always have positive distance |
| 3 | Symmetry | $d(x, y) = d(y, x)$ | Distance from A to B equals distance from B to A |
| 4 | Triangle inequality | $d(x, z) \leq d(x, y) + d(y, z)$ | A direct path is never longer than a detour |

**Example.** The most familiar metric space is Euclidean space $(\mathbb{R}^n, d)$ where:

$
d(x, y) = \|x - y\|_2 = \sqrt{\sum_{i=1}^{n}(x_i - y_i)^2}
$

In general, any norm $\|\cdot\|$ on a vector space induces a metric via $d(x, y) = \|x - y\|$. In RL we often use the **infinity norm** (or max norm) $\|\cdot\|_\infty$, which leads to a different but equally valid metric space.

---

### 2.4 Cauchy Sequence

A Cauchy sequence captures the idea that the terms of a sequence are "bunching together" as we go further out, even if we do not yet know what they are converging to.

> **Definition -- Cauchy Sequence.**
> Let $(X, d)$ be a metric space. A sequence $(x_1, x_2, \ldots, x_n, \ldots)$ of elements in $X$ is called a **Cauchy sequence** if for every $\varepsilon > 0$ (no matter how small), there exists a positive integer $N$ such that:
>
> $
> d(x_a, x_b) < \varepsilon \quad \text{for all } a, b > N
> $

**Unpacking the definition:**

- Pick any tiny tolerance $\varepsilon$ (say $0.001$).
- A Cauchy sequence guarantees there is some cutoff index $N$ beyond which every pair of terms is within $\varepsilon$ of each other.
- The further out you go, the closer the terms get to each other.
- Crucially, this definition talks only about terms of the sequence being close **to each other** -- it says nothing about whether a limit point exists.

**Intuition:** Imagine you are walking along a path and each step gets smaller and smaller. Eventually, your steps become so tiny that you are barely moving at all. The sequence of your positions is Cauchy -- beyond some point, all positions are within any given tolerance of one another.

---

### 2.5 Complete Metric Space

Cauchy sequences tell us that terms are clustering together, but they do not guarantee the cluster point actually lives in our space. Completeness fills that gap.

> **Definition -- Complete Metric Space.**
> A metric space $(X, d)$ is **complete** if every Cauchy sequence of elements in $X$ converges to a limit that is also an element of $X$.

In other words: if a sequence in $X$ "wants" to converge (its terms are getting arbitrarily close), then the space does not have any "holes" -- the limit actually exists within $X$.

**Why does completeness matter?** The iterative fixed point method (Section 2.2) produces a Cauchy sequence. If the space is complete, that sequence is guaranteed to converge to a point in the space. Without completeness, the sequence might try to converge to a point that is "missing" from the space, and the whole argument falls apart.

| Space | Complete? | Why |
|-------|-----------|-----|
| $\mathbb{R}$ (real numbers) | Yes | Every Cauchy sequence of reals converges to a real number |
| $\mathbb{Q}$ (rationals) | No | The sequence $3, 3.1, 3.14, 3.141, \ldots$ is Cauchy in $\mathbb{Q}$ but converges to $\pi \notin \mathbb{Q}$ |
| $\mathbb{R}^n$ with Euclidean metric | Yes | Standard result from analysis |
| Set of all bounded functions with $\|\cdot\|_\infty$ | Yes | This is the space used for value functions in RL |

---

## 3. Analogies

| Concept | Analogy |
|---------|---------|
| **Cauchy sequence** | A GPS approaching a destination. Each reported position is closer to the previous one. Beyond some point, all reported positions are within 1 meter of each other, then within 10 cm, then within 1 cm. The positions are "Cauchy" -- they are bunching together tighter and tighter. |
| **Complete metric space** | A room with no exits. If you keep walking in a Cauchy pattern (steps getting smaller and smaller), you must end up at some point inside the room. The room cannot have a hidden hole in the floor that you fall through. The limit of your walk is guaranteed to be a point in the room. |
| **Fixed point** | A whirlpool in a river. No matter where you drop a leaf in the basin, the current (the function) carries it closer and closer to the center. At the center itself, the leaf stays put -- it is the fixed point. |
| **Iterative convergence** | Adjusting a thermostat. You set a temperature (starting guess). The system overshoots, then corrects, then overshoots less. Each cycle (function application) gets closer to the target temperature (fixed point). |

---

## 4. Key Formulas

> **Fixed point condition:**
>
> $
> f(x^*) = x^*
> $

> **Conversion to root finding:**
>
> $
> g(x) = f(x) - x = 0
> $

> **Iterative convergence to fixed point:**
>
> $
> x^* = \lim_{n \to \infty} f^n(x_0)
> $

> **Metric space properties** -- for all $x, y, z \in X$:
>
> | # | Property | Formula |
> |---|----------|---------|
> | 1 | Identity | $d(x, x) = 0$ |
> | 2 | Non-negativity | $d(x, y) > 0 \text{ for } x \neq y$ |
> | 3 | Symmetry | $d(x, y) = d(y, x)$ |
> | 4 | Triangle inequality | $d(x, z) \leq d(x, y) + d(y, z)$ |

> **Cauchy sequence condition:**
>
> For every $\varepsilon > 0$, there exists $N \in \mathbb{Z}^+$ such that:
>
> $
> d(x_a, x_b) < \varepsilon \quad \text{for all } a, b > N
> $

---

## 5. Worked Examples

### Example 1 -- Iterative Convergence to a Fixed Point

**Problem.** Let $f(x) = \frac{1}{2}(x + 3)$. Find the fixed point by (a) algebra and (b) iteration from $x_0 = 0$.

**(a) Algebraic solution.** Set $f(x^*) = x^*$:

$
\frac{1}{2}(x^* + 3) = x^*
$

$
x^* + 3 = 2x^*
$

$
x^* = 3
$

**(b) Iterative solution.** Start with $x_0 = 0$ and repeatedly apply $f$:

| Iteration $n$ | $x_n$ | $f(x_n) = x_{n+1}$ | $|x_{n+1} - 3|$ (distance to fixed point) |
|---------------|--------|---------------------|------------------------------------------|
| 0 | 0.000 | 1.500 | 1.500 |
| 1 | 1.500 | 2.250 | 0.750 |
| 2 | 2.250 | 2.625 | 0.375 |
| 3 | 2.625 | 2.8125 | 0.1875 |
| 4 | 2.8125 | 2.90625 | 0.09375 |
| 5 | 2.90625 | 2.95313 | 0.04687 |
| 6 | 2.95313 | 2.97656 | 0.02344 |
| 7 | 2.97656 | 2.98828 | 0.01172 |

**Observations:**

- The distance to the fixed point halves at each step (the contraction factor is $\gamma = 0.5$).
- Regardless of the starting point $x_0 = 0$, the iteration converges to $x^* = 3$.
- After just 7 iterations, the error is already below $0.012$.

### Example 2 -- Verifying Metric Properties

**Problem.** Show that $d(x, y) = |x - y|$ on $\mathbb{R}$ satisfies all four metric properties.

| Property | Verification |
|----------|-------------|
| Identity | $d(x, x) = |x - x| = |0| = 0$ |
| Non-negativity | If $x \neq y$, then $|x - y| > 0$ (absolute value of a non-zero number is positive) |
| Symmetry | $d(x, y) = |x - y| = |-(y - x)| = |y - x| = d(y, x)$ |
| Triangle inequality | $|x - z| = |x - y + y - z| \leq |x - y| + |y - z|$ (standard absolute value inequality) |

All four properties hold, so $(\mathbb{R}, |\cdot|)$ is a valid metric space.

### Example 3 -- Checking if a Sequence is Cauchy

**Problem.** Is the sequence $x_n = \frac{1}{n}$ a Cauchy sequence in $(\mathbb{R}, |\cdot|)$?

**Solution.** For $a, b > N$:

$
d(x_a, x_b) = \left|\frac{1}{a} - \frac{1}{b}\right| \leq \frac{1}{a} + \frac{1}{b} < \frac{1}{N} + \frac{1}{N} = \frac{2}{N}
$

Given any $\varepsilon > 0$, choose $N > \frac{2}{\varepsilon}$. Then for all $a, b > N$, we have $d(x_a, x_b) < \varepsilon$.

Therefore, the sequence is Cauchy. Since $\mathbb{R}$ is complete, it converges to a limit in $\mathbb{R}$ (namely $0$).

---

## 6. Common Mistakes

| Mistake | Why It Is Wrong | Correct Understanding |
|---------|-----------------|-----------------------|
| "Every Cauchy sequence converges" | This is only true in a **complete** metric space. In an incomplete space, a Cauchy sequence can fail to converge within the space. | A Cauchy sequence converges **if and only if** the metric space is complete. Always state the completeness assumption. |
| Confusing "Cauchy" with "convergent" | Being Cauchy means terms get close **to each other**. Convergence means terms get close **to a specific limit**. In $\mathbb{Q}$, a sequence can be Cauchy without converging (in $\mathbb{Q}$). | Cauchy is a property of the sequence alone. Convergence depends on the sequence **and** the space containing a limit point. |
| Writing $f^n(x)$ to mean $[f(x)]^n$ | In this context, $f^n$ means **function composition**: apply $f$ a total of $n$ times. It does not mean raise $f(x)$ to the $n$-th power. | $f^3(x) = f(f(f(x)))$, not $(f(x))^3$. |
| Forgetting the completeness requirement for iterative convergence | The iterative method produces a Cauchy sequence, but without completeness, the limit might not exist in the space. | Always verify two things: (1) the function is a contraction, and (2) the space is complete. Both are needed. |
| Thinking the fixed point depends on $x_0$ | If the function is a contraction on a complete metric space, the fixed point is unique and the iteration converges to it from **any** starting point. | The choice of $x_0$ affects how many iterations you need, not **where** you end up. |

---

## 7. Self-Check Questions

<details>
<summary>Q1: What is a fixed point, and how does a fixed point problem differ from root finding?</summary>

A fixed point $x^*$ of a function $f$ satisfies $f(x^*) = x^*$ -- applying the function leaves the value unchanged. Root finding seeks $f(x) = 0$, while fixed point problems seek $f(x) = x$. Any fixed point problem $f(x) = x$ can be converted to a root-finding problem by defining $g(x) = f(x) - x$ and solving $g(x) = 0$.

</details>

<details>
<summary>Q2: Describe the iterative method for finding a fixed point. Why does $x^*$ satisfy $f(x^*) = x^*$?</summary>

Start with an arbitrary $x_0$, then repeatedly compute $x_{n+1} = f(x_n)$. If $f$ is a contraction on a complete metric space, the sequence converges: $x^* = \lim_{n \to \infty} f^n(x_0)$. The limit satisfies the fixed point condition because:

$f(x^*) = f(\lim f^n(x_0)) = \lim f^{n+1}(x_0) = x^*$

The key step is pulling $f$ inside the limit (valid by continuity), then recognizing that the limit of $f^{n+1}(x_0)$ is the same as the limit of $f^n(x_0)$.

</details>

<details>
<summary>Q3: State the four properties a metric must satisfy.</summary>

For a function $d: X \times X \to \mathbb{R}$ to be a metric on set $X$, it must satisfy for all $x, y, z \in X$:

1. **Identity:** $d(x, x) = 0$
2. **Non-negativity:** $d(x, y) > 0$ when $x \neq y$
3. **Symmetry:** $d(x, y) = d(y, x)$
4. **Triangle inequality:** $d(x, z) \leq d(x, y) + d(y, z)$

</details>

<details>
<summary>Q4: Define a Cauchy sequence. Why is being Cauchy not the same as being convergent?</summary>

A sequence $(x_n)$ in a metric space $(X, d)$ is Cauchy if for every $\varepsilon > 0$, there exists $N$ such that $d(x_a, x_b) < \varepsilon$ for all $a, b > N$. Intuitively, terms become arbitrarily close to each other beyond some index.

Being Cauchy is not the same as being convergent because convergence requires that a limit point exists **in the space**. In an incomplete space, the limit can lie outside the space. For example, a sequence of rationals converging toward $\pi$ is Cauchy in $\mathbb{Q}$, but does not converge in $\mathbb{Q}$ because $\pi \notin \mathbb{Q}$.

</details>

<details>
<summary>Q5: What does it mean for a metric space to be complete, and why is completeness important for RL?</summary>

A metric space $(X, d)$ is complete if every Cauchy sequence of elements in $X$ converges to a limit that is also in $X$. The space has no "holes" -- limits of Cauchy sequences cannot escape the space.

Completeness is critical in RL because the iterative method for solving the Bellman equation generates a Cauchy sequence of value functions. We need the space of value functions (bounded functions with the infinity norm) to be complete so that this sequence is guaranteed to converge to the optimal value function $V^*$ within the space. Without completeness, the Banach Fixed Point Theorem does not apply.

</details>

<details>
<summary>Q6: Give an example of a metric space that is not complete.</summary>

The rational numbers $\mathbb{Q}$ with the standard metric $d(x, y) = |x - y|$ form a metric space that is not complete. The sequence $3, 3.1, 3.14, 3.141, 3.1415, \ldots$ consists entirely of rational numbers, is Cauchy, but converges to $\pi$, which is not a rational number. The limit lies outside the space, so $\mathbb{Q}$ is incomplete.

</details>

---

## 8. Exam Focus

### Paper 1 -- Q4 (5 Marks): Cauchy Sequence and Convergent Series

This question asks you to explain how a Cauchy sequence relates to a convergent series.

**What to write:**

- State the definition of a Cauchy sequence with the $\varepsilon$-$N$ condition.
- State that in a **complete** metric space, every Cauchy sequence converges -- the two concepts are equivalent.
- In an incomplete space, a Cauchy sequence may not converge within the space. Provide the $\mathbb{Q}$ counterexample.
- Mention that this equivalence is what makes completeness a requirement for the Banach Fixed Point Theorem.

**Mark allocation hint (5M):**

| Component | Marks |
|-----------|-------|
| Formal definition of Cauchy sequence | 2 |
| Explanation of convergence and link to completeness | 2 |
| Example or counterexample | 1 |

### Paper 2 -- Q4 (10 Marks): Fixed Point Problem with Mathematical Justification

This question asks you to define the fixed point problem and provide mathematical justification for why the iterative method works.

**What to write:**

- Define a fixed point: $f(x^*) = x^*$.
- Distinguish from root finding; show the conversion $g(x) = f(x) - x = 0$.
- Describe the iterative method: start from $x_0$, compute $x_{n+1} = f(x_n)$.
- State the convergence result: $x^* = \lim_{n \to \infty} f^n(x_0)$.
- Provide the full chain of equalities proving $f(x^*) = x^*$ (the four-step derivation from Section 2.2).
- State the conditions required: $f$ must be a contraction on a complete metric space.
- Briefly connect to RL: the Bellman operator is such a contraction, and value iteration is this iterative process.

**Mark allocation hint (10M):**

| Component | Marks |
|-----------|-------|
| Fixed point definition | 2 |
| Iterative method description | 2 |
| Mathematical proof that $f(x^*) = x^*$ via limits | 3 |
| Conditions (contraction, completeness) | 2 |
| Connection to RL / Bellman equation | 1 |

### Cross-Paper Theme

Both papers use these mathematical foundations as prerequisites for the Banach Fixed Point Theorem (BFPT). Know the definitions cold -- they will be either directly examined or assumed in longer BFPT and Bellman operator questions. If you cannot state the Cauchy sequence definition or the fixed point condition precisely, you will lose marks on the higher-level questions as well.

---

## 9. Concept Links

| Direction | File | Relationship |
|-----------|------|-------------|
| Forward | [05_contraction_and_bfpt.md](./05_contraction_and_bfpt.md) | The metric space, Cauchy sequence, and completeness definitions from this module are the three prerequisites for stating and proving the **Banach Fixed Point Theorem**. The fixed point iterative method becomes the core mechanism of the BFPT proof. |
| Forward | [06_bellman_and_convergence.md](./06_bellman_and_convergence.md) | The Bellman equation is a fixed point equation ($B(V^*) = V^*$). Value iteration is the iterative method from Section 2.2 applied to the Bellman operator. Convergence of value iteration relies on the space of bounded value functions being a **complete metric space** under $\|\cdot\|_\infty$. |
| Backward | [02_elements_of_rl.md](./02_elements_of_rl.md) | The value function introduced there is the object that lives in the metric space studied here. |

---

*Next module: [05_contraction_and_bfpt.md](./05_contraction_and_bfpt.md) -- Contraction Mapping and Banach Fixed Point Theorem*
