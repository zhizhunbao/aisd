---
topic: kmeans
dimension: pitfalls
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Docs: scikit-learn KMeans — https://scikit-learn.org/stable/modules/clustering.html#k-means"
  - "📚 Book: Murphy K.P., PML1 §21.3.6-21.3.7 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📚 Book: Hastie ESL §13.2.1 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "🧪 经验: sklearn source code & common practitioner pitfalls"
expiry: 6m
status: current
---

# K-Means 踩坑记录

> ⚠️ **这是知识库中最有价值的维度。** 每次踩坑后请追加条目。

---


## 坑 1: 未标准化特征导致距离被高量纲特征主导

**场景：** 数据集有"年龄（0-100）"和"收入（0-100000）"两列，直接跑 K-Means

**症状：** 聚类结果完全由"收入"主导，"年龄"对聚类几乎没有影响；换算单位后结果大变

**根因：** K-Means 用欧氏距离，高量纲特征的微小差异在距离上远大于低量纲特征的大差异；年龄差 30 岁 = 30 距离，而收入差 3 万 = 30000 距离

**解法：**

❌ 错误写法 — 直接在原始数据上聚类

```python
km = KMeans(n_clusters=3)
km.fit(df[['age', 'income']])  # 收入量纲远大于年龄，完全失效
```

✅ 正确写法 — 先标准化，再聚类

```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[['age', 'income']])
km = KMeans(n_clusters=3)
km.fit(X_scaled)
# 如果需要解释质心，记得逆变换 / Inverse transform if needed:
# centers_original = scaler.inverse_transform(km.cluster_centers_)
```

**教训：** K-Means 前**必须**标准化数值特征；若特征含义完全不同（年龄 vs 收入），StandardScaler 是安全默认选项

> 📖 scikit-learn [Preprocessing guide](https://scikit-learn.org/stable/modules/preprocessing.html)

---


## 坑 2: n_init=1 导致结果不稳定（局部最优陷阱）

**场景：** 为了加速，设置 `n_init=1`；每次运行结果都不同，且质量很差

**症状：** WCSS 忽高忽低，质心位置随机次相差很大，聚类结果无法复现

**根因：** K-Means 的目标函数非凸，不同初始化会陷入不同局部最优；只跑一次抽到"坏"初始化的概率很高

**解法：**

❌ 错误写法 — n_init 太小

```python
km = KMeans(n_clusters=5, n_init=1, random_state=None)  # 不稳定
```

✅ 正确写法 — 多次重启 + 固定随机种子

```python
km = KMeans(
    n_clusters=5,
    init='k-means++',  # K-Means++ 比 random 初始化质量更高
    n_init=10,         # 默认值，生产中可设为 10-30
    random_state=42    # 固定种子确保可复现
)
km.fit(X)
print(f"最优 WCSS: {km.inertia_:.2f}")  # n_init 次中的最小值
```

**教训：** 永远使用 `init='k-means++'` 和 `n_init≥10`；结果报告必须附上 `random_state`

> 📚 Murphy §21.3.1; 📖 Arthur & Vassilvitskii 2007

---


## 坑 3: 用 K-Means 聚非球形数据（月牙/环形）

**场景：** 数据是两个半月形（make_moons）或同心环形（make_circles），K=2 跑 K-Means

**症状：** 聚类结果完全错误——K-Means "切"出来的是两个球形区域，不是两个月牙

**根因：** K-Means 假设每个簇是围绕质心的"球形"区域，本质上是 Voronoi Diagram；能识别的只有"凸形"和"各向同性"分布

**解法：**

❌ 错误写法 — 在非球形数据上用 K-Means

```python
from sklearn.datasets import make_moons
X, _ = make_moons(n_samples=300, noise=0.05, random_state=42)
km = KMeans(n_clusters=2)  # 结果错误！两个质心都在中心附近
km.fit(X)
```

✅ 正确写法 — 改用 DBSCAN 或谱聚类

```python
from sklearn.cluster import DBSCAN, SpectralClustering
# 方案 1: DBSCAN（基于密度，无需 K）
db = DBSCAN(eps=0.3, min_samples=5)
labels = db.fit_predict(X)

# 方案 2: 谱聚类（处理非凸）
sc = SpectralClustering(n_clusters=2, affinity='rbf')
labels = sc.fit_predict(X)
```

**教训：** 在用 K-Means 之前先可视化数据（或降维后可视化）；月牙/环形 → DBSCAN/谱聚类，球形/高斯 → K-Means

> 📚 Hastie §14.3 Spectral Clustering; Murphy §21.5

---


## 坑 4: 空簇（Empty Cluster）报错或警告

**场景：** `n_clusters` 设太大，或数据分布特殊，某个质心没有分配到任何数据点

**症状：** `ConvergenceWarning: Number of distinct clusters found smaller than n_clusters`，或某个簇完全为空

**根因：** 当初始质心落在数据密度极低的区域，E 步后没有点分配给它；下一次 M 步无法计算均值

**解法：**

❌ 错误写法 — K 设得远大于真实簇数，忽略警告

```python
import warnings
warnings.filterwarnings('ignore')  # 千万别这样！
km = KMeans(n_clusters=50)  # 数据只有 3 个自然簇，K=50 导致空簇
km.fit(X)
```

✅ 正确写法 — 合理选 K，开启警告

```python
import warnings
# 用 Elbow 或 Silhouette 先估计合理 K 范围
for k in [2, 3, 4, 5]:
    with warnings.catch_warnings():
        warnings.simplefilter("error")  # 把警告变成错误，立即发现
        try:
            km = KMeans(n_clusters=k, n_init=10)
            km.fit(X)
            print(f"K={k}: OK, inertia={km.inertia_:.2f}")
        except Exception as e:
            print(f"K={k}: 失败 - {e}")
```

**教训：** K 设合理；若出现警告，减小 K 或检查数据；不要屏蔽 `ConvergenceWarning`

> 📖 scikit-learn [KMeans common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html)

---


## 坑 5: 把"inertia 一直在下降"误认为"K 越大越好"

**场景：** 画 Elbow 曲线，发现 inertia 随 K 增大一直单调下降，选了 K=N（每个点一个簇）

**症状：** K=N 时 inertia=0，但这个模型毫无意义；模型完全过拟合

**根因：** WCSS（inertia）是 K-Means 的训练目标，K 越大必然越小（极端情况 K=N 时每点自己一簇，inertia=0）；但更多的簇不意味着更好的"结构发现"

**解法：**

❌ 错误写法 — 选 inertia 最小的 K

```python
best_k = k_range[np.argmin(inertias)]  # 这会选 K=max，完全错误
```

✅ 正确写法 — 找 Elbow 拐点，配合 Silhouette Score

```python
from sklearn.metrics import silhouette_score
import numpy as np

sil_scores = []
for k in range(2, 15):
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    labels = km.fit_predict(X)
    sil_scores.append(silhouette_score(X, labels))

# 选 Silhouette 最大的 K（而非 inertia 最小的 K）
best_k = range(2, 15)[np.argmax(sil_scores)]
print(f"最优 K (Silhouette): {best_k}")
```

**教训：** inertia 只用于"对比同一 K 的不同初始化结果"；选 K 时用 Silhouette Score（外部指标）或 Gap Statistic

> 📚 Murphy §21.3.7 "Choosing the number of clusters K"

---


## 坑 6: 对类别型特征直接进行 K-Means

**场景：** 数据含有 `["大"，"中"，"小"]` 这类字符串特征，直接传给 KMeans

**症状：** `ValueError: could not convert string to float`，或 One-Hot 后欧氏距离失效

**根因：** K-Means 使用欧氏距离，数值有序性假设对 One-Hot 编码不成立；K-Means 不适合纯分类数据

**解法：**

❌ 错误写法 — 数值编码后用欧氏距离

```python
# 错误：把"小=0, 中=1, 大=2"当连续数值
from sklearn.preprocessing import LabelEncoder
X_enc = LabelEncoder().fit_transform(df['size'])  # 假设了顺序性！
km = KMeans(n_clusters=3).fit(X_enc.reshape(-1, 1))
```

✅ 正确写法 — 改用 K-Prototypes 或 K-Modes（专为混合/分类数据设计）

```python
# 安装: pip install kmodes
from kmodes.kprototypes import KPrototypes

# 混合数据（数值+类别）用 KPrototypes
kp = KPrototypes(n_clusters=3, init='Cao', random_state=42)
clusters = kp.fit_predict(X_mixed, categorical=[2, 3])  # 指定类别列索引
```

**教训：** K-Means 只适合数值特征；分类特征 → K-Modes/K-Prototypes；多类型混合 → 先合理编码再谨慎使用

> 📚 Murphy §21.3.5 K-Medoids; 🧪 经验: 实际业务数据多为混合类型

---


## 调试清单

1. [ ] **数据已标准化？** → `StandardScaler().fit_transform()` 必须在 K-Means 之前
2. [ ] **n_init 足够大？** → 至少 10，重要场合 30；避免局部最优
3. [ ] **init='k-means++'？** → 比 'random' 初始化质量高得多，是默认值
4. [ ] **有 ConvergenceWarning？** → 减少 K 或检查数据是否有异常值
5. [ ] **K 是否合理？** → Elbow + Silhouette 双重确认，不要只看 inertia
6. [ ] **聚类数量是否符合预期？** → `len(set(labels_))` 是否 == n_clusters
7. [ ] **是否有空簇？** → `np.bincount(labels_)` 查看每簇点数，有 0 则有空簇
8. [ ] **数据是否含离群值？** → 先做 IQR 过滤或用 K-Medoids
9. [ ] **结果可复现？** → 报告时必须附 `random_state` 和 `n_init`
10. [ ] **数据是否球形分布？** → 可视化检查；月牙/环形 → DBSCAN/谱聚类
