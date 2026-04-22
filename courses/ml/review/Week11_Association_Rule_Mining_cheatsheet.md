# W11: Association Rule Mining (关联规则挖掘)

## 1. Definitions (定义)

### 基础概念 (Basic Concepts)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------|
| Association Rule (关联规则) | 形如 X → Y 的蕴含表达式，表示物品集合之间的共现关系 (Co-occurrence)，不代表因果关系 (Causality) | `{Diaper} → {Beer}`：买尿布的人也常买啤酒 |
| Itemset (项集) | 一个或多个物品的集合，是关联规则挖掘的基本单位 | `{Milk, Bread, Diaper}` 是一个 3-项集 |
| k-itemset (k-项集) | 包含 k 个物品的项集 | `{Beer}` 是 1-项集；`{Milk, Beer}` 是 2-项集 |
| Frequent Itemset (频繁项集) | 支持度 (Support) ≥ 最小支持度阈值 (minsup) 的项集 | minsup=3 时，Bread(count=4) 频繁；Eggs(count=1) 不频繁 |
| Transaction (交易记录) | 一次购买行为中包含的物品集合，是数据库中的一条记录 | TID=1: {Bread, Milk} |
| Itemset Lattice (项集格) | 所有可能项集按子集-超集关系构成的层级搜索结构 | 从空集 → 单品 → 成对 → 三元组 → … → 全集的网格图 |

### 评估指标 (Evaluation Metrics)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------|
| Support Count $\sigma$ (支持度计数) | 某个项集在交易数据库中出现的绝对频次 | $\sigma(\{M,B,D\}) = 2$（5笔中出现2次） |
| Support $s$ (支持度) | 包含该项集的交易数占总交易数的比例，衡量"普遍性" | $s(\{M,B,D\}) = 2/5 = 0.4$ |
| Confidence $c$ (置信度) | 在包含 X 的交易中同时包含 Y 的比例，衡量"可靠性" | $c(\{M,D\}\to\{B\}) = \frac{\sigma(\{M,D,B\})}{\sigma(\{M,D\})} = \frac{2}{3} \approx 0.67$ |
| minsup (最小支持度阈值) | 用户指定的支持度下限，$s \geq$ minsup 才保留 | minsup=3 → Coke(count=2) 被剪 |
| minconf (最小置信度阈值) | 用户指定的置信度下限，$c \geq$ minconf 才保留 | minconf=0.6 → c=0.5 被剪 |

### 算法与策略 (Algorithms & Strategies)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------|
| Brute-force (暴力穷举法) | 列出所有可能规则并逐一计算的朴素方法，复杂度 O(NMw)，M=2^d，实际不可行 | d=6 时有 602 条规则；d=20 时 ~35亿条 |
| Two-Step Approach (两步法) | 先生成所有频繁项集 (Step 1)，再从每个频繁项集生成满足置信度的规则 (Step 2) 的解耦策略 | Step 1: 找 {M,D,B} 频繁 → Step 2: 切出 {M,D}→{B} 等规则 |
| Anti-monotone Property (反单调性) | 支持度数学性质：$X \subseteq Y \Rightarrow s(X) \geq s(Y)$；Apriori 剪枝的理论基石 | $s(\{M\})=0.8 \to s(\{M,B\}) \leq 0.8$ |
| Apriori Principle (Apriori 原理) | 基于反单调性：子集不频繁 → 所有超集一定不频繁，直接剪掉 | $\{A,D\}$ 不频繁 → $\{ABD\},\{ACD\}$… 全剪 |
| Apriori Algorithm (Apriori 算法) | 基于 Apriori 原理的逐层 (level-wise) 频繁项集挖掘算法，每层执行四步循环 | F₁→L₂→F₂→L₃→F₃→… 直到 F_k 为空 |
| Candidate Generation (候选生成) | Apriori 四步循环的第一步：从频繁 k-项集 F_k 组合生成候选 (k+1)-项集 L_{k+1} | 从 F₁={Bread,Milk,Beer,Diaper} 生成 6 个候选 2-项集 |
| Candidate Pruning (候选剪枝) | Apriori 四步循环的第二步：如果候选的任何 k-子集不在 F_k 中，立即剔除 | ABCE 的子集 ACE∉F₃ → ABCE 被剪掉 |
| Support Counting (支持度计数) | Apriori 四步循环的第三步：扫描全部交易数据库，计算每个候选的支持度 | 扫描 5 笔交易统计 {Bread,Milk} 出现次数 |
| Candidate Elimination (候选淘汰) | Apriori 四步循环的第四步：保留 support ≥ minsup 的候选作为 F_{k+1} | {Bread,Beer}(count=2) < minsup=3 → 淘汰 |
| $F_{k-1} \times F_{k-1}$ Prefix Merge (前缀合并法) | 两个 $(k\!-\!1)$-项集共享前 $(k\!-\!2)$ 个元素时合并 | Merge(ABC,ABD)=ABCD ✅；(ABD,ACD) ❌ |
| Alternate $F_{k-1} \times F_{k-1}$ (后缀-前缀合并法) | 第一个后 $(k\!-\!2)$ = 第二个前 $(k\!-\!2)$ 时合并 | Merge(ABC,BCD)=ABCD ✅ |
| Rule Generation (规则生成) | 频繁 $k$-项集做二元划分，共 $2^k-2$ 条候选规则 | $L=\{A,B,C,D\}$ → 14 条规则 |
| Binary Partition (二元划分) | 将 $L$ 分成非空互补 $X$ 和 $L-X$，形成 $X \to (L-X)$ | $\{A,B,C\}\to\{D\}$ 或 $\{A,B\}\to\{C,D\}$ |

## 2. Comparisons (对比)

### 暴力法 vs 两步法 vs Apriori 算法 (Brute-force vs Two-Step vs Apriori)

| Dimension (维度) | Brute-force (暴力法) | Two-Step w/o Pruning (两步法无剪枝) | Apriori Algorithm (Apriori 算法) | Example (示例) |
|-----------|---|---|---|---------|
| 搜索空间 (Search Space) | 3^d 条规则 | 2^d 个项集 | 逐层缩减 (Level-wise reduction) | d=6: 602 → 64 → 16 |
| 核心策略 (Core Strategy) | 无优化 | 支持度/置信度解耦 | 反单调性剪枝 | 不频繁子集 → 超集全部跳过 |
| 数据库扫描 (DB Scans) | 极多次 | 每层一次 | 每层一次 | 3-项集需扫描 3 次 |
| 实际可行性 (Feasibility) | ❌ d>10 崩溃 | ❌ 仍太慢 | ✅ 实际可用 | 超市 10000+ 商品场景 |

### 前缀合并法 vs 后缀-前缀合并法 (Prefix Merge vs Suffix-Prefix Merge)

| Dimension (维度) | Prefix Merge (前缀合并法) | Suffix-Prefix Merge (后缀-前缀合并法) | Example (示例) |
|-----------|---|---|---------|
| 合并条件 (Merge Condition) | 前 k-2 个元素相同 | 第一个的后 k-2 = 第二个的前 k-2 | ABC+ABD=ABCD vs ABC+BCD=ABCD |
| 初始候选数 (Initial Candidates) | 较少 | 较多 | 3 个 vs 4 个 (课堂示例) |
| 剪枝后结果 (After Pruning) | 相同 | 相同 | 都只剩 {ABCD} |
| 中间开销 (Intermediate Cost) | 生成少、剪枝少 | 生成多、剪枝多 | 前者 3→1；后者 4→1 |

### 支持度 vs 置信度 (Support vs Confidence)

| Dimension (维度) | Support (支持度) | Confidence (置信度) | Example (示例) |
|-----------|---|---|---------|
| 衡量目标 (Measures) | 规则的普遍性 (How common) | 规则的可靠性 (How reliable) | 常见≠可靠 |
| 公式 (Formula) | $\sigma(X \cup Y) / |T|$ | $\sigma(X \cup Y) / \sigma(X)$ | $s=2/5$, $c=2/3$ |
| 分母 (Denominator) | 总交易数 $|T|$ | 仅前件 $\sigma(X)$ | $|T|=5$ vs $\sigma(M,D)=3$ |
| 同源规则 (Same itemset rules) | 全部相同 | 各不相同 | 6条规则 $s$ 全=0.4，$c$ 从 0.5~1.0 |

## 3. Formulas (公式)

### 核心公式 (Core Formulas)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| $s(X) = \dfrac{\sigma(X)}{|T|}$ | 支持度 = 出现次数 / 总交易数 | $s(\{M,B,D\}) = 2/5 = 0.4$ |
| $c(X \to Y) = \dfrac{\sigma(X \cup Y)}{\sigma(X)}$ | 置信度 = 含 $X \cup Y$ / 含 $X$ | $c(\{M,D\}\to\{B\}) = 2/3 \approx 0.67$ |
| $R = 3^d - 2^{d+1} + 1$ | $d$ 个物品的所有可能规则总数 | $d=6 \to 729-128+1=602$ |
| $\text{Total itemsets} = 2^d$ | $d$ 个物品的所有可能项集数 | $d=6 \to 64$ |
| $\text{Rules} = 2^k - 2$ | 频繁 $k$-项集的候选规则数（排除空集） | $k=4 \to 14$ 条 |
| $\forall X \subseteq Y: s(X) \geq s(Y)$ | 反单调性：子集支持度 $\geq$ 超集 | $s(\{M\}) \geq s(\{M,B\})$ |

### Apriori 复杂度 (Apriori Complexity)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| $O(NMw)$ | 暴力复杂度：$N$=交易数, $M=2^d$, $w$=交易宽度 | $N=5, M=64, w=3$ |
| 无剪枝: $\binom{6}{1}+\binom{6}{2}+\binom{6}{3}=41$ | 不用 Apriori 的候选总数 | 6+15+20=41 |
| 剪枝后: $6+6+4=16$ | Apriori 剪枝后候选总数，裁减 60%+ | 从 41 降至 16 |

## 4. Practical / Lab (实战结论)

### 📊 算法应用结论 (Algorithm Application Conclusions)

| Conclusion (结论) | Detail (详情) | Example (示例) |
|------------|--------|---------|
| Apriori 剪枝效果显著 (Pruning is highly effective) | 课堂 6 商品示例中，Apriori 将候选从 41 减至 16，裁减率 >60%；商品数越多效果越明显 | 41 → 16（仅 6 商品就裁减 60%+） |
| 每增加一层 k 需额外一次完整数据库扫描 (One full DB scan per k-level) | Apriori 的主要性能瓶颈是 I/O 密集型的逐层扫描；k 最大值受频繁项集大小限制 | 3-项集 → 需完整扫描 3 次数据库 |
| 前缀合并与后缀-前缀合并结果一致 (Both merge methods yield same result) | 两种候选生成方法仅中间候选数不同，最终经剪枝后的频繁项集完全一致 | 前缀: 3→1；后缀-前缀: 4→1；最终都是 {ABCD} |
| minsup 过低会导致候选爆炸 (Low minsup → candidate explosion) | 最小支持度设太低会保留太多频繁项集，后续候选和规则数量急剧增加 | minsup=1 → 所有物品都频繁 → 无剪枝效果 |

## 5. Exam Traps (考试陷阱)

### ⚠️ Common Traps (常见陷阱)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------|
| 误以为 → 表示因果关系 (Thinking → means causality) | 关联规则的 → 只表示共现 (Co-occurrence)，不表示因果 (Causality)；买尿布不会"导致"买啤酒 | {Diaper}→{Beer} = 常一起买，NOT 尿布导致买啤酒 |
| 混淆 Support 和 Confidence 的分母 (Confusing denominators) | Support 分母 = $|T|$；Confidence 分母 = $\sigma(X)$，两者不同 | $s = 2/5$（分母=5）; $c = 2/3$（分母=3） |
| 认为同源规则置信度也相同 (Thinking same-itemset rules have same confidence) | 同一频繁项集：**$s$ 相同**但 **$c$ 不同**（取决于划分方式） | $\{M,B\}\to\{D\}$: $c=1.0$ vs $\{D\}\to\{M,B\}$: $c=0.5$ |
| Apriori 原理方向错误 (Wrong direction of Apriori) | 正向：频繁项集的所有**子集**也频繁。逆否：不频繁项集的所有**超集**也不频繁。不能反过来说"频繁项集的超集也频繁" | {AB}不频繁 → {ABC}一定不频繁 ✅；{AB}频繁 → {ABC}不一定频繁 |
| 前缀合并法的前缀长度写错 (Wrong prefix length in merge) | 合并两个 (k-1)-项集时，要求**前 k-2 个**元素相同（不是前 k-1 个，也不是前 1 个） | k=4时: 两个 3-项集需共享前 2 个元素 → ABC+ABD=ABCD ✅ |
| 候选剪枝检查不完整 (Incomplete pruning check) | 候选 k-项集的**每一个** (k-1)-子集都必须在 F_{k-1} 中，只要有**任何一个**不在就剪掉 | ABCE →需检查 ABC,ABE,ACE,BCE 全部在 F₃ 中 |
| 忘记排除空规则 (Forgetting to exclude empty rules) | 候选规则数 = 2^k − 2，减去的 2 是 L→∅ 和 ∅→L（空集不能做前件或后件） | k=4: 2⁴−2 = 14 条有效规则（不是 16 条） |
| 混淆 σ 和 s 的含义 (Confusing σ and s) | σ(X) 是支持度**计数**（绝对次数）；s(X) 是支持度**比率**（百分比）。公式中需区分 | σ({M,B,D})=2（次数）; s({M,B,D})=2/5=0.4（比率） |
