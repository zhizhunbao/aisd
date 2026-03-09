# Lab 3 数学公式速查 | Math Formula Reference

> 所有公式含义 + 来源。详细推导见：[lab3_tutorial.md](./lab3_tutorial.md)

---

## 核心公式

### 余弦相似度 Cosine Similarity

$$\cos(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \cdot \|\mathbf{v}\|} = \frac{\sum_i u_i v_i}{\sqrt{\sum_i u_i^2} \cdot \sqrt{\sum_i v_i^2}}$$

- 范围：$[-1, 1]$，词向量实际约 $[0, 1]$
- ⚠️ 不受向量长度（词频）影响

---

### Pearson 相关系数 Pearson Correlation

$$r(X, Y) = \frac{\sum_i (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_i (x_i - \bar{x})^2} \cdot \sqrt{\sum_i (y_i - \bar{y})^2}}$$

等价于：先零均值化，再做余弦相似度。范围 $[-1, 1]$，Lab 用于量化嵌入质量。

---

### FastText 词向量合成

$$\mathbf{v}(w) = \sum_{g \in G_w} \mathbf{z}_g$$

- $G_w$：词 $w$ 的所有字符 n-gram 集合（长度 3–6）+ 整词
- $\mathbf{z}_g$：n-gram $g$ 的可训练向量
- OOV 词通过共享 n-gram 自动获得向量

---

### 词类比 Word Analogy

$$\mathbf{v}(D) \approx \mathbf{v}(A) - \mathbf{v}(B) + \mathbf{v}(C)$$

例：$\mathbf{v}(\text{queen}) \approx \mathbf{v}(\text{king}) - \mathbf{v}(\text{man}) + \mathbf{v}(\text{woman})$

语义方向：$\mathbf{d}_{\text{gender}} = \mathbf{v}(\text{man}) - \mathbf{v}(\text{woman})$（近似稳定）

---

### GloVe 目标函数（扩展参考）

$$J = \sum_{i,j=1}^{V} f(X_{ij}) \left( \mathbf{w}_i^T \tilde{\mathbf{w}}_j + b_i + \tilde{b}_j - \log X_{ij} \right)^2$$

权重函数：$f(x) = \left(\dfrac{x}{x_{\max}}\right)^\alpha$ for $x < x_{\max}$，否则 $f(x)=1$（$x_{\max}=100, \alpha=3/4$）

---

### SimLex-999 归一化（Lab 1 代码）

$$\text{simlex\_norm} = \frac{\text{SimLex999}}{10}$$

低估量（Gap）：$\text{gap} = \text{simlex\_norm} - \text{cosine\_sim}$（正值 = 嵌入低估人类）
