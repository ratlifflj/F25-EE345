---
title: Summations
nav_exclude: true
extra_css: ['resources.scss']
---

This document covers a few mathematical constructs that appear very frequently when doing algorithmic analysis. We spend minimal time in class reviewing these concepts, so this document is intended to serve as a general reference guide and as a concept refresher. Please head to office hours if you have any follow-up questions.

We also have a few practice problems located at the bottom if you're very rusty and want some practice.

This document was written by Michael Lee, Meredith Wu, & Brian Chan.

## Summations Review

The summation ($`\sum`$) is a way of concisely expressing the sum of a series of related
values. For example, suppose we wanted a concise way of writing
$`1 + 2 + 3 + \cdots + 8 + 9 + 10`$. We can do so like this:

```math
\sum_{i=1}^{10} i
```

The "$`i = 1`$" expression below the $`\sum`$ symbol is initializing a variable called
$`i`$ which is initially set to 1. We then increase $`i`$ by one from that initial value up
to and including the number at the top of the $`\sum`$ symbol. We then take each value of
$`i`$ and substitute it to the expression to the right of the $`\sum`$ symbol, and add
each of those expressions together.

Here is another example:

```math
\begin{aligned}
\sum_{i=1}^3 2 + i^2 &= (2 + 1^2) + (2 + 2^2) + (2 + 3^2)  \\
&= 3 + 6 + 11 \\
&= 20
\end{aligned}
```

More generally, the summation operation is defined as follows:

```math
\sum_{i=a}^b f(i) = f(a) + f(a + 1) + f(a + 2) + \cdots + f(b - 2) + f(b - 1) + f(b)
```

...where $`a, b`$ are integers such that $`a \leq b`$ and $`f(x)`$ is some arbitrary
function.

One thing to note is that the bounds of a summation are _inclusive_: in the
examples above, $`i`$ varies from $`a`$ up to _and including_ $`b`$.

We will see examples of summations in use when analyzing the behavior of loops
later this quarter.

## Useful Summation Identities

### Splitting a Sum

**Rule:**

$`\displaystyle \sum_{i=a}^b (x + y) = \sum_{i=a}^b x + \sum_{i=a}^b y`$

**Example:**

$`\displaystyle \sum_{i=5}^{8} i = 5 + 6 + 7 + 8 = \sum_{i=0}^{8} i - \sum_{i=0}^{4} i`$

### Adjusting Summation Bounds

**Rule:**

$`\displaystyle \sum_{i=a}^b f(x) = \sum_{i=0}^b f(x) - \sum_{i=0}^{a - 1} f(x)`$

**Example:**

$`\displaystyle \sum_{i=5}^{8} i = 5 + 6 + 7 + 8 = \sum_{i=0}^{8} i - \sum_{i=0}^{4} i`$

### Factoring out a Constant

**Rule:**

$`\displaystyle \sum_{i=a}^b cf(i) = c \sum_{i=a}^b f(i)`$

**Example:**

$`\displaystyle \sum_{i=1}^5 10n = 10\sum_{i=1}^5 n`$

### Summation of a Constant

**Rule:**

$`\displaystyle \sum_{i=0}^{n-1} c = \underbrace{c + c + \cdots + c}_{\text{$n$ times}} = cn`$

**Example:**

$`\displaystyle \sum_{i=0}^{5-1} 10 = 10 + 10 + 10 + 10 + 10 = 50`$

### Gauss's Identity

**Rule:**

$`\displaystyle \sum_{i=0}^{n-1} i = \frac{n(n - 1)}{2}`$

**Example:**

$`\displaystyle \sum_{i=0}^{10-1} i = \frac{10(9)}{2} = 45`$

### Sum of Squares

**Rule:**

$`\displaystyle \sum_{i=0}^{n-1} i^2 = \frac{n(n - 1)(2n - 1)}{6}`$

**Example:**

$`\displaystyle \sum_{i=0}^{10-1} i^2 = \frac{10 \cdot 9 \cdot 19}{6} = 285`$

### Finite Geometric Series

**Rule:**

(Applicable only when $`x \ne 1`$)

$`\displaystyle \sum_{i=0}^{n-1} x^i = \frac{x^n - 1}{x - 1}`$

**Example:**

$`\displaystyle \sum_{i=0}^{10 - 1} 5^i = \frac{5^{10} - 1}{5 - 1} = 2441406`$

### Infinite Geometric Series

**Rule:**

(Applicable only when $`-1 \lt x \lt 1`$)

$`\displaystyle \sum_{i=0}^\infty x^i = \frac{1}{1 - x}`$

**Example:**

$`\displaystyle \sum_{i=0}^\infty \left(\frac{1}{2}\right)^i = \frac{1}{1 - 1/2} = 2`$

## Practice Problems

1. Simplify $`\displaystyle \sum_{k=1}^n k(k + 1)`$
2. Show that the sum of the first $`n`$ positive odd integers is $`n^2`$.
3. Simplify $`\displaystyle \sum_{k=1}^n (n-k)`$.
4. Simplify $`\displaystyle \sum_{k=0}^n 2^k`$.
5. Show that $`\displaystyle \sum_{k=1}^{\infty} \frac{1}{2^k}`$ converges to 1.

??? "Solutions"

    **Problem 1:** Simplify $`\displaystyle \sum_{k=1}^n k(k + 1)`$

    $` \displaystyle  \begin{aligned}  \sum_{k=1}^n k(k+1)  &= \sum_{k=1}^n k^2+k \\  &= \frac{n(n+1)(2n+1)}{6} + \frac{n(n+1)}{2}  \end{aligned}  `$

    **Problem 2:** Show that the sum of the first $`n`$ positive odd integers is $`n^2`$.

    $` \displaystyle  \begin{aligned}  \sum_{k=1}^n (2k - 1)  &= 2 \sum_{k=1}^n k - \sum_{k=1}^n 1\\  & = 2 \frac{n(n+1)}{2} - n \\  & = n^2  \end{aligned}  `$

    **Problem 3:** Simplify $`\displaystyle \sum_{k=1}^n (n-k)`$.

    $` \displaystyle  \begin{aligned}  \sum_{k=1}^n (n-k)  &= (n-1) + (n-2) + (n-3) + ... + 0\\  &= 1 + 2 + ... + (n-1) \\  &= \sum_{k=1}^{n-1} k \\  &= \frac{n(n-1)}{2}  \end{aligned}  `$

    **Problem 4:** Simplify $`\displaystyle \sum_{k=0}^n 2^k`$.

    $` \displaystyle  \begin{aligned}  \sum_{k=0}^n 2^k  &= 2^0 + 2^1 + 2^2 + ... + 2^n \\  &= 1 + 2 + 4 + ... + 2^n \\  &= \frac{2^{n+1} - 1}{2 - 1} \\  &= 2^{n+1} - 1  \end{aligned}  `$

    **Problem 5:** Show that $`\displaystyle \sum_{k=1}^{\infty} \frac{1}{2^k}`$ converges to 1.

    $` \displaystyle  \begin{aligned}  \sum_{k=1}^{\infty} \frac{1}{2^k}  &= \frac{1}{2} + \frac{1}{4} + \frac{1}{8} + \frac{1}{16} ...\\  &= \sum_{k=0}^{\infty} \frac{1}{2}\frac{1}{2^k}\\  &= \frac{1}{2} \sum_{k=0}^{\infty} \frac{1}{2^k}\\  &= \frac{1}{2} \cdot \frac{1}{1-\frac{1}{2}} \\  &= 1  \end{aligned}  `$

