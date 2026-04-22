"""
Generate ROC curve plot from Week 9 storyline's 10-instance hand-calculation example.
"""
import matplotlib.pyplot as plt
import matplotlib
import os

matplotlib.use('Agg')

# ── ROC points from storyline §2.2 ──
fpr_points = [0,   0,   0,   0.2, 0.6, 0.8, 0.8, 1.0, 1.0]
tpr_points = [0,   0.2, 0.4, 0.4, 0.6, 0.6, 0.8, 0.8, 1.0]

# ── Annotations ──
annotations = [
    (0,   0.2, "#1(+) TP=1"),
    (0,   0.4, "#2(+) TP=2"),
    (0.2, 0.4, "#3(-) FP=1"),
    (0.6, 0.6, "#4-6 TP=3,FP=3"),
    (0.8, 0.6, "#7(-) FP=4"),
    (0.8, 0.8, "#8(+) TP=4"),
    (1.0, 0.8, "#9(-) FP=5"),
]

offsets = [
    (-70, 8),    # #1
    (-70, 8),    # #2
    (12, 12),    # #3
    (-10, 15),   # #4-6
    (12, -15),   # #7
    (-72, 12),   # #8
    (-10, 12),   # #9
]

# ── Plot ──
fig, ax = plt.subplots(figsize=(8, 7))

# Diagonal (random guess)
ax.plot([0, 1], [0, 1], 'k--', alpha=0.3, linewidth=1, label='Random Guess (AUC=0.5)')

# ROC curve
ax.plot(fpr_points, tpr_points, 'b-o', linewidth=2.5, markersize=8,
        markerfacecolor='#2196F3', markeredgecolor='white', markeredgewidth=1.5,
        label='ROC Curve', zorder=5)

# AUC shading
ax.fill_between(fpr_points, tpr_points, alpha=0.12, color='#2196F3')

# Ideal point
ax.plot(0, 1, 'r*', markersize=18, zorder=6, label='Ideal Point (0, 1)')

# Start & end labels
ax.annotate('Start\n(0,0)', (0, 0), textcoords="offset points", xytext=(15, -10),
            fontsize=8, color='#666')
ax.annotate('End\n(1,1)', (1, 1), textcoords="offset points", xytext=(-35, -25),
            fontsize=8, color='#666')

# Key point annotations
for i, (fx, ty, label) in enumerate(annotations):
    ax.annotate(label, (fx, ty),
                textcoords="offset points", xytext=offsets[i],
                fontsize=7.5, color='#333',
                arrowprops=dict(arrowstyle='->', color='#999', lw=0.8),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF9C4',
                          edgecolor='#FFD54F', alpha=0.9))

# ── Axes ──
ax.set_xlabel('FPR (False Positive Rate)', fontsize=13, fontweight='bold')
ax.set_ylabel('TPR (True Positive Rate = Recall)', fontsize=13, fontweight='bold')
ax.set_title('ROC Curve — 10-Instance Hand Calculation', fontsize=15, fontweight='bold', pad=15)

ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.05, 1.12)
ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_aspect('equal')
ax.grid(True, alpha=0.3, linestyle='-')
ax.legend(loc='lower right', fontsize=10, framealpha=0.9)

# AUC value
auc = sum((fpr_points[i] - fpr_points[i-1]) * (tpr_points[i] + tpr_points[i-1]) / 2
          for i in range(1, len(fpr_points)))
ax.text(0.55, 0.25, f'AUC = {auc:.2f}', fontsize=16, fontweight='bold',
        color='#1565C0', alpha=0.8,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#90CAF9'))

plt.tight_layout()

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Week9_ROC_curve.png')
fig.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
print(f"Saved: {output_path}")
plt.close()
