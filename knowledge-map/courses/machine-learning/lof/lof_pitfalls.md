---
topic: lof
dimension: pitfalls
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Docs: scikit-learn LocalOutlierFactor — https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LocalOutlierFactor.html"
  - "💻 Source: scikit-learn _lof.py — https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/neighbors/_lof.py"
  - "🧪 经验: LOF novelty/outlier 模式切换导致的 AttributeError 是最常见的运行时错误"
expiry: 6m
status: current
---

# LOF 踩坑记录

> ⚠️ **这是知识库中最有价值的维度。** 每次踩坑后请追加条目。

---

## 坑 1: novelty=False 时调用 predict() 报 AttributeError

**场景：** 训练完 `LocalOutlierFactor(novelty=False)` 后，想对新数据调用 `clf.predict(X_new)`。

**症状：** `AttributeError: predict is not available when novelty=False, use fit_predict if you want to predict on training data.`

**根因：** `novelty=False`（默认）是"异常检测"模式，只能对训练数据调用 `fit_predict`；`predict`/`decision_function`/`score_samples` 这三个方法仅在 `novelty=True` 时可用（详见 `_lof.py` `@available_if` 装饰器，lines 232/343）。

**解法：**

❌ 错误写法 — novelty=False 时调用 predict

```python
clf = LocalOutlierFactor(n_neighbors=20)      # novelty=False (默认)
clf.fit(X_train)
labels = clf.predict(X_test)                  # ❌ AttributeError
```

✅ 正确写法A — 异常检测：fit_predict 一步完成

```python
clf = LocalOutlierFactor(n_neighbors=20)
labels = clf.fit_predict(X_train)             # ✅ 返回训练集标签
scores = clf.negative_outlier_factor_         # ✅ 训练集 LOF 分数
```

✅ 正确写法B — 新颖性检测：novelty=True 后 predict 新数据

```python
clf = LocalOutlierFactor(n_neighbors=20, novelty=True)
clf.fit(X_train)
labels = clf.predict(X_test)                  # ✅ 对新数据预测
```

**教训：** 根据使用场景在构造时就决定 `novelty` 参数——不能在同一个对象上两用。

> 💻 Source: [sklearn/_lof.py](../../../.github/scikit-learn/sklearn/neighbors/_lof.py) `lines 332-341`

---

## 坑 2: 误解 negative_outlier_factor_ 的符号，把"最小"当"最正常"

**场景：** 训练后想找出"最异常的点"，取 `negative_outlier_factor_` 的最大值。

**症状：** 选出来的"异常点"实际上是正常内点，真正的异常点被忽略。

**根因：** sklearn 存储的是 $-\text{LOF}$（负数）。**数值越接近 -1 越正常；数值越小（越负）越异常。** 例如 `-73.37` 代表 LOF=73.37，是严重异常点，但其数值在所有值中最小，不是最大。

**解法：**

❌ 错误写法 — argmax 取到的是最正常的点

```python
scores = clf.negative_outlier_factor_
most_anomalous = np.argmax(scores)     # ❌ 找到的是接近 -1 的正常点
```

✅ 正确写法 — argmin 取到最异常的点

```python
scores = clf.negative_outlier_factor_
most_anomalous = np.argmin(scores)     # ✅ 最负 = 最异常
top_k_outliers = np.argsort(scores)[:k]  # ✅ 最小的 k 个 = 最异常的 k 个
```

**教训：** 记住 `negative_outlier_factor_` 的语义——"负 LOF"，越小（越负）越坏。

> 📖 Docs: [scikit-learn LocalOutlierFactor Attributes](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LocalOutlierFactor.html) — `negative_outlier_factor_`

---

## 坑 3: contamination='auto' 时 predict 全部返回 1（无法检出异常）

**场景：** 使用 `fit_predict` 后发现 `labels` 全为 1，没有任何 -1。

**症状：** `(labels == -1).sum() == 0`，但 LOF 分数中有明显的极端值。

**根因：** `contamination='auto'` 时 `offset_` 固定为 `-1.5`（来自论文原文设定）。如果数据集中最异常的点 LOF 分数只有约 1.3（比较正常的场景），那么 `-1.3 > -1.5`，所有点都不会被判为异常。

**解法：**

❌ 错误写法 — auto 时 offset 固定，可能漏判所有异常

```python
clf = LocalOutlierFactor(n_neighbors=20)   # contamination='auto'
labels = clf.fit_predict(X)                # 可能全为 1
```

✅ 正确写法A — 指定 contamination 比例

```python
clf = LocalOutlierFactor(n_neighbors=20, contamination=0.05)  # 预期 5% 异常
labels = clf.fit_predict(X)                # ✅ 强制选出最异常的 5%
```

✅ 正确写法B — 手动用 LOF 分数排序，不依赖 predict

```python
clf = LocalOutlierFactor(n_neighbors=20)
clf.fit_predict(X)                         # 触发训练
scores = clf.negative_outlier_factor_
threshold = np.percentile(scores, 5)       # 最差的 5% 为异常
labels = np.where(scores < threshold, -1, 1)
```

**教训：** `contamination='auto'` 适合对算法"原味"行为做验证；生产环境应根据业务估计真实异常比例。

> 📖 Docs: [scikit-learn LOF contamination](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LocalOutlierFactor.html) — `offset_` attribute
> 💻 Source: [sklearn/_lof.py](../../../.github/scikit-learn/sklearn/neighbors/_lof.py) `lines 314-320`

---

## 坑 4: 重复值导致 LOF 分数出现 nan 或极大值

**场景：** 数据集中存在完全相同的点（重复行），如类别型特征 One-Hot 后大量相同的组合。

**症状：** `negative_outlier_factor_` 中出现 `-inf` 或极端负值（如 -1e8）；sklearn 0.22+ 会打印 `UserWarning: Duplicate values are leading to incorrect results.`

**根因：** 当 `dist(o, p) = 0` 时，reach-dist 被 k-dist 替换，但若 k-dist 本身也为 0（点完全重合），LRD = 1/0 → inf。sklearn 用 `1e-10` 防止 nan（`_lof.py` line 521），但极端值仍然存在。

**解法：**

❌ 错误写法 — 不处理重复值直接运行

```python
X_with_dupes = np.vstack([X, X[:10]])     # ❌ 含大量重复行
clf = LocalOutlierFactor(n_neighbors=5)
clf.fit_predict(X_with_dupes)             # ⚠️ Warning + 结果不可靠
```

✅ 正确写法 — 去重或增大 n_neighbors

```python
X_clean = np.unique(X_with_dupes, axis=0)  # ✅ 去重
clf = LocalOutlierFactor(n_neighbors=20)   # ✅ 增大 k 缓解影响
clf.fit_predict(X_clean)
```

**教训：** 运行 LOF 前先检查 `np.unique(X, axis=0).shape[0]` vs `X.shape[0]`，如差异大则去重或增大 k。

> 💻 Source: [sklearn/_lof.py](../../../.github/scikit-learn/sklearn/neighbors/_lof.py) `lines 521` (1e-10 guard) & `lines 323-328` (warning)

---

## 坑 5: 高维数据 LOF 分数全部趋近于 1，无区分力

**场景：** 在 100+ 维特征上直接运行 LOF，发现几乎所有点的 LOF 分数都约为 1.0。

**症状：** `negative_outlier_factor_.std() ≈ 0`；即使改变 n_neighbors 也无改善。

**根因：** 高维空间的"维度灾难"——欧氏距离集中现象：所有点对之间的距离趋于相等（期望值相同，方差趋零），导致 k-dist / reach-dist 对所有点近似相等，LRD 相等，LOF 全为 1。

**解法：**

❌ 错误写法 — 高维原始特征直接 LOF

```python
X_high_dim = np.random.randn(200, 200)    # ❌ 200 维
clf = LocalOutlierFactor(n_neighbors=20)
clf.fit_predict(X_high_dim)               # LOF 分数会全约等于 1
```

✅ 正确写法A — 先降维再运行 LOF

```python
from sklearn.decomposition import PCA
X_reduced = PCA(n_components=10).fit_transform(X_high_dim)  # ✅ 降到 10 维
clf = LocalOutlierFactor(n_neighbors=20)
clf.fit_predict(X_reduced)
```

✅ 正确写法B — 换用高维友好的异常检测算法

```python
from sklearn.ensemble import IsolationForest                 # ✅ 高维首选
clf = IsolationForest(contamination=0.05, random_state=42)
clf.fit_predict(X_high_dim)
```

**教训：** LOF 适合低到中维（< 50 维）；高维先降维，或改用 Isolation Forest。

> 📖 Paper: Breunig et al., [LOF](../../../.documents/papers/lof/breunig_2000_lof.pdf), Sec. 6 Conclusions

---

## 调试清单

1. [ ] **AttributeError on predict?** → 检查 `novelty` 参数：需 `novelty=True` 才能对新数据调用 `predict/decision_function/score_samples`
2. [ ] **所有 labels 都为 1?** → 检查 `offset_` 值；考虑显式设置 `contamination=0.05`（或实际异常比例）而非 `'auto'`
3. [ ] **LOF 分数全接近 -1?** → 检查数据维度（是否 > 50）；若是，先做 PCA 降维
4. [ ] **看到 UserWarning: Duplicate values?** → 用 `np.unique(X, axis=0)` 去重，或增大 `n_neighbors`
5. [ ] **LOF 分数包含 nan/inf?** → 同坑 4，重复值 + `n_neighbors` 过小导致；增大 `n_neighbors` 或去重
6. [ ] **结果对 n_neighbors 极度敏感?** → 尝试多个 k 值（10/20/40）再集成，或换用鲁棒性更强的 Isolation Forest
7. [ ] **novelty=True 但 score_samples 和 fit_predict 结果不同?** → 这是预期行为：novelty=True 的 predict 不把训练点算作自己的邻居，与 noevlty=False 语义不同
8. [ ] **想对新数据给出概率/置信度?** → LOF 无内置概率输出；考虑用 `decision_function` 的值做归一化，或换用 PyOD 库的 LOF 实现
9. [ ] **运行速度过慢?** → 设 `algorithm='ball_tree'` 或 `'kd_tree'`；`n_jobs=-1` 开并行；数据规模 > 10万考虑近似 kNN（如 HNSW）
10. [ ] **指定了 metric='precomputed' 但报形状错误?** → 输入必须是方阵 $(n, n)$ 距离矩阵，且 `fit_predict` 和 `predict` 都要传距离矩阵

> 📖 Docs: [scikit-learn LocalOutlierFactor](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LocalOutlierFactor.html)
> 💻 Source: [sklearn/_lof.py](../../../.github/scikit-learn/sklearn/neighbors/_lof.py)
