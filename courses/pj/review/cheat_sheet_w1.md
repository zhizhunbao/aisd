# W1: LLM Evaluation Principles — Observability & Instrumentation (LLM 评估原则——可观测性与插桩)

> **本页缩写 (Abbreviations used)**
> **GPT** = Generative Pre-trained Transformer  
> **ML** = Machine Learning  
> **CPU** = Central Processing Unit  



## 1. Definitions (定义)

### Observability & Telemetry (可观测性与遥测)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Observability (可观测性) | 通过系统发出的外部信号来诊断内部行为的能力 (ability to diagnose internal behavior from external signals)，无需打开黑箱 | 通过追踪 LLM 请求发现某个 prompt 导致高延迟 |
| Telemetry (遥测) | 系统运行时自动发出的行为数据 (data emitted from a system about its behavior)，包括 Spans/Traces/Metrics/Logs 四类信号 | OpenTelemetry 采集 token 使用量 |
| Span (跨度) | 遥测数据的基本单位，代表一次请求中的单个操作，包含 Name/ParentID/Timestamps/Attributes/Events 等字段 | LLM 调用耗时 234ms 的一条 Span 记录 |
| Trace (追踪) | 一个请求在整个应用中的完整路径，由多个 Span 组成 (path of a request through the application) | AI Agent 计算斐波那契：规划→执行→验证的完整链路 |
| OpenTelemetry (开放遥测) | 开源行业标准的可观测性工具框架 (open source industry standard for instrumenting observability) | 用 `@autotrace` 装饰器自动追踪 LLM 调用 |
| Monitoring (传统监控) | 只能查看预定义指标的被动方式 (passive checking of pre-defined metrics)，无法探索未知问题 | 查看 CPU 使用率、内存占用等固定 dashboard |

### Instrumentation Methods (插桩方法)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| SDK-based Instrumentation (基于 SDK 的插桩) | 开发者手动用装饰器/包装器追踪函数调用 (manually wrap functions using vendor-specific SDK)，粒度最高但代码侵入大 | LangSmith, Langfuse, MLflow |
| Auto-Instrumentation / OTel (自动插桩) | 运行时通过 Monkey-patch 替换标准库函数来自动发出追踪 (replace original function with wrapped function at runtime)，代码改动最少 | OpenLLMetry, Arize Phoenix, OpenLIT |
| Proxy-based Instrumentation (基于代理的插桩) | 应用通过中间件代理路由 LLM 请求，零代码改动但只能看到输入输出 (zero overhead, language agnostic, black-box) | Helicone, MLflow AI Gateway |

## 2. Comparisons (对比)

### Instrumentation Methods (三种插桩方法对比)

| Dimension (维度) | SDK-based | Auto-Instrumentation (OTel) | Proxy-based | Example (示例) |
|-----------|---|---|---|---------| 
| 代码侵入 (Code Intrusion) | 高 | 最小（一行初始化） | 零 | OTel 只需 `@autotrace` |
| 粒度 (Granularity) | 最高 | 中等 | 低（只看输入/输出） | SDK 可捕获自定义中间步骤 |
| 厂商锁定 (Vendor Lock-in) | 高 | 低（标准化） | 低 | OTel 可切换后端 |
| 代表工具 (Tools) | LangSmith, Langfuse | OpenLLMetry, Phoenix | Helicone | — |

### Observability vs Monitoring (可观测性 vs 传统监控)

| Dimension (维度) | Monitoring (传统监控) | Observability (可观测性) | Example (示例) |
|-----------|---|---|---------| 
| 问题类型 | 只能回答已知问题 | 可以探索**未知问题** | Monitoring: "CPU 多少？" vs Observability: "为什么 GPT-4 突然慢了？" |
| 指标范围 | 预定义指标（CPU/内存） | 任何维度的数据信号 | 固定 dashboard vs 灵活查询 |
| 适用场景 | 传统 IT 系统 | LLM/AI 应用（行为不可预测） | LLM 输出随机性→需要 Observability |

## 3. Formulas (公式)

_本周无计算公式。_

## 4. Practical / Lab (实战结论)

### 📊 Lab/Assignment Conclusions (实验/作业结论)

| Conclusion (结论) | Detail (详情) | Example (示例) |
|------------|--------|---------| 
| OpenTelemetry Hello World 练习验证了 Span 追踪的完整流程 | 通过 `TracerProvider` + `ConsoleSpanExporter` + `tracer.start_as_current_span()` 可以手动创建嵌套 Span 并输出到控制台 | `say_hello` → `format` → `println` 三层嵌套 Span |

## 5. Exam Traps (考试陷阱)

### ⚠️ Common Traps (常见陷阱)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------| 
| 混淆 Observability 和 Monitoring (传统监控) | Monitoring 只能看预定义指标（CPU/内存）；**Observability 可以问任何问题** 来探索未知问题 | Observability 能回答"为什么 GPT-4 在周二突然变慢了？" |
| 自动插桩 (OTel) = 完全不用写代码 | OTel 仍需一行初始化代码 (`@autotrace`)，且**可能与其他 monkey-patch 库冲突** | OpenLLMetry 与某些自定义中间件冲突 |
