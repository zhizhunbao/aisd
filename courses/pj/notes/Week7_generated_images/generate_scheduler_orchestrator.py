"""
Generate Scheduler vs Orchestrator comparison and Airflow drawbacks visualization
生成调度器 vs 编排器对比图 + Airflow 缺陷对比图

Output: Week7_scheduler_vs_orchestrator.png
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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# ============================================================
# Left: Scheduler vs Orchestrator
# ============================================================
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis('off')
ax1.set_title('Scheduler vs Orchestrator\n调度器 vs 编排器', fontsize=14, fontweight='bold', pad=15)

# Scheduler box
sched_rect = patches.FancyBboxPatch(
    (0.5, 5.5), 4, 3.5,
    boxstyle='round,pad=0.15',
    facecolor='#E3F2FD', edgecolor='#1976D2', linewidth=2
)
ax1.add_patch(sched_rect)
ax1.text(2.5, 8.5, 'Scheduler (调度器)', ha='center', fontsize=12, fontweight='bold', color='#1565C0')
ax1.text(2.5, 7.7, 'Focuses on:', ha='center', fontsize=10, color='#333')
ax1.text(2.5, 7.1, 'WHEN to run jobs', ha='center', fontsize=11, fontweight='bold', color='#1976D2')
ax1.text(2.5, 6.5, 'WHAT resources needed', ha='center', fontsize=11, fontweight='bold', color='#1976D2')
ax1.text(2.5, 5.9, 'DAG | Priority Queues | Quotas', ha='center', fontsize=9, color='#666', style='italic')

# Orchestrator box
orch_rect = patches.FancyBboxPatch(
    (5.5, 5.5), 4, 3.5,
    boxstyle='round,pad=0.15',
    facecolor='#FFF3E0', edgecolor='#EF6C00', linewidth=2
)
ax1.add_patch(orch_rect)
ax1.text(7.5, 8.5, 'Orchestrator (编排器)', ha='center', fontsize=12, fontweight='bold', color='#E65100')
ax1.text(7.5, 7.7, 'Focuses on:', ha='center', fontsize=10, color='#333')
ax1.text(7.5, 7.1, 'WHERE to get resources', ha='center', fontsize=11, fontweight='bold', color='#EF6C00')
ax1.text(7.5, 6.5, 'Dynamic scaling', ha='center', fontsize=11, fontweight='bold', color='#EF6C00')
ax1.text(7.5, 5.9, 'Machines | Clusters | Replicas', ha='center', fontsize=9, color='#666', style='italic')

# Tools row
tools_rect = patches.FancyBboxPatch(
    (0.5, 3.8), 9, 1.2,
    boxstyle='round,pad=0.1',
    facecolor='#F5F5F5', edgecolor='#BDBDBD', linewidth=1
)
ax1.add_patch(tools_rect)
ax1.text(2.5, 4.4, 'Slurm, Airflow', ha='center', fontsize=10, fontweight='bold', color='#1976D2')
ax1.text(7.5, 4.4, 'Kubernetes', ha='center', fontsize=10, fontweight='bold', color='#EF6C00')
ax1.text(5, 4.4, '|', ha='center', fontsize=14, color='#BDBDBD')

# Analogy row
ax1.text(2.5, 3.0, 'Restaurant Manager\n(安排顾客点菜顺序)',
         ha='center', fontsize=9, color='#666', style='italic')
ax1.text(7.5, 3.0, 'Kitchen Manager\n(调配厨师和灶台)',
         ha='center', fontsize=9, color='#666', style='italic')

# Evolution arrow
ax1.annotate('', xy=(8, 1.5), xytext=(2, 1.5),
             arrowprops=dict(arrowstyle='->', color='#4CAF50', lw=3))
ax1.text(5, 1.8, 'Cron -> Scheduler -> Orchestrator', ha='center', fontsize=10,
         fontweight='bold', color='#2E7D32')
ax1.text(5, 1.1, '演进路径：从定时任务到智能编排', ha='center', fontsize=9, color='#666')

# ============================================================
# Right: Airflow Drawbacks
# ============================================================
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis('off')
ax2.set_title('Airflow: 3 Critical Drawbacks\nAirflow 三大致命缺陷', fontsize=14, fontweight='bold', pad=15)

drawbacks = [
    {
        'y': 7.0, 'label': '[X] 1. Monolithic (单体架构)',
        'desc': 'Entire workflow in one container\n一个步骤失败 -> 全部重启',
        'color': '#EF5350', 'bg': '#FFEBEE'
    },
    {
        'y': 4.5, 'label': '[X] 2. Not Parameterized (不可参数化)',
        'desc': 'Cannot pass params to DAGs\n试不同 lr? -> 创建 N 个工作流!',
        'color': '#FF7043', 'bg': '#FBE9E7'
    },
    {
        'y': 2.0, 'label': '[X] 3. Static DAG (静态 DAG)',
        'desc': 'Cannot create steps at runtime\n无法根据中间结果调整后续步骤',
        'color': '#FFA726', 'bg': '#FFF8E1'
    },
]

for db in drawbacks:
    rect = patches.FancyBboxPatch(
        (0.5, db['y']), 9, 2.0,
        boxstyle='round,pad=0.15',
        facecolor=db['bg'], edgecolor=db['color'], linewidth=2
    )
    ax2.add_patch(rect)
    ax2.text(1.0, db['y'] + 1.5, db['label'], ha='left', fontsize=11,
             fontweight='bold', color=db['color'])
    ax2.text(1.0, db['y'] + 0.6, db['desc'], ha='left', fontsize=10, color='#555')

# Solution
ax2.text(5, 0.7, '[OK] Solutions: Argo + Prefect (Next-gen Orchestrators)',
         ha='center', fontsize=10, fontweight='bold', color='#2E7D32')
ax2.text(5, 0.2, '解决方案：下一代编排器支持参数化、动态 DAG、微服务架构',
         ha='center', fontsize=9, color='#666')

plt.tight_layout()
output_path = os.path.join(os.path.dirname(__file__), 'Week7_scheduler_vs_orchestrator.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print(f"Saved: {output_path}")
