"""
SHAP Feature Importance Example — SHAP 特征重要性示例
Generates a simulated SHAP bar plot + waterfall for a credit risk prediction scenario.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
import os

# --- CJK Font ---
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial']
matplotlib.rcParams['axes.unicode_minus'] = False

plt.style.use('seaborn-v0_8-whitegrid')

fig, axes = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={'width_ratios': [1, 1.2]})

# ========== Left: Global Feature Importance ==========
features = [
    'Credit History\n信用历史',
    'Debt-Income Ratio\n债务收入比',
    'Employment Length\n工作年限',
    'Loan Amount\n贷款金额',
    'Annual Income\n年收入',
    'Home Ownership\n房屋所有权',
    'Loan Purpose\n贷款用途',
    'Interest Rate\n利率',
]
# Simulated mean |SHAP| values (sorted descending)
shap_values = [0.42, 0.35, 0.28, 0.22, 0.18, 0.12, 0.08, 0.05]

bar_colors = ['#e74c3c' if v > 0.3 else '#3498db' if v > 0.15 else '#95a5a6'
              for v in shap_values]

ax1 = axes[0]
y_pos = range(len(features))
bars = ax1.barh(y_pos, shap_values, color=bar_colors, edgecolor='white', linewidth=1.5, height=0.6)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(features, fontsize=9)
ax1.set_xlabel('Mean |SHAP Value|', fontsize=11)
ax1.set_title('Global Feature Importance\n全局特征重要性', fontsize=13, fontweight='bold')
ax1.invert_yaxis()

# Add value labels
for bar, val in zip(bars, shap_values):
    ax1.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height() / 2,
             f'{val:.2f}', ha='left', va='center', fontsize=9, fontweight='bold')

# Legend
legend_items = [
    mpatches.Patch(color='#e74c3c', label='High Impact (高影响)'),
    mpatches.Patch(color='#3498db', label='Medium Impact (中影响)'),
    mpatches.Patch(color='#95a5a6', label='Low Impact (低影响)'),
]
ax1.legend(handles=legend_items, loc='lower right', fontsize=8, framealpha=0.8)

# ========== Right: Single Prediction Waterfall ==========
ax2 = axes[1]

# Simulated waterfall for a single prediction
base_value = 0.35  # average model output (probability of default)
contributions = [
    ('Credit History\n信用历史', +0.15, '#e74c3c'),
    ('Debt-Income Ratio\n债务收入比', +0.10, '#e74c3c'),
    ('Annual Income\n年收入', -0.08, '#27ae60'),
    ('Employment Length\n工作年限', -0.05, '#27ae60'),
    ('Loan Amount\n贷款金额', +0.03, '#e74c3c'),
]

# Calculate cumulative positions
cumulative = base_value
positions = []
for name, delta, color in contributions:
    start = cumulative
    cumulative += delta
    positions.append((name, start, cumulative, delta, color))

final_value = cumulative

# Plot base value line
ax2.axvline(x=base_value, color='#7f8c8d', linestyle='--', linewidth=1, alpha=0.7)
ax2.text(base_value, len(contributions) + 0.3, f'Base: {base_value:.2f}',
         ha='center', fontsize=9, color='#7f8c8d')

# Plot bars
for i, (name, start, end, delta, color) in enumerate(positions):
    y = len(contributions) - 1 - i
    width = end - start
    left = min(start, end)
    ax2.barh(y, abs(width), left=left, color=color, edgecolor='white',
             linewidth=1.5, height=0.5, alpha=0.85)
    # Label
    sign = '+' if delta > 0 else ''
    ax2.text(end + 0.005, y, f'{sign}{delta:.2f}',
             ha='left' if delta > 0 else 'right', va='center',
             fontsize=9, fontweight='bold', color=color)

ax2.set_yticks(range(len(contributions)))
ax2.set_yticklabels([c[0] for c in reversed(contributions)], fontsize=9)
ax2.set_xlabel('Model Output (Probability of Default)', fontsize=10)
ax2.set_title('Single Prediction Explanation\n单次预测解释 (Waterfall)', fontsize=13, fontweight='bold')

# Final value annotation
ax2.axvline(x=final_value, color='#2c3e50', linestyle='-', linewidth=2, alpha=0.8)
ax2.text(final_value, -0.8, f'Final: {final_value:.2f}\n(High Risk 高风险)',
         ha='center', fontsize=10, fontweight='bold', color='#e74c3c')

# Legend
legend_items2 = [
    mpatches.Patch(color='#e74c3c', label='↑ Increases Risk (推高风险)'),
    mpatches.Patch(color='#27ae60', label='↓ Decreases Risk (降低风险)'),
]
ax2.legend(handles=legend_items2, loc='upper right', fontsize=8, framealpha=0.8)

fig.suptitle("SHAP — Feature Importance Analysis\nSHAP 特征重要性分析",
             fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()

output_path = os.path.join(os.path.dirname(__file__), "Week3_shap_example.png")
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
print(f"Saved: {output_path}")
plt.close()
