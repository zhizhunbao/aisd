# Week 5: Naive Bayes & BBN — 概念速查

> **Source:** slides `Week5_NaiveBayes.pdf` + quiz4 + lab4 code
> **Scope:** Conditional Probability, Bayes Theorem, Naïve Bayes, Laplace Smoothing, BBN
> **See also:** [week5_naivebayes_math.md](week5_naivebayes_math.md) (公式+手算) | [week5_naivebayes_code.md](week5_naivebayes_code.md) (代码)

---

## Conditional Probability & Bayes Theorem

### 📖 Definition

- **Conditional Probability (条件概率):** probability of event A given event B has occurred
- **Bayes Theorem (贝叶斯定理):** formula to "flip" conditional probability — from P(X|Y) to P(Y|X)
- **Posterior (后验概率):** P(Y|X) — probability of class Y AFTER seeing features X
- **Likelihood (似然):** P(X|Y) — probability of features X IF class is Y
- **Prior (先验概率):** P(Y) — probability of class Y BEFORE seeing any features
- **Evidence (证据):** P(X) — total probability of observing features X across ALL classes
- **MAP (Maximum A-Posteriori, 最大后验估计):** decision rule — pick class with highest posterior

### 💡 Key Points

- P(X) is the SAME for all classes → can be ignored in MAP comparison
- Bayes "flips" P(X|Y) → P(Y|X): we know how features distribute per class → want class per feature
- Prior P(Y) = class frequency in training data (e.g. 7/10 vs 3/10)

### ⚠️ Traps

- ⚠️ MAP does NOT require computing P(X) — only compare numerators P(X|Y)×P(Y)
- ⚠️ Goal of Bayesian classification → maximize posterior P(Y|X), NOT joint P(X,Y) (quiz4 Q1)
- ⚠️ P(Y|X) is Posterior, NOT Prior — Prior is P(Y) without seeing X

---

## Naïve Bayes Classifier

### 📖 Definition

- **Naïve Bayes (朴素贝叶斯):** classifier that assumes ALL features are conditionally independent given class
- **Conditional Independence (条件独立):** P(X|Y,Z) = P(X|Z) — knowing Y adds no info about X once Z is known
- **"Naïve" Assumption (朴素假设):** P(X₁,X₂,...,Xd|Y) = ∏ P(Xᵢ|Y) — joint = product of marginals

### 💡 Key Points

- Conditional independence example: **arm length & reading skill** — correlated, but given **age**, independent
- NB can make decisions with **partial info**: even without all features, use available P(Xᵢ|Y)
- Parameters grow **linearly** with features (vs exponential for full joint)
- Despite "naïve" assumption, works well in practice — classification only needs correct **relative** ranking

### ⚠️ Traps

- ⚠️ Continuous attributes → use Gaussian distribution, NOT counting/frequency
- ⚠️ Sample variance uses **ddof=1** (divide by n-1), NOT ddof=0 (divide by n)
- ⚠️ Even if one P(Xᵢ|Y) is very small, it can dominate the product → check extreme values

---

## Zero Probability & Laplace Smoothing

### 📖 Definition

- **Zero Probability Problem (零概率问题):** if ANY P(Xᵢ=c|Y) = 0, entire product P(X|Y) = 0
- **Laplace Smoothing (拉普拉斯平滑):** add 1 to every count to eliminate zero probabilities
- **m-estimate (m-估计):** generalized smoothing with confidence parameter m

### 💡 Key Points

- Without smoothing: one zero kills ENTIRE product, regardless of other strong evidence
- With smoothing: assigns small non-zero probability to unseen combinations
- m=0 → no smoothing; m=v, p=1/v → Laplace; larger m → stronger pull toward prior
- Smoothing effect diminishes with more data (counts dominate the +1)

### ⚠️ Traps

- ⚠️ v = number of possible values **of that attribute** (e.g. Marital Status: v=3), NOT number of classes
- ⚠️ Apply smoothing to ALL conditional probabilities consistently, not just the zero ones
- ⚠️ Laplace can change classification outcome — recompute ALL probabilities with smoothing

---

## Naïve Bayes: Strengths & Weaknesses

### 📖 Definition

- **Noise Robustness (噪声鲁棒性):** isolated outliers don't significantly affect probability estimates
- **Missing Value Handling (缺失值处理):** skip missing attribute in the product — still valid
- **Irrelevant Attribute Robustness (无关属性鲁棒性):** P(Xᵢ|Y₁) ≈ P(Xᵢ|Y₂) → attribute cancels out in comparison
- **Redundant Attributes (冗余属性):** correlated features violate independence assumption

### 💡 Key Points

- NB is **robust to**: isolated noise, missing values, irrelevant attributes
- NB is **vulnerable to**: redundant/correlated attributes (violate CI assumption)
- Even when CI assumption violated: still works decently (only relative order matters)

### ⚠️ Traps

- ⚠️ NB handles missing values naturally — just drop that term from product
- ⚠️ Correlated features → double-counting evidence → biased posterior

### 📊 Compare

| Property            | Naïve Bayes            |
| ------------------- | ---------------------- |
| Noise               | Robust                 |
| Missing Values      | Handles naturally      |
| Irrelevant Features | Robust (cancels out)   |
| Correlated Features | ❌ Violates assumption |

---

## Bayesian Belief Network (BBN)

### 📖 Definition

- **BBN (Bayesian Belief Network, 贝叶斯信念网络):** graphical model with DAG to represent probabilistic dependencies
- **DAG (Directed Acyclic Graph, 有向无环图):** graph where edges have direction & no cycles
- **Node (节点):** represents a random variable
- **Arc/Edge (弧/边):** represents dependency between two variables
- **Probability Table (概率表):** conditional probability table associated with each node
- **Parent/Child/Ancestor/Descendant:** directed graph relationships

### 💡 Key Points

- BBN CI rule: node is conditionally independent of **all non-descendants** given its **parents**
- Naïve Bayes = special case of BBN where Y is the ONLY parent of all Xᵢ
- BBN allows modeling dependencies that NB cannot (e.g. feature→feature edges)

### ⚠️ Traps

- ⚠️ BBN differs from NB: BBN allows conditional dependencies through DAG (quiz4 Q2)
- ⚠️ BBN CI condition: **parents known** → independent of non-descendants. NOT "any node known"
- ⚠️ BBN does NOT assume all attributes are independent — that's NB's assumption

### 📊 Compare

| Feature      | Naïve Bayes             | BBN                                   |
| ------------ | ----------------------- | ------------------------------------- |
| Structure    | Y → all Xᵢ (star)       | Any DAG                               |
| Independence | ALL features CI given Y | Only non-descendants CI given parents |
| Flexibility  | Low — fixed structure   | High — models real dependencies       |
| Data needed  | Less (fewer params)     | More (complex tables)                 |
| Accuracy     | Good if CI holds        | Better when features depend           |
