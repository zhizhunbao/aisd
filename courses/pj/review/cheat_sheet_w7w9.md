# W7/W9: MLOps Infrastructure & Tooling (MLOps 基础设施与工具)

> **本页缩写 (Abbreviations used)**
> **CPU** = Central Processing Unit  
> **GCP** = Google Cloud Platform  
> **GPU** = Graphics Processing Unit  



## 1. Definitions (定义)

### Four-Layer Architecture (四层架构)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Storage & Compute Layer (存储与计算层) | ML 系统的"地基"，提供数据存储 (HDD/SSD/Cloud) 和算力 (GPU/CPU) (foundation layer providing data storage and compute power) | AWS S3 存数据，A100 GPU 跑训练 |
| Resource Management Layer (资源管理层) | ML 系统的"水电管道"，解决多任务调度、依赖关系和资源分配 (scheduling, dependency management, resource allocation) | Airflow DAG 调度、Slurm 排队、K8s 编排 |
| ML Platform Layer (ML 平台层) | ML 系统的"精装修"工具集，管理模型/特征/部署的全生命周期 (full lifecycle management for models, features, deployment) | SageMaker 部署、MLFlow 模型存储、Feast 特征存储 |
| Development Environment Layer (开发环境层) | ML 工程师的日常工作台 (daily workspace)，包含 IDE + 版本控制 + CI/CD | Jupyter Notebook + Git + GitHub Actions |

### Storage & Compute (存储与计算)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| HDD (机械硬盘) | 传统磁盘存储，便宜但慢 (cheap but slow)，适合冷数据归档 | 历史日志长期存档 |
| SSD (固态硬盘) | 高速闪存存储，快但贵 (fast but expensive)，适合热数据访问 | 模型训练时频繁读取的数据集 |
| Compute Utilization (计算利用率) | 作业实际使用的 FLOPS / 计算单元最大 FLOPS 能力 (actual FLOPS / max FLOPS capability)，实际通常只有 ~50% | 你付了 100% 云费用但只用到 50% 算力 |
| Cloud Repatriation (云回迁) | 将工作负载从公有云搬回自有数据中心 (move workloads from public cloud back to on-premise)，因为云成本约占收入的 50% | a16z 分析：云支出约占收入成本的 50% |

### Development Environment (开发环境)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Stateful Notebook (有状态 Notebook) | 运行后保留变量和数据状态的交互式开发环境 (retains state after execution)，支持断点恢复和代码+文档一体化 | Netflix 在生产环境中使用 Notebook |
| Papermill | Notebook 参数化执行工具 (parameterized notebook execution)，同一个 Notebook 自动跑 N 组超参数 | 一个 Notebook 跑 100 组学习率实验 |
| Commuter | Notebook 共享平台，团队内查看/搜索/共享 Notebook (team-wide notebook sharing platform) | 团队成员浏览共享的分析报告 |
| nbdev | 将代码/文档/测试写在同一个 Notebook 里的开发框架 (code + docs + tests in one notebook) | 一个 Notebook 生成 Python 包 + 文档 + 测试 |

### Containerization (容器化)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Docker Container (Docker 容器) | 轻量级、独立、可执行的软件包，包含运行所需的一切 (self-contained executable package with code + runtime + tools + libraries + settings) | 解决"在我电脑上能跑"的环境一致性问题 |
| Docker Image (Docker 镜像) | 容器的构建"配方" (recipe/blueprint for building containers)，由 Dockerfile 定义 | Dockerfile → docker build → image → container |
| Pod | Kubernetes 中最小的部署单元，一组紧密协作的容器 (smallest deployable unit in K8s, group of tightly-coupled containers)，共享 IP 和端口空间，是扩缩容的原子单位 | Model API 容器 + Logging 容器 = 1 个 Pod |

### Resource Management (资源管理)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Cron | 最原始的任务调度工具，在固定时间运行任务 (run tasks at fixed times)，致命缺陷：不理解任务间的依赖关系 | 每天凌晨 2 点跑数据清洗脚本 |
| Scheduler (调度器) | 管 **When + What** 的升级版 Cron (manages when to run and what resources needed)，理解 DAG 依赖关系 | Slurm, Airflow |
| Orchestrator (编排器) | 管 **Where** 的底层资源调配 (manages where to get resources)，动态增减实例 | Kubernetes |
| DAG (有向无环图) | 定义任务之间先后依赖关系的图结构 (directed acyclic graph defining task dependencies) | 数据清洗 → 特征工程 → 训练 → 评估 |
| Airflow | Airbnb 开发的第一代工作流管理工具，有三大致命缺陷：单体架构/不可参数化/静态 DAG | DAG 写在 Python 里但不能动态创建步骤 |

### ML Platform (ML 平台)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Model Deployment (模型部署) | 将模型推送到生产环境并暴露为 API 端点 (push model to production and expose API endpoints)，最成熟的 ML 平台组件 | AWS SageMaker, Azure AzureML, GCP VertexAI |
| Model Store (模型存储) | 管理模型全生命周期元数据的系统 (system managing full model lifecycle metadata)，需存储 **8 类元数据** | 定义/参数/函数/依赖/数据/代码/制品/标签 |
| Feature Store (特征存储) | 保证训练和推理特征 100% 一致的管理系统 (ensure training-serving feature consistency)，解决 Management/Computation/Consistency 三大问题 | Feast（批量特征强）, Tecton（在线+批量） |

## 2. Comparisons (对比)

### Scheduler vs Orchestrator (调度器 vs 编排器)

| Dimension (维度) | Scheduler (调度器) | Orchestrator (编排器) | Example (示例) |
|-----------|---|---|---------| 
| 关心什么 | **When** + **What** | **Where** | 何时运行 vs 从哪里获取资源 |
| 抽象层级 | 高层：DAG、优先队列、用户配额 | 底层：机器、实例、集群、副本 | — |
| 代表工具 | Slurm, Airflow | **Kubernetes** | — |
| 比喻 | 餐厅经理（安排点菜顺序） | 厨房主管（调配厨师和灶台） | — |

### Docker 五大优势

| Dimension (维度) | Without Docker | With Docker | Example (示例) |
|-----------|---|---|---------| 
| Portability | 环境依赖不可移植 | 一次构建到处运行 | 本地训练 → 云端部署无需修改 |
| Consistency | 开发/测试/生产不一致 | 行为完全相同 | 告别"在我机器上能跑" |
| Isolation | 多模型互相干扰 | 容器间完全隔离 | 多个模型版本可并行运行 |
| Scalability | 手动扩容 | 一键伸缩容 | 流量高峰时自动扩容 |
| Version Control | 环境不可版本化 | 镜像可版本化共享 | Docker Hub 分享环境 |

### Airflow vs 新一代编排器 (Argo/Prefect)

| Dimension (维度) | Airflow | Argo / Prefect | Example (示例) |
|-----------|---|---|---------| 
| 架构 | **单体** (一个步骤失败整个重启) | 微服务架构 | 单步骤失败不影响其他步骤 |
| 参数化 | **不可参数化** (不能向 DAG 传参) | 支持参数化 | 不同学习率用同一个工作流 |
| DAG 类型 | **静态 DAG** (运行时不能动态创建步骤) | 动态 DAG | 根据中间结果自动调整后续步骤 |

### Feast vs Tecton (特征存储)

| Dimension (维度) | Feast | Tecton | Example (示例) |
|-----------|---|---|---------| 
| 批量特征 (Batch) | ✅ 擅长 | ✅ 支持 | 离线计算的统计特征 |
| 流式特征 (Streaming) | ⚠️ 弱 | ✅ 同时支持在线和批量 | 实时点击流特征 |
| 集成深度 | 轻量 | 需要深度集成 | — |

## 3. Formulas (公式)

### 计算利用率

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| $Utilization = \frac{Actual\ FLOPS}{Max\ FLOPS}$ | 计算利用率 = 实际 FLOPS / 最大 FLOPS 能力，实际通常只有 ~50% | 付了 100% 云费用只用到 50% 算力 |

## 4. Practical / Lab (实战结论)

### 📊 Lab/Assignment Conclusions (实验/作业结论)

| Conclusion (结论) | Detail (详情) | Example (示例) |
|------------|--------|---------| 
| Model Store 需要 8 类元数据 | "定参函依数码品标"——Model Definition / Parameters / Featurize&Predict / Dependencies / Data / Model Gen Code / Experiment Artifacts / Tags | 仅存 model.pt 远远不够 |
| Feature Store 核心价值是保证一致性 | 训练时用"过去7天平均消费"，推理时却用"过去30天平均消费" → 预测完全不可信；Feature Store 统一管理计算逻辑 | 训练-推理特征不一致是常见 bug |
| Slurm 脚本是声明式资源请求 | `#SBATCH --mem-per-cpu=4096` 声明需要什么，调度器自动排队分配 | 这种声明式哲学也是 K8s 的设计核心 |

## 5. Exam Traps (考试陷阱)

### ⚠️ Common Traps (常见陷阱)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------| 
| 混淆 Scheduler 和 Orchestrator | Scheduler 管 **When + What**（时间和需求），Orchestrator 管 **Where**（资源位置）——**两者不是同一层** | Airflow(调度) + K8s(编排) 配合使用 |
| 以为 Pod = Container | Pod 是一组容器的"组队"，是 K8s 扩缩容的**原子单位**；Pod 中的容器共享 IP 和端口空间  | 一个 Pod 可以包含 Model API + Logging 两个容器 |
| 以为 Notebook 只是实验工具 | Netflix 在**生产环境**中使用 Notebook | Notebook 的有状态特性使其适合生产数据管道 |
| 以为 Airflow 是最佳工作流工具 | Airflow 有**三大致命缺陷**：单体/不可参数化/静态 DAG；新一代 Argo/Prefect 已解决 | 试不同学习率 → Airflow 需要创建 N 个工作流 |
| Model Store 只需存权重文件 | 需要 **8 类元数据**：定义/参数/函数/依赖/数据/代码/制品/标签——缺一不可 | 没有 Dependencies 信息 → 无法重现环境 |
| 云计算利用率接近 100% | 实际计算利用率通常只有 **~50%**——一半算力在"空转" | 云支出约占上市公司收入成本的 50% |
