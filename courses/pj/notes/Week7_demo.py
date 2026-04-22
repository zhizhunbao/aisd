# %%
# ============================================================
# Week 7: MLOps Infrastructure and Tooling — Python Demo
# 第七周：MLOps 基础设施与工具 — Python 概念演示
# ============================================================
# 每个 cell 独立运行，演示一个 MLOps 核心概念
# Each cell runs independently, demonstrating one MLOps concept
# ============================================================

import math
import tabulate as _tabulate_mod
_tabulate_mod.WIDE_CHARS_MODE = True  # 修复中文对齐 / Fix CJK alignment
from tabulate import tabulate as _tabulate_fn

def ptable(rows, **kwargs):
    """格式化表格输出 / Formatted table output"""
    print(_tabulate_fn(rows, **kwargs, tablefmt="simple_grid"))


# %%
# ============================================================
# 概念01：四层基础设施架构
# Concept 01: Four-Layer Infrastructure Architecture
# ============================================================
# ML 系统的四层基础设施：存储计算 → 资源管理 → ML 平台 → 开发环境
# Four layers: Storage/Compute → Resource Mgmt → ML Platform → Dev Env
# ============================================================

# ── 本单元自包含数据与函数 ──

# 四层架构数据 / Four-layer architecture data
layers = [
    ["Layer 1", "Storage & Compute", "存储与计算", "HDD, SSD, Cloud, GPU, CPU"],
    ["Layer 2", "Resource Management", "资源管理", "Airflow, Slurm, Kubernetes"],
    ["Layer 3", "ML Platform", "ML 平台", "SageMaker, MLFlow, Feast"],
    ["Layer 4", "Development Env", "开发环境", "Jupyter, VS Code, Git, CI/CD"],
]

# 每层解决的核心问题 / Core problem each layer solves
problems = [
    ["Layer 1", "Where to store data? Where to get compute?", "数据存哪？算力从哪来？"],
    ["Layer 2", "How to schedule and orchestrate tasks?", "多个任务怎么排队？"],
    ["Layer 3", "How to manage models/features/deployment?", "模型/特征/部署怎么管？"],
    ["Layer 4", "Where to write code and run experiments?", "在哪写代码做实验？"],
]

# ── 演示 ──
print("=" * 60)
print("概念01: 四层基础设施架构 / Four-Layer Infrastructure")
print("=" * 60)

ptable(layers, headers=["Layer", "English Name", "中文名", "Key Tools"])
print()
ptable(problems, headers=["Layer", "Core Problem", "核心问题"])


# %%
# ============================================================
# 概念02：存储介质对比——HDD vs SSD
# Concept 02: Storage Media Comparison — HDD vs SSD
# ============================================================
# 两种基本存储介质的速度、成本和适用场景对比
# Comparison of two basic storage types: speed, cost, use cases
# ============================================================

# ── 本单元自包含数据与函数 ──

# HDD vs SSD 对比数据 / HDD vs SSD comparison data
storage_comparison = [
    ["HDD (Hard Drive Disk)", "Slow (~100 MB/s)", "Low ($0.02/GB)", "Cold data archival"],
    ["SSD (Solid State Drive)", "Fast (~500 MB/s)", "High ($0.10/GB)", "Hot data access"],
    ["Cloud (S3/Blob/GCS)", "Variable", "Pay-per-use", "Default choice today"],
]

# 成本计算示例 / Cost calculation example
# 假设存储 50TB 训练数据 / Assume 50TB training data
data_size_tb = 50
data_size_gb = data_size_tb * 1024

# HDD 成本 / HDD cost per GB
hdd_cost_per_gb = 0.02
# SSD 成本 / SSD cost per GB
ssd_cost_per_gb = 0.10

# 总成本计算 / Total cost calculation
hdd_total = data_size_gb * hdd_cost_per_gb
ssd_total = data_size_gb * ssd_cost_per_gb

# ── 演示 ──
print("=" * 60)
print("概念02: 存储介质对比 / Storage Media Comparison")
print("=" * 60)

ptable(storage_comparison, headers=["Storage Type", "Speed", "Cost", "Best For"])
print()

cost_rows = [
    ["HDD", f"{data_size_tb} TB", f"${hdd_cost_per_gb}/GB", f"${hdd_total:,.0f}"],
    ["SSD", f"{data_size_tb} TB", f"${ssd_cost_per_gb}/GB", f"${ssd_total:,.0f}"],
    ["Difference", "", "", f"${ssd_total - hdd_total:,.0f} (SSD costs {ssd_total/hdd_total:.1f}x more)"],
]
ptable(cost_rows, headers=["Type", "Data Size", "Unit Cost", "Total Cost"])


# %%
# ============================================================
# 概念03：计算利用率
# Concept 03: Compute Utilization
# ============================================================
# Compute Utilization = 实际 FLOPS / 最大 FLOPS 能力
# The ratio of actual FLOPS used to max FLOPS capability
# ============================================================

# ── 本单元自包含数据与函数 ──

# 计算利用率公式 / Compute utilization formula
def compute_utilization(actual_flops, max_flops):
    """计算利用率 = 实际 FLOPS / 最大 FLOPS / Compute Utilization = actual / max"""
    return actual_flops / max_flops

# GPU 规格示例数据 / GPU specification example data
# NVIDIA A100: 最大 312 TFLOPS (FP16) / Max 312 TFLOPS (FP16)
gpu_max_tflops = 312.0
# 实际训练中通常只达到约 50% / Typically ~50% during training
gpu_actual_tflops = 156.0

# 多个场景的利用率 / Utilization across scenarios
scenarios = [
    ["Ideal (theoretical)", 312.0, 312.0],
    ["Optimized training", 218.0, 312.0],
    ["Typical training", 156.0, 312.0],
    ["Unoptimized code", 93.6, 312.0],
    ["Idle waiting (I/O)", 31.2, 312.0],
]

# ── 演示 ──
print("=" * 60)
print("概念03: 计算利用率 / Compute Utilization")
print("=" * 60)
print()
print("Formula: Compute Utilization = Actual FLOPS / Max FLOPS")
print("公式: 计算利用率 = 作业实际 FLOPS / 计算单元最大 FLOPS 能力")
print()

rows = []
for name, actual, maximum in scenarios:
    util = compute_utilization(actual, maximum)
    rows.append([name, f"{actual} TFLOPS", f"{maximum} TFLOPS", f"{util:.0%}"])

ptable(rows, headers=["Scenario", "Actual FLOPS", "Max FLOPS", "Utilization"])
print()
print("Key insight: Practically, utilization is ~50% — half of compute is 'wasted'")
print("关键洞察: 实际中利用率约 50%，一半算力在'空转'")


# %%
# ============================================================
# 概念04：云支出与云回迁
# Concept 04: Cloud Spending & Cloud Repatriation
# ============================================================
# 云支出约占收入成本 50%，部分公司进行"云回迁"
# Cloud spending ~50% of revenue cost; some do "cloud repatriation"
# ============================================================

# ── 本单元自包含数据与函数 ──

# 模拟公司云支出占比数据 / Simulated cloud spending ratios
# 基于 a16z 分析 / Based on a16z analysis
companies = [
    ["Company A (SaaS startup)", 5_000_000, 0.52],
    ["Company B (Mid-size ML)", 20_000_000, 0.48],
    ["Company C (Large enterprise)", 100_000_000, 0.45],
    ["Company D (Cloud-native)", 50_000_000, 0.55],
]

# 云回迁节省计算函数 / Cloud repatriation savings calculation
def repatriation_savings(cloud_cost, on_prem_ratio=0.60):
    """
    计算云回迁潜在节省 / Calculate potential savings from cloud repatriation
    on_prem_ratio: 自建数据中心相对于云的成本比例 / On-prem cost as ratio of cloud
    """
    on_prem_cost = cloud_cost * on_prem_ratio
    savings = cloud_cost - on_prem_cost
    return on_prem_cost, savings

# ── 演示 ──
print("=" * 60)
print("概念04: 云支出与云回迁 / Cloud Spending & Repatriation")
print("=" * 60)
print()
print("a16z finding: Cloud = ~50% of revenue cost for public software companies")
print("a16z 发现: 云支出约占上市软件公司收入成本的 50%")
print()

rows = []
for name, revenue, cloud_pct in companies:
    cloud_cost = revenue * cloud_pct
    _, savings = repatriation_savings(cloud_cost)
    rows.append([
        name,
        f"${revenue:>12,}",
        f"{cloud_pct:.0%}",
        f"${cloud_cost:>12,.0f}",
        f"${savings:>12,.0f}"
    ])

ptable(rows, headers=["Company", "Revenue", "Cloud %", "Cloud Cost", "Repatriation Savings (40%)"])


# %%
# ============================================================
# 概念05：计算单元切分——线程、容器、Pod
# Concept 05: Compute Unit Slicing — Threads, Containers, Pods
# ============================================================
# 物理机器可切分为不同粒度的并发单元
# Physical machines sliced into concurrent units at different granularity
# ============================================================

# ── 本单元自包含数据与函数 ──

# 计算单元层次数据 / Compute unit hierarchy data
compute_units = [
    ["Thread", "Finest granularity", "Shared memory space", "CPU-bound tasks"],
    ["Container", "Isolated environment", "Own filesystem + network", "App packaging"],
    ["Pod", "K8s scheduling unit", "Multiple containers", "Service deployment"],
]

# 资源分配示例 / Resource allocation example
# 假设一台 8-GPU 服务器 / Assume one 8-GPU server
total_gpus = 8
total_memory_gb = 512
total_cpus = 64

# 不同切分方式 / Different slicing approaches
slicing = [
    ["Single job (no slicing)", 1, total_gpus, total_memory_gb, total_cpus],
    ["2 large containers", 2, total_gpus // 2, total_memory_gb // 2, total_cpus // 2],
    ["4 medium containers", 4, total_gpus // 4, total_memory_gb // 4, total_cpus // 4],
    ["8 small containers", 8, total_gpus // 8, total_memory_gb // 8, total_cpus // 8],
]

# ── 演示 ──
print("=" * 60)
print("概念05: 计算单元切分 / Compute Unit Slicing")
print("=" * 60)

ptable(compute_units, headers=["Unit Type", "Granularity", "Isolation", "Use Case"])
print()
print(f"Example: Server with {total_gpus} GPUs, {total_memory_gb}GB RAM, {total_cpus} CPUs")
print()

rows = []
for name, n, gpus, mem, cpus in slicing:
    rows.append([name, n, f"{gpus} GPUs", f"{mem} GB", f"{cpus} cores"])

ptable(rows, headers=["Slicing Strategy", "# Units", "GPUs/Unit", "Memory/Unit", "CPUs/Unit"])


# %%
# ============================================================
# 概念06：开发环境三大组件
# Concept 06: Development Environment — Three Components
# ============================================================
# IDE + 版本控制 + CI/CD 构成完整开发环境
# IDE + Version Control + CI/CD make a complete dev env
# ============================================================

# ── 本单元自包含数据与函数 ──

# 开发环境三组件数据 / Three dev env components data
dev_components = [
    ["IDE", "Write code, debug", "Jupyter Notebook, VS Code, PyCharm", "编写代码、调试"],
    ["Version Control", "Track changes", "Git, DVC, W&B", "版本控制"],
    ["CI/CD", "Automate test & deploy", "Jenkins, GitHub Actions", "自动测试部署"],
]

# Notebook 特性对比 / Notebook characteristics
notebook_features = [
    ["Stateful", "Yes", "Retains state after run", "运行后保留状态"],
    ["Resume from failure", "Yes", "Restart from failed point", "可从失败处恢复"],
    ["Rich content", "Yes", "Images, LaTeX, tables", "图片、LaTeX、表格"],
    ["Execution order", "Caution!", "Must track cell order", "需要跟踪执行顺序"],
]

# ── 演示 ──
print("=" * 60)
print("概念06: 开发环境三大组件 / Dev Environment Components")
print("=" * 60)

ptable(dev_components, headers=["Component", "Function", "Tools", "功能"])
print()
print("Notebook key feature: STATEFUL (有状态)")
print()
ptable(notebook_features, headers=["Feature", "Status", "Description", "描述"])


# %%
# ============================================================
# 概念07：Notebook 工具生态
# Concept 07: Notebook Ecosystem Tools
# ============================================================
# Papermill、Commuter、nbdev 扩展了 Notebook 的能力
# Papermill, Commuter, nbdev extend Notebook capabilities
# ============================================================

# ── 本单元自包含数据与函数 ──

# Notebook 生态工具数据 / Notebook ecosystem tools data
notebook_tools = [
    ["Papermill", "Parameterized execution", "Run same notebook with N hyperparams", "参数化执行"],
    ["Commuter", "Sharing hub", "Find, view, share notebooks in org", "组织内共享平台"],
    ["nbdev", "Docs + Tests", "Code, docs, tests in same notebook", "文档+测试一体化"],
]

# Netflix 生产环境使用案例 / Netflix production use case
production_usage = [
    ["Netflix", "Production env", "Uses notebooks in production pipelines", "在生产环境中使用 Notebook"],
]

# ── 演示 ──
print("=" * 60)
print("概念07: Notebook 工具生态 / Notebook Ecosystem")
print("=" * 60)

ptable(notebook_tools, headers=["Tool", "Category", "Description", "描述"])
print()
print("Notable: Netflix uses Notebooks in PRODUCTION (not just experiments)")
print("注意: Netflix 在生产环境中使用 Notebook（不仅仅是实验）")


# %%
# ============================================================
# 概念08：Docker 容器
# Concept 08: Docker Containers
# ============================================================
# 轻量级、独立、可执行的软件包，解决环境一致性问题
# Lightweight, standalone, executable package solving env consistency
# ============================================================

# ── 本单元自包含数据与函数 ──

# Docker 五大优势数据 / Five Docker advantages data
docker_advantages = [
    ["Portability", "可移植性", "Build once, run anywhere", "一次构建，到处运行"],
    ["Consistency", "一致性", "Same behavior in dev/test/prod", "开发/测试/生产行为一致"],
    ["Isolation", "隔离性", "No conflicts between apps", "容器间互不干扰"],
    ["Scalability", "可扩展性", "Easy scale up/down", "轻松伸缩"],
    ["Version Control", "版本控制", "Share via Docker Hub", "通过 Docker Hub 共享"],
]

# Docker 容器的组成部分 / Docker container components
container_parts = [
    ["Code", "Application source code", "应用源代码"],
    ["Runtime", "Language runtime (Python, etc.)", "语言运行时"],
    ["System Tools", "OS utilities", "系统工具"],
    ["Libraries", "Dependencies and packages", "依赖库和包"],
    ["Settings", "Configuration files", "配置文件"],
]

# ── 演示 ──
print("=" * 60)
print("概念08: Docker 容器 / Docker Containers")
print("=" * 60)
print()
print("Docker Container = Image (recipe) -> Container (dish)")
print("Docker 容器 = 镜像 (配方) -> 容器 (做出来的菜)")
print()

print("Five Advantages / 五大优势:")
ptable(docker_advantages, headers=["Advantage", "中文", "Description", "描述"])
print()

print("Container includes / 容器包含:")
ptable(container_parts, headers=["Component", "Description", "描述"])


# %%
# ============================================================
# 概念09：Kubernetes Pod
# Concept 09: Kubernetes Pod
# ============================================================
# Pod 是 K8s 最小部署单元，一组共享网络/存储的容器
# Pod is smallest K8s unit: group of containers sharing network/storage
# ============================================================

# ── 本单元自包含数据与函数 ──

# Pod 关键特性数据 / Pod key characteristics data
pod_features = [
    ["Basic Concept", "Group of 1+ containers", "一个或多个容器的组合"],
    ["Shared Context", "Same IP + port space", "共享 IP 地址和端口空间"],
    ["Communication", "Via localhost", "通过 localhost 通信"],
    ["Atomic Unit", "Scaling unit in K8s", "K8s 扩缩容的原子单元"],
    ["Use Case", "Tightly coupled services", "紧密协作的服务单元"],
]

# Pod vs Container 对比 / Pod vs Container comparison
pod_vs_container = [
    ["Granularity", "Single process/app", "Group of related processes"],
    ["Networking", "Own IP (bridged)", "Shared IP within pod"],
    ["Scaling unit", "No (in K8s)", "Yes — K8s scales pods"],
    ["Communication", "Between containers: network", "Within pod: localhost"],
]

# ── 演示 ──
print("=" * 60)
print("概念09: Kubernetes Pod")
print("=" * 60)

ptable(pod_features, headers=["Feature", "Description", "描述"])
print()

print("Pod vs Container / Pod 与容器的区别:")
ptable(pod_vs_container, headers=["Dimension", "Container", "Pod"])


# %%
# ============================================================
# 概念10：调度器 vs 编排器
# Concept 10: Scheduler vs Orchestrator
# ============================================================
# Scheduler 管 When/What，Orchestrator 管 Where
# Scheduler handles When/What; Orchestrator handles Where
# ============================================================

# ── 本单元自包含数据与函数 ──

# 调度器 vs 编排器对比数据 / Scheduler vs Orchestrator comparison
sched_vs_orch = [
    ["Focuses on", "WHEN + WHAT", "WHERE"],
    ["Core question", "When to run? What resources?", "Where to get resources?"],
    ["Abstraction", "DAG, priority queues, quotas", "Machines, clusters, replicas"],
    ["Representative", "Slurm, Airflow", "Kubernetes"],
    ["Dynamic?", "Follows static DAG", "Dynamically scale instances"],
    ["Analogy", "Restaurant manager", "Kitchen manager"],
]

# Cron -> Scheduler 演进 / Evolution from Cron to Scheduler
evolution = [
    ["Cron", "Fixed-time scheduling", "Cannot handle dependencies", "不能处理依赖"],
    ["Scheduler", "DAG-aware scheduling", "Knows task ordering", "理解 DAG 依赖"],
    ["Orchestrator", "Resource allocation", "Dynamic scaling", "动态资源分配"],
]

# ── 演示 ──
print("=" * 60)
print("概念10: 调度器 vs 编排器 / Scheduler vs Orchestrator")
print("=" * 60)

ptable(sched_vs_orch, headers=["Dimension", "Scheduler (调度器)", "Orchestrator (编排器)"])
print()

print("Evolution / 演进路径: Cron -> Scheduler -> Orchestrator")
ptable(evolution, headers=["Tool", "Capability", "Key Feature", "特点"])


# %%
# ============================================================
# 概念11：DAG（有向无环图）与工作流
# Concept 11: DAG (Directed Acyclic Graph) & Workflow
# ============================================================
# DAG 描述任务间的依赖关系，是工作流调度的核心数据结构
# DAG describes task dependencies — core data structure for scheduling
# ============================================================

# ── 本单元自包含数据与函数 ──

# ML Pipeline DAG 示例 / Example ML Pipeline DAG
# 任务定义 / Task definitions
tasks = {
    "A": {"name": "Data Ingestion", "duration_min": 30, "depends_on": []},
    "B": {"name": "Data Cleaning", "duration_min": 60, "depends_on": ["A"]},
    "C": {"name": "Feature Engineering", "duration_min": 45, "depends_on": ["B"]},
    "D": {"name": "Model Training", "duration_min": 120, "depends_on": ["C"]},
    "E": {"name": "Evaluation", "duration_min": 20, "depends_on": ["D"]},
    "F": {"name": "Deployment", "duration_min": 15, "depends_on": ["E"]},
}

# 拓扑排序函数 / Topological sort function
def topological_sort(tasks):
    """
    对 DAG 进行拓扑排序，返回执行顺序
    Topological sort of DAG, returns execution order
    """
    visited = set()
    order = []

    def dfs(task_id):
        if task_id in visited:
            return
        visited.add(task_id)
        for dep in tasks[task_id]["depends_on"]:
            dfs(dep)
        order.append(task_id)

    for tid in tasks:
        dfs(tid)
    return order

# 计算总执行时间（串行）/ Calculate total time (serial)
def total_serial_time(tasks, order):
    """计算串行执行总时间 / Total serial execution time"""
    return sum(tasks[tid]["duration_min"] for tid in order)

# ── 演示 ──
print("=" * 60)
print("概念11: DAG 与工作流 / DAG & Workflow")
print("=" * 60)
print()

# 展示 DAG 结构 / Show DAG structure
print("ML Pipeline DAG:")
print("A(Ingest) -> B(Clean) -> C(Features) -> D(Train) -> E(Eval) -> F(Deploy)")
print()

order = topological_sort(tasks)
rows = []
# 累计开始时间 / Cumulative start time
start_time = 0
for tid in order:
    t = tasks[tid]
    deps = ", ".join(t["depends_on"]) if t["depends_on"] else "None"
    rows.append([tid, t["name"], f'{t["duration_min"]} min', deps, f'{start_time} min'])
    start_time += t["duration_min"]

ptable(rows, headers=["ID", "Task", "Duration", "Depends On", "Start Time"])
print()
total = total_serial_time(tasks, order)
print(f"Total serial execution time: {total} min ({total/60:.1f} hours)")
print(f"串行总执行时间: {total} 分钟 ({total/60:.1f} 小时)")


# %%
# ============================================================
# 概念12：Airflow 的三大缺陷
# Concept 12: Airflow's Three Critical Drawbacks
# ============================================================
# 单体架构、不可参数化、静态 DAG 是 Airflow 的致命缺陷
# Monolithic, Not Parameterized, Static DAG are critical flaws
# ============================================================

# ── 本单元自包含数据与函数 ──

# Airflow 缺陷数据 / Airflow drawbacks data
airflow_drawbacks = [
    [
        "1. Monolithic",
        "单体架构",
        "Entire workflow in one container",
        "One step fails -> restart ALL",
    ],
    [
        "2. Not Parameterized",
        "不可参数化",
        "Cannot pass params to DAGs",
        "Different lr? Create N workflows!",
    ],
    [
        "3. Static DAG",
        "静态 DAG",
        "No runtime step creation",
        "Cannot auto-adjust based on results",
    ],
]

# Airflow vs 下一代对比 / Airflow vs next-gen comparison
airflow_vs_nextgen = [
    ["Architecture", "Monolithic", "Microservice-based"],
    ["Parameterization", "Not supported", "Fully supported"],
    ["Dynamic DAG", "Static only", "Dynamic step creation"],
    ["Failure recovery", "Restart entire workflow", "Retry individual steps"],
]

# ── 演示 ──
print("=" * 60)
print("概念12: Airflow 的三大缺陷 / Airflow's Three Drawbacks")
print("=" * 60)

ptable(airflow_drawbacks, headers=["Drawback", "中文", "Description", "Consequence"])
print()

print("Airflow vs Next-Gen (Argo / Prefect):")
ptable(airflow_vs_nextgen, headers=["Dimension", "Airflow", "Argo / Prefect"])


# %%
# ============================================================
# 概念13：ML 平台三大组件
# Concept 13: ML Platform — Three Core Components
# ============================================================
# Model Deployment + Model Store + Feature Store 构成 ML 平台
# ML Platform = Model Deployment + Model Store + Feature Store
# ============================================================

# ── 本单元自包含数据与函数 ──

# ML 平台三组件数据 / ML Platform three components data
ml_platform_components = [
    [
        "Model Deployment",
        "模型部署",
        "Push model to prod + expose as API endpoint",
        "Most mature component",
    ],
    [
        "Model Store",
        "模型存储",
        "Store model metadata (8 types)",
        "Beyond just weights file",
    ],
    [
        "Feature Store",
        "特征存储",
        "Ensure train/inference feature consistency",
        "Solve consistency problem",
    ],
]

# 云提供商部署工具 / Cloud provider deployment tools
deployment_tools = [
    ["AWS", "SageMaker"],
    ["Azure", "AzureML"],
    ["GCP", "VertexAI"],
    ["Startups", "MLFlow Models, Seldon, Cortex, Ray-Serve"],
]

# ── 演示 ──
print("=" * 60)
print("概念13: ML 平台三大组件 / ML Platform Components")
print("=" * 60)

ptable(ml_platform_components, headers=["Component", "中文", "Function", "Note"])
print()

print("Deployment Tools by Cloud Provider / 各云部署工具:")
ptable(deployment_tools, headers=["Provider", "Tool"])


# %%
# ============================================================
# 概念14：模型存储的八类元数据
# Concept 14: Model Store — Eight Metadata Types
# ============================================================
# 完整的模型存储不只存权重，还需要 8 类元数据
# Complete Model Store needs 8 metadata types, not just weights
# ============================================================

# ── 本单元自包含数据与函数 ──

# 八类元数据 / Eight metadata types
model_metadata = [
    ["1. Model Definition", "模型定义", "Loss function, layers, params per layer", "Reproduce experiment"],
    ["2. Model Parameters", "模型参数", "Actual parameter values post-training", "Load for inference"],
    ["3. Features & Predict", "特征与预测函数", "Featurize and predict functions", "Ensure inference consistency"],
    ["4. Dependencies", "依赖", "Python packages and versions", "Reproduce environment"],
    ["5. Data", "数据", "Pointers to data storage", "Data lineage"],
    ["6. Model Gen Code", "模型代码", "Pointer to GitHub repo", "Code audit"],
    ["7. Experiment Artifacts", "实验产物", "Loss curves, metrics", "Compare models"],
    ["8. Tags", "标签", "Searchable labels", "Discovery and retrieval"],
]

# 记忆口诀 / Memory mnemonic
mnemonic = "定参函依数码品标"
mnemonic_parts = [
    ["定", "模型定义 (Definition)"],
    ["参", "模型参数 (Parameters)"],
    ["函", "预测函数 (Functions)"],
    ["依", "依赖包 (Dependencies)"],
    ["数", "数据指针 (Data)"],
    ["码", "代码仓库 (Code)"],
    ["品", "实验制品 (Artifacts)"],
    ["标", "标签 (Tags)"],
]

# ── 演示 ──
print("=" * 60)
print("概念14: 模型存储八类元数据 / Model Store 8 Metadata Types")
print("=" * 60)

ptable(model_metadata, headers=["Metadata Type", "中文", "Content", "Why Needed"])
print()

print(f"Memory mnemonic / 记忆口诀: '{mnemonic}'")
ptable(mnemonic_parts, headers=["字", "Meaning"])


# %%
# ============================================================
# 概念15：特征存储与一致性问题
# Concept 15: Feature Store & Consistency Problem
# ============================================================
# 特征存储解决特征管理、计算复用、训练推理一致性三大问题
# Feature Store solves management, computation reuse, consistency
# ============================================================

# ── 本单元自包含数据与函数 ──

# 特征存储解决的三个问题 / Three problems Feature Store solves
feature_store_problems = [
    ["Feature Management", "特征管理", "How to organize 1000+ features?", "如何组织 1000+ 特征？"],
    ["Feature Computation", "特征计算", "How to reuse computation logic?", "如何复用计算逻辑？"],
    ["Feature Consistency", "特征一致性", "Same features in train & inference?", "训练推理特征一致？"],
]

# 一致性问题演示 / Consistency problem demonstration
# 训练时特征 / Training features
train_feature_window = 7   # 过去 7 天平均消费 / Past 7-day avg spending
train_avg_spending = 150.0

# 推理时特征（错误!）/ Inference features (WRONG!)
inference_feature_window = 30  # 过去 30 天平均消费 / Past 30-day avg spending
inference_avg_spending = 120.0

# 正确的推理特征 / Correct inference feature
correct_inference_spending = 150.0  # 必须与训练时用相同窗口 / Must use same window

# Feast vs Tecton 对比 / Feast vs Tecton comparison
feast_vs_tecton = [
    ["Batch features", "Strong", "Supported"],
    ["Streaming features", "Weak", "Supported"],
    ["Online features", "Limited", "Supported"],
    ["Integration depth", "Lightweight", "Deep integration required"],
]

# ── 演示 ──
print("=" * 60)
print("概念15: 特征存储 / Feature Store")
print("=" * 60)

ptable(feature_store_problems, headers=["Problem", "中文", "Question", "问题"])
print()

print("Consistency Problem Example / 一致性问题示例:")
consistency_rows = [
    ["Training", f"{train_feature_window}-day window", f"${train_avg_spending:.0f}", "Correct"],
    ["Inference (WRONG!)", f"{inference_feature_window}-day window", f"${inference_avg_spending:.0f}", "INCONSISTENT!"],
    ["Inference (CORRECT)", f"{train_feature_window}-day window", f"${correct_inference_spending:.0f}", "Matches training"],
]
ptable(consistency_rows, headers=["Phase", "Feature Window", "Avg Spending", "Status"])
print()

print("Feast vs Tecton:")
ptable(feast_vs_tecton, headers=["Capability", "Feast", "Tecton"])


# %%
# ============================================================
# 概念16：ML 平台选型——两个关键维度
# Concept 16: ML Platform Selection — Two Key Dimensions
# ============================================================
# 云兼容性和开源 vs 托管是选型的两个关键考量
# Cloud compatibility and open-source vs managed are two key factors
# ============================================================

# ── 本单元自包含数据与函数 ──

# 选型矩阵 / Selection matrix
selection_matrix = [
    ["Cloud Compatibility", "云兼容性", "Does it work with YOUR cloud?", "只支持特定云 = 锁定风险"],
    ["Open Source vs Managed", "开源 vs 托管", "Self-host or pay for service?", "开源=自控; 托管=省心但贵"],
]

# 开源 vs 托管详细对比 / Open-source vs Managed detailed comparison
oss_vs_managed = [
    ["Cost", "Free (+ engineering time)", "Pay per use (can be expensive)"],
    ["Control", "Full control", "Limited customization"],
    ["Security", "Self-managed (more control)", "May not comply with regulations"],
    ["Engineering", "Requires more resources", "Minimal setup needed"],
    ["Privacy", "Data stays on-prem", "Data on provider's cloud"],
]

# ── 演示 ──
print("=" * 60)
print("概念16: ML 平台选型 / Platform Selection Criteria")
print("=" * 60)

ptable(selection_matrix, headers=["Dimension", "中文", "Key Question", "Risk"])
print()

print("Open Source vs Managed Service / 开源 vs 托管服务:")
ptable(oss_vs_managed, headers=["Aspect", "Open Source", "Managed Service"])


# %%
# ============================================================
# 概念17：Slurm 脚本解读
# Concept 17: Slurm Script Structure
# ============================================================
# Slurm 是 HPC 集群最常用的声明式任务调度器
# Slurm is the most common declarative job scheduler for HPC
# ============================================================

# ── 本单元自包含数据与函数 ──

# Slurm 脚本指令详解 / Slurm script directives explained
slurm_directives = [
    ["#SBATCH -J JobName", "Job name", "作业名称 — 用于标识和查找"],
    ["#SBATCH --time=11:00:00", "Max run time (11h)", "最大运行时间 — 超时自动终止"],
    ["#SBATCH --mem-per-cpu=4096", "Memory per CPU (4GB)", "每 CPU 分配 4GB 内存"],
    ["#SBATCH --cpus-per-task=4", "CPUs per task (4 cores)", "每任务 4 个 CPU 核"],
]

# 资源计算示例 / Resource calculation example
cpus_per_task = 4
mem_per_cpu_mb = 4096
total_mem_per_task_gb = (cpus_per_task * mem_per_cpu_mb) / 1024

# 声明式 vs 命令式对比 / Declarative vs imperative comparison
declarative_vs_imperative = [
    ["Style", "Declarative (声明式)", "Imperative (命令式)"],
    ["How", "Say WHAT you need", "Say HOW to do it"],
    ["Example", "#SBATCH --mem=4096", "ssh server; allocate_mem 4096"],
    ["Tools", "Slurm, Kubernetes, SQL", "Shell scripts, manual setup"],
    ["Benefit", "System optimizes execution", "Full manual control"],
]

# ── 演示 ──
print("=" * 60)
print("概念17: Slurm 脚本 / Slurm Script Structure")
print("=" * 60)

ptable(slurm_directives, headers=["Directive", "Meaning", "说明"])
print()
print(f"Resource calculation: {cpus_per_task} CPUs x {mem_per_cpu_mb}MB = {total_mem_per_task_gb}GB total memory per task")
print(f"资源计算: {cpus_per_task} 个 CPU x {mem_per_cpu_mb}MB = {total_mem_per_task_gb}GB 每任务总内存")
print()

print("Declarative vs Imperative / 声明式 vs 命令式:")
ptable(declarative_vs_imperative, headers=["Aspect", "Option A", "Option B"])
print()
print("Key insight: Slurm's declarative style is also Kubernetes' design philosophy")
print("关键洞察: Slurm 的声明式风格也是 Kubernetes 的设计哲学")


# %%
# ============================================================
# 概念18：Dockerfile 结构解读
# Concept 18: Dockerfile Structure Walkthrough
# ============================================================
# Dockerfile 是构建 Docker 镜像的"配方"
# Dockerfile is the "recipe" for building Docker images
# ============================================================

# ── 本单元自包含数据与函数 ──

# Dockerfile 指令解读 / Dockerfile instruction walkthrough
dockerfile_instructions = [
    ["FROM pytorch/pytorch:latest", "Base image", "选择 PyTorch 作为基础镜像"],
    ["RUN git clone .../apex", "Clone repo", "克隆 NVIDIA apex 混合精度库"],
    ["RUN cd apex && python3 setup.py install", "Install package", "编译安装 apex"],
    ["WORKDIR /fancy-nlp-project", "Set working dir", "设置工作目录"],
    ["RUN git clone .../transformers", "Clone HuggingFace", "克隆 HuggingFace transformers"],
    ["RUN pip install .", "Install HF", "安装 transformers 包"],
]

# 常用 Dockerfile 指令速查 / Common Dockerfile directives
common_directives = [
    ["FROM", "Set base image", "所有 Dockerfile 必须以此开头"],
    ["RUN", "Execute command during build", "构建时执行命令"],
    ["WORKDIR", "Set working directory", "设置后续命令的工作目录"],
    ["COPY", "Copy files from host to image", "从宿主机复制文件"],
    ["ENV", "Set environment variable", "设置环境变量"],
    ["CMD", "Default command on container start", "容器启动时的默认命令"],
    ["EXPOSE", "Document which port to expose", "声明暴露的端口"],
]

# ── 演示 ──
print("=" * 60)
print("概念18: Dockerfile 结构 / Dockerfile Structure")
print("=" * 60)

print("NLP Project Dockerfile Walkthrough:")
ptable(dockerfile_instructions, headers=["Instruction", "Action", "说明"])
print()

print("Common Dockerfile Directives / 常用指令速查:")
ptable(common_directives, headers=["Directive", "Purpose", "说明"])
print()
print("Reading order: Top to bottom = step-by-step env setup")
print("阅读顺序: 从上到下 = 逐步搭建环境的过程")
