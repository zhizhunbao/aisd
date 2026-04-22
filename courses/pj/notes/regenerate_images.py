"""Regenerate all storyline images with English-only text (no Chinese)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# Ensure output dirs exist
for d in ['Week3_generated_images', 'Week4_generated_images', 'Week6_generated_images',
          'Week7_generated_images', 'Week12_generated_images']:
    os.makedirs(d, exist_ok=True)

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'font.size': 12,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'savefig.dpi': 150,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.3,
})

# ============================================================
# Week 3 - Image 1: Feature Engineering Pipeline
# ============================================================
def gen_w3_pipeline():
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_xlim(0, 14); ax.set_ylim(0, 6); ax.axis('off')
    fig.suptitle('Feature Engineering Pipeline', fontsize=18, fontweight='bold', y=0.98)

    steps = [
        (1, 4.2, 2.2, 1.2, '#e74c3c', 'Raw Data', 'Dirty & messy'),
        (3.8, 4.2, 2.2, 1.2, '#3498db', 'Missing Values', 'MCAR / MAR / MNAR\nDeletion / Imputation'),
        (6.6, 4.2, 2.2, 1.2, '#3498db', 'Feature Scaling', 'Min-Max / Box-Cox\nDiscretization'),
        (9.4, 4.2, 2.2, 1.2, '#3498db', 'Category Encoding', 'One-Hot -> Embedding\nWord2Vec / GloVe'),
        (1.5, 1.2, 2.5, 1.2, '#e67e22', 'Data Leakage Check', 'Split first, then process!'),
        (5, 1.2, 2.5, 1.2, '#3498db', 'Feature Selection', 'SHAP / Shapley Values\nGlobal + Local'),
        (8.5, 1.2, 2.5, 1.2, '#2ecc71', 'Generalization', 'Coverage + Distribution'),
    ]
    for x, y, w, h, color, title, desc in steps:
        rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                                        facecolor=color, edgecolor='#333', linewidth=1.5, alpha=0.9)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h*0.7, title, ha='center', va='center', fontsize=11,
                fontweight='bold', color='white')
        ax.text(x + w/2, y + h*0.3, desc, ha='center', va='center', fontsize=8, color='white')

    # arrows top row
    for i in range(3):
        ax.annotate('', xy=(3.8 + 2.8*i, 4.8), xytext=(3.2 + 2.8*i, 4.8),
                    arrowprops=dict(arrowstyle='->', color='#333', lw=2))
    # arrow down
    ax.annotate('', xy=(10.5, 3.0), xytext=(10.5, 4.2),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2))
    ax.annotate('', xy=(2.75, 2.4), xytext=(2.75, 3.0),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2))
    # arrows bottom row
    ax.annotate('', xy=(5, 1.8), xytext=(4, 1.8),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2))
    ax.annotate('', xy=(8.5, 1.8), xytext=(7.5, 1.8),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2))

    # legend
    legend_items = [
        mpatches.Patch(color='#e74c3c', label='Start / Input'),
        mpatches.Patch(color='#3498db', label='Processing Step'),
        mpatches.Patch(color='#e67e22', label='Critical Check'),
        mpatches.Patch(color='#2ecc71', label='Final Validation'),
    ]
    ax.legend(handles=legend_items, loc='lower right', fontsize=9, framealpha=0.9)
    fig.savefig('Week3_generated_images/Week3_feature_pipeline.png')
    plt.close(fig)
    print('  OK: Week3_feature_pipeline.png')


# ============================================================
# Week 3 - Image 2: Three Types of Missing Data
# ============================================================
def gen_w3_missing():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle('Three Types of Missing Data', fontsize=18, fontweight='bold')

    types = [
        ('MCAR', 'Completely Random', 'Missingness is purely random\n(equipment failure)', '#3498db'),
        ('MAR', 'At Random', 'Depends on observed variable\n(Age -> Income missing)', '#e67e22'),
        ('MNAR', 'Not At Random', 'Depends on missing value itself\n(high income -> hide income)', '#e74c3c'),
    ]

    data = np.array([
        [25, 50000, 1],
        [30, 80000, 2],
        [45, 60000, 3],
        [22, 45000, 1],
        [38, 70000, 2],
        [50, 90000, 3],
        [28, 55000, 1],
        [35, 65000, 2],
    ])
    cols = ['Age', 'Income', 'Color']

    # MCAR: random cells missing
    mcar_mask = np.zeros_like(data, dtype=bool)
    mcar_mask[1, 2] = True; mcar_mask[3, 0] = True; mcar_mask[5, 1] = True; mcar_mask[7, 2] = True
    # MAR: Income missing when Age < 30
    mar_mask = np.zeros_like(data, dtype=bool)
    mar_mask[0, 1] = True; mar_mask[1, 2] = True; mar_mask[3, 1] = True; mar_mask[6, 1] = True
    # MNAR: Income missing when Income > 65000
    mnar_mask = np.zeros_like(data, dtype=bool)
    mnar_mask[1, 1] = True; mnar_mask[3, 2] = True; mnar_mask[5, 1] = True; mnar_mask[6, 1] = True

    masks = [mcar_mask, mar_mask, mnar_mask]

    for idx, (ax, (name, subtitle, desc, color), mask) in enumerate(zip(axes, types, masks)):
        ax.set_xlim(0, 3); ax.set_ylim(-0.5, 9.5); ax.axis('off')
        ax.set_title(f'{name}\n{subtitle}', fontsize=14, fontweight='bold', color=color)

        # column headers
        for ci, col in enumerate(cols):
            ax.text(ci + 0.5, 8.8, col, ha='center', va='center', fontsize=10, fontweight='bold')

        # data cells
        for ri in range(8):
            for ci in range(3):
                y = 7.8 - ri
                if mask[ri, ci]:
                    rect = mpatches.FancyBboxPatch((ci + 0.05, y - 0.35), 0.9, 0.7,
                            boxstyle="round,pad=0.05", facecolor='#ffcccc', edgecolor='#ddd')
                    ax.add_patch(rect)
                    ax.text(ci + 0.5, y, '?', ha='center', va='center', fontsize=11,
                            color='#cc0000', fontweight='bold')
                else:
                    rect = mpatches.FancyBboxPatch((ci + 0.05, y - 0.35), 0.9, 0.7,
                            boxstyle="round,pad=0.05", facecolor='#cce5ff', edgecolor='#ddd')
                    ax.add_patch(rect)
                    val = int(data[ri, ci])
                    ax.text(ci + 0.5, y, str(val), ha='center', va='center', fontsize=10)

        ax.text(1.5, -0.3, desc, ha='center', va='center', fontsize=8, style='italic', color='#555')

    # legend
    obs = mpatches.Patch(facecolor='#cce5ff', edgecolor='#ddd', label='Observed')
    mis = mpatches.Patch(facecolor='#ffcccc', edgecolor='#ddd', label='Missing')
    fig.legend(handles=[obs, mis], loc='lower center', ncol=2, fontsize=10, framealpha=0.9)
    fig.tight_layout(rect=[0, 0.05, 1, 0.92])
    fig.savefig('Week3_generated_images/Week3_missing_value_types.png')
    plt.close(fig)
    print('  OK: Week3_missing_value_types.png')


# ============================================================
# Week 3 - Image 3: SHAP Feature Importance
# ============================================================
def gen_w3_shap():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), gridspec_kw={'width_ratios': [1, 1.2]})
    fig.suptitle('SHAP — Feature Importance Analysis', fontsize=18, fontweight='bold')

    # Global bar chart
    features = ['Credit History', 'Debt-Income Ratio', 'Employment Length',
                'Loan Amount', 'Annual Income', 'Home Ownership', 'Loan Purpose', 'Interest Rate']
    values = [0.42, 0.35, 0.28, 0.22, 0.18, 0.12, 0.08, 0.05]
    colors = ['#e74c3c', '#e74c3c', '#3498db', '#3498db', '#3498db', '#95a5a6', '#95a5a6', '#95a5a6']

    y_pos = np.arange(len(features))
    ax1.barh(y_pos, values, color=colors, edgecolor='white', height=0.6)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(features, fontsize=10)
    ax1.invert_yaxis()
    ax1.set_xlabel('Mean |SHAP Value|', fontsize=11)
    ax1.set_title('Global Feature Importance', fontsize=14, fontweight='bold')
    for i, v in enumerate(values):
        ax1.text(v + 0.005, i, f'{v:.2f}', va='center', fontsize=9, color='#555')
    legend_items = [
        mpatches.Patch(color='#e74c3c', label='High Impact'),
        mpatches.Patch(color='#3498db', label='Medium Impact'),
        mpatches.Patch(color='#95a5a6', label='Low Impact'),
    ]
    ax1.legend(handles=legend_items, loc='lower right', fontsize=9)

    # Waterfall chart
    base = 0.35
    shap_vals = [('Credit History', 0.15), ('Debt-Income', 0.10),
                 ('Annual Income', -0.08), ('Employment', -0.05), ('Loan Amount', 0.03)]
    final = base + sum(v for _, v in shap_vals)

    feats = [f for f, _ in shap_vals]
    vals = [v for _, v in shap_vals]
    y_pos2 = np.arange(len(feats))
    bar_colors = ['#e74c3c' if v > 0 else '#2ecc71' for v in vals]

    starts = []
    cum = base
    for v in vals:
        if v > 0:
            starts.append(cum)
        else:
            starts.append(cum + v)
        cum += v

    ax2.barh(y_pos2, [abs(v) for v in vals], left=starts, color=bar_colors, edgecolor='white', height=0.5)
    ax2.set_yticks(y_pos2)
    ax2.set_yticklabels(feats, fontsize=10)
    ax2.invert_yaxis()
    ax2.axvline(x=final, color='#333', linestyle='-', linewidth=1.5)
    ax2.set_xlabel('Model Output (Probability of Default)', fontsize=10)
    ax2.set_title('Single Prediction Explanation\n(Waterfall)', fontsize=14, fontweight='bold')
    ax2.text(base, -0.8, f'Base: {base}', ha='center', fontsize=9, color='#888')
    ax2.text(final, len(feats), f'Final: {final:.2f}\n(High Risk)', ha='center', fontsize=9,
             color='#e74c3c', fontweight='bold')
    for i, v in enumerate(vals):
        x = starts[i] + abs(v)/2
        ax2.text(x + abs(v)/2 + 0.01, i, f'{v:+.2f}', va='center', fontsize=9,
                 color='#e74c3c' if v > 0 else '#2ecc71', fontweight='bold')

    inc = mpatches.Patch(color='#e74c3c', label='Increases Risk')
    dec = mpatches.Patch(color='#2ecc71', label='Decreases Risk')
    ax2.legend(handles=[inc, dec], loc='upper right', fontsize=9)

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig('Week3_generated_images/Week3_shap_example.png')
    plt.close(fig)
    print('  OK: Week3_shap_example.png')


# ============================================================
# Week 4 - Image 1: Three Parallelism Strategies
# ============================================================
def gen_w4_parallelism():
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Three Parallelism Strategies Comparison', fontsize=18, fontweight='bold')

    strategies = [
        ('Data Parallelism', '#3498db',
         ['Full model copy on each GPU', 'Data split into shards', 'All-Reduce gradient sync',
          'Problem: Straggler Effect', 'Use: Model fits in 1 GPU']),
        ('Model Parallelism', '#e67e22',
         ['Model layers split across GPUs', 'Sequential processing', 'GPU idle = "Bubble" waste',
          'Problem: Pipeline Bubbles', 'Use: Model too large for 1 GPU']),
        ('Pipeline Parallelism', '#2ecc71',
         ['Model split + Micro-batches', 'Interleaved execution', 'Reduces bubble time',
          'Solution: Micro-batch overlap', 'Use: Large model + efficiency']),
    ]

    for ax, (title, color, points) in zip(axes, strategies):
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis('off')
        # title box
        rect = mpatches.FancyBboxPatch((0.5, 8), 9, 1.5, boxstyle="round,pad=0.2",
                facecolor=color, edgecolor='#333', alpha=0.9)
        ax.add_patch(rect)
        ax.text(5, 8.75, title, ha='center', va='center', fontsize=14,
                fontweight='bold', color='white')

        # GPU boxes
        for gi in range(3):
            y = 5.8 - gi * 2.2
            rect = mpatches.FancyBboxPatch((1, y), 8, 1.5, boxstyle="round,pad=0.1",
                    facecolor='#f8f9fa', edgecolor=color, linewidth=2)
            ax.add_patch(rect)
            ax.text(2, y + 0.75, f'GPU {gi}:', ha='left', va='center', fontsize=10,
                    fontweight='bold', color=color)
            ax.text(5, y + 0.75, points[gi], ha='left', va='center', fontsize=9, color='#333')

        # bottom note
        ax.text(5, 0.3, points[3], ha='center', va='center', fontsize=10,
                fontweight='bold', color='#c0392b')
        ax.text(5, -0.2, points[4], ha='center', va='center', fontsize=9, color='#555')

    fig.tight_layout(rect=[0, 0.02, 1, 0.93])
    fig.savefig('Week4_generated_images/Week4_parallelism_strategies.png')
    plt.close(fig)
    print('  OK: Week4_parallelism_strategies.png')


# ============================================================
# Week 4 - Image 2: DDP vs FSDP
# ============================================================
def gen_w4_ddp_fsdp():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle('DDP vs FSDP — PyTorch Distributed Training', fontsize=18, fontweight='bold')

    # DDP
    ax1.set_xlim(0, 10); ax1.set_ylim(0, 10); ax1.axis('off')
    ax1.set_title('DDP (DistributedDataParallel)', fontsize=14, fontweight='bold', color='#3498db')
    for gi in range(3):
        x = 0.5 + gi * 3.2
        rect = mpatches.FancyBboxPatch((x, 3), 2.6, 5, boxstyle="round,pad=0.15",
                facecolor='#d6eaf8', edgecolor='#3498db', linewidth=2)
        ax1.add_patch(rect)
        ax1.text(x + 1.3, 7.5, f'GPU {gi}', ha='center', va='center', fontsize=11,
                fontweight='bold', color='#3498db')
        # Full model
        inner = mpatches.FancyBboxPatch((x + 0.2, 3.5), 2.2, 3.2, boxstyle="round,pad=0.1",
                facecolor='#aed6f1', edgecolor='#2980b9')
        ax1.add_patch(inner)
        ax1.text(x + 1.3, 5.5, 'FULL Model\nCopy', ha='center', va='center', fontsize=9,
                fontweight='bold', color='#2c3e50')
        ax1.text(x + 1.3, 4.2, f'Data Shard {gi+1}', ha='center', va='center', fontsize=8, color='#555')
    ax1.text(5, 1.5, 'All-Reduce Gradient Sync', ha='center', va='center', fontsize=12,
            fontweight='bold', color='#2980b9')
    ax1.text(5, 0.7, 'Best for: model fits in 1 GPU (e.g. 7B)', ha='center', fontsize=10, color='#555')
    ax1.annotate('', xy=(7, 2.2), xytext=(3, 2.2),
                arrowprops=dict(arrowstyle='<->', color='#2980b9', lw=2))

    # FSDP
    ax2.set_xlim(0, 10); ax2.set_ylim(0, 10); ax2.axis('off')
    ax2.set_title('FSDP (FullyShardedDataParallel)', fontsize=14, fontweight='bold', color='#e67e22')
    shard_colors = ['#fadbd8', '#d5f5e3', '#d6eaf8']
    shard_labels = ['Params\nShard 1', 'Params\nShard 2', 'Params\nShard 3']
    for gi in range(3):
        x = 0.5 + gi * 3.2
        rect = mpatches.FancyBboxPatch((x, 3), 2.6, 5, boxstyle="round,pad=0.15",
                facecolor='#fdebd0', edgecolor='#e67e22', linewidth=2)
        ax2.add_patch(rect)
        ax2.text(x + 1.3, 7.5, f'GPU {gi}', ha='center', va='center', fontsize=11,
                fontweight='bold', color='#e67e22')
        # Shard only
        inner = mpatches.FancyBboxPatch((x + 0.2, 4.0), 2.2, 2.5, boxstyle="round,pad=0.1",
                facecolor=shard_colors[gi], edgecolor='#d35400')
        ax2.add_patch(inner)
        ax2.text(x + 1.3, 5.25, shard_labels[gi], ha='center', va='center', fontsize=9,
                fontweight='bold', color='#2c3e50')
    ax2.text(5, 1.5, 'Gather -> Compute -> Release', ha='center', va='center', fontsize=12,
            fontweight='bold', color='#d35400')
    ax2.text(5, 0.7, 'Best for: model > 1 GPU memory (e.g. 70B+)', ha='center', fontsize=10, color='#555')

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig('Week4_generated_images/Week4_ddp_vs_fsdp.png')
    plt.close(fig)
    print('  OK: Week4_ddp_vs_fsdp.png')


# ============================================================
# Week 4 - Image 3: NAS Methods Comparison
# ============================================================
def gen_w4_nas():
    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(polar=True))
    fig.suptitle('NAS Methods Comparison', fontsize=18, fontweight='bold', y=1.02)

    categories = ['Search Speed', 'Search Quality', 'Memory Efficiency',
                  'Implementation\nSimplicity', 'Flexibility']
    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    methods = {
        'RL-based (NASNet)': ([3, 9, 4, 3, 8], '#e74c3c'),
        'Evolutionary (AmoebaNet)': ([3, 8, 5, 4, 9], '#3498db'),
        'DARTS (Differentiable)': ([9, 7, 7, 6, 6], '#2ecc71'),
    }

    for name, (vals, color) in methods.items():
        vals_plot = vals + vals[:1]
        ax.plot(angles, vals_plot, 'o-', linewidth=2, label=name, color=color)
        ax.fill(angles, vals_plot, alpha=0.1, color=color)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=8)
    ax.legend(loc='lower right', bbox_to_anchor=(1.3, -0.05), fontsize=10)
    ax.set_title('Radar Chart', fontsize=12, pad=20, color='#555')

    fig.tight_layout()
    fig.savefig('Week4_generated_images/Week4_nas_comparison.png')
    plt.close(fig)
    print('  OK: Week4_nas_comparison.png')


# ============================================================
# Week 6 - Image 1: Model Compression Techniques
# ============================================================
def gen_w6_compression():
    fig, ax = plt.subplots(figsize=(14, 7))
    fig.suptitle('Model Compression Techniques — Comparison', fontsize=18, fontweight='bold')

    techniques = ['Quantization', 'Knowledge\nDistillation', 'Pruning', 'Low-Rank\nFactorization']
    metrics = {
        'Speed Improvement': [4, 1.6, 2, 3],
        'Size Reduction': [4, 1.7, 3.5, 2.5],
        'Quality Retention': [3.5, 4.0, 3.0, 3.5],
    }
    colors = ['#3498db', '#2ecc71', '#e67e22']

    x = np.arange(len(techniques))
    width = 0.25

    for i, (metric, vals) in enumerate(metrics.items()):
        bars = ax.bar(x + i * width, vals, width, label=metric, color=colors[i],
                     edgecolor='white', linewidth=1.5)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                   f'{v:.1f}x' if 'Speed' in metric or 'Size' in metric else f'{v:.1f}',
                   ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.set_xticks(x + width)
    ax.set_xticklabels(techniques, fontsize=11)
    ax.set_ylabel('Score (relative)', fontsize=11)
    ax.set_ylim(0, 5)
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3)

    # annotations
    notes = [
        'Most commonly used\nin industry',
        'DistilBERT: 60% size\n97% capability, 160% speed',
        'Remove 90% weights\nthen fine-tune',
        'SqueezeNet: 50x smaller',
    ]
    for i, note in enumerate(notes):
        ax.text(i + width, -0.8, note, ha='center', fontsize=8, color='#555', style='italic')

    ax.set_xlim(-0.3, len(techniques) - 0.3 + 3 * width)
    fig.tight_layout(rect=[0, 0.08, 1, 0.93])
    fig.savefig('Week6_generated_images/Week6_compression_comparison.png')
    plt.close(fig)
    print('  OK: Week6_compression_comparison.png')


# ============================================================
# Week 6 - Image 2: Roblox BERT 4-Step Optimization
# ============================================================
def gen_w6_roblox():
    fig, ax = plt.subplots(figsize=(16, 6))
    fig.suptitle('Roblox BERT 4-Step Optimization Journey', fontsize=18, fontweight='bold')
    ax.set_xlim(0, 16); ax.set_ylim(0, 6); ax.axis('off')

    steps = [
        (0.5, 2.5, 3, 2.5, '#e74c3c', 'Step 1: BERT',
         'Fixed 128 tokens\nSlow baseline\n~100 pred/sec'),
        (4.2, 2.5, 3, 2.5, '#e67e22', 'Step 2: DistilBERT',
         'Knowledge Distillation\n60% size, 97% NLU\n~300 pred/sec'),
        (7.9, 2.5, 3, 2.5, '#3498db', 'Step 3: Dynamic Input',
         'Remove padding\nVariable length\n~800 pred/sec'),
        (11.6, 2.5, 3, 2.5, '#2ecc71', 'Step 4: INT8 Quant',
         'FP32 -> INT8\n4x smaller\n~3000 pred/sec'),
    ]
    for x, y, w, h, color, title, desc in steps:
        rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                facecolor=color, edgecolor='#333', linewidth=2, alpha=0.9)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h*0.8, title, ha='center', va='center', fontsize=12,
                fontweight='bold', color='white')
        ax.text(x + w/2, y + h*0.35, desc, ha='center', va='center', fontsize=9, color='white')

    # arrows
    for i in range(3):
        ax.annotate('', xy=(4.2 + 3.7*i, 3.75), xytext=(3.5 + 3.7*i, 3.75),
                    arrowprops=dict(arrowstyle='->', color='#333', lw=2.5))

    # bottom note
    ax.text(8, 0.8, 'Result: 1 Billion predictions/day on CPU', ha='center', fontsize=14,
            fontweight='bold', color='#2c3e50')
    ax.text(8, 0.2, 'Counter-intuitive: Setting PyTorch threads=1 is FASTER (avoids thread contention)',
            ha='center', fontsize=10, color='#e74c3c', style='italic')

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig('Week6_generated_images/Week6_roblox_optimization.png')
    plt.close(fig)
    print('  OK: Week6_roblox_optimization.png')


# ============================================================
# Week 7 - Image 1: Four-Layer Architecture
# ============================================================
def gen_w7_architecture():
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.suptitle('MLOps Four-Layer Architecture', fontsize=18, fontweight='bold')
    ax.set_xlim(0, 14); ax.set_ylim(0, 10); ax.axis('off')

    layers = [
        (0.5, 7.5, 13, 2, '#9b59b6', 'Layer 4: Development Environment',
         'Jupyter / Git / CI-CD / VS Code\n"Your Workbench"'),
        (0.5, 5.2, 13, 2, '#3498db', 'Layer 3: ML Platform',
         'Model Store / Feature Store / Deployment / SageMaker / MLflow\n"Furnished Office"'),
        (0.5, 2.9, 13, 2, '#e67e22', 'Layer 2: Resource Management',
         'Airflow (Scheduler) / Kubernetes (Orchestrator) / Slurm\n"Plumbing & Electrical"'),
        (0.5, 0.6, 13, 2, '#27ae60', 'Layer 1: Storage & Compute',
         'HDD / SSD / Cloud Storage / GPU / CPU\n"Foundation"'),
    ]

    for x, y, w, h, color, title, desc in layers:
        rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                facecolor=color, edgecolor='#333', linewidth=2, alpha=0.88)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h*0.65, title, ha='center', va='center', fontsize=14,
                fontweight='bold', color='white')
        ax.text(x + w/2, y + h*0.3, desc, ha='center', va='center', fontsize=10, color='white')

    # arrows between layers
    for y in [7.5, 5.2, 2.9]:
        ax.annotate('', xy=(7, y), xytext=(7, y + 0.0001),
                    arrowprops=dict(arrowstyle='-', color='#333', lw=1, linestyle='--'))

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig('Week7_generated_images/Week7_four_layer_architecture.png')
    plt.close(fig)
    print('  OK: Week7_four_layer_architecture.png')


# ============================================================
# Week 7 - Image 2: Scheduler vs Orchestrator
# ============================================================
def gen_w7_scheduler():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle('Scheduler vs Orchestrator & Airflow Drawbacks', fontsize=18, fontweight='bold')

    # Scheduler vs Orchestrator
    ax1.set_xlim(0, 10); ax1.set_ylim(0, 10); ax1.axis('off')
    ax1.set_title('Scheduler vs Orchestrator', fontsize=14, fontweight='bold')

    # Scheduler box
    rect1 = mpatches.FancyBboxPatch((0.5, 5.5), 4, 4, boxstyle="round,pad=0.2",
            facecolor='#3498db', edgecolor='#333', alpha=0.9)
    ax1.add_patch(rect1)
    ax1.text(2.5, 9, 'SCHEDULER', ha='center', va='center', fontsize=13, fontweight='bold', color='white')
    ax1.text(2.5, 8, 'Manages WHEN + WHAT', ha='center', va='center', fontsize=10, color='white')
    ax1.text(2.5, 7.2, 'Understands DAG\ndependencies', ha='center', va='center', fontsize=9, color='#d6eaf8')
    ax1.text(2.5, 6.2, 'Tools: Airflow, Slurm', ha='center', va='center', fontsize=9, color='#d6eaf8')

    # Orchestrator box
    rect2 = mpatches.FancyBboxPatch((5.5, 5.5), 4, 4, boxstyle="round,pad=0.2",
            facecolor='#e67e22', edgecolor='#333', alpha=0.9)
    ax1.add_patch(rect2)
    ax1.text(7.5, 9, 'ORCHESTRATOR', ha='center', va='center', fontsize=13, fontweight='bold', color='white')
    ax1.text(7.5, 8, 'Manages WHERE', ha='center', va='center', fontsize=10, color='white')
    ax1.text(7.5, 7.2, 'Dynamic scaling\nof resources', ha='center', va='center', fontsize=9, color='#fdebd0')
    ax1.text(7.5, 6.2, 'Tool: Kubernetes', ha='center', va='center', fontsize=9, color='#fdebd0')

    # Analogy
    ax1.text(2.5, 4.5, 'Restaurant Manager\n(orders & timing)', ha='center', fontsize=10,
            color='#3498db', fontweight='bold')
    ax1.text(7.5, 4.5, 'Kitchen Manager\n(assign chefs & stoves)', ha='center', fontsize=10,
            color='#e67e22', fontweight='bold')
    ax1.text(5, 3.5, 'They work at DIFFERENT\nabstraction layers', ha='center', fontsize=11,
            fontweight='bold', color='#c0392b')

    # Airflow Drawbacks
    ax2.set_xlim(0, 10); ax2.set_ylim(0, 10); ax2.axis('off')
    ax2.set_title("Airflow's 3 Fatal Flaws", fontsize=14, fontweight='bold', color='#c0392b')

    flaws = [
        ('Monolithic', 'One step fails = entire DAG restarts',
         'Argo/Prefect: Microservices\n(each step independent)'),
        ('Non-Parameterizable', 'Cannot pass params to DAGs\n(need N workflows for N configs)',
         'Argo/Prefect: Parameterized\n(same workflow, different params)'),
        ('Static DAGs', 'Cannot create steps at runtime',
         'Argo/Prefect: Dynamic DAGs\n(adjust based on results)'),
    ]
    for i, (title, problem, solution) in enumerate(flaws):
        y = 8 - i * 2.8
        # Problem
        rect = mpatches.FancyBboxPatch((0.3, y - 0.5), 4.2, 2.2, boxstyle="round,pad=0.1",
                facecolor='#fadbd8', edgecolor='#e74c3c', linewidth=1.5)
        ax2.add_patch(rect)
        ax2.text(2.4, y + 1.2, f'Flaw: {title}', ha='center', fontsize=11, fontweight='bold', color='#c0392b')
        ax2.text(2.4, y + 0.2, problem, ha='center', fontsize=8, color='#555')
        # Solution
        rect2 = mpatches.FancyBboxPatch((5.3, y - 0.5), 4.2, 2.2, boxstyle="round,pad=0.1",
                facecolor='#d5f5e3', edgecolor='#27ae60', linewidth=1.5)
        ax2.add_patch(rect2)
        ax2.text(7.4, y + 1.2, 'Solution', ha='center', fontsize=11, fontweight='bold', color='#27ae60')
        ax2.text(7.4, y + 0.2, solution, ha='center', fontsize=8, color='#555')
        # Arrow
        ax2.annotate('', xy=(5.3, y + 0.5), xytext=(4.5, y + 0.5),
                    arrowprops=dict(arrowstyle='->', color='#333', lw=2))

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig('Week7_generated_images/Week7_scheduler_vs_orchestrator.png')
    plt.close(fig)
    print('  OK: Week7_scheduler_vs_orchestrator.png')


# ============================================================
# Week 12 - Image 1: Fine-Tuning Decision Framework
# ============================================================
def gen_w12_decision():
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.suptitle('Fine-Tuning Decision Framework', fontsize=18, fontweight='bold')
    ax.set_xlim(0, 14); ax.set_ylim(0, 10); ax.axis('off')

    # Start
    rect = mpatches.FancyBboxPatch((5, 8.5), 4, 1, boxstyle="round,pad=0.15",
            facecolor='#3498db', edgecolor='#333', linewidth=2)
    ax.add_patch(rect)
    ax.text(7, 9, 'LLM not performing well?', ha='center', va='center', fontsize=12,
            fontweight='bold', color='white')

    # Step 1
    rect1 = mpatches.FancyBboxPatch((1, 6.5), 4, 1.2, boxstyle="round,pad=0.15",
            facecolor='#2ecc71', edgecolor='#333', linewidth=2)
    ax.add_patch(rect1)
    ax.text(3, 7.3, 'Step 1: Prompt Eng.', ha='center', va='center', fontsize=11,
            fontweight='bold', color='white')
    ax.text(3, 6.8, 'Zero cost, try first', ha='center', fontsize=9, color='white')

    # Step 2
    rect2 = mpatches.FancyBboxPatch((5.5, 6.5), 4, 1.2, boxstyle="round,pad=0.15",
            facecolor='#e67e22', edgecolor='#333', linewidth=2)
    ax.add_patch(rect2)
    ax.text(7.5, 7.3, 'Step 2: RAG', ha='center', va='center', fontsize=11,
            fontweight='bold', color='white')
    ax.text(7.5, 6.8, 'Runtime retrieval, no model change', ha='center', fontsize=9, color='white')

    # Step 3
    rect3 = mpatches.FancyBboxPatch((9.5, 6.5), 4, 1.2, boxstyle="round,pad=0.15",
            facecolor='#e74c3c', edgecolor='#333', linewidth=2)
    ax.add_patch(rect3)
    ax.text(11.5, 7.3, 'Step 3: Fine-Tuning', ha='center', va='center', fontsize=11,
            fontweight='bold', color='white')
    ax.text(11.5, 6.8, 'Last resort, highest cost', ha='center', fontsize=9, color='white')

    # Arrows
    ax.annotate('', xy=(3, 7.7), xytext=(5, 8.5),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2))
    ax.annotate('', xy=(5.5, 7.1), xytext=(5, 7.1),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2))
    ax.text(5.25, 7.4, 'Not\nenough', ha='center', fontsize=8, color='#e74c3c')
    ax.annotate('', xy=(9.5, 7.1), xytext=(9.5, 7.1),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2))
    ax.annotate('', xy=(9.5, 7.1), xytext=(9.0, 7.1),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2))

    # Fine-tuning options
    rect_full = mpatches.FancyBboxPatch((8, 3.5), 3, 2, boxstyle="round,pad=0.15",
            facecolor='#fadbd8', edgecolor='#e74c3c', linewidth=1.5)
    ax.add_patch(rect_full)
    ax.text(9.5, 5.1, 'Full Fine-Tuning', ha='center', fontsize=11, fontweight='bold', color='#c0392b')
    ax.text(9.5, 4.3, 'All params trainable\nRisk: catastrophic forgetting\nNeed: multiple H100s', ha='center', fontsize=8, color='#555')

    rect_lora = mpatches.FancyBboxPatch((11.5, 3.5), 3, 2, boxstyle="round,pad=0.15",
            facecolor='#d5f5e3', edgecolor='#27ae60', linewidth=1.5)
    ax.add_patch(rect_lora)
    ax.text(13, 5.1, 'LoRA (PEFT)', ha='center', fontsize=11, fontweight='bold', color='#27ae60')
    ax.text(13, 4.3, 'Only ~1% params trained\nNo forgetting\nNeed: single RTX 4090', ha='center', fontsize=8, color='#555')

    ax.annotate('', xy=(9.5, 5.5), xytext=(11.5, 6.5),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))
    ax.annotate('', xy=(13, 5.5), xytext=(11.5, 6.5),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))

    # Don't fine-tune box
    rect_no = mpatches.FancyBboxPatch((1, 3.5), 5, 2, boxstyle="round,pad=0.15",
            facecolor='#fef9e7', edgecolor='#f39c12', linewidth=1.5)
    ax.add_patch(rect_no)
    ax.text(3.5, 5.1, 'When NOT to Fine-Tune', ha='center', fontsize=11, fontweight='bold', color='#e67e22')
    ax.text(3.5, 4.0, 'Simple task (use Prompt)\nData changes fast (use RAG)\nLow quality data (GIGO)\nPrivacy concerns (RAG + local)', ha='center', fontsize=8, color='#555')

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig('Week12_generated_images/Week12_FT_decision_framework.png')
    plt.close(fig)
    print('  OK: Week12_FT_decision_framework.png')


# ============================================================
# Week 12 - Image 2: LoRA Parameter Efficiency
# ============================================================
def gen_w12_lora():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle('LoRA Parameter Efficiency & Weight Decomposition', fontsize=18, fontweight='bold')

    # Left: bar chart comparison
    ax1.set_title('Parameter Comparison', fontsize=14, fontweight='bold')
    models = ['Full FT\n(d=4096)', 'LoRA r=4', 'LoRA r=8', 'LoRA r=16', 'LoRA r=64']
    params = [16777216, 32768, 65536, 131072, 524288]
    pcts = [100, 0.20, 0.39, 0.78, 3.13]
    colors = ['#e74c3c', '#2ecc71', '#2ecc71', '#2ecc71', '#2ecc71']

    bars = ax1.barh(range(len(models)), [p/1e6 for p in params], color=colors, edgecolor='white', height=0.5)
    ax1.set_yticks(range(len(models)))
    ax1.set_yticklabels(models, fontsize=10)
    ax1.set_xlabel('Parameters (Millions)', fontsize=11)
    ax1.set_xscale('log')
    for i, (bar, pct) in enumerate(zip(bars, pcts)):
        ax1.text(bar.get_width() * 1.1, i, f'{pct:.2f}%', va='center', fontsize=10, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)

    # Right: matrix decomposition diagram
    ax2.set_xlim(0, 10); ax2.set_ylim(0, 10); ax2.axis('off')
    ax2.set_title('LoRA Weight Decomposition', fontsize=14, fontweight='bold')

    # W_orig (frozen)
    rect_w = mpatches.FancyBboxPatch((0.5, 3), 3, 4, boxstyle="round,pad=0.1",
            facecolor='#d5dbdb', edgecolor='#95a5a6', linewidth=2)
    ax2.add_patch(rect_w)
    ax2.text(2, 5.5, 'W_orig', ha='center', fontsize=14, fontweight='bold', color='#555')
    ax2.text(2, 4.5, '(d x d)', ha='center', fontsize=11, color='#777')
    ax2.text(2, 3.5, 'FROZEN', ha='center', fontsize=10, fontweight='bold', color='#e74c3c')

    ax2.text(4, 5, '+', ha='center', fontsize=24, fontweight='bold', color='#333')

    # A matrix
    rect_a = mpatches.FancyBboxPatch((4.8, 3.5), 1.2, 3, boxstyle="round,pad=0.1",
            facecolor='#aed6f1', edgecolor='#2980b9', linewidth=2)
    ax2.add_patch(rect_a)
    ax2.text(5.4, 5.3, 'A', ha='center', fontsize=14, fontweight='bold', color='#2980b9')
    ax2.text(5.4, 4.5, '(d x r)', ha='center', fontsize=9, color='#555')

    ax2.text(6.3, 5, 'x', ha='center', fontsize=18, fontweight='bold', color='#333')

    # B matrix
    rect_b = mpatches.FancyBboxPatch((6.8, 4), 2.5, 1.2, boxstyle="round,pad=0.1",
            facecolor='#abebc6', edgecolor='#27ae60', linewidth=2)
    ax2.add_patch(rect_b)
    ax2.text(8.05, 4.8, 'B', ha='center', fontsize=14, fontweight='bold', color='#27ae60')
    ax2.text(8.05, 4.3, '(r x d)', ha='center', fontsize=9, color='#555')

    ax2.text(5, 2.5, 'TRAINABLE', ha='center', fontsize=10, fontweight='bold', color='#2ecc71')
    ax2.annotate('', xy=(5.4, 2.8), xytext=(5.4, 3.5),
                arrowprops=dict(arrowstyle='->', color='#2ecc71', lw=2))
    ax2.annotate('', xy=(8.05, 2.8), xytext=(8.05, 4.0),
                arrowprops=dict(arrowstyle='->', color='#2ecc71', lw=2))
    ax2.text(7, 2.5, 'TRAINABLE', ha='center', fontsize=10, fontweight='bold', color='#2ecc71')

    # Formula
    ax2.text(5, 8.5, 'W_new = W_orig (Frozen) + A x B (Trainable)', ha='center', fontsize=13,
            fontweight='bold', color='#2c3e50',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#f8f9fa', edgecolor='#333'))

    # Ratio formula
    ax2.text(5, 1.2, 'Ratio = 2dr / d^2 = 2r / d', ha='center', fontsize=11,
            color='#555', fontweight='bold')
    ax2.text(5, 0.5, 'Example: d=4096, r=16 -> Ratio = 32/4096 = 0.78%', ha='center',
            fontsize=10, color='#e67e22', fontweight='bold')

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig('Week12_generated_images/Week12_LoRA_parameter_comparison.png')
    plt.close(fig)
    print('  OK: Week12_LoRA_parameter_comparison.png')


# ============================================================
# Run all generators
# ============================================================
if __name__ == '__main__':
    print('Generating Week 3 images...')
    gen_w3_pipeline()
    gen_w3_missing()
    gen_w3_shap()

    print('Generating Week 4 images...')
    gen_w4_parallelism()
    gen_w4_ddp_fsdp()
    gen_w4_nas()

    print('Generating Week 6 images...')
    gen_w6_compression()
    gen_w6_roblox()

    print('Generating Week 7 images...')
    gen_w7_architecture()
    gen_w7_scheduler()

    print('Generating Week 12 images...')
    gen_w12_decision()
    gen_w12_lora()

    print('\nAll 12 images regenerated with English-only text!')
