"""
Generate MLOps Four-Layer Architecture Visualization
生成 MLOps 四层架构可视化图表

Output: Week7_four_layer_architecture.png
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
import os

# === CJK Font Setup (Windows) ===
cjk_font = None
for fname in ['Microsoft YaHei', 'SimHei', 'DengXian']:
    try:
        fp = fm.FontProperties(family=fname)
        if fm.findfont(fp) != fm.findfont(fm.FontProperties()):
            cjk_font = fname
            break
    except Exception:
        continue

if cjk_font:
    plt.rcParams['font.sans-serif'] = [cjk_font, 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

# === Configuration ===
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis('off')

# === Color scheme ===
colors = {
    'layer1': '#2196F3',
    'layer2': '#FF9800',
    'layer3': '#9C27B0',
    'layer4': '#4CAF50',
    'text_dark': '#212121',
    'text_light': '#FFFFFF',
    'arrow': '#607D8B',
}

# === Title ===
ax.text(6, 9.5, 'MLOps Four-Layer Infrastructure Architecture',
        ha='center', va='center', fontsize=16, fontweight='bold',
        color=colors['text_dark'])
ax.text(6, 9.1, 'MLOps 四层基础设施架构',
        ha='center', va='center', fontsize=12, color='#666666')

# === Draw layers (bottom to top) ===
layers = [
    {'y': 1.0, 'color': colors['layer1'],
     'label_en': 'Layer 1: Storage & Compute',
     'label_cn': '存储与计算层',
     'desc': 'HDD/SSD  |  Cloud  |  GPU/CPU  |  FLOPS'},
    {'y': 3.0, 'color': colors['layer2'],
     'label_en': 'Layer 2: Resource Management',
     'label_cn': '资源管理层',
     'desc': 'Cron -> Scheduler -> Orchestrator (K8s)'},
    {'y': 5.0, 'color': colors['layer3'],
     'label_en': 'Layer 3: ML Platform',
     'label_cn': 'ML 平台层',
     'desc': 'Model Deploy  |  Model Store  |  Feature Store'},
    {'y': 7.0, 'color': colors['layer4'],
     'label_en': 'Layer 4: Development Environment',
     'label_cn': '开发环境层',
     'desc': 'IDE  |  Git/DVC  |  CI/CD  |  Notebooks'},
]

box_width = 9
box_height = 1.5
x_start = 1.5

for layer in layers:
    rect = patches.FancyBboxPatch(
        (x_start, layer['y']), box_width, box_height,
        boxstyle='round,pad=0.1',
        facecolor=layer['color'], edgecolor='white',
        linewidth=2, alpha=0.9
    )
    ax.add_patch(rect)

    ax.text(x_start + 0.4, layer['y'] + box_height - 0.35,
            layer['label_en'],
            ha='left', va='center', fontsize=12, fontweight='bold',
            color=colors['text_light'])

    ax.text(x_start + box_width - 0.3, layer['y'] + box_height - 0.35,
            layer['label_cn'],
            ha='right', va='center', fontsize=11,
            color='#E0E0E0')

    ax.text(x_start + 0.4, layer['y'] + 0.45,
            layer['desc'],
            ha='left', va='center', fontsize=10,
            color='#E0E0E0', style='italic')

# === Arrows between layers ===
for i in range(len(layers) - 1):
    y_bottom = layers[i]['y'] + box_height
    y_top = layers[i + 1]['y']
    mid_x = x_start + box_width / 2
    ax.annotate('', xy=(mid_x, y_top - 0.05),
                xytext=(mid_x, y_bottom + 0.05),
                arrowprops=dict(arrowstyle='->', color=colors['arrow'],
                                lw=2, mutation_scale=20))

# === Right side annotations ===
annotations = [
    (1.0, '地基 Foundation'),
    (3.0, '管道 Plumbing'),
    (5.0, '装修 Furnishing'),
    (7.0, '入住 Move-in'),
]

for y, label in annotations:
    ax.text(x_start + box_width + 0.3, y + box_height / 2,
            label, ha='left', va='center', fontsize=9,
            color='#999999', style='italic')

plt.tight_layout()
output_path = os.path.join(os.path.dirname(__file__), 'Week7_four_layer_architecture.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print(f"Saved: {output_path}")
