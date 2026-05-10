# Contraction Mapping and Banach Fixed Point Theorem

**Module**: 1 (Mathematical Foundations for RL)
**Priority**: P1 -- appears in every past paper (2/2)
**Prerequisites**: [Metric Spaces, Cauchy Sequences, Complete Metric Spaces](./04_mathematical_foundations.md)

---

## 1. Learning Objectives

After working through this section, you should be able to:

- State the formal definition of a contraction mapping on a metric space and explain each component
- Determine whether a given function is a contraction by computing the Lipschitz constant
- State the Banach Fixed Point Theorem precisely and explain what it guarantees
- Prove uniqueness of the fixed point by contradiction
- Prove existence of the fixed point using the Cauchy sequence argument
- Connect BFPT to reinforcement learning: why iterating the Bellman operator converges to the optimal value function
- Solve exam-style contraction verification problems with iterative convergence from a starting point
- Identify functions that are **not** contractions and explain why

---

## 2. Ground-Up Explanation

### 2.1 Contraction Mapping

**What problem are we solving?** In reinforcement learning, we want to find a value function $V^*$ that satisfies the Bellman equation $V^* = BV^*$, where $B$ is the Bellman operator. This is a fixed-point problem: we need $x$ such that $f(x) = x$. But how do we know such a point exists, and how do we find it? The answer lies in contraction mappings.

**Informal idea.** A contraction mapping is a function that brings points closer together every time you apply it. No matter which two points you start with, after applying the function, the distance between their images is strictly smaller than the original distance. Repeat the function many times, and all points collapse toward a single location -- the fixed point.

**Formal definition.** Let $(X, d)$ be a metric space. A function $f : X \to X$ is called a **contraction mapping** (or **contractor**) if there exists a constant $\gamma \in [0, 1)$ such that for all $x_1, x_2 \in X$:

$$
d(f(x_1), f(x_2)) \leq \gamma \cdot d(x_1, x_2)
$$

The constant $\gamma$ is called the **contraction factor**. The smallest such $\gamma$ that satisfies the inequality for all pairs is called the **Lipschitz constant** of $f$.

**Key observations:**

- The contraction factor $\gamma$ must be **strictly less than 1**. This is what guarantees that distances shrink.
- If $\gamma = 1$, the function is called a **short mapping** (or non-expansive mapping), **not** a contraction. A short mapping does not shrink distances -- it merely does not increase them. This distinction matters: short mappings do not guarantee a fixed point.
- The Lipschitz constant has applications beyond RL. It is an important quantity in the theory of **Generative Adversarial Networks (GANs)**, where enforcing a Lipschitz constraint on the discriminator is central to Wasserstein GANs.
- After applying a contraction, the distance between any two elements shrinks by at least a factor of $\gamma$. After applying it $n$ times, the distance is at most $\gamma^n$ times the original distance. Since $\gamma < 1$, we have $\gamma^n \to 0$ as $n \to \infty$.
- Sequential values $x, f(x), f(f(x)), \ldots$ get progressively closer together after each application of a contraction. This is the mechanism that drives convergence.

**How to verify a function is a contraction.** For a differentiable function $f : \mathbb{R} \to \mathbb{R}$, the contraction condition is equivalent to:

$$
|f'(x)| \leq \gamma < 1 \quad \text{for all } x \text{ in the domain}
$$

This follows from the Mean Value Theorem. In practice, to find the Lipschitz constant, compute $\sup_x |f'(x)|$ over the domain and check whether it is strictly less than 1.

---

### 2.2 Worked Contraction Example: $f(x) = (x+3)/4$

Consider the metric space $X = [0, 2]$ with the usual (Euclidean) distance $d(x, y) = |x - y|$. Let $f(x) = \frac{x + 3}{4}$.

**Step 1 -- Show $f : X \to X$ (the function maps $X$ into itself).**

We need to verify that if $x \in [0, 2]$, then $f(x) \in [0, 2]$.

- When $x = 0$: $f(0) = \frac{0 + 3}{4} = \frac{3}{4} = 0.75$
- When $x = 2$: $f(2) = \frac{2 + 3}{4} = \frac{5}{4} = 1.25$

Since $f$ is a linear (increasing) function of $x$, the range of $f$ on $[0, 2]$ is:

$$
f([0, 2]) = [0.75, 1.25] \subset [0, 2]
$$

So $f$ maps $X$ into itself.

**Step 2 -- Show $f$ is a contraction and find the contraction constant $k$.**

For any $x, y \in [0, 2]$:

$$
|f(x) - f(y)| = \left| \frac{x + 3}{4} - \frac{y + 3}{4} \right| = \left| \frac{x - y}{4} \right| = \frac{1}{4} |x - y|
$$

Therefore:

$$
d(f(x), f(y)) = \frac{1}{4} \cdot d(x, y)
$$

The contraction constant is $k = \frac{1}{4} = 0.25$. Since $0.25 < 1$, the function $f$ is a contraction.

Alternatively, $f'(x) = \frac{1}{4}$, so $|f'(x)| = 0.25 < 1$ everywhere. This confirms the contraction.

**Step 3 -- Find the fixed point analytically.**

Solve $f(x^*) = x^*$:

$$
x^* = \frac{x^* + 3}{4}
$$

$$
4x^* = x^* + 3
$$

$$
3x^* = 3
$$

$$
x^* = 1
$$

The unique fixed point is $x^* = 1$.

**Step 4 -- Iterate from $x_0 = 0$ to demonstrate convergence.**

| Iteration $n$ | $x_n$ | $f(x_n) = x_{n+1}$ |
|:-:|:-:|:-:|
| 0 | 0 | 0.75 |
| 1 | 0.75 | 0.9375 |
| 2 | 0.9375 | 0.984375 |
| 3 | 0.984375 | 0.99609375 |
| 4 | 0.99609375 | 0.9990234375 |
| 5 | 0.9990234375 | 0.9997558594 |

The sequence converges toward $x^* = 1$, as predicted by the Banach Fixed Point Theorem.

**Verification via the convergence bound.** After $n$ iterations, the error is bounded by:

$$
|x_n - x^*| \leq \frac{k^n}{1 - k} \cdot d(f(x_0), x_0)
$$

Here $k = 0.25$, $d(f(x_0), x_0) = |0.75 - 0| = 0.75$, so:

$$
|x_n - 1| \leq \frac{0.25^n}{0.75} \cdot 0.75 = 0.25^n
$$

At $n = 4$: $0.25^4 = 0.00390625$, and indeed $|x_4 - 1| = |0.99609375 - 1| = 0.00390625$. The bound is tight.

---

### 2.3 Previous Exam Contraction Questions (from Lecture Slides)

The following functions are explicitly listed in the Module 1 slides as previous exam questions. You should be prepared to verify each is a contraction and iterate from the given starting point.

**Example A: $f(x) = 0.5 \sin(x)$, starting from $x_0 = 0.2$.**

*Is it a contraction?* Compute the derivative: $f'(x) = 0.5 \cos(x)$. Since $|\cos(x)| \leq 1$ for all $x$, we have $|f'(x)| = 0.5 |\cos(x)| \leq 0.5 < 1$. Therefore $f$ is a contraction with Lipschitz constant $\gamma = 0.5$.

*Fixed point.* Solve $x = 0.5 \sin(x)$. By inspection, $x^* = 0$ is a solution (since $\sin(0) = 0$). Uniqueness is guaranteed by BFPT.

*Iteration from $x_0 = 0.2$:*

| $n$ | $x_n$ | $f(x_n) = 0.5 \sin(x_n)$ |
|:-:|:-:|:-:|
| 0 | 0.2 | 0.09933 |
| 1 | 0.09933 | 0.04951 |
| 2 | 0.04951 | 0.02473 |
| 3 | 0.02473 | 0.01236 |
| 4 | 0.01236 | 0.00618 |
| 5 | 0.00618 | 0.00309 |

The sequence converges rapidly toward $x^* = 0$.

**Example B: $f(x) = 0.25 \cos^2(x)$, starting from $x_0 = 0.2$.**

*Is it a contraction?* Compute the derivative using the chain rule:

$$
f'(x) = 0.25 \cdot 2\cos(x) \cdot (-\sin(x)) = -0.5 \cos(x) \sin(x) = -0.25 \sin(2x)
$$

Therefore $|f'(x)| = 0.25 |\sin(2x)| \leq 0.25 < 1$ for all $x$. The function is a contraction with Lipschitz constant $\gamma = 0.25$.

*Fixed point.* Solve $x = 0.25 \cos^2(x)$. This does not have a neat closed-form solution, but the fixed point can be found numerically by iteration.

*Iteration from $x_0 = 0.2$:*

| $n$ | $x_n$ | $f(x_n) = 0.25 \cos^2(x_n)$ |
|:-:|:-:|:-:|
| 0 | 0.2 | 0.24010 |
| 1 | 0.24010 | 0.23570 |
| 2 | 0.23570 | 0.23614 |
| 3 | 0.23614 | 0.23609 |
| 4 | 0.23609 | 0.23610 |
| 5 | 0.23610 | 0.23610 |

The sequence converges to $x^* \approx 0.2361$.

---

### 2.4 Banach Fixed Point Theorem (BFPT)

The Banach Fixed Point Theorem is the cornerstone result that guarantees convergence in reinforcement learning algorithms like value iteration and policy evaluation.

**Informal statement.** If you have a "nice" space (complete metric space) and a function that always brings points closer together (contraction), then:

1. There is exactly **one** point that the function maps to itself (the fixed point).
2. Starting from **any** point and repeatedly applying the function, you will converge to that fixed point.

Why does this work intuitively? We know three things:

- A contractor brings elements closer together with every application.
- Repeatedly applying a contractor to any starting point produces a sequence $x_0, f(x_0), f(f(x_0)), \ldots$ where consecutive terms get closer and closer. This is a Cauchy sequence.
- In a complete metric space, every Cauchy sequence converges to a point that is inside the space.

Combining these three facts: the sequence converges to some point $x^*$ in the space, and that point must be the fixed point.

**Formal statement.**

> **Banach Fixed Point Theorem.** Let $(X, d)$ be a **complete metric space** and let $f : X \to X$ be a **contraction mapping** (i.e., there exists $\gamma \in [0, 1)$ such that $d(f(x_1), f(x_2)) \leq \gamma \cdot d(x_1, x_2)$ for all $x_1, x_2 \in X$). Then:
>
> 1. $f$ has a **unique fixed point** $x^* \in X$, meaning $f(x^*) = x^*$.
> 2. For **any** starting point $x_0 \in X$, the sequence defined by $x_{n+1} = f(x_n)$ converges to $x^*$. That is, $\lim_{n \to \infty} f^n(x_0) = x^*$.

Both conditions -- completeness of the space and the contraction property -- are essential. Drop either one, and the theorem can fail.

---

### 2.5 Proof of Uniqueness

The uniqueness proof is short and elegant. It uses proof by contradiction.

**Claim.** The fixed point $x^*$ is unique.

**Proof.** Suppose for contradiction that there are **two distinct** fixed points $x_1^*$ and $x_2^*$ in $X$, with $x_1^* \neq x_2^*$.

Since both are fixed points:

$$
f(x_1^*) = x_1^* \quad \text{and} \quad f(x_2^*) = x_2^*
$$

Therefore:

$$
d(f(x_1^*), f(x_2^*)) = d(x_1^*, x_2^*) \tag{1}
$$

But $f$ is a contraction, so:

$$
d(f(x_1^*), f(x_2^*)) \leq \gamma \cdot d(x_1^*, x_2^*) \tag{2}
$$

From equations (1) and (2):

$$
d(x_1^*, x_2^*) \leq \gamma \cdot d(x_1^*, x_2^*)
$$

Since $x_1^* \neq x_2^*$, we have $d(x_1^*, x_2^*) > 0$. Dividing both sides by $d(x_1^*, x_2^*)$:

$$
1 \leq \gamma
$$

But $\gamma \in [0, 1)$, so $\gamma < 1$. This is a **contradiction**.

Therefore our assumption was false, and $x_1^* = x_2^*$. The fixed point is unique. $\square$

---

### 2.6 Proof of Existence

The existence proof constructs the fixed point explicitly by showing that the iterative sequence is Cauchy, and then invoking completeness.

**Claim.** The sequence $x_n = f^n(x_0)$ converges to a fixed point $x^* \in X$.

**Proof.** Let $x_0 \in X$ be any starting point, and define the sequence $x_n = f^n(x_0)$, i.e., $x_1 = f(x_0)$, $x_2 = f(x_1) = f^2(x_0)$, and so on.

**Step 1: Bound consecutive distances.**

Since $f$ is a contraction with factor $\gamma$:

$$
d(x_{n+1}, x_n) = d(f(x_n), f(x_{n-1})) \leq \gamma \cdot d(x_n, x_{n-1})
$$

Applying this recursively:

$$
d(x_{n+1}, x_n) \leq \gamma^n \cdot d(x_1, x_0) = \gamma^n \cdot d(f(x_0), x_0)
$$

**Step 2: Show the sequence is Cauchy.**

For $m > n$, apply the triangle inequality repeatedly:

$$
d(x_m, x_n) \leq d(x_m, x_{m-1}) + d(x_{m-1}, x_{m-2}) + \cdots + d(x_{n+1}, x_n)
$$

$$
d(x_m, x_n) \leq \sum_{i=n}^{m-1} d(x_{i+1}, x_i) \leq \sum_{i=n}^{m-1} \gamma^i \cdot d(f(x_0), x_0)
$$

$$
d(x_m, x_n) \leq d(f(x_0), x_0) \cdot \sum_{i=n}^{m-1} \gamma^i
$$

Since $\gamma \in [0, 1)$, the geometric series converges. Bounding the partial sum by the tail of the infinite series:

$$
\sum_{i=n}^{m-1} \gamma^i \leq \sum_{i=n}^{\infty} \gamma^i = \frac{\gamma^n}{1 - \gamma}
$$

Therefore:

$$
d(x_m, x_n) \leq \frac{\gamma^n}{1 - \gamma} \cdot d(f(x_0), x_0)
$$

**Step 3: Conclude convergence.**

Given any $\epsilon > 0$, choose $N$ large enough so that:

$$
\frac{\gamma^N}{1 - \gamma} \cdot d(f(x_0), x_0) < \epsilon
$$

This is always possible because $\gamma^N \to 0$ as $N \to \infty$. Then for all $m > n \geq N$:

$$
d(x_m, x_n) < \epsilon
$$

This means the sequence $(x_n)$ is **Cauchy**. Since $(X, d)$ is a **complete metric space**, every Cauchy sequence converges to a point in $X$. Therefore there exists $x^* \in X$ such that $\lim_{n \to \infty} x_n = x^*$.

**Step 4: Verify $x^*$ is a fixed point.**

We need to show $f(x^*) = x^*$. Since $f$ is a contraction, it is continuous. Therefore:

$$
f(x^*) = f\left(\lim_{n \to \infty} x_n\right) = \lim_{n \to \infty} f(x_n) = \lim_{n \to \infty} x_{n+1} = x^*
$$

Hence $x^*$ is a fixed point. Combined with the uniqueness proof, we have shown that $f$ has a unique fixed point $x^*$, and the iterative sequence converges to it from any starting point. $\square$

---

## 3. Analogies

### The Zoom Lens Analogy

Imagine you are looking at a map through a camera with a zoom lens. Each time you "apply the contraction," you zoom in closer. The field of view gets smaller -- points that were far apart on the map appear closer together through the lens. No matter where on the map you initially point the camera, each zoom step shrinks the visible area by a factor $\gamma$. After enough zoom steps, everything converges to a single point -- the fixed point. The key constraint is that $\gamma < 1$: the zoom always tightens. If $\gamma = 1$ (a short mapping), the camera never actually zooms in, and you never converge to a single point.

### The Negotiation Analogy

Think of two parties negotiating a price. A contraction mapping is like a mediator who, at each round, forces the two parties to move at least $(1 - \gamma)$ fraction of the way closer to each other. After enough rounds, the gap between their positions becomes negligibly small, and they converge on a single price -- the fixed point. If the mediator only prevents the gap from growing ($\gamma = 1$) but does not actively shrink it, the parties might never agree.

---

## 4. Key Formulas

### Contraction Condition

> **CRITICAL EQUATION**
>
> $$
> d(f(x_1), f(x_2)) \leq \gamma \cdot d(x_1, x_2)
> $$

> **Where:**
> - $f : X \to X$ = the mapping (function) being tested
> - $(X, d)$ = the metric space (a set $X$ with distance function $d$)
> - $x_1, x_2$ = any two elements in $X$
> - $\gamma \in [0, 1)$ = the contraction factor (strictly less than 1)
> - $d(\cdot, \cdot)$ = the distance function (metric) on $X$

### Derivative Test for Contraction (one-dimensional case)

$$
|f'(x)| \leq \gamma < 1 \quad \text{for all } x \text{ in the domain}
$$

> **Where:**
> - $f'(x)$ = the derivative of $f$ at $x$
> - $\gamma$ = the Lipschitz constant (supremum of $|f'(x)|$ over the domain)

### BFPT Convergence Bound

> **CRITICAL EQUATION**
>
> $$
> d(x_m, x_n) \leq \frac{\gamma^n}{1 - \gamma} \cdot d(f(x_0), x_0)
> $$

> **Where:**
> - $x_n = f^n(x_0)$ = the point obtained after applying $f$ a total of $n$ times to starting point $x_0$
> - $x_m = f^m(x_0)$ = the point after $m$ applications (with $m > n$)
> - $\gamma$ = the contraction factor
> - $d(f(x_0), x_0)$ = the distance between the starting point and its first iterate
> - The right-hand side goes to 0 as $n \to \infty$, proving the sequence is Cauchy

### Error After $n$ Iterations

$$
d(x_n, x^*) \leq \frac{\gamma^n}{1 - \gamma} \cdot d(f(x_0), x_0)
$$

> **Where:**
> - $x^*$ = the unique fixed point
> - This bounds how far the $n$-th iterate is from the true fixed point

### Contraction Applied $n$ Times

$$
d(f^n(x_1), f^n(x_2)) \leq \gamma^n \cdot d(x_1, x_2)
$$

> **Where:**
> - $f^n$ denotes $f$ composed with itself $n$ times
> - The distance shrinks exponentially with each application

---

## 5. Derivations

### 5.1 Full Uniqueness Proof

See [Section 2.5](#25-proof-of-uniqueness) above for the complete proof by contradiction.

**Summary of the argument:**

1. Assume two distinct fixed points $x_1^*$ and $x_2^*$ exist.
2. Since they are fixed points: $d(f(x_1^*), f(x_2^*)) = d(x_1^*, x_2^*)$.
3. Since $f$ is a contraction: $d(f(x_1^*), f(x_2^*)) \leq \gamma \cdot d(x_1^*, x_2^*)$.
4. Combining: $d(x_1^*, x_2^*) \leq \gamma \cdot d(x_1^*, x_2^*)$.
5. Since $d(x_1^*, x_2^*) > 0$, this gives $1 \leq \gamma$, contradicting $\gamma < 1$.
6. Therefore $x_1^* = x_2^*$.

### 5.2 Full Existence Proof

See [Section 2.6](#26-proof-of-existence) above for the complete constructive proof.

**Summary of the argument:**

1. Define $x_n = f^n(x_0)$.
2. Show $d(x_{n+1}, x_n) \leq \gamma^n \cdot d(f(x_0), x_0)$ by repeated application of the contraction condition.
3. Use the triangle inequality to bound $d(x_m, x_n) \leq \sum_{i=n}^{m-1} \gamma^i \cdot d(f(x_0), x_0)$.
4. Bound the geometric sum: $\sum_{i=n}^{m-1} \gamma^i \leq \gamma^n / (1 - \gamma)$.
5. Conclude $d(x_m, x_n) \leq \frac{\gamma^n}{1 - \gamma} \cdot d(f(x_0), x_0)$, which can be made arbitrarily small.
6. Therefore the sequence is Cauchy. By completeness of $(X, d)$, it converges to some $x^* \in X$.
7. By continuity of $f$ (contractions are continuous): $f(x^*) = x^*$.

### 5.3 Deriving the Geometric Series Bound

The key step in the existence proof uses the geometric series formula. Here is the derivation:

$$
\sum_{i=n}^{m-1} \gamma^i = \gamma^n + \gamma^{n+1} + \cdots + \gamma^{m-1} = \gamma^n (1 + \gamma + \gamma^2 + \cdots + \gamma^{m-1-n})
$$

$$
= \gamma^n \cdot \frac{1 - \gamma^{m-n}}{1 - \gamma} \leq \gamma^n \cdot \frac{1}{1 - \gamma} = \frac{\gamma^n}{1 - \gamma}
$$

The inequality holds because $1 - \gamma^{m-n} \leq 1$ for any positive power of $\gamma < 1$.

---

## 6. Worked Examples

### Example 1: $f(x) = (x + 3)/4$ on $X = [0, 2]$

This is the primary lecture example. See [Section 2.2](#22-worked-contraction-example-fx--x34) for the full four-step solution:

1. $f([0, 2]) = [0.75, 1.25] \subset [0, 2]$ -- maps $X$ into itself.
2. $|f(x) - f(y)| = \frac{1}{4}|x - y|$ -- contraction with $k = 0.25$.
3. Fixed point: $x^* = 1$.
4. Iteration from $x_0 = 0$: $0 \to 0.75 \to 0.9375 \to 0.984375 \to 0.996 \to 0.999 \to \cdots \to 1$.

---

### Example 2: $f(x) = 0.5 \sin(x)$ from $x_0 = 0.2$

See [Section 2.3, Example A](#23-previous-exam-contraction-questions-from-lecture-slides) for the full solution.

1. $f'(x) = 0.5\cos(x)$, so $|f'(x)| \leq 0.5 < 1$ -- contraction with $\gamma = 0.5$.
2. Fixed point: $x^* = 0$ (since $\sin(0) = 0$).
3. Iteration: $0.2 \to 0.0993 \to 0.0495 \to 0.0247 \to 0.0124 \to 0.0062 \to \cdots \to 0$.

---

### Example 3: $f(x) = 0.25 \sin^2(x)$ from $x_0 = 0.2$

*Is it a contraction?* Compute the derivative using the chain rule:

$$
f'(x) = 0.25 \cdot 2 \sin(x) \cdot \cos(x) = 0.25 \sin(2x)
$$

Therefore $|f'(x)| = 0.25 |\sin(2x)| \leq 0.25 < 1$. The function is a contraction with $\gamma = 0.25$.

*Fixed point.* One solution is $x^* = 0$ (since $\sin^2(0) = 0$). But check: are there others? By BFPT, the fixed point is unique in the complete metric space. Numerically, iterating reveals convergence to $x^* = 0$.

*Iteration from $x_0 = 0.2$:*

| $n$ | $x_n$ | $f(x_n) = 0.25 \sin^2(x_n)$ |
|:-:|:-:|:-:|
| 0 | 0.2 | 0.00987 |
| 1 | 0.00987 | 0.0000244 |
| 2 | 0.0000244 | $\approx 0$ |

The sequence converges very rapidly to $x^* = 0$ because the contraction factor is only 0.25 and $\sin^2(x)$ is very small near zero.

> **Note:** This function appeared in the past Paper 2, Q3(b), but with $\cos^2$ instead of $\sin^2$. Both follow the same verification technique. The exam question used $f(x) = 0.25\sin^2(x)$ in the slides as a previous exam question and $f(x) = 0.25\cos^2(x)$ in the slides as another. Be prepared for both variants.

---

### Example 4: Identifying Contractions -- $T_1(x) = 0.9x + 1$ vs $T_2(x) = 1.2x^2 + 3$

This example tests whether you can distinguish a contraction from a non-contraction.

**$T_1(x) = 0.9x + 1$:**

Compute the derivative: $T_1'(x) = 0.9$. Therefore $|T_1'(x)| = 0.9 < 1$ for all $x$. The function $T_1$ **is** a contraction with Lipschitz constant $\gamma = 0.9$.

*Verification directly from the definition:*

$$
|T_1(x_1) - T_1(x_2)| = |0.9x_1 + 1 - 0.9x_2 - 1| = 0.9|x_1 - x_2|
$$

*Fixed point:* Solve $x = 0.9x + 1$, giving $0.1x = 1$, so $x^* = 10$.

*Iteration from $x_0 = 0$:*

| $n$ | $x_n$ |
|:-:|:-:|
| 0 | 0 |
| 1 | 1.0 |
| 2 | 1.9 |
| 3 | 2.71 |
| 4 | 3.439 |
| 5 | 4.095 |

The sequence converges slowly (because $\gamma = 0.9$ is close to 1) toward $x^* = 10$.

**$T_2(x) = 1.2x^2 + 3$:**

Compute the derivative: $T_2'(x) = 2.4x$. At $x = 1$, $|T_2'(1)| = 2.4 > 1$. In fact, for any $|x| > 1/2.4 \approx 0.417$, the derivative exceeds 1.

The function $T_2$ is **not** a contraction. The coefficient 1.2 already exceeds 1 for the quadratic term, and the derivative grows without bound as $|x|$ increases.

*No fixed point convergence:* Solve $x = 1.2x^2 + 3$. This gives $1.2x^2 - x + 3 = 0$. The discriminant is $1 - 4(1.2)(3) = 1 - 14.4 = -13.4 < 0$. There are **no real fixed points**.

*Iteration from $x_0 = 0$: $0 \to 3 \to 13.8 \to 231.5 \to \cdots$ -- the sequence diverges rapidly.*

> **Key takeaway for the exam.** When given two operators and asked which is a contraction, check the derivative (or Lipschitz constant). A coefficient greater than or equal to 1 on the dominant term is a strong signal the function is not a contraction. The absence of real fixed points further confirms divergence.

---

## 7. Common Mistakes

- **Confusing $\gamma < 1$ with $\gamma \leq 1$.** The contraction factor must be **strictly** less than 1. At $\gamma = 1$, the function is a short mapping, not a contraction. BFPT does not apply to short mappings.

- **Forgetting to verify $f : X \to X$.** A contraction must map the space **into itself**. If $f$ sends some elements outside $X$, it is not a valid contraction on $X$. Always check this before checking the contraction condition.

- **Using the wrong derivative for trigonometric compositions.** For $f(x) = a \sin^2(x)$, the derivative is $f'(x) = a \sin(2x)$ (via the chain rule), **not** $f'(x) = 2a \sin(x)$. Similarly, for $f(x) = a \cos^2(x)$, the derivative is $f'(x) = -a \sin(2x)$, not $-2a\cos(x)$.

- **Claiming non-contraction without checking the full domain.** A function might have $|f'(x)| > 1$ at some points but still satisfy $|f'(x)| \leq \gamma < 1$ everywhere on a restricted domain. Always evaluate the supremum of $|f'(x)|$ over the **entire** relevant domain.

- **Forgetting completeness in BFPT.** The theorem requires a **complete** metric space. If the space is not complete (e.g., the open interval $(0, 1)$ with the usual metric), a contraction might not have a fixed point in that space. Always state the completeness requirement.

- **Mixing up the convergence bound.** The bound is $\frac{\gamma^n}{1 - \gamma} \cdot d(f(x_0), x_0)$, not $\frac{\gamma^n}{1 - \gamma} \cdot d(x_1, x_2)$ for arbitrary $x_1, x_2$. The initial distance is specifically between the starting point and its first iterate.

- **Assuming all linear functions are contractions.** The function $f(x) = 1.2x + 3$ is **not** a contraction because $|f'(x)| = 1.2 > 1$, even though it is linear. The slope must be strictly less than 1 in absolute value.

- **Confusing the uniqueness proof direction.** The contradiction in the uniqueness proof arises from $1 \leq \gamma$, not from $d(x_1^*, x_2^*) < 0$. Make sure you state that you divide both sides by $d(x_1^*, x_2^*) > 0$ and arrive at $1 \leq \gamma$.

---

## 8. Self-Check Questions

<details>
<summary>Q1: What is the formal definition of a contraction mapping?</summary>

**Answer:** A function $f : X \to X$ on a metric space $(X, d)$ is a contraction mapping if there exists $\gamma \in [0, 1)$ such that for all $x_1, x_2 \in X$:

$$
d(f(x_1), f(x_2)) \leq \gamma \cdot d(x_1, x_2)
$$

The constant $\gamma$ is the contraction factor. The smallest such $\gamma$ is the Lipschitz constant.

</details>

<details>
<summary>Q2: Why does BFPT fail if $\gamma = 1$?</summary>

**Answer:** If $\gamma = 1$, the function is a short mapping (non-expansive), not a contraction. The uniqueness proof breaks down because $d(x_1^*, x_2^*) \leq 1 \cdot d(x_1^*, x_2^*)$ is always true and gives no contradiction. The existence proof breaks down because $\gamma^n = 1^n = 1$ does not go to zero, so the Cauchy sequence argument fails -- the bound $\frac{\gamma^n}{1-\gamma}$ diverges.

</details>

<details>
<summary>Q3: Prove that the fixed point of a contraction is unique.</summary>

**Answer:** Assume two distinct fixed points $x_1^*$ and $x_2^*$ exist. Since $f(x_1^*) = x_1^*$ and $f(x_2^*) = x_2^*$, we have $d(f(x_1^*), f(x_2^*)) = d(x_1^*, x_2^*)$. But the contraction condition gives $d(f(x_1^*), f(x_2^*)) \leq \gamma \cdot d(x_1^*, x_2^*)$. Combining: $d(x_1^*, x_2^*) \leq \gamma \cdot d(x_1^*, x_2^*)$. Since $x_1^* \neq x_2^*$, $d(x_1^*, x_2^*) > 0$, so we can divide to get $1 \leq \gamma$. This contradicts $\gamma < 1$. Hence $x_1^* = x_2^*$.

</details>

<details>
<summary>Q4: Is $f(x) = x^2$ a contraction on $[0, 0.4]$?</summary>

**Answer:** Compute $f'(x) = 2x$. On $[0, 0.4]$, we have $|f'(x)| \leq 2(0.4) = 0.8 < 1$. Check that $f$ maps $[0, 0.4]$ into itself: $f(0) = 0$, $f(0.4) = 0.16$, so $f([0, 0.4]) = [0, 0.16] \subset [0, 0.4]$. Yes, $f(x) = x^2$ **is** a contraction on $[0, 0.4]$ with Lipschitz constant $\gamma = 0.8$. The fixed point is $x^* = 0$.

</details>

<details>
<summary>Q5: What are the two conditions required by the Banach Fixed Point Theorem?</summary>

**Answer:**

1. The metric space $(X, d)$ must be **complete** (every Cauchy sequence in $X$ converges to a point in $X$).
2. The function $f : X \to X$ must be a **contraction** (there exists $\gamma \in [0, 1)$ such that $d(f(x_1), f(x_2)) \leq \gamma \cdot d(x_1, x_2)$ for all $x_1, x_2$).

Both conditions are necessary. Without completeness, the limit of the Cauchy sequence might not belong to $X$. Without contraction, the sequence might not be Cauchy (or might diverge).

</details>

<details>
<summary>Q6: Explain in one sentence how BFPT connects to reinforcement learning.</summary>

**Answer:** The Bellman operator $B$ is a contraction mapping on the complete metric space of value functions (under the $L_\infty$ norm), so by BFPT, repeatedly applying $B$ (i.e., value iteration) converges to the unique optimal value function $V^*$ that satisfies $V^* = BV^*$.

</details>

<details>
<summary>Q7: Is $T_2(x) = 1.2x^2 + 3$ a contraction? Why or why not?</summary>

**Answer:** No. The derivative is $T_2'(x) = 2.4x$, which exceeds 1 for $|x| > 0.417$. The Lipschitz constant is unbounded on $\mathbb{R}$. Furthermore, the equation $x = 1.2x^2 + 3$ has no real solutions (discriminant is negative), so no real fixed point exists. Iteration from any starting point diverges.

</details>

<details>
<summary>Q8: In the existence proof of BFPT, what role does the triangle inequality play?</summary>

**Answer:** The triangle inequality is used to bound the distance between non-consecutive terms $x_m$ and $x_n$ by a telescoping sum of consecutive distances: $d(x_m, x_n) \leq d(x_m, x_{m-1}) + d(x_{m-1}, x_{m-2}) + \cdots + d(x_{n+1}, x_n)$. Each consecutive distance is then bounded using the contraction property, yielding a geometric series that can be summed and shown to vanish as $n \to \infty$.

</details>

---

## 9. Exam Focus

> **CRITICAL -- This topic appears in every past paper (2/2). Expect 5--10 marks on contraction mapping and BFPT.**

### 9.1 How This Topic Has Been Examined

| Paper | Question | What Was Asked | Marks |
|:-----:|:--------:|----------------|:-----:|
| Paper 1 | Q3(a) | Describe contraction mapping; establish need for Bellman convergence | 5 |
| Paper 1 | Q3(b) | Identify which of $T_1(x) = 0.9x + 1$ and $T_2(x) = 1.2x^2 + 3$ is a contraction | 5 |
| Paper 2 | Q3(a) | Policy evaluation as fixed-point problem; check $f(x) = 0.25\sin^2(x)$ is a contraction | 5 |
| Paper 2 | Q3(b) | Verify contraction and perform iterative convergence | 5 |
| Paper 2 | Q4 | Define fixed-point problem; relate to RL via BFPT; discuss existence and uniqueness | 10 |

### 9.2 Exam Question Patterns

**Pattern A (Paper 1, Q3 -- 10 marks total):**
- Part (a): Describe contraction mapping mathematically. Explain why it matters for Bellman convergence. (5M)
- Part (b): Given two operators, identify which is a contraction and which is not. Find the contraction constant. (5M)

**Pattern B (Paper 2, Q3 -- 10 marks total):**
- Part (a): Frame policy evaluation as a fixed-point problem. Given a specific function, verify it is a contraction. (5M)
- Part (b): From a given starting point, perform 3--5 iterations to demonstrate convergence. (5M)

**Pattern C (Paper 2, Q4 -- 10 marks):**
- Define the fixed-point problem with mathematical justification.
- Relate the fixed-point concept to reinforcement learning (value function as fixed point of Bellman operator).
- State BFPT and discuss existence and uniqueness. Proof sketches may be expected for full marks.

### 9.3 What to Prepare

1. **Memorize the contraction mapping definition** word for word, including the inequality and the constraint $\gamma \in [0, 1)$.
2. **Memorize the BFPT statement** -- both the hypotheses (complete metric space, contraction) and the conclusions (unique fixed point, iterative convergence).
3. **Be able to write the uniqueness proof** from scratch. It is short (5 lines) and has appeared in Paper 2, Q4.
4. **Be able to sketch the existence proof** -- at minimum, state the Cauchy sequence argument and the convergence bound.
5. **Practise verifying contractions** using the derivative test. Be fast with the chain rule for $\sin^2$, $\cos^2$, and $\sin$ compositions.
6. **Practise iterative convergence** from a starting point. Show at least 3--5 iterations in a table.
7. **Be able to identify non-contractions** and explain why (derivative exceeds 1, or no real fixed point).
8. **Connect to RL.** State that the Bellman operator $B$ (or $T^\pi$ for policy evaluation) is a contraction with factor $\gamma$ (the discount factor) under the $L_\infty$ norm. By BFPT, iterating $B$ converges to the unique $V^*$ (or $V^\pi$).

### 9.4 Likely Variations for the Next Exam

- A new trigonometric function (e.g., $f(x) = a\cos(x)$ for some $a < 1$, or $f(x) = a\sin^2(x) + b$ for small constants).
- A pair of operators where you must identify the contraction (same style as Paper 1, Q3(b)).
- A 10-mark question combining the fixed-point definition, BFPT statement, and proof of uniqueness.
- Asking you to state and prove why the Bellman operator is a contraction (ties into [06_bellman_and_convergence.md](./06_bellman_and_convergence.md)).

---

## 10. Concept Links

- **Prerequisite**: [Metric Spaces, Cauchy Sequences, Complete Metric Spaces](./04_mathematical_foundations.md) -- you need these definitions to state and prove BFPT.
- **Application**: [Bellman Equation and Convergence](./06_bellman_and_convergence.md) -- BFPT is applied to the Bellman operator to prove value iteration converges to $V^*$.
- **Context**: [Elements of RL](./02_elements_of_rl.md) -- the value function and policy that BFPT guarantees we can find.
- **Formula Reference**: [Formula Sheet](./08_formula_sheet.md) -- contraction condition and BFPT convergence bound.
- **Practice**: [Worked Problems](./07_worked_problems.md) -- additional past paper solutions involving contraction verification.
