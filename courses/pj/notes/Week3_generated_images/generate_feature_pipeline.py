"""
Feature Engineering Pipeline — 特征工程净化链流程图
Generates a visual flow chart of the complete feature engineering pipeline.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
import os

# --- CJK Font ---
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial']
matplotlib.rcParams['axes.unicode_minus'] = False

# --- Style ---
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis('off')

# --- Color palette ---
colors = {
    'start': '#e74c3c',      # red
    'step': '#3498db',        # blue
    'danger': '#e67e22',      # orange (data leakage)
    'final': '#27ae60',       # green
    'arrow': '#2c3e50',       # dark
    'bg': '#ecf0f1',          # light gray
    'text': '#2c3e50',
}

# --- Pipeline boxes ---
boxes = [
    (1, 6.5, "Raw Data\n原始数据", colors['start'], "脏、乱、杂\nDirty & messy"),
    (4, 6.5, "Missing Values\n缺失值处理", colors['step'], "MCAR / MAR / MNAR\nDeletion / Imputation"),
    (7, 6.5, "Feature Scaling\n特征缩放", colors['step'], "Min-Max / Box-Cox\nDiscretization"),
    (10, 6.5, "Category Encoding\n类别编码", colors['step'], "One-Hot → Embedding\nWord2Vec / GloVe"),
    (4, 3.0, "Data Leakage\n数据泄漏防治", colors['danger'], "⚠️ 先拆分, 后处理!\nSplit first, then process!"),
    (7, 3.0, "Feature Selection\n特征选择", colors['step'], "SHAP / Shapley Values\nGlobal + Local"),
    (10, 3.0, "Generalization\n泛化验证", colors['final'], "Coverage + Distribution\n覆盖率 + 分布一致性"),
]

for x, y, title, color, desc in boxes:
    # Box
    rect = mpatches.FancyBboxPatch(
        (x - 1.3, y - 0.8), 2.6, 1.6,
        boxstyle="round,pad=0.15",
        facecolor=color, edgecolor='white', linewidth=2, alpha=0.9
    )
    ax.add_patch(rect)
    # Title
    ax.text(x, y + 0.2, title, ha='center', va='center',
            fontsize=10, fontweight='bold', color='white', linespacing=1.3)
    # Description
    ax.text(x, y - 0.45, desc, ha='center', va='center',
            fontsize=7.5, color='white', alpha=0.9, linespacing=1.2)

# --- Arrows (horizontal, top row) ---
arrow_props = dict(arrowstyle='->', color=colors['arrow'], lw=2.5)
for x_start, x_end in [(2.3, 2.7), (5.3, 5.7), (8.3, 8.7)]:
    ax.annotate('', xy=(x_end, 6.5), xytext=(x_start, 6.5),
                arrowprops=arrow_props)

# --- Arrow from Encoding down to Data Leakage path ---
# From Category Encoding → down
ax.annotate('', xy=(10, 5.5), xytext=(10, 5.7),
            arrowprops=dict(arrowstyle='->', color=colors['arrow'], lw=2.5))
# Horizontal line from (10, 5.2) to (4, 5.2) with bend
ax.plot([10, 10, 4, 4], [5.7, 4.5, 4.5, 3.8], color=colors['arrow'], lw=2.5)
ax.annotate('', xy=(4, 3.8), xytext=(4, 4.2),
            arrowprops=dict(arrowstyle='->', color=colors['arrow'], lw=2.5))

# --- Arrows (horizontal, bottom row) ---
for x_start, x_end in [(5.3, 5.7), (8.3, 8.7)]:
    ax.annotate('', xy=(x_end, 3.0), xytext=(x_start, 3.0),
                arrowprops=arrow_props)

# --- Title ---
ax.text(7, 7.7, "Feature Engineering Pipeline — 特征工程净化链",
        ha='center', va='center', fontsize=16, fontweight='bold',
        color=colors['text'])

# --- Legend ---
legend_items = [
    mpatches.Patch(color=colors['start'], label='Start / Input'),
    mpatches.Patch(color=colors['step'], label='Processing Step'),
    mpatches.Patch(color=colors['danger'], label='⚠️ Critical Check'),
    mpatches.Patch(color=colors['final'], label='Final Validation'),
]
ax.legend(handles=legend_items, loc='lower right', fontsize=9, framealpha=0.8)

plt.tight_layout()
output_path = os.path.join(os.path.dirname(__file__), "Week3_feature_pipeline.png")
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
print(f"Saved: {output_path}")
plt.close()
