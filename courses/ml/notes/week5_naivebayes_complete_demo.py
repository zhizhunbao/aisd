"""
Week 5: Naive Bayes & Bayesian Belief Network — Complete Demo
Demonstrates conditional probability, Bayes theorem, Naive Bayes classification,
Laplace smoothing, and BBN inference using examples from lecture slides.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.stats import norm

# ============================================================
# 配置常量
# Configuration Constants
# ============================================================

RANDOM_STATE = 42
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          'week5_naivebayes_complete_demo_pages')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 图表全局设置
# Global plot settings
plt.rcParams.update({
    'figure.figsize': (10, 6),
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
})

# ============================================================
# 步骤 1：条件概率 — 骰子例子
# Step 1: Conditional Probability — Dice Example
# ============================================================

# 掷两个骰子，A = 两骰子之和为8，B = 第一个骰子为5
# Roll two dice, A = sum is 8, B = first die is 5

# 枚举所有36种可能
# Enumerate all 36 outcomes
all_outcomes = [(d1, d2) for d1 in range(1, 7) for d2 in range(1, 7)]
total = len(all_outcomes)

# 事件 A: 两骰子之和为8
# Event A: sum of two dice is 8
event_A = [(d1, d2) for d1, d2 in all_outcomes if d1 + d2 == 8]

# 事件 B: 第一个骰子为5
# Event B: first die is 5
event_B = [(d1, d2) for d1, d2 in all_outcomes if d1 == 5]

# 交集 A ∩ B
# Intersection A ∩ B
event_AB = [(d1, d2) for d1, d2 in all_outcomes if d1 + d2 == 8 and d1 == 5]

P_A = len(event_A) / total
P_B = len(event_B) / total
P_AB = len(event_AB) / total

# 条件概率公式: P(A|B) = P(A ∩ B) / P(B)
# Conditional probability formula: P(A|B) = P(A ∩ B) / P(B)
P_A_given_B = P_AB / P_B

print("=" * 60)
print("Step 1: Conditional Probability — Dice Example")
print("=" * 60)
print(f"Event A (sum=8): {event_A}")
print(f"Event B (die1=5): {event_B}")
print(f"Event A ∩ B: {event_AB}")
print(f"P(A) = {len(event_A)}/{total} = {P_A:.4f}")
print(f"P(B) = {len(event_B)}/{total} = {P_B:.4f}")
print(f"P(A ∩ B) = {len(event_AB)}/{total} = {P_AB:.4f}")
print(f"P(A|B) = P(A∩B)/P(B) = ({P_AB:.4f})/({P_B:.4f}) = {P_A_given_B:.4f}")
print(f"  → Knowing die1=5, probability sum=8 is 1/6 ≈ {1/6:.4f}")

# 可视化：条件概率的"缩小宇宙"效果
# Visualization: "shrinking universe" effect of conditional probability
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# 左图：全部36种结果
# Left: all 36 outcomes
grid = np.zeros((6, 6))
for d1, d2 in event_A:
    grid[d1-1][d2-1] = 1  # 标记 sum=8
ax = axes[0]
ax.imshow(grid, cmap='Blues', alpha=0.7, origin='lower', extent=[0.5, 6.5, 0.5, 6.5])
for d1 in range(1, 7):
    for d2 in range(1, 7):
        color = 'red' if d1 + d2 == 8 else 'gray'
        weight = 'bold' if d1 + d2 == 8 else 'normal'
        ax.text(d2, d1, f"({d1},{d2})", ha='center', va='center',
                fontsize=7, color=color, fontweight=weight)
ax.set_xlabel("Die 2")
ax.set_ylabel("Die 1")
ax.set_title(f"Full Universe: P(A=sum8) = {len(event_A)}/36 = {P_A:.3f}")
ax.set_xticks(range(1, 7))
ax.set_yticks(range(1, 7))

# 右图：条件 B (die1=5) 后缩小的宇宙
# Right: reduced universe after conditioning on B (die1=5)
grid2 = np.zeros((6, 6))
for d1, d2 in event_B:
    grid2[d1-1][d2-1] = 0.3  # 标记 die1=5 的行
for d1, d2 in event_AB:
    grid2[d1-1][d2-1] = 1    # 标记交集
ax = axes[1]
ax.imshow(grid2, cmap='Oranges', alpha=0.7, origin='lower', extent=[0.5, 6.5, 0.5, 6.5])
for d1 in range(1, 7):
    for d2 in range(1, 7):
        if d1 == 5:
            color = 'red' if d1 + d2 == 8 else 'darkblue'
            weight = 'bold'
        else:
            color = 'lightgray'
            weight = 'normal'
        ax.text(d2, d1, f"({d1},{d2})", ha='center', va='center',
                fontsize=7, color=color, fontweight=weight)
ax.set_xlabel("Die 2")
ax.set_ylabel("Die 1")
ax.set_title(f"Conditional: P(A|B=die1=5) = {len(event_AB)}/{len(event_B)} = {P_A_given_B:.3f}")
ax.set_xticks(range(1, 7))
ax.set_yticks(range(1, 7))

plt.suptitle("Conditional Probability = Shrinking the Universe",
             fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'step1_conditional_probability.png'),
            dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# 步骤 2：贝叶斯定理 — 概率的"翻转"
# Step 2: Bayes Theorem — "Flipping" Probabilities
# ============================================================

# 医院检查类比：P(Disease|Positive) vs P(Positive|Disease)
# Hospital test analogy: P(Disease|Positive) vs P(Positive|Disease)

# 已知参数
# Known parameters
p_disease = 0.001         # 先验：人群中有病的比例 / Prior: prevalence
p_positive_given_disease = 0.99  # 灵敏度：有病检测阳性 / Sensitivity: true positive rate
p_positive_given_no_disease = 0.05  # 假阳性率 / False positive rate

# 贝叶斯定理计算
# Bayes theorem calculation
p_no_disease = 1 - p_disease
p_positive = (p_positive_given_disease * p_disease +
              p_positive_given_no_disease * p_no_disease)
p_disease_given_positive = (p_positive_given_disease * p_disease) / p_positive

print("\n" + "=" * 60)
print("Step 2: Bayes Theorem — Hospital Test Example")
print("=" * 60)
print(f"Prior: P(Disease) = {p_disease}")
print(f"Sensitivity: P(Positive|Disease) = {p_positive_given_disease}")
print(f"False Positive Rate: P(Positive|No Disease) = {p_positive_given_no_disease}")
print(f"\nP(Positive) = P(+|D)×P(D) + P(+|~D)×P(~D)")
print(f"            = {p_positive_given_disease}×{p_disease} + "
      f"{p_positive_given_no_disease}×{p_no_disease}")
print(f"            = {p_positive:.6f}")
print(f"\nP(Disease|Positive) = P(+|D)×P(D) / P(+)")
print(f"                    = ({p_positive_given_disease}×{p_disease}) / {p_positive:.6f}")
print(f"                    = {p_disease_given_positive:.4f}")
print(f"\n→ Even with 99% sensitivity, positive test only means "
      f"{p_disease_given_positive:.1%} chance of disease!")
print(f"  Reason: The disease is very rare (prior = {p_disease})")

# 可视化：先验对后验的影响
# Visualization: How prior affects posterior
prevalences = np.linspace(0.0001, 0.1, 200)
posteriors = []
for prev in prevalences:
    p_pos = p_positive_given_disease * prev + p_positive_given_no_disease * (1 - prev)
    post = (p_positive_given_disease * prev) / p_pos
    posteriors.append(post)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(prevalences * 100, np.array(posteriors) * 100, 'b-', linewidth=2)
ax.axhline(y=50, color='r', linestyle='--', alpha=0.5, label='50% threshold')
ax.axvline(x=p_disease * 100, color='g', linestyle=':', alpha=0.7,
           label=f'Our example ({p_disease*100:.2f}%)')
ax.scatter([p_disease * 100], [p_disease_given_positive * 100],
           color='red', s=100, zorder=5, label=f'P(D|+)={p_disease_given_positive:.1%}')
ax.set_xlabel("Disease Prevalence P(Disease) [%]")
ax.set_ylabel("P(Disease | Positive Test) [%]")
ax.set_title("Bayes Theorem: Prior Matters!\n"
             "Even a 99% accurate test can give misleading results with rare diseases")
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'step2_bayes_theorem_prior_effect.png'),
            dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# 步骤 3：税务逃税数据集 — 朴素贝叶斯分类
# Step 3: Tax Evasion Dataset — Naive Bayes Classification
# ============================================================

# 从 slides 中的数据集
# Dataset from slides
# 属性: Refund (Y/N), Marital Status (S/M/D), Taxable Income, Evade (Y/N)
# Attributes: Refund (Y/N), Marital Status (S/M/D), Taxable Income, Evade (Y/N)

print("\n" + "=" * 60)
print("Step 3: Tax Evasion — Naive Bayes Classification")
print("=" * 60)

# 数据集（10条记录）
# Dataset (10 records)
data = {
    'Refund':   ['Yes', 'No',  'No',  'Yes', 'No',  'No',  'Yes', 'No',  'No',  'No'],
    'Marital':  ['Single', 'Married', 'Single', 'Married', 'Divorced',
                 'Married', 'Divorced', 'Single', 'Married', 'Single'],
    'Income':   [125, 100, 70, 120, 95, 60, 220, 85, 75, 90],
    'Evade':    ['No', 'No', 'No', 'No', 'Yes', 'No', 'No', 'Yes', 'No', 'Yes']
}

# 测试记录: X = (Refund=No, Divorced, Income=120K)
# Test record: X = (Refund=No, Divorced, Income=120K)
test_refund = 'No'
test_marital = 'Divorced'
test_income = 120

# ----------------------------------------
# 步骤 3.1：计算先验概率 P(Y)
# Step 3.1: Compute prior probabilities P(Y)
# ----------------------------------------

n_total = len(data['Evade'])
n_no = data['Evade'].count('No')
n_yes = data['Evade'].count('Yes')
p_no = n_no / n_total
p_yes = n_yes / n_total

print(f"\nPrior Probabilities:")
print(f"  P(Evade=No)  = {n_no}/{n_total} = {p_no:.1f}")
print(f"  P(Evade=Yes) = {n_yes}/{n_total} = {p_yes:.1f}")

# ----------------------------------------
# 步骤 3.2：计算分类属性的条件概率
# Step 3.2: Compute conditional probs for categorical attributes
# ----------------------------------------

# 根据类别分组索引
# Group indices by class
idx_no = [i for i, e in enumerate(data['Evade']) if e == 'No']
idx_yes = [i for i, e in enumerate(data['Evade']) if e == 'Yes']

# P(Refund=No | Evade=No)
refund_no_given_no = sum(1 for i in idx_no if data['Refund'][i] == 'No') / len(idx_no)
# P(Refund=No | Evade=Yes)
refund_no_given_yes = sum(1 for i in idx_yes if data['Refund'][i] == 'No') / len(idx_yes)
# P(Divorced | Evade=No)
divorced_given_no = sum(1 for i in idx_no if data['Marital'][i] == 'Divorced') / len(idx_no)
# P(Divorced | Evade=Yes)
divorced_given_yes = sum(1 for i in idx_yes if data['Marital'][i] == 'Divorced') / len(idx_yes)

print(f"\nCategorical Likelihoods:")
print(f"  P(Refund=No  | Evade=No)  = {sum(1 for i in idx_no if data['Refund'][i] == 'No')}/{len(idx_no)} = {refund_no_given_no:.4f}")
print(f"  P(Refund=No  | Evade=Yes) = {sum(1 for i in idx_yes if data['Refund'][i] == 'No')}/{len(idx_yes)} = {refund_no_given_yes:.4f}")
print(f"  P(Divorced   | Evade=No)  = {sum(1 for i in idx_no if data['Marital'][i] == 'Divorced')}/{len(idx_no)} = {divorced_given_no:.4f}")
print(f"  P(Divorced   | Evade=Yes) = {sum(1 for i in idx_yes if data['Marital'][i] == 'Divorced')}/{len(idx_yes)} = {divorced_given_yes:.4f}")

# ----------------------------------------
# 步骤 3.3：计算连续属性的条件概率（高斯分布）
# Step 3.3: Compute conditional probs for continuous attribute (Gaussian)
# ----------------------------------------

income_no = [data['Income'][i] for i in idx_no]
income_yes = [data['Income'][i] for i in idx_yes]

# 均值和方差（样本方差 ddof=1）
# Mean and variance (sample variance ddof=1)
mu_no = np.mean(income_no)
var_no = np.var(income_no, ddof=1)
mu_yes = np.mean(income_yes)
var_yes = np.var(income_yes, ddof=1)

# 高斯PDF: P(x|class) = (1/√(2πσ²)) × exp(-(x-μ)²/(2σ²))
# Gaussian PDF: P(x|class) = (1/√(2πσ²)) × exp(-(x-μ)²/(2σ²))
p_income_given_no = norm.pdf(test_income, mu_no, np.sqrt(var_no))
p_income_given_yes = norm.pdf(test_income, mu_yes, np.sqrt(var_yes))

print(f"\nContinuous Attribute (Income, Gaussian assumption):")
print(f"  Evade=No:  μ={mu_no:.1f}, σ²={var_no:.1f}")
print(f"    P(Income=120K | No)  = {p_income_given_no:.6e}")
print(f"  Evade=Yes: μ={mu_yes:.1f}, σ²={var_yes:.1f}")
print(f"    P(Income=120K | Yes) = {p_income_given_yes:.6e}")

# ----------------------------------------
# 步骤 3.4：计算后验概率并分类
# Step 3.4: Compute posterior probabilities and classify
# ----------------------------------------

# P(X|No) × P(No) vs P(X|Yes) × P(Yes)
posterior_no = refund_no_given_no * divorced_given_no * p_income_given_no * p_no
posterior_yes = refund_no_given_yes * divorced_given_yes * p_income_given_yes * p_yes

print(f"\nPosterior (unnormalized):")
print(f"  P(X|No)×P(No)   = {refund_no_given_no:.4f} × {divorced_given_no:.4f} × "
      f"{p_income_given_no:.4e} × {p_no:.1f}")
print(f"                   = {posterior_no:.6e}")
print(f"  P(X|Yes)×P(Yes)  = {refund_no_given_yes:.4f} × {divorced_given_yes:.4f} × "
      f"{p_income_given_yes:.4e} × {p_yes:.1f}")
print(f"                   = {posterior_yes:.6e}")

# 归一化
# Normalize
total_post = posterior_no + posterior_yes
print(f"\nNormalized Posterior:")
print(f"  P(Evade=No  | X) = {posterior_no/total_post:.6f}")
print(f"  P(Evade=Yes | X) = {posterior_yes/total_post:.6f}")
print(f"\n→ Classification: Evade = {'No' if posterior_no > posterior_yes else 'Yes'}")

# 可视化：两个类别的收入分布及测试点
# Visualization: Income distribution for both classes and test point
fig, ax = plt.subplots(figsize=(10, 6))
x_range = np.linspace(30, 250, 500)

# 绘制两个类别的高斯分布
# Plot Gaussian distributions for both classes
pdf_no = norm.pdf(x_range, mu_no, np.sqrt(var_no))
pdf_yes = norm.pdf(x_range, mu_yes, np.sqrt(var_yes))

ax.plot(x_range, pdf_no, 'b-', linewidth=2, label=f'Evade=No (μ={mu_no:.0f}, σ²={var_no:.0f})')
ax.plot(x_range, pdf_yes, 'r-', linewidth=2, label=f'Evade=Yes (μ={mu_yes:.0f}, σ²={var_yes:.0f})')
ax.fill_between(x_range, pdf_no, alpha=0.2, color='blue')
ax.fill_between(x_range, pdf_yes, alpha=0.2, color='red')

# 标记测试点
# Mark test point
ax.axvline(x=test_income, color='green', linestyle='--', linewidth=2, label=f'Test: Income={test_income}K')
ax.scatter([test_income], [p_income_given_no], color='blue', s=80, zorder=5, marker='o')
ax.scatter([test_income], [p_income_given_yes], color='red', s=80, zorder=5, marker='o')

ax.annotate(f'P(120K|No)={p_income_given_no:.4f}', xy=(test_income, p_income_given_no),
            xytext=(test_income+20, p_income_given_no+0.002), fontsize=9,
            arrowprops=dict(arrowstyle='->', color='blue'))

ax.set_xlabel("Taxable Income (K$)")
ax.set_ylabel("Probability Density")
ax.set_title("Naive Bayes: Gaussian Likelihood for Continuous Feature\n"
             "Income=120K is very unlikely for Evade=Yes (μ=90, σ²=25)")
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'step3_gaussian_likelihood.png'),
            dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# 步骤 4：零概率问题与拉普拉斯平滑
# Step 4: Zero Probability Problem & Laplace Smoothing
# ============================================================

print("\n" + "=" * 60)
print("Step 4: Zero Probability Problem & Laplace Smoothing")
print("=" * 60)

# 问题：P(Married | Evade=Yes) = 0/3 = 0
# Problem: P(Married | Evade=Yes) = 0/3 = 0
married_given_yes_count = sum(1 for i in idx_yes if data['Marital'][i] == 'Married')
p_married_given_yes_raw = married_given_yes_count / len(idx_yes)

print(f"\nZero Probability Problem:")
print(f"  P(Married | Evade=Yes) = {married_given_yes_count}/{len(idx_yes)} = {p_married_given_yes_raw}")
print(f"  → ANY product involving this term becomes 0!")

# 如果测试记录是 (Married, ...)
# If test record is (Married, ...)
print(f"\n  For test X = (Married, ...): P(X|Yes) = P(Married|Yes) × ... = 0 × ... = 0")
print(f"  → Cannot classify! No matter how 'suspicious' other features are.")

# ----------------------------------------
# 步骤 4.1：拉普拉斯平滑（加1平滑）
# Step 4.1: Laplace Smoothing (add-1 smoothing)
# ----------------------------------------

# 拉普拉斯平滑: P(Xᵢ = c | Y) = (nᶜ + 1) / (n + v)
# Laplace smoothing: P(Xᵢ = c | Y) = (nᶜ + 1) / (n + v)
# 其中 v = Marital Status 的可取值数 = 3 (Single, Married, Divorced)
# where v = number of possible values for Marital Status = 3

v_marital = 3  # Single, Married, Divorced

# 用平滑重新计算
# Recalculate with smoothing
print(f"\nLaplace Smoothing (v={v_marital} for Marital Status):")
print(f"  P(c|Y) = (nᶜ + 1) / (n + v)")
print(f"  v = number of possible values for the attribute")

marital_counts_yes = {s: sum(1 for i in idx_yes if data['Marital'][i] == s)
                      for s in ['Single', 'Married', 'Divorced']}
marital_counts_no = {s: sum(1 for i in idx_no if data['Marital'][i] == s)
                     for s in ['Single', 'Married', 'Divorced']}

print(f"\n  Without smoothing (Evade=Yes, n={len(idx_yes)}):")
for status, count in marital_counts_yes.items():
    print(f"    P({status}|Yes) = {count}/{len(idx_yes)} = {count/len(idx_yes):.4f}")

print(f"\n  With Laplace smoothing (Evade=Yes, n={len(idx_yes)}, v={v_marital}):")
for status, count in marital_counts_yes.items():
    smoothed = (count + 1) / (len(idx_yes) + v_marital)
    print(f"    P({status}|Yes) = ({count}+1)/({len(idx_yes)}+{v_marital}) = "
          f"{count+1}/{len(idx_yes)+v_marital} = {smoothed:.4f}")

# ----------------------------------------
# 步骤 4.2：m-估计
# Step 4.2: m-estimate
# ----------------------------------------

print(f"\nm-estimate: P(c|Y) = (nᶜ + m×p) / (n + m)")
print(f"  p = prior estimate (usually 1/v = 1/{v_marital} = {1/v_marital:.4f})")
print(f"  m = confidence in p (hyperparameter)")

for m_val in [0, 3, 10]:
    p_val = 1 / v_marital
    smoothed = (married_given_yes_count + m_val * p_val) / (len(idx_yes) + m_val)
    interpretation = "no smoothing" if m_val == 0 else (
        "≈ Laplace" if m_val == v_marital else "strong prior")
    print(f"  m={m_val}: P(Married|Yes) = ({married_given_yes_count}+{m_val}×{p_val:.2f})/({len(idx_yes)}+{m_val}) = {smoothed:.4f}  [{interpretation}]")

# 可视化：平滑效果对比
# Visualization: Smoothing effect comparison
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 左图：原始 vs 平滑概率
# Left: Original vs smoothed probabilities
statuses = ['Single', 'Married', 'Divorced']
raw_probs = [marital_counts_yes[s] / len(idx_yes) for s in statuses]
smoothed_probs = [(marital_counts_yes[s] + 1) / (len(idx_yes) + v_marital) for s in statuses]

x_pos = np.arange(len(statuses))
width = 0.35

axes[0].bar(x_pos - width/2, raw_probs, width, label='Original', color='coral', alpha=0.8)
axes[0].bar(x_pos + width/2, smoothed_probs, width, label='Laplace Smoothed', color='steelblue', alpha=0.8)
axes[0].set_xticks(x_pos)
axes[0].set_xticklabels(statuses)
axes[0].set_ylabel('P(Status | Evade=Yes)')
axes[0].set_title('Zero Probability Fix:\nP(Married|Yes) = 0 → 1/6')
axes[0].legend()
axes[0].annotate('ZERO!', xy=(1 - width/2, 0.01), fontsize=12, color='red',
                fontweight='bold', ha='center')
axes[0].grid(axis='y', alpha=0.3)

# 右图：不同 m 值的 m-估计效果
# Right: m-estimate with different m values
m_values = np.linspace(0, 20, 100)
m_estimates = [(married_given_yes_count + m * (1/v_marital)) / (len(idx_yes) + m) for m in m_values]

axes[1].plot(m_values, m_estimates, 'b-', linewidth=2)
axes[1].axhline(y=1/v_marital, color='red', linestyle='--', alpha=0.5,
                label=f'Prior p=1/{v_marital}={1/v_marital:.3f}')
axes[1].axhline(y=0, color='gray', linestyle=':', alpha=0.5, label='Original (m=0)')
axes[1].axvline(x=v_marital, color='green', linestyle=':', alpha=0.5,
                label=f'm={v_marital} (≈Laplace)')
axes[1].set_xlabel('m (confidence in prior)')
axes[1].set_ylabel('P(Married | Evade=Yes)')
axes[1].set_title('m-estimate: How m Controls Smoothing\n'
                  'Larger m → more trust in prior, less in data')
axes[1].legend(fontsize=9)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'step4_laplace_smoothing.png'),
            dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# 步骤 5：朴素贝叶斯的优缺点 — 实验演示
# Step 5: NB Strengths & Weaknesses — Experimental Demo
# ============================================================

print("\n" + "=" * 60)
print("Step 5: Naive Bayes — Strengths & Weaknesses Demo")
print("=" * 60)

# 用 sklearn 的 GaussianNB 在合成数据上演示
# Use sklearn's GaussianNB on synthetic data to demonstrate
from sklearn.datasets import make_classification
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ----------------------------------------
# 步骤 5.1：独立特征 → NB 表现优
# Step 5.1: Independent features → NB performs well
# ----------------------------------------

# 生成独立特征的数据
# Generate data with independent features
X_indep, y_indep = make_classification(
    n_samples=500, n_features=4, n_informative=4,
    n_redundant=0, n_clusters_per_class=1, random_state=RANDOM_STATE
)
X_train, X_test, y_train, y_test = train_test_split(
    X_indep, y_indep, test_size=0.3, random_state=RANDOM_STATE
)

gnb = GaussianNB()
gnb.fit(X_train, y_train)
acc_indep = accuracy_score(y_test, gnb.predict(X_test))

print(f"\nCase 1: Independent features (n_redundant=0)")
print(f"  Accuracy: {acc_indep:.4f}")

# ----------------------------------------
# 步骤 5.2：冗余特征 → NB 可能下降
# Step 5.2: Redundant features → NB may degrade
# ----------------------------------------

# 生成有冗余特征的数据
# Generate data with redundant features
X_redun, y_redun = make_classification(
    n_samples=500, n_features=4, n_informative=2,
    n_redundant=2, n_clusters_per_class=1, random_state=RANDOM_STATE
)
X_train2, X_test2, y_train2, y_test2 = train_test_split(
    X_redun, y_redun, test_size=0.3, random_state=RANDOM_STATE
)

gnb2 = GaussianNB()
gnb2.fit(X_train2, y_train2)
acc_redun = accuracy_score(y_test2, gnb2.predict(X_test2))

print(f"\nCase 2: Redundant features (n_redundant=2)")
print(f"  Accuracy: {acc_redun:.4f}")
print(f"  → NB can still work decently because classification only needs")
print(f"    correct relative ranking, not exact probability values!")

# ============================================================
# 步骤 6：贝叶斯信念网络 (BBN) — 心脏病预测
# Step 6: Bayesian Belief Network (BBN) — Heart Disease
# ============================================================

print("\n" + "=" * 60)
print("Step 6: Bayesian Belief Network — Heart Disease Example")
print("=" * 60)

# BBN 结构（从 slides）:
# BBN structure (from slides):
#  Exercise → Heart Disease ← Diet
#  Heart Disease → Chest Pain
#  Heart Disease → Blood Pressure

# 概率表（根节点）
# Probability tables (root nodes)
P_Exercise = {'Yes': 0.7, 'No': 0.3}
P_Diet = {'Healthy': 0.25, 'Unhealthy': 0.75}

# P(Heart Disease | Exercise, Diet)
P_HD_given = {
    ('Yes', 'Healthy'):   {'Yes': 0.25, 'No': 0.75},
    ('Yes', 'Unhealthy'): {'Yes': 0.55, 'No': 0.45},
    ('No', 'Healthy'):    {'Yes': 0.45, 'No': 0.55},
    ('No', 'Unhealthy'):  {'Yes': 0.75, 'No': 0.25},
}

# P(Chest Pain | Heart Disease)
P_CP_given_HD = {'Yes': {'Yes': 0.80, 'No': 0.20},
                 'No':  {'Yes': 0.01, 'No': 0.99}}

# P(Blood Pressure=High | Heart Disease)
P_BP_given_HD = {'Yes': {'High': 0.85, 'Low': 0.15},
                 'No':  {'High': 0.20, 'Low': 0.80}}

# 查询: X = (Exercise=No, Diet=Healthy, Chest Pain=Yes, BP=High)
# Query: X = (Exercise=No, Diet=Healthy, Chest Pain=Yes, BP=High)
test_exercise = 'No'
test_diet = 'Healthy'
test_cp = 'Yes'
test_bp = 'High'

print(f"\nQuery: Exercise={test_exercise}, Diet={test_diet}, "
      f"CP={test_cp}, BP={test_bp}")
print(f"\nNetwork Structure:")
print(f"  Exercise → Heart Disease ← Diet")
print(f"  Heart Disease → Chest Pain")
print(f"  Heart Disease → Blood Pressure")

# BBN 推理
# BBN Inference
p_hd_yes = P_HD_given[(test_exercise, test_diet)]['Yes']
p_hd_no = P_HD_given[(test_exercise, test_diet)]['No']

print(f"\nStep 1: P(HD | Exercise={test_exercise}, Diet={test_diet})")
print(f"  P(HD=Yes | E=No, D=Healthy) = {p_hd_yes}")
print(f"  P(HD=No  | E=No, D=Healthy) = {p_hd_no}")

# 似然 P(CP, BP | HD)
# Likelihood P(CP, BP | HD)
p_symptoms_given_hd_yes = P_CP_given_HD['Yes'][test_cp] * P_BP_given_HD['Yes'][test_bp]
p_symptoms_given_hd_no = P_CP_given_HD['No'][test_cp] * P_BP_given_HD['No'][test_bp]

print(f"\nStep 2: P(Symptoms | HD)")
print(f"  P(CP=Yes, BP=High | HD=Yes) = {P_CP_given_HD['Yes'][test_cp]} × {P_BP_given_HD['Yes'][test_bp]} = {p_symptoms_given_hd_yes:.4f}")
print(f"  P(CP=Yes, BP=High | HD=No)  = {P_CP_given_HD['No'][test_cp]} × {P_BP_given_HD['No'][test_bp]} = {p_symptoms_given_hd_no:.4f}")

# 后验（未归一化）
# Posterior (unnormalized)
posterior_hd_yes = p_hd_yes * p_symptoms_given_hd_yes
posterior_hd_no = p_hd_no * p_symptoms_given_hd_no

print(f"\nStep 3: Posterior (unnormalized)")
print(f"  P(HD=Yes) × P(Symptoms|Yes) = {p_hd_yes} × {p_symptoms_given_hd_yes:.4f} = {posterior_hd_yes:.4f}")
print(f"  P(HD=No)  × P(Symptoms|No)  = {p_hd_no} × {p_symptoms_given_hd_no:.4f} = {posterior_hd_no:.4f}")

# 归一化
# Normalize
total_hd = posterior_hd_yes + posterior_hd_no
p_hd_yes_norm = posterior_hd_yes / total_hd

print(f"\nStep 4: Normalized")
print(f"  P(HD=Yes | all evidence) = {p_hd_yes_norm:.4f}")
print(f"  P(HD=No  | all evidence) = {1-p_hd_yes_norm:.4f}")
print(f"\n→ Classification: Heart Disease = {'Yes' if posterior_hd_yes > posterior_hd_no else 'No'}")
print(f"  ({posterior_hd_yes:.4f} >> {posterior_hd_no:.4f})")

# 可视化：BBN 结构与推理过程
# Visualization: BBN structure and inference process
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# 左图：BBN 网络结构
# Left: BBN network structure
ax = axes[0]
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# 节点位置
# Node positions
nodes = {
    'Exercise': (3, 8),
    'Diet': (7, 8),
    'Heart\nDisease': (5, 5),
    'Chest\nPain': (3, 2),
    'Blood\nPressure': (7, 2),
}

# 绘制节点
# Draw nodes
for name, (x, y) in nodes.items():
    circle = plt.Circle((x, y), 1, fill=True, facecolor='lightblue',
                        edgecolor='navy', linewidth=2)
    ax.add_patch(circle)
    ax.text(x, y, name, ha='center', va='center', fontsize=9, fontweight='bold')

# 绘制有向边
# Draw directed edges
edges = [('Exercise', 'Heart\nDisease'), ('Diet', 'Heart\nDisease'),
         ('Heart\nDisease', 'Chest\nPain'), ('Heart\nDisease', 'Blood\nPressure')]
for src, dst in edges:
    sx, sy = nodes[src]
    dx, dy = nodes[dst]
    ax.annotate('', xy=(dx, dy + 1), xytext=(sx, sy - 1),
                arrowprops=dict(arrowstyle='->', color='navy', lw=2))

ax.set_title("BBN: Heart Disease Network\n(DAG with conditional probability tables)",
             fontsize=13, fontweight='bold')

# 右图：推理结果柱状图
# Right: Inference result bar chart
ax = axes[1]
categories = ['P(HD=Yes|E,D)\n×P(symp|Yes)', 'P(HD=No|E,D)\n×P(symp|No)']
values = [posterior_hd_yes, posterior_hd_no]
colors = ['#e74c3c', '#3498db']
bars = ax.bar(categories, values, color=colors, alpha=0.8, edgecolor='black')

for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
            f'{val:.4f}', ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_ylabel('Unnormalized Posterior')
ax.set_title(f"BBN Inference: HD=Yes ({posterior_hd_yes:.4f}) >> HD=No ({posterior_hd_no:.4f})\n"
             f"Query: Exercise=No, Diet=Healthy, CP=Yes, BP=High",
             fontsize=11)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'step6_bbn_heart_disease.png'),
            dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# 步骤 7：朴素贝叶斯 vs BBN — 结构对比
# Step 7: Naive Bayes vs BBN — Structural Comparison
# ============================================================

print("\n" + "=" * 60)
print("Step 7: Naive Bayes vs BBN — Comparison")
print("=" * 60)

print("""
┌─────────────────────────────────────────────────────────────┐
│  Naive Bayes (Star Structure)    │  BBN (Flexible DAG)     │
│                                  │                         │
│        Y (class)                 │  Exercise    Diet       │
│       /|\\  \\                     │      \\       /          │
│      X₁ X₂ X₃ Xd                │    Heart Disease        │
│                                  │       /      \\          │
│  ALL features independent        │  Chest Pain  BP         │
│  given Y                         │                         │
│                                  │  Only non-descendants   │
│  Fewer parameters (linear)       │  CI given parents       │
│  Simple, fast                    │                         │
│  Works even when CI violated     │  More parameters        │
│                                  │  More flexible          │
│                                  │  Models real deps       │
└─────────────────────────────────────────────────────────────┘
""")

comparison = {
    'Feature': ['Structure', 'Independence', 'Flexibility', 'Parameters', 'Data Needed'],
    'Naive Bayes': ['Y → all Xᵢ (star)', 'ALL features CI given Y',
                    'Low — fixed structure', 'O(d×v) linear', 'Less'],
    'BBN': ['Any DAG allowed', 'Non-descendants CI given parents',
            'High — models real deps', 'Depends on DAG', 'More (complex tables)']
}

print(f"{'Feature':<20} {'Naive Bayes':<30} {'BBN':<30}")
print("-" * 80)
for i in range(len(comparison['Feature'])):
    print(f"{comparison['Feature'][i]:<20} {comparison['Naive Bayes'][i]:<30} {comparison['BBN'][i]:<30}")

# ============================================================
# 步骤 8：完整流程图 — 从数据到分类
# Step 8: Complete Pipeline — From Data to Classification
# ============================================================

print("\n" + "=" * 60)
print("Step 8: Complete Naive Bayes Pipeline Summary")
print("=" * 60)

print("""
Complete Naive Bayes Classification Pipeline:

  ┌──────────────────────────────────────────────────┐
  │  1. Compute Prior: P(Y) = count(Y) / total       │
  ├──────────────────────────────────────────────────┤
  │  2. For each feature Xᵢ:                         │
  │     • Categorical: P(Xᵢ=c|Y) = nᶜ/n             │
  │     • Continuous:  Fit Gaussian → N(μ, σ²)        │
  ├──────────────────────────────────────────────────┤
  │  3. Apply Laplace if zero probability:            │
  │     P(Xᵢ=c|Y) = (nᶜ+1)/(n+v)                    │
  ├──────────────────────────────────────────────────┤
  │  4. Multiply: P(Y) × ∏ᵢ P(Xᵢ|Y)                 │
  ├──────────────────────────────────────────────────┤
  │  5. Pick Y that maximizes the product (MAP)       │
  └──────────────────────────────────────────────────┘
""")

print(f"\nAll visualizations saved to: {OUTPUT_DIR}")
print(f"Files generated:")
for f in sorted(os.listdir(OUTPUT_DIR)):
    fpath = os.path.join(OUTPUT_DIR, f)
    size_kb = os.path.getsize(fpath) / 1024
    print(f"  {f} ({size_kb:.1f} KB)")
