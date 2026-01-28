---
description: Apply bilingual (Chinese/English) comments to code files
---

1. Identify the file to be commented (e.g., target.py)

2. Apply the following rules:
   - **File docstring**: English only.
   - **Function/Class docstring**: Chinese description + `----` separator + English description.
   - **Inline comments**: Chinese comment + `#` + English comment.
   - **Section dividers**: English only.

3. Example:

```python
# 数据预处理 # Data Pre-processing
def preprocess(data):
    """
    对输入数据进行归一化处理。
    ----
    Normalize the input data.
    """
    pass
```
