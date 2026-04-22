# %%
# ============================================================
# Cell 0: 工具函数（唯一共享单元）
# Utility Functions (Shared Cell)
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
# 概念01：SOTA 陷阱分析
# Concept 01: SOTA Model Trap Analysis
# ============================================================
# 为什么不应该直接使用 SOTA 模型？通过量化分析展示
# Why you shouldn't jump to SOTA models — quantitative analysis
# ============================================================

# ── 本单元自包含数据与函数 ──

# 模型评估数据：名称、准确率(%)、训练成本($)、推理延迟(ms)
# Model eval data: name, accuracy(%), training cost($), inference latency(ms)
models = [
    ("Logistic Regression", 82.3, 10, 2),
    ("Random Forest",       87.5, 50, 5),
    ("XGBoost",             89.1, 100, 8),
    ("BERT-base",           91.2, 5000, 45),
    ("GPT-4 Fine-tuned",    92.0, 50000, 200),
]

# ── 演示 ──
print("=" * 70)
print("概念01: SOTA 陷阱分析 / SOTA Model Trap Analysis")
print("=" * 70)

# 计算性价比：准确率提升 / 成本增加 / Cost-effectiveness ratio
# 性价比 = 准确率 / log(训练成本) — 越高越好
# Cost-effectiveness = accuracy / log(training_cost) — higher is better
rows = []
for name, acc, cost, latency in models:
    cost_eff = acc / math.log(cost + 1)
    rows.append([name, f"{acc}%", f"${cost:,}", f"{latency}ms", f"{cost_eff:.1f}"])

ptable(rows, headers=["模型 / Model", "准确率", "训练成本", "推理延迟", "性价比指数"])

print("\n💡 结论: XGBoost 性价比最高 — SOTA 模型准确率仅高 ~3% 但成本高 500 倍！")
print("   Conclusion: XGBoost has best cost-effectiveness — SOTA only ~3% better but 500x costlier!")


# %%
# ============================================================
# 概念02：从简单模型开始 — Baseline 比较
# Concept 02: Start with Simple Models — Baseline Comparison
# ============================================================
# 展示为什么简单模型是复杂模型的标尺
# Show why simple models serve as yardstick for complex ones
# ============================================================

# ── 本单元自包含数据与函数 ──

# 模型复杂度金字塔数据 / Model complexity pyramid data
# [模型名, 准确率, 训练时间(min), 可解释性(1-5), 部署难度(1-5)]
pyramid = [
    ("Linear Regression",    78.5, 1,    5, 1),
    ("Logistic Regression",  82.3, 2,    5, 1),
    ("SVM",                  84.0, 10,   3, 2),
    ("Random Forest",        87.5, 30,   4, 2),
    ("XGBoost",              89.1, 60,   3, 3),
    ("Neural Network (3L)",  90.2, 300,  1, 4),
    ("Transformer",          91.5, 3000, 1, 5),
]

# 增量价值函数 / Incremental value function
# 计算每增加一级复杂度带来的准确率提升
# Calculate accuracy gain per complexity level increase
def calc_incremental_gain(data):
    """计算每个模型相对于前一个模型的增量收益 / Calculate incremental gain"""
    gains = []
    for i, (name, acc, time, interp, deploy) in enumerate(data):
        if i == 0:
            gains.append((name, acc, "-", "-", f"{interp}/5", f"{deploy}/5"))
        else:
            prev_acc = data[i-1][1]
            prev_time = data[i-1][2]
            acc_gain = acc - prev_acc
            time_ratio = time / max(prev_time, 1)
            gains.append((name, f"{acc:.1f}%", f"+{acc_gain:.1f}%",
                         f"{time_ratio:.0f}x", f"{interp}/5", f"{deploy}/5"))
    return gains

# ── 演示 ──
print("\n" + "=" * 70)
print("概念02: 从简单模型开始 / Start with Simple Models")
print("=" * 70)

rows = calc_incremental_gain(pyramid)
ptable(rows, headers=["模型", "准确率", "增量提升", "时间倍数", "可解释性", "部署难度"])

print("\n💡 关键洞察: 从 RF→XGBoost 仅提升 1.6%，但从 XGBoost→Transformer 增加 50x 训练时间换 2.4% 提升")
print("   Key insight: RF→XGBoost gains only 1.6%, XGBoost→Transformer adds 50x training for 2.4%")


# %%
# ============================================================
# 概念03：学习曲线分析
# Concept 03: Learning Curve Analysis
# ============================================================
# 模拟不同模型在不同数据量下的学习曲线
# Simulate learning curves for different models at varying data sizes
# ============================================================

# ── 本单元自包含数据与函数 ──

# 模拟学习曲线函数 / Simulated learning curve function
# score = max_score * (1 - exp(-rate * n))
# n = 数据量(千条) / data size (thousands)
def learning_curve(n, max_score, rate):
    """模拟学习曲线 / Simulate learning curve"""
    return max_score * (1 - math.exp(-rate * n))

# 三个模型的参数 / Parameters for three models
# (模型名, 最大分数, 学习速率)
lc_models = [
    ("Logistic Reg.", 0.85, 0.8),   # 快速饱和 / Quick saturation
    ("Random Forest", 0.90, 0.5),   # 中速收敛 / Medium convergence
    ("Deep Learning", 0.95, 0.15),  # 慢速但高上限 / Slow but high ceiling
]

# 数据量点（千条）/ Data size points (thousands)
data_sizes = [0.1, 0.5, 1, 2, 5, 10, 50, 100]

# ── 演示 ──
print("\n" + "=" * 70)
print("概念03: 学习曲线分析 / Learning Curve Analysis")
print("=" * 70)

header = ["数据量(K)"] + [m[0] for m in lc_models]
rows = []
for n in data_sizes:
    row = [f"{n}K"]
    for name, max_s, rate in lc_models:
        score = learning_curve(n, max_s, rate)
        row.append(f"{score:.3f}")
    rows.append(row)

ptable(rows, headers=header)

print("\n💡 关键洞察: DL 在小数据(<5K)时不如 LR/RF；只有数据充足(>50K)时 DL 才显优势")
print("   Key insight: DL underperforms LR/RF on small data(<5K); only shines with >50K data")


# %%
# ============================================================
# 概念04：权衡评估 — FP vs FN 分析
# Concept 04: Trade-off Evaluation — FP vs FN Analysis
# ============================================================
# 展示假阳性和假阴性在不同场景中的代价差异
# Show how FP and FN costs differ across scenarios
# ============================================================

# ── 本单元自包含数据与函数 ──

# 场景数据 / Scenario data
# (场景, FP代价, FN代价, 哪个更严重, 应优化指标)
scenarios = [
    ("垃圾邮件过滤 / Spam Filter",    "正常邮件被标为垃圾", "垃圾邮件进入收件箱", "FP更严重", "Precision"),
    ("癌症筛查 / Cancer Screening",   "健康人被误诊为癌症", "癌症患者被漏诊",   "FN更严重", "Recall"),
    ("欺诈检测 / Fraud Detection",    "正常交易被拦截",    "欺诈交易未被拦截",  "FN更严重", "Recall"),
    ("推荐系统 / Recommendation",     "推荐用户不感兴趣的", "错过用户可能喜欢的", "均衡",     "F1-Score"),
]

# ── 演示 ──
print("\n" + "=" * 70)
print("概念04: 权衡评估 — FP vs FN / Trade-off Evaluation")
print("=" * 70)

rows = []
for scene, fp_desc, fn_desc, severity, metric in scenarios:
    rows.append([scene, fp_desc, fn_desc, severity, metric])

ptable(rows, headers=["场景", "FP (假阳性)", "FN (假阴性)", "哪个更严重", "优化指标"])

print("\n💡 没有完美模型，只有最佳权衡！不同场景对 FP/FN 的容忍度截然不同。")
print("   No perfect model, only best trade-offs! Different scenarios have different FP/FN tolerance.")


# %%
# ============================================================
# 概念05：模型假设检查
# Concept 05: Model Assumptions Check
# ============================================================
# 展示算法的隐含假设以及违反假设后的后果
# Show implicit model assumptions and consequences of violation
# ============================================================

# ── 本单元自包含数据与函数 ──

# 常见假设数据 / Common assumptions data
assumptions = [
    ("正态性 Normality",           "数据服从正态分布",     "线性回归, LDA",  "参数估计有偏"),
    ("IID",                        "数据独立同分布",       "大多数ML算法",   "时序数据泄漏"),
    ("平滑性 Smoothness",          "相似输入→相似输出",    "KNN, 核方法",    "高维失效(维度灾难)"),
    ("可处理性 Tractability",      "计算可行",            "贝叶斯方法",     "需要近似推断"),
    ("边界 Boundaries",            "类别间可分",          "SVM",           "重叠数据效果差"),
    ("条件独立 Cond.Indep.",       "特征在类别下独立",     "朴素贝叶斯",     "概率估计偏差"),
]

# ── 演示 ──
print("\n" + "=" * 70)
print("概念05: 模型假设检查 / Model Assumptions Check")
print("=" * 70)

rows = []
for name, meaning, algos, consequence in assumptions:
    rows.append([name, meaning, algos, consequence])

ptable(rows, headers=["假设", "含义", "典型算法", "违反后果"])

print("\n💡 George Box (1976): 'All models are wrong, but some are useful.'")
print("   所有模型都是对现实的近似——关键是确认你的数据是否满足模型假设!")


# %%
# ============================================================
# 概念06：梯度检查点 — 内存优化演示
# Concept 06: Gradient Checkpointing — Memory Optimization
# ============================================================
# 计算梯度检查点的内存节省和计算开销
# Calculate memory savings and compute overhead of gradient checkpointing
# ============================================================

# ── 本单元自包含数据与函数 ──

# 模拟不同层数的网络 / Simulate networks with different layer counts
layer_counts = [16, 64, 100, 256, 1024]

# 单层激活值内存占用 (MB) / Memory per layer activation (MB)
mem_per_layer = 50  # 假设每层激活占 50 MB / Assume 50MB per layer

# 最优检查点策略：每 sqrt(n) 个节点标记一个检查点
# Optimal strategy: checkpoint every sqrt(n) nodes
def checkpoint_analysis(n_layers, mem_per_layer_mb):
    """分析梯度检查点的内存和计算权衡 / Analyze checkpoint memory-compute tradeoff"""
    # 正常训练：保存所有层激活 / Normal: store all activations
    normal_mem = n_layers * mem_per_layer_mb
    # 检查点训练：只保存 sqrt(n) 个检查点 / Checkpoint: store sqrt(n)
    n_checkpoints = int(math.sqrt(n_layers))
    checkpoint_mem = n_checkpoints * mem_per_layer_mb
    # 内存节省比 / Memory savings ratio
    savings = normal_mem / max(checkpoint_mem, 1)
    # 计算开销：约 20% 增加 / Compute overhead: ~20% increase
    compute_overhead = 1.20
    return normal_mem, checkpoint_mem, n_checkpoints, savings, compute_overhead

# ── 演示 ──
print("\n" + "=" * 70)
print("概念06: 梯度检查点 / Gradient Checkpointing")
print("=" * 70)
print(f"假设每层激活占 {mem_per_layer} MB / Assume {mem_per_layer}MB per layer\n")

rows = []
for n in layer_counts:
    norm_mem, ckpt_mem, n_ckpt, saving, overhead = checkpoint_analysis(n, mem_per_layer)
    rows.append([
        n, n_ckpt,
        f"{norm_mem/1024:.1f} GB", f"{ckpt_mem/1024:.1f} GB",
        f"{saving:.1f}x", f"+{(overhead-1)*100:.0f}%"
    ])

ptable(rows, headers=["层数", "检查点数(√n)", "正常内存", "检查点内存", "内存节省", "计算开销"])

print("\n💡 关键权衡: 仅增加 20% 计算时间，可容纳 10x+ 更大模型!")
print("   Key trade-off: Only 20% more compute enables 10x+ larger models!")


# %%
# ============================================================
# 概念07：数据并行 — 同步 vs 异步模式
# Concept 07: Data Parallelism — Sync vs Async Mode
# ============================================================
# 模拟同步和异步梯度收集的行为差异
# Simulate sync and async gradient gathering behaviors
# ============================================================

# ── 本单元自包含数据与函数 ──

# 4 台机器的训练时间模拟 (秒) / Training time simulation (sec) for 4 machines
# 异构GPU导致不同速度 / Heterogeneous GPUs cause different speeds
machine_times = [10, 12, 11, 25]  # Machine 4 是落后者 / Machine 4 is straggler

# 同步模式：等最慢的 / Sync: wait for slowest
def sync_mode(times):
    """同步模式总时间 = max(所有机器) / Sync total = max(all machines)"""
    total = max(times)
    idle_times = [total - t for t in times]
    return total, idle_times

# 异步模式：不等待 / Async: no waiting
def async_mode(times):
    """异步模式：每台机器独立更新，可能用过时梯度 / Async: independent updates, stale gradients possible"""
    # 最快的机器可能在慢机器完成前就更新了多次
    # Fastest machine may update multiple times before slow ones finish
    min_time = min(times)
    staleness = [round(t / min_time - 1, 1) for t in times]
    return min_time, staleness

# ── 演示 ──
print("\n" + "=" * 70)
print("概念07: 数据并行 — 同步 vs 异步 / Data Parallelism — Sync vs Async")
print("=" * 70)

# 展示机器完成时间
rows_machines = []
for i, t in enumerate(machine_times):
    label = f"Machine {i+1}" + (" ⚠️ STRAGGLER" if t == max(machine_times) else "")
    rows_machines.append([label, f"{t}s"])
ptable(rows_machines, headers=["机器", "Batch 完成时间"])

# 同步模式分析
sync_total, idle = sync_mode(machine_times)
print(f"\n📌 同步模式 (Synchronous):")
print(f"   总等待时间 = {sync_total}s (等最慢的 Machine 4)")
sync_rows = []
for i, (t, idle_t) in enumerate(zip(machine_times, idle)):
    sync_rows.append([f"Machine {i+1}", f"{t}s", f"{idle_t}s", f"{idle_t/sync_total*100:.0f}%"])
ptable(sync_rows, headers=["机器", "计算时间", "空闲等待", "浪费比例"])

# 异步模式分析
async_fastest, staleness = async_mode(machine_times)
print(f"\n📌 异步模式 (Asynchronous):")
print(f"   最快更新间隔 = {async_fastest}s (Machine 1)")
async_rows = []
for i, (t, stale) in enumerate(zip(machine_times, staleness)):
    async_rows.append([f"Machine {i+1}", f"{t}s", f"{stale} 轮"])
ptable(async_rows, headers=["机器", "完成时间", "梯度过时轮数"])

print("\n💡 同步: Straggler Problem — Machine 4 拖慢整体 60%")
print("   异步: Gradient Staleness — Machine 4 的梯度过时 1.5 轮")


# %%
# ============================================================
# 概念08：三种并行策略比较
# Concept 08: Three Parallelism Strategies Comparison
# ============================================================
# 对比数据并行、模型并行和流水线并行
# Compare Data, Model, and Pipeline Parallelism
# ============================================================

# ── 本单元自包含数据与函数 ──

# 三种策略的维度对比 / Dimensions comparison
strategies = [
    ("数据并行\nData Parallel",
     "数据分片到多机", "每机完整模型副本", "最常用，数据多时",
     "All-Reduce梯度", "Straggler / Staleness"),
    ("模型并行\nModel Parallel",
     "相同数据", "模型不同层分到不同机器", "模型一台放不下时",
     "层间激活值传输", "气泡(Bubble)空闲"),
    ("流水线并行\nPipeline Parallel",
     "微批次(micro-batch)", "模型分层+批次交错", "大模型(如LLaMA2 70B)",
     "微批次间流水交接", "微批次管理复杂"),
]

# ── 演示 ──
print("\n" + "=" * 70)
print("概念08: 三种并行策略 / Three Parallelism Strategies")
print("=" * 70)

rows = []
for name, data_split, model_split, use_case, comm, problem in strategies:
    rows.append([name, data_split, model_split, use_case, comm, problem])

ptable(rows, headers=["策略", "数据处理", "模型处理", "适用场景", "通信方式", "主要问题"])


# %%
# ============================================================
# 概念09：DDP vs FSDP 对比
# Concept 09: DDP vs FSDP Comparison
# ============================================================
# 计算 DDP 和 FSDP 在不同模型大小下的内存效率
# Calculate memory efficiency of DDP vs FSDP for different model sizes
# ============================================================

# ── 本单元自包含数据与函数 ──

# 模型参数和每参数内存 / Model params and memory per param
# FP32: 4 bytes/param, optimizer states: ~12 bytes/param (Adam)
bytes_per_param = 4
optimizer_bytes = 12  # Adam: 2 copies (momentum + variance) + param = 12 bytes

# GPU数量 / Number of GPUs
n_gpus = 4

# 单GPU显存 (GB) / Single GPU memory (GB)
gpu_memory_gb = 24  # A10G

# 模型大小 (百万参数) / Model sizes (millions of params)
model_sizes_m = [125, 350, 1000, 7000, 13000, 70000]

def ddp_memory(params_m, n_gpus):
    """DDP: 每个 GPU 存完整模型+优化器 / DDP: full model+optimizer per GPU"""
    total_bytes = params_m * 1e6 * (bytes_per_param + optimizer_bytes)
    per_gpu = total_bytes  # 每个 GPU 都有完整副本 / Full replica per GPU
    return per_gpu / (1024**3)  # 转 GB

def fsdp_memory(params_m, n_gpus):
    """FSDP: 参数+优化器均分片 / FSDP: params+optimizer sharded"""
    total_bytes = params_m * 1e6 * (bytes_per_param + optimizer_bytes)
    per_gpu = total_bytes / n_gpus  # 分片到 N 个 GPU / Sharded across N GPUs
    return per_gpu / (1024**3)  # 转 GB

# ── 演示 ──
print("\n" + "=" * 70)
print("概念09: DDP vs FSDP / DDP vs FSDP Comparison")
print(f"GPU数量: {n_gpus}, 单GPU显存: {gpu_memory_gb}GB (A10G)")
print("=" * 70)

rows = []
for m in model_sizes_m:
    ddp_gb = ddp_memory(m, n_gpus)
    fsdp_gb = fsdp_memory(m, n_gpus)
    ddp_fit = "✓" if ddp_gb <= gpu_memory_gb else "✗ OOM"
    fsdp_fit = "✓" if fsdp_gb <= gpu_memory_gb else "✗ OOM"
    label = f"{m}M" if m < 1000 else f"{m/1000:.0f}B"
    rows.append([label, f"{ddp_gb:.1f} GB", ddp_fit, f"{fsdp_gb:.1f} GB", fsdp_fit])

ptable(rows, headers=["模型参数", "DDP 每GPU", "DDP能放下?", "FSDP 每GPU", "FSDP能放下?"])

print(f"\n💡 DDP: 每 GPU 需要完整模型 — 7B+ 模型就 OOM")
print(f"   FSDP: 分片后内存降 {n_gpus}x — 可训练更大模型!")


# %%
# ============================================================
# 概念10：软 AutoML — 超参数搜索方法
# Concept 10: Soft AutoML — Hyperparameter Search Methods
# ============================================================
# 模拟 Grid Search / Random Search / Bayesian Optimization 的搜索效率
# Simulate search efficiency of Grid / Random / Bayesian methods
# ============================================================

# ── 本单元自包含数据与函数 ──

# 模拟一个 2D 超参空间 / Simulate a 2D hyperparameter space
# 真实最优解在 (lr=0.003, batch=64) / True optimum at (lr=0.003, batch=64)
def score_function(lr, batch_size):
    """模拟超参空间的性能函数 / Simulated performance function in HP space"""
    # 以 (0.003, 64) 为中心的高斯函数 / Gaussian centered at (0.003, 64)
    lr_dist = (math.log(lr) - math.log(0.003)) ** 2
    bs_dist = ((batch_size - 64) / 32) ** 2
    return 95.0 * math.exp(-3 * lr_dist - 0.5 * bs_dist)

# Grid Search: 穷举 / Grid Search: exhaustive
def grid_search():
    """网格搜索 / Grid Search"""
    lr_grid = [0.0001, 0.001, 0.003, 0.01, 0.1]
    bs_grid = [16, 32, 64, 128, 256]
    best, best_params, n_eval = 0, None, 0
    for lr in lr_grid:
        for bs in bs_grid:
            s = score_function(lr, bs)
            n_eval += 1
            if s > best:
                best, best_params = s, (lr, bs)
    return best, best_params, n_eval

# Random Search: 随机采样 / Random Search: random sampling
def random_search(n_samples=10, seed=42):
    """随机搜索（伪随机模拟）/ Random Search (pseudo-random simulation)"""
    # 使用固定种子的伪随机 / Pseudo-random with fixed seed
    lr_options = [0.0001, 0.0005, 0.001, 0.003, 0.005, 0.01, 0.05, 0.1]
    bs_options = [8, 16, 32, 48, 64, 96, 128, 256]
    # 预设的随机采样结果 / Pre-set random samples
    samples = [(0.001, 128), (0.01, 32), (0.0001, 64), (0.003, 48),
               (0.05, 256), (0.005, 64), (0.003, 64), (0.1, 16),
               (0.001, 96), (0.003, 32)]
    best, best_params = 0, None
    for lr, bs in samples[:n_samples]:
        s = score_function(lr, bs)
        if s > best:
            best, best_params = s, (lr, bs)
    return best, best_params, n_samples

# Bayesian: 模拟贝叶斯优化（逐步逼近最优）/ Simulated Bayesian Optimization
def bayesian_search(n_iter=5):
    """贝叶斯优化模拟 / Bayesian Optimization simulation"""
    # 模拟贝叶斯优化的逐步逼近过程 / Simulate convergence
    trajectory = [
        (0.01, 32, "初始探索"),   # Initial exploration
        (0.005, 64, "利用结果"),   # Exploit result
        (0.003, 48, "逼近最优"),   # Approaching optimum
        (0.003, 64, "找到最优"),   # Found optimum
        (0.002, 64, "确认最优"),   # Confirm optimum
    ]
    best, best_params = 0, None
    for lr, bs, note in trajectory[:n_iter]:
        s = score_function(lr, bs)
        if s > best:
            best, best_params = s, (lr, bs)
    return best, best_params, n_iter, trajectory

# ── 演示 ──
print("\n" + "=" * 70)
print("概念10: 超参数搜索对比 / Hyperparameter Search Comparison")
print("=" * 70)

g_best, g_params, g_n = grid_search()
r_best, r_params, r_n = random_search()
b_best, b_params, b_n, b_traj = bayesian_search()

rows = [
    ["Grid Search 网格搜索",    f"{g_n}", f"lr={g_params[0]}, bs={g_params[1]}", f"{g_best:.2f}%"],
    ["Random Search 随机搜索",  f"{r_n}", f"lr={r_params[0]}, bs={r_params[1]}", f"{r_best:.2f}%"],
    ["Bayesian Opt 贝叶斯优化", f"{b_n}",  f"lr={b_params[0]}, bs={b_params[1]}", f"{b_best:.2f}%"],
]
ptable(rows, headers=["方法", "评估次数", "最佳超参", "最佳得分"])

print("\n贝叶斯优化逐步收敛轨迹 / Bayesian Optimization convergence:")
traj_rows = []
for i, (lr, bs, note) in enumerate(b_traj):
    s = score_function(lr, bs)
    traj_rows.append([f"Step {i+1}", f"lr={lr}", f"bs={bs}", f"{s:.2f}%", note])
ptable(traj_rows, headers=["步骤", "学习率", "BatchSize", "得分", "状态"])

print("\n💡 Grid=25次评估, Random=10次, Bayesian=5次就找到最优 — 效率差 5 倍!")


# %%
# ============================================================
# 概念11：NAS 三大组件
# Concept 11: NAS Three Components
# ============================================================
# 展示神经架构搜索的搜索空间、搜索策略、性能估计
# Show NAS components: search space, strategy, estimation
# ============================================================

# ── 本单元自包含数据与函数 ──

# 搜索空间中的典型操作 / Typical operations in search space
search_space = [
    ("3x3 Convolution",  "标准卷积", "特征提取"),
    ("5x5 Convolution",  "大核卷积", "更大感受野"),
    ("3x3 Dilated Conv",  "空洞卷积", "扩大感受野不增参数"),
    ("Max Pooling",       "最大池化", "降维"),
    ("Avg Pooling",       "平均池化", "降维(保留均值)"),
    ("Skip Connection",   "跳跃连接", "梯度直通(ResNet核心)"),
    ("Identity",          "不做操作", "保持原样"),
    ("Zero (No Connection)", "零连接", "切断路径"),
]

# 三种搜索策略对比 / Three search strategies
search_strategies = [
    ("RL-Based",    "Controller(RNN)提出架构→评估→reward反馈", "有全局优化目标"),
    ("Evolutionary","种群→变异→淘汰→下一代",                   "无需全局目标"),
    ("DARTS",       "Supernet+梯度下降同时优化",               "最快(连续优化)"),
]

# ── 演示 ──
print("\n" + "=" * 70)
print("概念11: NAS 三大组件 / NAS Three Components")
print("=" * 70)

print("\n① 搜索空间 (Search Space) — 可选的积木块:")
ss_rows = []
for op, cn_name, purpose in search_space:
    ss_rows.append([op, cn_name, purpose])
ptable(ss_rows, headers=["操作 / Operation", "中文名", "用途"])

print("\n② 搜索策略 (Search Strategy) — 怎么拼积木:")
st_rows = []
for name, method, strength in search_strategies:
    st_rows.append([name, method, strength])
ptable(st_rows, headers=["策略", "搜索方式", "优势"])

print("\n③ 性能估计 (Performance Estimation):")
print("   使用 k-fold 交叉验证评估每个候选架构的性能")
print("   Use k-fold cross validation to evaluate each candidate architecture")


# %%
# ============================================================
# 概念12：RL-Based NAS 工作流模拟
# Concept 12: RL-Based NAS Workflow Simulation
# ============================================================
# 模拟 Controller 生成架构并获得 reward 的循环过程
# Simulate Controller generating architectures and receiving rewards
# ============================================================

# ── 本单元自包含数据与函数 ──

# 模拟 NAS 迭代过程 / Simulate NAS iterations
# 每轮 Controller 提出架构，获得性能 reward
nas_iterations = [
    (1, "Conv3-Pool-Conv3-FC",        72.1, "初始随机架构"),
    (2, "Conv3-Conv5-Pool-FC",        75.3, "增加了 5x5 卷积"),
    (3, "Conv3-Conv5-Skip-Pool-FC",   79.8, "发现 Skip Connection 有帮助"),
    (4, "Conv3-Skip-Conv3-Skip-FC",   83.5, "强化 Skip Connection"),
    (5, "Conv3-Skip-Conv5-Skip-Pool", 85.2, "加入池化降维"),
    (6, "(NASNet Cell) x6",           87.0, "收敛到重复单元结构"),
]

# ── 演示 ──
print("\n" + "=" * 70)
print("概念12: RL-Based NAS 模拟 / RL-Based NAS Simulation")
print("=" * 70)
print("Controller(RNN/Transformer) 作为 Agent 不断提出架构\n")

rows = []
for iter_n, arch, acc, note in nas_iterations:
    reward = f"+{acc - (nas_iterations[iter_n-2][2] if iter_n > 1 else 0):.1f}" if iter_n > 1 else "-"
    rows.append([f"Iter {iter_n}", arch, f"{acc}%", reward, note])

ptable(rows, headers=["迭代", "架构字符串", "准确率(Reward)", "增量", "学习到了什么"])

print("\n💡 NASNet 最终在 ImageNet 上击败了人工设计的模型!")
print("   但代价是数千 GPU 小时的搜索成本")


# %%
# ============================================================
# 概念13：进化算法 NAS — 种群演化模拟
# Concept 13: Evolutionary NAS — Population Evolution
# ============================================================
# 模拟进化算法的"初始化-评估-淘汰-变异"循环
# Simulate evolution: initialize → evaluate → kill → mutate cycle
# ============================================================

# ── 本单元自包含数据与函数 ──

# 初始种群 / Initial population
initial_pop = [
    ("Arch-A", "Conv3-Conv3-FC",            68.2),
    ("Arch-B", "Conv5-Pool-FC",             71.5),
    ("Arch-C", "Conv3-Conv5-Conv3-FC",      74.1),
    ("Arch-D", "Pool-Conv3-FC",             62.3),
    ("Arch-E", "Conv3-Skip-Conv3-FC",       76.8),
    ("Arch-F", "Conv5-Conv5-Pool-FC",       69.0),
]

# 淘汰阈值 / Kill threshold
kill_threshold = 70.0

# 变异函数 / Mutation function
def mutate(name, arch, acc):
    """模拟变异：对架构做随机修改 / Simulate mutation on architecture"""
    mutations = {
        "Arch-B": ("Arch-B'",  "Conv5-Pool-Skip-FC",       73.8),
        "Arch-C": ("Arch-C'",  "Conv3-Conv5-Skip-Conv3-FC", 78.2),
        "Arch-E": ("Arch-E'",  "Conv3-Skip-Conv3-Skip-FC", 80.5),
        "Arch-F": ("Arch-F'",  "Conv5-Conv5-Skip-Pool-FC", 72.1),
    }
    return mutations.get(name, (name + "'", arch + "-Skip", acc + 1.0))

# ── 演示 ──
print("\n" + "=" * 70)
print("概念13: 进化算法 NAS / Evolutionary NAS")
print("=" * 70)

# 第一代
print("\n🧬 第 0 代 — 初始种群:")
rows = []
for name, arch, acc in initial_pop:
    status = "💀 淘汰" if acc < kill_threshold else "✓ 存活"
    rows.append([name, arch, f"{acc}%", status])
ptable(rows, headers=["架构", "结构", "准确率", "命运"])

# 存活者
survivors = [(n, a, s) for n, a, s in initial_pop if s >= kill_threshold]
print(f"\n存活: {len(survivors)} / {len(initial_pop)} (阈值 = {kill_threshold}%)")

# 第一轮变异
print("\n🧬 第 1 代 — 变异后:")
gen1 = []
for name, arch, acc in survivors:
    new_name, new_arch, new_acc = mutate(name, arch, acc)
    gen1.append((new_name, new_arch, new_acc))

all_gen1 = survivors + gen1
all_gen1.sort(key=lambda x: x[2], reverse=True)

rows = []
for name, arch, acc in all_gen1:
    origin = "变异" if "'" in name else "原始"
    rows.append([name, arch, f"{acc}%", origin])
ptable(rows, headers=["架构", "结构", "准确率", "来源"])

print(f"\n💡 AmoebaNet 证明: 进化能找到人类从未考虑过的高性能架构!")


# %%
# ============================================================
# 概念14：DARTS — Supernet 权重优化模拟
# Concept 14: DARTS — Supernet Weight Optimization
# ============================================================
# 模拟 DARTS 中 Supernet 路径权重的梯度优化过程
# Simulate gradient optimization of path weights in DARTS Supernet
# ============================================================

# ── 本单元自包含数据与函数 ──

# Supernet 中的候选操作 / Candidate operations in Supernet
# 每个操作有一个架构权重 alpha
operations = ["Conv3x3", "Conv5x5", "MaxPool", "AvgPool", "SkipConn", "Zero"]

# 初始权重（均匀）/ Initial weights (uniform)
# 模拟梯度优化 5 轮后的权重变化
# Simulate weight changes after 5 rounds of gradient optimization
alpha_history = [
    # [Conv3, Conv5, MaxPool, AvgPool, Skip, Zero]
    [0.167, 0.167, 0.167, 0.167, 0.167, 0.167],  # 初始: 均匀 / Initial: uniform
    [0.200, 0.180, 0.160, 0.140, 0.190, 0.130],  # Round 1: 微分化 / Differentiating
    [0.250, 0.150, 0.130, 0.100, 0.280, 0.090],  # Round 2: Conv3+Skip 上升
    [0.300, 0.100, 0.080, 0.060, 0.400, 0.060],  # Round 3: Skip 明显领先
    [0.330, 0.070, 0.040, 0.030, 0.500, 0.030],  # Round 4: 趋于收敛
    [0.350, 0.050, 0.020, 0.010, 0.560, 0.010],  # Round 5: 最终选择
]

# Softmax 函数 / Softmax function
def softmax(values):
    """计算 softmax 归一化 / Compute softmax normalization"""
    max_v = max(values)
    exps = [math.exp(v - max_v) for v in values]
    total = sum(exps)
    return [e / total for e in exps]

# ── 演示 ──
print("\n" + "=" * 70)
print("概念14: DARTS — Supernet 路径权重优化 / DARTS Supernet Optimization")
print("=" * 70)
print("每条路径的权重 alpha 通过梯度下降优化\n")

rows = []
for round_n, alphas in enumerate(alpha_history):
    row = [f"Round {round_n}"]
    for a in alphas:
        # 用 bar chart 可视化
        bar = "█" * int(a * 20)
        row.append(f"{a:.3f} {bar}")
    rows.append(row)

ptable(rows, headers=["轮次"] + operations)

# 最终选择
final_alphas = alpha_history[-1]
max_idx = final_alphas.index(max(final_alphas))
second_idx = sorted(range(len(final_alphas)), key=lambda i: final_alphas[i], reverse=True)[1]
print(f"\n🏆 最终选择: {operations[max_idx]} (alpha={final_alphas[max_idx]:.3f})")
print(f"   次优选择: {operations[second_idx]} (alpha={final_alphas[second_idx]:.3f})")
print(f"   其余路径 alpha→0，被\"关掉\"")

print("\n💡 DARTS 将离散搜索变成连续优化 — 搜索时间从数千GPU小时降至几小时!")
print("   DARTS turns discrete search into continuous optimization — 1000x speedup!")


# %%
# ============================================================
# 概念15：NAS 三种方法终极对比
# Concept 15: NAS Three Methods — Ultimate Comparison
# ============================================================
# 全面对比 RL / Evolutionary / DARTS 三种 NAS 方法
# Comprehensive comparison of three NAS approaches
# ============================================================

# ── 本单元自包含数据与函数 ──

# 对比维度 / Comparison dimensions
nas_comparison = [
    ("搜索时间",       "数千 GPU-hours",  "数千 GPU-hours",  "数小时"),
    ("搜索方式",       "离散(字符串)",     "离散(变异)",      "连续(梯度)"),
    ("全局控制器",     "有(RNN/Transformer)", "无(群体涌现)", "有(Supernet)"),
    ("代表成果",       "NASNet",          "AmoebaNet",       "DARTS Cell"),
    ("核心思想",       "RL Agent 迭代",    "自然选择",        "可微分松弛"),
    ("ImageNet 表现",  "Top-1: 82.7%",    "Top-1: 83.1%",    "Top-1: 73.3%*"),
    ("资源门槛",       "极高(Google级)",   "极高(Google级)",   "低(单卡可搜)"),
    ("灵活性",         "高",              "极高",             "中(受限于Supernet)"),
    ("工业可用性",     "低(太贵)",         "低(太贵)",         "高(成本可控)"),
]

# ── 演示 ──
print("\n" + "=" * 70)
print("概念15: NAS 三种方法终极对比 / NAS Three Methods Comparison")
print("=" * 70)
print("* DARTS 的 ImageNet 数字较低，因为搜的是小网络，不直接可比\n")

rows = []
for dim, rl, evo, darts in nas_comparison:
    rows.append([dim, rl, evo, darts])

ptable(rows, headers=["维度", "RL-Based NAS", "Evolutionary NAS", "DARTS"])

print("\n💡 总结:")
print("   - RL/进化: 性能天花板高，但搜索成本极其昂贵")
print("   - DARTS: 搜索效率革命性突破，让NAS从'贵族技术'变为'平民技术'")
print("   - 实际工业: DARTS 系列最实用（搜索快、成本低）")
