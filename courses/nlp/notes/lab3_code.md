# Lab 3 代码速查 | Code Reference

> 关键代码模式 + 参数说明 + 陷阱。完整代码见：[`code/lab3/`](../code/lab3/)

---

## 加载模型

```python
import gensim.downloader as api
import fasttext

# Word2Vec — Google News 300d (3M vocab)
w2v_model = api.load('word2vec-google-news-300')

# GloVe — Wikipedia + Gigaword 300d (400K vocab)
glove_model = api.load('glove-wiki-gigaword-300')

# FastText — Common Crawl 300d (2M vocab + subwords)
ft_model = fasttext.load_model('cc.en.300.bin')
```

---

## 余弦相似度

```python
# Word2Vec / GloVe — 先检查词汇表，再计算
def safe_similarity(w1, w2, model):
    if w1 not in model.key_to_index or w2 not in model.key_to_index:
        return None               # ⚠️ OOV → 返回 None，不要让代码崩溃
    return float(model.similarity(w1, w2))

# FastText — 无需检查，任意词均有向量
import numpy as np
def ft_similarity(w1, w2, model):
    v1 = model.get_word_vector(w1)
    v2 = model.get_word_vector(w2)
    norm1, norm2 = np.linalg.norm(v1), np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0:  # 防止除以零（极极罕见）
        return None
    return float(np.dot(v1, v2) / (norm1 * norm2))
```

---

## SimLex-999 数据处理

```python
import pandas as pd

df = pd.read_csv('SimLex-999.txt', sep='\t')             # 制表符分隔
df = df[['word1', 'word2', 'SimLex999']]                  # 只取三列
df_top60 = df.sort_values('SimLex999', ascending=False).head(60).reset_index(drop=True)

# 统计量
sim_min = df['SimLex999'].min()    # 0.23
sim_avg = df['SimLex999'].mean()   # 4.56
sim_max = df['SimLex999'].max()    # 9.80
```

---

## Pearson 相关系数

```python
# 方法 1：pandas（Lab 代码用法）
corr_w2v = df_valid['similarity_w2v'].corr(df_valid['SimLex999'])

# 方法 2：scipy（带 p-value）
from scipy import stats
r, p = stats.pearsonr(df_valid['similarity_w2v'], df_valid['SimLex999'])
```

---

## 词类比（FastText 手动实现）

```python
# A - B + C = ? （例：king - man + woman）
result_vec = (ft_model.get_word_vector('king')
              - ft_model.get_word_vector('man')
              + ft_model.get_word_vector('woman'))
result_vec /= np.linalg.norm(result_vec)   # 归一化

# 搜索最近邻（排除输入词，限制前 50,000 高频词提速）
exclude = {'king', 'man', 'woman'}
LIMIT = 50000
top_results = []
for word in ft_model.get_words()[:LIMIT]:
    if word in exclude:
        continue
    wv = ft_model.get_word_vector(word)
    wv /= np.linalg.norm(wv)
    top_results.append((word, float(np.dot(result_vec, wv))))

top_results.sort(key=lambda x: x[1], reverse=True)
print(top_results[:5])
```

---

## 拼写容错对比

```python
test_words = {
    "correct":    ["apple", "banana", "computer", "science", "education"],
    "misspelled": ["appple", "bananna", "computar", "sciience", "edcation"]
}

for correct, misspelled in zip(test_words["correct"], test_words["misspelled"]):
    print(f"Correct: {correct}, Misspelled: {misspelled}")
    # Word2Vec：OOV → N/A
    w2v_sim = safe_similarity(correct, misspelled, w2v_model)
    print(f"  Word2Vec: {w2v_sim:.4f}" if w2v_sim else "  Word2Vec: N/A (OOV)")
    # FastText：总有值
    ft_sim = ft_similarity(correct, misspelled, ft_model)
    print(f"  FastText: {ft_sim:.4f}")
```

---

## 输出格式化

```python
from tabulate import tabulate

# 结果表格（Step 5 格式）
headers = ['word1', 'word2', 'similarity_w2v', 'similarity_glove', 'SimLex999']
table_data = [
    [row['word1'], row['word2'],
     f"{row['similarity_w2v']:.4f}" if row['similarity_w2v'] else "N/A",
     f"{row['similarity_glove']:.4f}" if row['similarity_glove'] else "N/A",
     f"{row['SimLex999']:.2f}"]
    for _, row in df_results.iterrows()
]
print(tabulate(table_data, headers=headers, tablefmt='simple'))
```

---

## ⚠️ 代码陷阱

| 陷阱 | 错误写法 | 正确写法 |
|---|---|---|
| OOV 未检查 | `model.similarity(w1, w2)` | 先 `if w1 in model.key_to_index` |
| FastText 路径 | `fasttext.load_model('en')` | `fasttext.load_model('cc.en.300.bin')` |
| 工作目录问题 | 硬编码路径 | `SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))` |
| 除以零 | `np.dot(v1, v2) / (norm1 * norm2)` | 先检查 `norm1 == 0 or norm2 == 0` |
| 结果包含输入词 | 不过滤 | `if word in exclude: continue` |
