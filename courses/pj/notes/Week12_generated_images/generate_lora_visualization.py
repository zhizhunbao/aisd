"""
Week 12: LLM Fine-Tuning — LoRA Visualization
Generates two plots:
1. LoRA parameter efficiency comparison (bar chart)
2. Fine-tuning decision flowchart (conceptual diagram)
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib as mpl
import numpy as np
import os

# CJK font configuration for Windows
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
mpl.rcParams['axes.unicode_minus'] = False

# Output directory = same as this script
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Plot 1: LoRA Parameter Efficiency ──────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

# --- Left: parameter count comparison ---
ax1 = axes[0]
d_values = [2048, 4096, 8192]
r = 16
full_params = [d * d for d in d_values]
lora_params = [2 * d * r for d in d_values]
ratios = [l / f * 100 for l, f in zip(lora_params, full_params)]

x = np.arange(len(d_values))
width = 0.35

bars1 = ax1.bar(x - width/2, [p / 1e6 for p in full_params], width,
                label='Full Fine-Tuning', color='#e74c3c', alpha=0.85)
bars2 = ax1.bar(x + width/2, [p / 1e6 for p in lora_params], width,
                label='LoRA (r=16)', color='#2ecc71', alpha=0.85)

# Add ratio annotations
for i, (ratio, bar) in enumerate(zip(ratios, bars2)):
    ax1.annotate(f'{ratio:.1f}%',
                 xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                 xytext=(0, 8), textcoords='offset points',
                 ha='center', fontsize=10, fontweight='bold', color='#27ae60')

ax1.set_xlabel('Model Dimension (d)', fontsize=11)
ax1.set_ylabel('Parameters (Millions)', fontsize=11)
ax1.set_title('Full Fine-Tuning vs LoRA\nParameter Count Comparison', fontsize=13, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels([f'd={d}' for d in d_values])
ax1.legend(fontsize=10)
ax1.set_yscale('log')
ax1.grid(axis='y', alpha=0.3)

# --- Right: W_new = W_orig + A×B visual ---
ax2 = axes[1]
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 8)
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_title('LoRA Weight Decomposition\nW_new = W_orig + (A × B)', fontsize=13, fontweight='bold')

# W_orig (large square)
w_orig = mpatches.FancyBboxPatch((0.3, 2.5), 2.5, 2.5,
                                  boxstyle="round,pad=0.1",
                                  facecolor='#3498db', alpha=0.7, edgecolor='#2c3e50', linewidth=2)
ax2.add_patch(w_orig)
ax2.text(1.55, 3.75, r'$W_{orig}$' + '\n(d × d)\nFROZEN', ha='center', va='center',
         fontsize=11, fontweight='bold', color='white')

# Plus sign
ax2.text(3.3, 3.75, '+', ha='center', va='center', fontsize=24, fontweight='bold')

# A matrix (tall thin)
a_mat = mpatches.FancyBboxPatch((3.8, 2.5), 0.7, 2.5,
                                 boxstyle="round,pad=0.05",
                                 facecolor='#e74c3c', alpha=0.8, edgecolor='#2c3e50', linewidth=2)
ax2.add_patch(a_mat)
ax2.text(4.15, 3.75, 'A\n(d×r)', ha='center', va='center',
         fontsize=9, fontweight='bold', color='white')

# × sign
ax2.text(4.85, 3.75, '×', ha='center', va='center', fontsize=18, fontweight='bold')

# B matrix (short wide)
b_mat = mpatches.FancyBboxPatch((5.2, 3.0), 2.5, 0.7,
                                 boxstyle="round,pad=0.05",
                                 facecolor='#e67e22', alpha=0.8, edgecolor='#2c3e50', linewidth=2)
ax2.add_patch(b_mat)
ax2.text(6.45, 3.35, 'B  (r × d)', ha='center', va='center',
         fontsize=9, fontweight='bold', color='white')

# = sign
ax2.text(5.8, 1.6, '=', ha='center', va='center', fontsize=24, fontweight='bold')

# W_new (large square)
w_new = mpatches.FancyBboxPatch((6.5, 2.5), 2.5, 2.5,
                                 boxstyle="round,pad=0.1",
                                 facecolor='#9b59b6', alpha=0.7, edgecolor='#2c3e50', linewidth=2)
ax2.add_patch(w_new)
ax2.text(7.75, 3.75, r'$W_{new}$' + '\n(d × d)\nFINAL', ha='center', va='center',
         fontsize=11, fontweight='bold', color='white')

# Labels below
ax2.text(1.55, 1.8, 'Billions\n(Frozen)', ha='center', fontsize=9, color='#3498db', fontweight='bold')
ax2.text(4.5, 1.8, 'Millions\n(Trainable)', ha='center', fontsize=9, color='#e74c3c', fontweight='bold')
ax2.text(7.75, 1.8, 'Merged for\nInference', ha='center', fontsize=9, color='#9b59b6', fontweight='bold')

# r << d annotation
ax2.text(4.5, 6.0, 'r ≪ d  (e.g., r=16, d=4096)', ha='center', fontsize=11,
         style='italic', color='#7f8c8d',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#ecf0f1', edgecolor='#bdc3c7'))

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "Week12_LoRA_parameter_comparison.png"), dpi=150, bbox_inches="tight")
plt.close()
print("[OK] Generated: Week12_LoRA_parameter_comparison.png")


# ── Plot 2: Fine-Tuning Decision Framework ─────────────────────────
fig, ax = plt.subplots(figsize=(12, 7))
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('LLM Fine-Tuning Decision Framework\nLLM 微调决策框架', fontsize=15, fontweight='bold', pad=15)

def draw_box(ax, x, y, w, h, text, color, fontsize=9, textcolor='white'):
    box = mpatches.FancyBboxPatch((x, y), w, h,
                                   boxstyle="round,pad=0.15",
                                   facecolor=color, alpha=0.85,
                                   edgecolor='#2c3e50', linewidth=1.5)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center',
            fontsize=fontsize, fontweight='bold', color=textcolor, linespacing=1.4)

def draw_arrow(ax, x1, y1, x2, y2, label='', color='#2c3e50'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=2))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx + 0.15, my, label, fontsize=8, fontweight='bold', color=color)

# Step 1: Problem
draw_box(ax, 4, 8.5, 4, 1, 'LLM 表现不够好？\nLLM not good enough?', '#34495e', fontsize=10)

# Step 2: Try Prompt Engineering
draw_arrow(ax, 6, 8.5, 6, 7.8)
draw_box(ax, 3.5, 6.8, 5, 1, 'Try Prompt Engineering\n(Few-shot, CoT, OPRO)', '#3498db')
draw_arrow(ax, 3.5, 7.3, 2.5, 7.3, '')
ax.text(2.3, 7.3, '✅ Solved!', fontsize=9, fontweight='bold', color='#27ae60', ha='right')

# Step 3: Try RAG
draw_arrow(ax, 6, 6.8, 6, 6.1)
draw_box(ax, 3.5, 5.1, 5, 1, 'Try Advanced RAG\n(Semantic Chunk, Re-rank)', '#2980b9')
draw_arrow(ax, 3.5, 5.6, 2.5, 5.6, '')
ax.text(2.3, 5.6, '✅ Solved!', fontsize=9, fontweight='bold', color='#27ae60', ha='right')

# Step 4: Check data quality
draw_arrow(ax, 6, 5.1, 6, 4.4)
draw_box(ax, 3.5, 3.3, 5, 1.1, 'Data Check\n✓ High quality?  ✓ Stable?\n✓ No privacy issues?', '#f39c12', textcolor='#2c3e50')
draw_arrow(ax, 8.5, 3.85, 9.5, 3.85, '')
ax.text(10.8, 3.85, '❌ Fix data first\nor use RAG', fontsize=9, fontweight='bold', color='#e74c3c', ha='center')

# Step 5: Choose method
draw_arrow(ax, 6, 3.3, 6, 2.6)
draw_box(ax, 4, 1.5, 4, 1.1, '✅ Fine-Tune!\nLoRA (推荐) > Full FT', '#27ae60', fontsize=10)

# Step 6: Choose framework
draw_arrow(ax, 6, 1.5, 6, 0.8)
draw_box(ax, 1, 0, 10, 0.8,
         'Unsloth (速度)  |  Axolotl (大规模)  |  LLaMA-Factory (易用)  |  HF PEFT (灵活)',
         '#8e44ad', fontsize=9)

# "No" labels on the main path
ax.text(6.3, 8.2, 'Still not\nenough', fontsize=7, color='#7f8c8d', style='italic')
ax.text(6.3, 6.5, 'Still not\nenough', fontsize=7, color='#7f8c8d', style='italic')
ax.text(5.6, 4.5, 'All good ✓', fontsize=7, color='#7f8c8d', style='italic')

plt.savefig(os.path.join(OUT_DIR, "Week12_FT_decision_framework.png"), dpi=150, bbox_inches="tight")
plt.close()
print("[OK] Generated: Week12_FT_decision_framework.png")

print("\n[DONE] All Phase 5b visualizations generated.")
