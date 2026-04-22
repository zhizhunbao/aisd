"""
Missing Value Types Comparison — 三种缺失值机制对比图
Visualizes MCAR, MAR, and MNAR with example patterns.
"""
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

# --- CJK Font ---
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial']
matplotlib.rcParams['axes.unicode_minus'] = False

np.random.seed(42)
plt.style.use('seaborn-v0_8-whitegrid')

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Color palette
colors = {
    'observed': '#3498db',
    'missing': '#e74c3c',
    'bg': '#ecf0f1',
}

# --- Helper: Create a data matrix with missing pattern ---
def plot_missing_pattern(ax, title, subtitle, data, mask, ylabel="Samples"):
    n_rows, n_cols = data.shape
    # Plot data cells
    for i in range(n_rows):
        for j in range(n_cols):
            color = colors['missing'] if mask[i, j] else colors['observed']
            alpha = 0.3 if mask[i, j] else 0.8
            rect = plt.Rectangle((j, n_rows - 1 - i), 1, 1,
                                  facecolor=color, edgecolor='white',
                                  linewidth=1.5, alpha=alpha)
            ax.add_patch(rect)
            if not mask[i, j]:
                ax.text(j + 0.5, n_rows - 0.5 - i, f"{data[i,j]:.0f}",
                        ha='center', va='center', fontsize=7, color='white',
                        fontweight='bold')
            else:
                ax.text(j + 0.5, n_rows - 0.5 - i, "?",
                        ha='center', va='center', fontsize=10, color='white',
                        fontweight='bold')

    ax.set_xlim(0, n_cols)
    ax.set_ylim(0, n_rows)
    ax.set_title(title, fontsize=12, fontweight='bold', pad=10)
    ax.set_xlabel(subtitle, fontsize=9, color='#7f8c8d')
    ax.set_xticks([0.5, 1.5, 2.5])
    ax.set_xticklabels(['Age\n年龄', 'Income\n收入', 'Color\n颜色'], fontsize=8)
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# --- MCAR: random missing ---
data1 = np.array([
    [25, 50000, 1],
    [30, 80000, 2],
    [45, 60000, 3],
    [22, 45000, 1],
    [38, 70000, 2],
    [50, 90000, 3],
    [28, 55000, 1],
    [35, 65000, 2],
])
mask1 = np.zeros_like(data1, dtype=bool)
# Randomly missing entries
mask1[1, 2] = True
mask1[3, 0] = True
mask1[5, 1] = True
mask1[7, 2] = True

plot_missing_pattern(axes[0], "MCAR\n完全随机缺失",
                     "Missingness is purely random\n缺失纯属偶然", data1, mask1)

# --- MAR: missing depends on observed variable ---
data2 = data1.copy()
mask2 = np.zeros_like(data2, dtype=bool)
# Young people (age < 35) more likely to skip income
mask2[0, 1] = True   # age 25
mask2[1, 1] = True   # age 30
mask2[3, 1] = True   # age 22
mask2[6, 1] = True   # age 28

plot_missing_pattern(axes[1], "MAR\n随机缺失",
                     "Depends on observed var (Age)\n缺失与已知变量(年龄)有关", data2, mask2)

# --- MNAR: missing depends on value itself ---
data3 = np.array([
    [25, 50000, 1],
    [30, 20000, 2],
    [45, 60000, 3],
    [22, 15000, 1],
    [38, 70000, 2],
    [50, 90000, 3],
    [28, 18000, 1],
    [35, 65000, 2],
])
mask3 = np.zeros_like(data3, dtype=bool)
# Low income people don't report income
mask3[1, 1] = True   # income 20000
mask3[3, 1] = True   # income 15000
mask3[6, 1] = True   # income 18000

plot_missing_pattern(axes[2], "MNAR\n非随机缺失",
                     "Depends on missing value itself\n缺失与缺失值本身有关", data3, mask3)

# --- Legend ---
legend_items = [
    plt.Rectangle((0, 0), 1, 1, fc=colors['observed'], alpha=0.8, label='Observed (有值)'),
    plt.Rectangle((0, 0), 1, 1, fc=colors['missing'], alpha=0.3, label='Missing (缺失)'),
]
fig.legend(handles=legend_items, loc='lower center', ncol=2, fontsize=10,
           framealpha=0.8, bbox_to_anchor=(0.5, -0.02))

fig.suptitle("Three Types of Missing Data — 三种缺失值机制", fontsize=15,
             fontweight='bold', y=1.02)
plt.tight_layout()

output_path = os.path.join(os.path.dirname(__file__), "Week3_missing_value_types.png")
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
print(f"Saved: {output_path}")
plt.close()
