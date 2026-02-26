# Week 5: Naive Bayes & BBN — 数学公式 + 手算

> **Source:** slides `Week5_NaiveBayes.pdf` + quiz4 + lab4 code
> **Scope:** Conditional Probability, Bayes Theorem, Naïve Bayes, Laplace Smoothing, BBN
> **See also:** [week5_naivebayes_cheatsheet.md](week5_naivebayes_cheatsheet.md) (概念速查) | [week5_naivebayes_code.md](week5_naivebayes_code.md) (代码)

---

## Conditional Probability & Bayes Theorem

### 📐 Formula

- **Conditional Probability:**

$$P(A|B) = \frac{P(A \cap B)}{P(B)}$$

$A$ = event, $B$ = condition, $P(A \cap B)$ = joint probability

- **Bayes Theorem:**

$$P(Y|X) = \frac{P(X|Y) \cdot P(Y)}{P(X)}$$

$Y$ = class, $X$ = features, $P(X|Y)$ = likelihood, $P(Y)$ = prior, $P(X)$ = evidence

- **MAP Rule:**

$$\hat{y} = \arg\max_Y \left[ P(X|Y) \cdot P(Y) \right]$$

$P(X)$ dropped because same for all classes

- **Evidence (Total Probability):**

$$P(X) = \sum_Y P(X|Y) \cdot P(Y)$$

Sum over all possible classes

### 📝 Hand Calc

- **Dice Example:** 2 dice, $A$ = sum is 8, $B$ = first die is 5

$$P(A) = \frac{5}{36}, \quad P(B) = \frac{6}{36}, \quad P(A \cap B) = \frac{1}{36} \quad \text{(only (5,3))}$$

$$P(A|B) = \frac{P(A \cap B)}{P(B)} = \frac{1/36}{6/36} = \mathbf{\frac{1}{6}}$$

---

## Naïve Bayes Classifier

### 📐 Formula

- **NB Classification:**

$$\hat{y} = \arg\max_Y \; P(Y) \times \prod_{i=1}^{d} P(X_i | Y)$$

$P(Y)$ = prior, $P(X_i|Y)$ = individual feature likelihood

- **Categorical Feature:**

$$P(X_i = c \mid Y = y) = \frac{n_c}{n}$$

$n_c$ = count of $X_i = c$ in class $y$, $n$ = total in class $y$

- **Continuous Feature (Gaussian):**

$$P(X_i \mid Y) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(X_i - \mu)^2}{2\sigma^2}\right)$$

$\mu$ = class mean, $\sigma^2$ = class variance (sample, ddof=1)

### 📝 Hand Calc

- **Tax Evasion Example:** $X = (\text{Refund=No, Divorced, Income=120K})$, 10 records, 7 No + 3 Yes

  **Step 1: Prior**

$$P(\text{No}) = \frac{7}{10} = 0.7, \quad P(\text{Yes}) = \frac{3}{10} = 0.3$$

**Step 2: Categorical likelihoods**

$$P(\text{Refund=No} \mid \text{No}) = \frac{4}{7}, \quad P(\text{Refund=No} \mid \text{Yes}) = \frac{3}{3} = 1$$

$$P(\text{Divorced} \mid \text{No}) = \frac{1}{7}, \quad P(\text{Divorced} \mid \text{Yes}) = \frac{1}{3}$$

**Step 3: Continuous likelihood (Gaussian)**

$$P(\text{Income=120K} \mid \text{No}): \; \mu=110, \; \sigma^2=2975 \;\Rightarrow\; P = 0.0072$$

$$P(\text{Income=120K} \mid \text{Yes}): \; \mu=90, \; \sigma^2=25 \;\Rightarrow\; P = 1.2 \times 10^{-9}$$

**Step 4: Posterior (unnormalized) — multiply all**

$$P(X \mid \text{No}) \times P(\text{No}) = \frac{4}{7} \times \frac{1}{7} \times 0.0072 \times 0.7 \approx \mathbf{4.2 \times 10^{-4}}$$

$$P(X \mid \text{Yes}) \times P(\text{Yes}) = 1 \times \frac{1}{3} \times 1.2 \times 10^{-9} \times 0.3 \approx \mathbf{1.2 \times 10^{-10}}$$

**Result:** $\text{No} \gg \text{Yes}$ → **Classify as No (不逃税)**

- **Lab4 Gender Example:** $X = (H=5.0, W=80, FS=5.0)$, 4M + 4F

  **Step 1:** $P(M) = P(F) = \frac{4}{8} = 0.5$

  **Step 2:** Compute $\mu$, $\sigma^2$ per class per feature (ddof=1 for sample variance)

  **Step 3:** Gaussian PDF $= \frac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$ for each feature

  **Step 4:** Posterior $\propto$ Prior $\times \prod P(X_i \mid \text{class})$ — multiply prior × all PDFs

  **Step 5:** Compare $P(M|X)$ vs $P(F|X)$ → classify

---

## Zero Probability & Laplace Smoothing

### 📐 Formula

- **Laplace Smoothing:**

$$P(X_i = c \mid Y) = \frac{n_c + 1}{n + v}$$

$n_c$ = count, $n$ = class total, $v$ = **number of possible values for $X_i$**

- **m-estimate:**

$$P(X_i = c \mid Y) = \frac{n_c + m \cdot p}{n + m}$$

$p$ = prior estimate (usually $1/v$), $m$ = confidence in $p$

### 📝 Hand Calc

- **Smoothing Example:** $P(\text{Married} \mid \text{Evade=Yes})$, 0 married evaders out of 3, Status has 3 values ($v=3$)

$$\text{Original: } P = \frac{0}{3} = \mathbf{0} \quad \leftarrow \text{entire product dies!}$$

$$\text{Laplace: } P = \frac{0 + 1}{3 + 3} = \mathbf{\frac{1}{6}} \quad \leftarrow \text{product survives}$$

- **m-estimate variants:**

$$m=0: \quad P = \frac{0 + 0 \times \frac{1}{3}}{3 + 0} = \frac{0}{3} = 0 \quad \text{[no smoothing]}$$

$$m=3: \quad P = \frac{0 + 3 \times \frac{1}{3}}{3 + 3} = \frac{1}{6} \quad \text{[≈ Laplace]}$$

$$m=10: \quad P = \frac{0 + 10 \times \frac{1}{3}}{3 + 10} = \frac{3.33}{13} \approx 0.256 \quad \text{[strong prior]}$$

---

## Bayesian Belief Network (BBN)

### 📐 Formula

- **No parents:** table contains $P(X)$ — prior
- **One parent $Y$:** table contains $P(X|Y)$ — conditional
- **Multiple parents $Y_1, \ldots, Y_k$:** table contains $P(X|Y_1, \ldots, Y_k)$ — joint conditional

### 📝 Hand Calc

- **Heart Disease BBN:** Exercise→HD, Diet→HD, HD→ChestPain, HD→BloodPressure
  - Query: $X = (E=\text{No}, D=\text{Healthy}, CP=\text{Yes}, BP=\text{High})$

  **Step 1: Get $P(\text{HD} \mid \text{parents})$**

$$P(\text{HD=Yes} \mid E=\text{No}, D=\text{Healthy}) = 0.45$$

$$P(\text{HD=No} \mid E=\text{No}, D=\text{Healthy}) = 0.55$$

**Step 2: Multiply symptoms given HD**

$$P(\text{all} \mid \text{HD=Yes}) = 0.45 \times 0.80 \times 0.85 = \mathbf{0.306}$$

$$P(\text{all} \mid \text{HD=No}) = 0.55 \times 0.01 \times 0.20 = \mathbf{0.0011}$$

**Step 3: Compare**

$$0.306 \gg 0.0011 \quad \Rightarrow \quad \mathbf{HD = Yes}$$

---

## Quick Formula Reference

| Name             | Formula                                             | Key Params                                      |
| ---------------- | --------------------------------------------------- | ----------------------------------------------- |
| Conditional Prob | $P(A \mid B) = \frac{P(A \cap B)}{P(B)}$            | $A$=event, $B$=condition                        |
| Bayes Theorem    | $P(Y \mid X) = \frac{P(X \mid Y) \cdot P(Y)}{P(X)}$ | Posterior = Lik×Prior/Evidence                  |
| NB Independence  | $P(X_1 \ldots X_d \mid Y) = \prod P(X_i \mid Y)$    | $d$ features, each independent                  |
| MAP Decision     | $\arg\max_Y P(Y) \times \prod P(X_i \mid Y)$        | Ignore $P(X)$ denominator                       |
| Categorical $P$  | $\frac{n_c}{n}$                                     | $n_c$=count in class, $n$=class total           |
| Gaussian $P$     | $\mathcal{N}(\mu, \sigma^2)$ PDF                    | $\mu$=class mean, $\sigma^2$=class var (ddof=1) |
| Laplace          | $\frac{n_c + 1}{n + v}$                             | $v$=attribute value count                       |
| m-estimate       | $\frac{n_c + mp}{n + m}$                            | $p$=prior est, $m$=confidence                   |
