"""
Week 6 — Model Compression Techniques Comparison & Roblox Optimization Journey
Two figures:
  1. Four model compression techniques multi-dimensional comparison
  2. Roblox BERT four-step optimization journey + CPU vs GPU
"""
import matplotlib.pyplot as plt
import numpy as np

# ── Global style ──
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.facecolor'] = '#fafafa'

# =============================================================================
# Figure 1: Four Compression Techniques Comparison
# =============================================================================
fig1, ax1 = plt.subplots(figsize=(12, 6))

techniques = ['Low-Rank\nFactorization', 'Knowledge\nDistillation', 'Pruning', 'Quantization']
# Scores (0-10) based on slides descriptions
compression_ratio = [5, 4, 9, 7.5]       # How much it compresses
accuracy_retention = [7, 9.7, 7, 8]      # How much accuracy is kept
ease_of_use = [4, 6, 5, 9]               # Ease of implementation
speed_improvement = [5, 6, 8, 8]         # Speed boost

x = np.arange(len(techniques))
width = 0.2

colors = ['#6366f1', '#10b981', '#f59e0b', '#ef4444']
bars1 = ax1.bar(x - 1.5*width, compression_ratio, width, label='Compression Ratio', color=colors[0], edgecolor='white', linewidth=0.5)
bars2 = ax1.bar(x - 0.5*width, accuracy_retention, width, label='Accuracy Retention', color=colors[1], edgecolor='white', linewidth=0.5)
bars3 = ax1.bar(x + 0.5*width, ease_of_use, width, label='Ease of Use', color=colors[2], edgecolor='white', linewidth=0.5)
bars4 = ax1.bar(x + 1.5*width, speed_improvement, width, label='Speed Improvement', color=colors[3], edgecolor='white', linewidth=0.5)

ax1.set_ylabel('Score (0-10)', fontsize=12, fontweight='bold')
ax1.set_title('Model Compression Techniques — Multi-Dimensional Comparison', fontsize=14, fontweight='bold', pad=15)
ax1.set_xticks(x)
ax1.set_xticklabels(techniques, fontsize=11, fontweight='bold')
ax1.set_ylim(0, 11)
ax1.legend(loc='upper right', fontsize=9, framealpha=0.9)

# Annotate bar values
for bars in [bars1, bars2, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax1.annotate(f'{height:.0f}' if height == int(height) else f'{height:.1f}',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=8, fontweight='bold')

# Key highlights as bottom annotation
ax1.text(0.5, -0.12,
         'Quantization: most commonly used | Pruning: up to 90% param reduction | Distillation: 97% accuracy retention (DistilBERT)',
         transform=ax1.transAxes, ha='center', fontsize=8, style='italic', color='#666')

fig1.tight_layout()
fig1.savefig('courses/pj/notes/Week6_generated_images/Week6_compression_comparison.png', dpi=150, bbox_inches='tight')
print("OK Generated: Week6_compression_comparison.png")


# =============================================================================
# Figure 2: Roblox BERT Optimization Journey + CPU vs GPU
# =============================================================================
fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={'width_ratios': [1.2, 1]})

# LEFT: Optimization steps — latency & throughput
steps = ['Step 1\nBERT\n(fixed 128)', 'Step 2\nDistilBERT\n(fixed 128)', 'Step 3\nDistilBERT\n(dynamic)', 'Step 4\nDistilBERT\n(quantized)']

# Simulated data based on slides trends
latency = [45, 28, 15, 8]       # Latency decreasing
throughput = [500, 900, 2000, 3000]  # Throughput increasing

color_latency = '#ef4444'
color_throughput = '#10b981'

ax2a_twin = ax2a.twinx()

bar_width = 0.35
x_pos = np.arange(len(steps))

bars_lat = ax2a.bar(x_pos - bar_width/2, latency, bar_width,
                    color=color_latency, alpha=0.85, edgecolor='white', label='Latency (ms)')
bars_thr = ax2a_twin.bar(x_pos + bar_width/2, throughput, bar_width,
                         color=color_throughput, alpha=0.85, edgecolor='white', label='Throughput (req/s)')

ax2a.set_ylabel('Latency (ms)  [lower is better]', fontsize=10, color=color_latency, fontweight='bold')
ax2a_twin.set_ylabel('Throughput (req/s)  [higher is better]', fontsize=10, color=color_throughput, fontweight='bold')
ax2a.set_xticks(x_pos)
ax2a.set_xticklabels(steps, fontsize=9, fontweight='bold')
ax2a.set_title('Roblox BERT — 4-Step Optimization Journey', fontsize=13, fontweight='bold', pad=15)

# Data labels
for bar in bars_lat:
    ax2a.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
              f'{bar.get_height():.0f}ms', ha='center', va='bottom', fontsize=9, fontweight='bold', color=color_latency)
for bar in bars_thr:
    ax2a_twin.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
                   f'{bar.get_height():.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold', color=color_throughput)

ax2a.set_ylim(0, 60)
ax2a_twin.set_ylim(0, 4000)

# Merged legend
lines1, labels1 = ax2a.get_legend_handles_labels()
lines2, labels2 = ax2a_twin.get_legend_handles_labels()
ax2a.legend(lines1 + lines2, labels1 + labels2, loc='upper center', fontsize=8.5)

# RIGHT: CPU vs GPU comparison
categories = ['Training\nSpeed', 'Batch\nInference', 'Single Infer.\nCost-Eff.', 'Throughput\n(same cost)']
gpu_scores = [9, 8, 3, 2]
cpu_scores = [3, 5, 8, 9]

x_pos2 = np.arange(len(categories))
ax2b.barh(x_pos2 + 0.17, gpu_scores, 0.3, color='#8b5cf6', alpha=0.85, label='GPU (V100)', edgecolor='white')
ax2b.barh(x_pos2 - 0.17, cpu_scores, 0.3, color='#3b82f6', alpha=0.85, label='CPU (Xeon 36-core)', edgecolor='white')

ax2b.set_yticks(x_pos2)
ax2b.set_yticklabels(categories, fontsize=10, fontweight='bold')
ax2b.set_xlabel('Score (0-10)', fontsize=10, fontweight='bold')
ax2b.set_title('CPU vs GPU for Inference', fontsize=13, fontweight='bold', pad=15)
ax2b.set_xlim(0, 11)
ax2b.legend(loc='lower right', fontsize=9)

ax2b.text(5.5, -0.8, 'CPU: 3,000 req/s vs GPU: 400-500 req/s (same cost)',
          fontsize=8.5, style='italic', color='#666', ha='center')

fig2.tight_layout()
fig2.savefig('courses/pj/notes/Week6_generated_images/Week6_roblox_optimization.png', dpi=150, bbox_inches='tight')
print("OK Generated: Week6_roblox_optimization.png")

plt.close('all')
print("\nOK All Week6 visualizations generated successfully!")
