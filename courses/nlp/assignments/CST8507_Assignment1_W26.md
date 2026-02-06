# CST8507: Natural Language Processing - Assignment 1

**Source:** `CST8507_Assignment 1 _W26.pdf`  
**Total Pages:** 4

---

## Part 1: Comparative Analysis of Text Representation

### Learning Objectives

- Apply classical machine learning classifiers to text data.
- Compare performance across different feature representations.

### Learning Resources

Lecture Slides, in class code and resources including Hybrid work (week 2 - 5).

### Overview

The goal of this part is to look for the best model that can classify Amazon reviews into five categories (1-5) using different textual features. The categories include business, entertainment, politics, and sports. The performance of each technique will be evaluated using accuracy and confusion matrix.

### Dataset

Download `Reviews.csv` dataset from:  
<https://www.kaggle.com/datasets/jagdishchavan/amazon-reviews>

> ⚠️ If your computer cannot handle analyzing the entire dataset, you may randomly select a subset of the data, but it must include **at least 10,000 records**.

### Processing

1. **Split the dataset** into a train set and a test set with a common ratio being 80% for the train set and 20% for the test set. Perform steps from 3 onwards on train dataset then test dataset. It is recommended to split the data into train and test sets before preprocessing and feature extraction. The reason for this is that preprocessing, and feature extraction can significantly change the distribution of the data, and it is important to ensure that the train and test sets are representative of the original data distribution.

   > 📝 **Notes:**
   > - 使用 `sklearn.model_selection.train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)`
   > - `stratify=y` 确保训练集和测试集中各类别比例一致（分层抽样）
   > - 先 split 再 preprocess，避免数据泄露（data leakage）
   > - `Score` 列作为 label（1-5 分），`Text` 列作为特征输入

2. **Data Preprocessing:** Perform necessary preprocessing steps on the collected data. Explain your preprocessing steps in your report.

   > 📝 **Notes:**
   > - **Lowercasing:** 统一小写 `text.lower()`
   > - **Remove punctuation/special chars:** `re.sub(r'[^a-zA-Z\s]', '', text)`
   > - **Tokenization:** `nltk.word_tokenize()` 或 `text.split()`
   > - **Stop words removal:** `nltk.corpus.stopwords.words('english')`
   > - **Stemming/Lemmatization:** `PorterStemmer()` 或 `WordNetLemmatizer()`
   > - **Remove HTML tags:** 如果评论中有 HTML（`<br/>` 等），用 `BeautifulSoup` 或 regex 清理
   > - Report 中需要解释每一步的原因和效果

3. **Feature Extraction:** Extract features from the preprocessed data using:
   - n-gram (choose n)
   - TF-IDF
   - One of the embedding techniques (Word2Vec, GloVe or FastText)

   > 📝 **Notes:**
   > - **n-gram (BoW):** 使用 `CountVectorizer(ngram_range=(1,2))` — unigram+bigram 通常效果较好
   > - **TF-IDF:** 使用 `TfidfVectorizer(ngram_range=(1,2), max_features=10000)` — `max_features` 限制维度
   > - **Word2Vec:** `gensim.models.Word2Vec(sentences, vector_size=100, window=5, min_count=2)`
   >   - 需要对每条文本取词向量的**平均值**作为文本向量
   > - **GloVe:** 下载预训练模型 `glove.6B.100d.txt`，用平均 pooling 生成文本向量
   > - **FastText:** `gensim.models.FastText()` 或加载预训练模型，优势在于能处理 OOV 词
   > - 三种方法生成的特征矩阵形状不同，注意检查维度

4. **Modeling:** Use the extracted feature vectors as input to two different machine learning models of your choice. Evaluate the models using `Score` as the label.

   > 📝 **Notes:**
   > - 推荐选择两个经典分类器，例如：
   >   - **Logistic Regression:** `LogisticRegression(max_iter=1000, multi_class='multinomial')`
   >   - **SVM:** `LinearSVC()` 或 `SVC(kernel='linear')` — 适合高维稀疏特征
   >   - **Random Forest:** `RandomForestClassifier()` — 适合 embedding 特征
   >   - **Naive Bayes:** `MultinomialNB()` — 适合 BoW/TF-IDF（注意不能用于负值特征）
   > - 每种 feature × 每个 model = 共 6 个实验（3 features × 2 models）
   > - Label 是 `Score`（1-5），这是一个 **多分类问题**（5 classes）

5. **Model Evaluation:** The model should be evaluated on the test set using the accuracy metric. This will give an idea of how well the model is able to classify new unseen data.

   > 📝 **Notes:**
   > - **Accuracy:** `accuracy_score(y_test, y_pred)`
   > - **F-score:** `f1_score(y_test, y_pred, average='weighted')` — 加权 F1 适合类别不均衡
   > - **Confusion Matrix:** `confusion_matrix(y_test, y_pred)` + `ConfusionMatrixDisplay` 可视化
   > - **Classification Report:** `classification_report(y_test, y_pred)` 查看每个类别的 precision/recall/f1
   > - 所有 6 个模型都需要在 **同一个 test set** 上评估，确保公平比较

6. **Tune the model's hyperparameters:** If the model does not perform well on the test set, the model's hyperparameters can be fine-tuned to improve performance.

   > 📝 **Notes:**
   > - 使用 `GridSearchCV` 或 `RandomizedSearchCV` 进行超参数搜索
   > - **Logistic Regression:** 调 `C`（正则化强度）、`solver`
   > - **SVM:** 调 `C`、`kernel`、`gamma`
   > - **Random Forest:** 调 `n_estimators`、`max_depth`、`min_samples_split`
   > - 使用 `cv=5`（5-fold cross validation）在训练集上调参
   > - Report 中需要说明调了什么参数、调参前后的对比
   > - 将最佳结果填入上面的表格

### Include The Following Information in Your Report

1. Explain how you preprocess the data.
2. Include the confusion matrix for all the models.
3. Your interpretation and discussion of the results.
4. Discuss how you Tune your model's hyperparameters to get the best accuracy results.
5. Fill in the best results for all the used methods:

| Feature Type | Model | Accuracy | F-score |
|:------------|:------|:---------|:--------|
| Embedding   |       |          |         |
| n-gram      |       |          |         |
| TF-IDF      |       |          |         |

---

## Part 2: Error Analysis Across Feature Representations

The goal of this task is to interpret model behavior by analyzing misclassified text instances across different feature extraction techniques.

**For each representation:**

1. Extract all test instances where the predicted label differs from the true label.

   > 📝 **Notes:**
   > - `misclassified = X_test[y_pred != y_test]` 获取所有预测错误的样本
   > - 保存 `true_label`、`predicted_label`、`text` 方便后续分析

2. Select at least **10 misclassified examples** per representation.

   > 📝 **Notes:**
   > - 每种 feature representation（n-gram, TF-IDF, Embedding）各选 10+ 个错误样本
   > - 优先选择有代表性的错误（如高置信度的误分类）

3. Identify and analyze:
   - Texts that are misclassified by **all** representations
   - Texts misclassified by only **simpler models** (BoW / TF–IDF)
   - Texts misclassified by **embedding-based models** only

   > 📝 **Notes:**
   > - 用集合操作找交集/差集：`common_errors = set(ngram_errors) & set(tfidf_errors) & set(emb_errors)`
   > - **所有模型都错的** → 可能是标注噪声、模糊文本、讽刺/反讽语句
   > - **仅 BoW/TF-IDF 错的** → 可能需要语义理解，简单词袋无法捕获上下文
   > - **仅 Embedding 错的** → 可能是关键词明确但语义向量平均后被稀释

4. Explain what linguistic or semantic features may have caused the error.

   > 📝 **Notes:**
   > - 常见错误原因分析：
   >   - **Ambiguity（歧义）:** 词语在不同语境下有不同含义
   >   - **Sarcasm/Irony（讽刺）:** 用词正面但实际评价负面
   >   - **Mixed sentiment（混合情感）:** 一条评论中同时有正面和负面内容
   >   - **Short text（短文本）:** 信息不足，特征稀疏
   >   - **Domain-specific terms（领域术语）:** 模型未见过的专业词汇
   > - 结合具体样本逐条分析，给出合理的语言学解释

---

## Submission Instruction

Submit your Report and code as a Jupyter Notebook with the running code, you can do the following steps:

1. **Open your Jupyter Notebook:** You can open Jupyter Notebook either from the command line by typing `jupyter notebook` or from Anaconda Navigator.
2. **Write your code:** Write the code you want to submit in the cells of the Jupyter Notebook. Make sure to run the cells so that the output is generated.
3. **Save the Notebook:** Once you have written and run your code, save the Jupyter Notebook by clicking on `File -> Save and Checkpoint` or by pressing `Ctrl + S`.
4. **Export the Notebook:** To export the Jupyter Notebook, go to `File -> Download as -> Notebook (.ipynb)`. This will download the Notebook as a `.ipynb` file on your laptop.
5. **Create a folder** named `Assignment 1`, Inside the `Assignment 1` folder, include:
   - `Report.doc`
   - `Assignment1_Code.ipynb`

Zip the `Assignment 1` folder and Submit the zipped folder on Brightspace.

> You can submit multiple times, with only the most recent submission (before the due date) graded. There will be mark deduction if you are not following the submission requirements.

---

## Grading Criteria

| Criteria | Points |
|:---------|:------:|
| Preprocessing | 10 |
| BoW Implementation | 10 |
| TF–IDF Implementation | 10 |
| Word Embeddings Implementation | 20 |
| Comparative Analysis | 25 |
| Error Analysis | 10 |
| Report and discussion | 15 |

---

## Due Date

Check Brightspace for due dates.
