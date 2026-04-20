# 📝 简答速查 (Short Answer Quick Reference)

> **考试策略**: 5道核心题覆盖 W3/W9/W10/W12/W13，每题6分=30分。先写公式→代入数值→写结论。
> **时间分配**: 每题≤8分钟，先做会的，公式记不清也要写思路拿步骤分。

---

## 🔴 核心5题 (必考，每题6分)

### SA-1: TF-IDF + Cosine Similarity (W3) [2+2+2]

**公式三件套**:
$\text{TF}=\frac{count}{total}$ | $\text{IDF}=\log_2\frac{N}{df}$ | $\text{TF-IDF}=\text{TF}\times\text{IDF}$

$\cos(\mathbf{A},\mathbf{B})=\frac{\mathbf{A}\cdot\mathbf{B}}{\|\mathbf{A}\|\times\|\mathbf{B}\|}$

**⚠️ 陷阱**: 共同词 $df=N \Rightarrow \text{IDF}=\log_2 1=0$ → 被消除!

**完整例题**: D1="the cat sat on the mat", D2="the dog sat on the log" (N=2)
- **(a)** TF(cat,D1)=1/6≈0.167, IDF(cat)=log₂(2/1)=1.0, **TF-IDF=0.167**
- **(b)** 共同词(the,sat,on) IDF=0→消除; D1=[0,1/6,0,0,1/6,0,0], D2=[0,0,0,0,0,1/6,1/6]
- **(c)** D1·D2=0 → **cos=0** (独有词不重叠)

**向量计算模板**: w₁=(0.2,0.2,0.3,0.7) w₂=(0.3,0.4,0.8,0.5) → 点积=0.73, ‖w₁‖=√0.66≈0.81, ‖w₂‖=√1.14≈1.07 → cos≈**0.84**

---

### SA-2: Transformer Attention (W9) [2+2+2]

**(a) 公式**: $\text{Attention}(Q,K,V)=\text{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right)V$

**(b) QKV**: $Q=XW_Q$(找什么), $K=XW_K$(提供什么), $V=XW_V$(实际内容); Cross-Attn: Q=解码器,KV=编码器

**(c) 为什么÷$\sqrt{d_k}$**: $d_k$大→$QK^T$方差~$d_k$→softmax过尖[0.99,0.005]→梯度≈0→训练崩; ÷$\sqrt{d_k}$→方差~1→softmax平滑[0.4,0.3]→梯度健康

**参数速记**: $d_{model}=768, h=12, d_k=64, N=12$ | $PE_{(pos,2i)}=\sin(pos/10000^{2i/d})$

**数值计算模板**: $Q=[1,0], K_1=[1,0], K_2=[0,1], V_1=[10,0], V_2=[0,10], d_k=2$
1. 点积: $Q \cdot K_1^T=1, \; Q \cdot K_2^T=0$
2. 缩放: $\frac{1}{\sqrt{2}}≈0.707, \; \frac{0}{\sqrt{2}}=0$
3. Softmax: $e^{0.707}≈2.03, e^0=1 \Rightarrow \alpha_1≈0.67, \alpha_2≈0.33$
4. 输出: $0.67\times[10,0]+0.33\times[0,10]≈\mathbf{[6.7, 3.3]}$

---

### SA-3: BERT MLM + NSP (W10) [3+1+2]

**(a) MLM**: 随机选**15%** token → 80%→[MASK] | 10%→随机词 | 10%→不变

**(b) NSP**: [CLS]SentA[SEP]SentB[SEP] → 二分类IsNext/NotNext(各50%); $\mathcal{L}=\mathcal{L}_{MLM}+\mathcal{L}_{NSP}$

**(c) 为什么80/10/10**: 100%[MASK]→推理时无[MASK]→**训练-推理不匹配**; 10%随机→强制关注所有位置; 10%不变→保持正常token表示

**速记**: BERT-base: 12层/768维/12头/110M | 输入=Token+Segment+Position Embedding | WordPiece~30.5K

---

### SA-4: RAG Pipeline (W12) [3+2+1]

**(a) 6步** ← 口诀 **P-C-E-R-A-G**:
①Parse(文档→文本) ②Chunk(256-512tok+overlap) ③Embed(块→向量) ④Retrieve(cosine→top-k) ⑤Augment(块→prompt) ⑥Generate(LLM生成)

**(b) 2优势**: ①解决知识过时(运行时检索最新文档) ②减少幻觉+可追溯(可引用源"Ch.3,p.45")

**(c) 消除幻觉?** ❌减少但不消除! retriever可能检索错误chunk→LLM仍可能错 | RAG≠FT(RAG不改权重)

---

### SA-5: Compression + Memory (W13) [3+2+1]

**(a) 三种压缩**:
| 方法 | 做什么 | 重训? | 例子 |
|------|--------|-------|------|
| Quantization | 降精度FP32→INT8 | ❌不需要 | BERT 1.36GB→340MB |
| Pruning | 移除权重(设0) | ⚠️可能需要 | 移除90%→微调 |
| Distillation | 学生模仿教师软概率 | ✅需训练 | BERT→DistilBERT 97%质量60%小 |

**(b) 显存计算**: $\text{Memory}=N\times\text{bytes}$ → $\boxed{\text{FP32}=\times4,\;\text{FP16}=\times2,\;\text{INT8}=\times1,\;\text{INT4}=\times0.5}$

| 模型 | FP32 | FP16 | INT8 | INT4 |
|--|--|--|--|--|
| 7B | 28GB | 14GB | 7GB | 3.5GB |

**(c) LoRA**: 冻结基座,只训 $A(d\times r),B(r\times d)$, $r\ll d$; $d^2\to 2dr$(98%减); QLoRA=LoRA+4bit基座

**LoRA 计算模板**: BERT-base, $d=768$, $r=8$, 只对 Q+V 加 LoRA
- 原始 Q+V 每层: $768^2 \times 2 = 1,179,648$
- LoRA 每层: $(768\times8 + 8\times768)\times 2 = 24,576$
- 全12层: $24,576\times12 = 294,912 \approx 295K$ → 占比 $\frac{295K}{14.2M}\approx\mathbf{2.08\%}$

---

## 🟡 备选题 (按出题可能性排序)

### B-1: Edit Distance DP (W3) ⭐⭐⭐

**3种操作**(每次代价=1): 插入 | 删除 | 替换

**填格规则**:
- 行字母==列字母(**match**): $d[i][j]=$ 左上角值（免费继承）
- 行字母≠列字母(**mismatch**): $d[i][j]=1+\min(\text{左},\text{上},\text{左上})$
  - 左=插入, 上=删除, 左上=替换

**例 CAT→CAR**: 目标词(CAR)放行, 源词(CAT)放列

```
        ""   C   A   T
  ""  [  0   1   2   3 ]  ← 空→CAT需3步插入
  C   [  1   0   1   2 ]  ← C==C→左上0
  A   [  2   1   0   1 ]  ← A==A→左上0
  R   [  3   2   1   1 ]  ← R≠T→1+min(1,1,0)=1
```

**答案=右下角=1** (只需把T替换成R) **⚠️必须画完整矩阵!**

### B-2: N-gram 条件概率 (W5) ⭐⭐⭐

$P(w_3|w_1 w_2) = \frac{Count(w_1 w_2 w_3)}{Count(w_1 w_2)}$

**例**: 语料: "I love NLP"×1, "I love ML"×2, "I hate bugs"×1
- $Count(\text{"I love"})=1+2=3$
- $P(\text{NLP}|\text{I love})=\frac{1}{3}≈0.333$, $P(\text{ML}|\text{I love})=\frac{2}{3}≈0.667$
- ⚠️ "I hate bugs" 不参与计算! 条件概率只看匹配的前缀

**Bigram**: $P(w_2|w_1)=\frac{Count(w_1 w_2)}{Count(w_1)}$ | 例: $P(\text{happy}|\text{feel})=\frac{40}{100}=0.4$ (Count(happy)=30是干扰!)

### B-3: QA Token-level F1 (W10) ⭐⭐

$P=\frac{|pred \cap gold|}{|pred|}$, $R=\frac{|pred \cap gold|}{|gold|}$, $F1=\frac{2PR}{P+R}$

**例**: gold="the quick brown fox"(4词), pred="quick brown cat"(3词), overlap={quick,brown}=2
- $P=\frac{2}{3}≈0.667$, $R=\frac{2}{4}=0.5$, $F1=\frac{2\times0.667\times0.5}{0.667+0.5}≈\mathbf{0.571}$, $EM=0$(非完全匹配)
- ⚠️ EM=0 **不代表完全错误**, F1=0.571说明大部分正确!

### B-4: LSTM Gates (W5) ⭐⭐

$f_t=\sigma(W_f[h_{t-1},x_t]+b_f)$ | $i_t=\sigma(W_i[\cdot]+b_i)$ | $o_t=\sigma(W_o[\cdot]+b_o)$

$\boxed{c_t=f_t\odot c_{t-1}+i_t\odot\tilde{c}_t}$ ← **加法不是乘法!** | $h_t=o_t\odot\tanh(c_t)$

### B-5: Retrieval Metrics (W12) ⭐

$P@k=\frac{rel_{top-k}}{k}$ | $R@k=\frac{rel_{top-k}}{total_{rel}}$ | $MRR=\frac{1}{rank_1}$ | $DCG@k=\sum\frac{rel_i}{\log_2(i+1)}$ | $NDCG=\frac{DCG}{IDCG}$
