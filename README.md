# AISD — AI & Software Development Course Materials

> 📚 **Complete study materials for Algonquin College AI & Software Development (AISD) program**
> Including lecture notes, lab solutions, interactive review hubs, practice quizzes, cheat sheets, math foundations, and more.
>
> 🇨🇳 Algonquin College AI 与软件开发课程学习资料全集 — 包含讲义笔记、实验代码、交互式复习平台、练习题库、速查表、数学基础等。

---

## ✨ Highlights / 亮点

| Feature | Description |
|---------|-------------|
| 🎯 **6 Complete Courses** | ML, MV, NLP, RL, Math Foundations, Capstone Project |
| 📝 **Interactive Review Hubs** | Self-hosted HTML quiz apps with instant feedback for each course |
| 🧮 **Math Foundations** | 16 standalone math prereq documents with textbook citations |
| 📊 **100+ Practice Quiz Questions** | JSON-based quizzes covering midterms, finals, and weekly topics |
| 📖 **Week-by-Week Storylines** | Narrative lecture notes explaining *why* before *how* |
| 🔬 **Lab Code & Solutions** | Jupyter notebooks and Python scripts for all lab assignments |
| 📋 **Exam Cheat Sheets** | Condensed review sheets optimized for open-book exams |

---

## 📂 Project Structure / 项目结构

```
aisd/
├── courses/
│   ├── ml/           # Machine Learning (机器学习) — CST8507
│   ├── mv/           # Machine Vision (机器视觉) — CST8508
│   ├── nlp/          # Natural Language Processing (自然语言处理) — CST8507
│   ├── rl/           # Reinforcement Learning (强化学习) — CST8509
│   ├── pj/           # Capstone Project (毕业设计) — CST8510
│   ├── math/         # Math Foundations (数学基础) — cross-course
│   └── fuse/         # FUSE Challenge (跨学科创客挑战赛)
├── knowledge-map/    # AI knowledge maps & concept registry
├── textbooks/        # Reference textbook PDFs
├── scripts/          # Utility scripts (PDF processing, search, etc.)
└── pyproject.toml    # Python dependencies (uv managed)
```

---

## 📘 Course Details / 课程详情

### Machine Learning (ML) — CST8507

> 机器学习：从数据预处理到集成学习的完整课程

**Topics covered:**
- Data Preprocessing (数据预处理) — normalization, missing values, feature scaling
- Support Vector Machines (SVM, 支持向量机) — kernel trick, margin optimization
- Convolutional Neural Networks (CNN, 卷积神经网络) — architecture, backpropagation
- Recurrent Neural Networks (RNN, 循环神经网络) — LSTM, sequence modeling
- Naive Bayes Classifier (朴素贝叶斯) — Gaussian, Multinomial, Bernoulli
- Clustering (聚类) — K-Means, EM algorithm, Gaussian Mixture Models
- Imbalanced Class Problem (类别不平衡) — SMOTE, cost-sensitive learning
- Classifier Fusion (分类器融合) — Bagging, Boosting, Stacking
- Association Rule Mining (关联规则挖掘) — Apriori, support/confidence/lift

**Materials include:**
- 📊 Weekly review notes (Week 1–11)
- 📝 Interactive Review Hub (`courses/ml/review/index.html`)
- 🧮 Calculation problem sets with worked solutions
- 📋 Quiz bank: midterm + final + weekly quizzes (JSON)
- 📖 Week-by-week storyline narratives

---

### Machine Vision (MV) — CST8508

> 机器视觉：从图像处理基础到深度学习目标检测

**Topics covered:**
- Image Processing Fundamentals (图像处理基础) — filters, convolution, edge detection
- Feature Detection & Matching (特征检测与匹配) — SIFT, ORB, FAST
- CNN for Vision (视觉CNN) — LeNet, AlexNet, VGG, ResNet
- Deep Learning Frameworks (深度学习框架) — PyTorch, TensorFlow
- Object Detection (目标检测) — YOLO, R-CNN, SSD
- Object Tracking (目标跟踪) — optical flow, Kalman filter
- Sensor Fusion (传感器融合) — LiDAR + Camera, multi-modal
- OpenMMLab Ecosystem (OpenMMLab 生态) — MMPretrain, MMDetection

**Materials include:**
- 🔬 5 complete lab solutions with Jupyter notebooks (OpenCV, ORB, PyTorch)
- 📝 Interactive Review Hub (`courses/mv/review/index.html`)
- 📋 Quiz bank: midterm + final + weekly quizzes (JSON)
- 📖 11-week storyline narratives with slide summaries
- 🎤 Audio storyline narrations for review

---

### Natural Language Processing (NLP) — CST8507

> 自然语言处理：从文本预处理到大语言模型

**Topics covered:**
- Text Preprocessing (文本预处理) — tokenization, stemming, lemmatization
- Word Embeddings (词嵌入) — Word2Vec, GloVe, FastText
- Language Models (语言模型) — N-gram, neural LMs
- Sequence Models (序列模型) — RNN, LSTM, GRU, Seq2Seq
- Attention Mechanisms (注意力机制) — self-attention, multi-head
- Transformer Architecture (Transformer 架构) — encoder-decoder, positional encoding
- Pre-trained Models (预训练模型) — BERT, GPT, T5
- NLP Applications (NLP 应用) — NER, sentiment analysis, machine translation

**Materials include:**
- 📝 13-lecture storyline narratives and slide notes
- 📋 Comprehensive cheat sheets per topic (12 files)
- 📊 Unified cheat sheet (HTML + Markdown)
- 📋 Quiz bank: weekly quizzes + final short answer (JSON)
- 🔬 Demo scripts with Python implementations

---

### Reinforcement Learning (RL) — CST8509

> 强化学习：从 MDP 到 DQN，从 Gymnasium 到 Gazebo

**Topics covered:**
- RL Fundamentals (强化学习基础) — agent, environment, reward, policy
- Markov Decision Process (MDP, 马尔可夫决策过程) — Bellman equation, discount factor
- OpenAI Gymnasium (Gymnasium 环境) — CartPole, FrozenLake, custom envs
- Stable-Baselines3 (SB3) — PPO, A2C, DQN training
- Deep Q-Network (DQN, 深度Q网络) — experience replay, target network
- Dynamic Programming (动态规划) — value iteration, policy iteration
- Monte Carlo Methods (蒙特卡洛方法) — first-visit, every-visit MC
- Value Function Approximation (值函数近似) — linear, neural network
- Gazebo + ROS (机器人仿真) — robotic RL simulation
- Docker for RL (容器化部署) — containerized training environments

**Materials include:**
- 🔬 5 lab reports (CliffWalking, Gymnasium, Gazebo, Actor-Critic, Docker)
- 📝 Interactive Review Hub (`courses/rl/review/index.html`)
- 📋 Quiz bank: 11 quiz files including midterm + final (JSON)
- 📖 10-week storyline narratives
- 📋 Final exam cheat sheet
- 🔬 Complete merged RL notes (586K+ words)

---

### Math Foundations (数学基础)

> 跨课程数学前置知识，每个公式都有教科书出处

**Topics covered:**
- **Linear Algebra** — vectors, matrices, inner product, norms, eigenvalues, SVD
- **Calculus** — derivatives, chain rule, gradients, geometric series
- **Probability** — conditional probability, Bayes' theorem, Markov chains, cross entropy
- **Statistics** — mean, variance, Gaussian distribution, MLE
- **Optimization** — gradient descent, Lagrange multipliers
- **General** — argmax, convolution

**16 standalone documents** with dependency maps and course reading lists.
Each formula includes citations from: *Mathematics for Machine Learning*, *Bayesian Reasoning and ML*, *Deep Learning (Goodfellow)*, *Convex Optimization (Boyd)*, *Reinforcement Learning (Sutton & Barto)*.

---

### Capstone Project (PJ) — CST8510

> 毕业设计：Ottawa Economic Development RAG System

A RAG (Retrieval-Augmented Generation) system for Ottawa economic development data.

**Materials include:**
- 📊 Final presentation slides
- 📄 Final report (Word)
- 📋 Quiz materials and review notes
- 🔗 Reference GitHub repositories

---

## 🎮 Interactive Review Hubs / 交互式复习平台

Each course has a **self-contained HTML review hub** that runs locally in your browser — no server needed.

```bash
# Open any review hub directly in your browser:
start courses/rl/review/index.html    # Windows
open courses/mv/review/index.html     # macOS
```

**Features:**
- ✅ Multiple choice, true/false, and short answer quizzes
- ✅ Instant answer reveal with explanations
- ✅ LaTeX formula rendering (MathJax)
- ✅ Score tracking per quiz
- ✅ Storyline and cheat sheet tabs for narrative review

---

## 🧮 Quiz Data Format / 题库数据格式

All quizzes use a standardized JSON format, making them easy to extend or port to other tools:

```json
{
  "title": "Quiz Title",
  "questions": [
    {
      "id": 1,
      "type": "multiple_choice",
      "question": "What is the Bellman equation?",
      "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
      "answer": "B",
      "explanation": "The Bellman equation expresses..."
    }
  ]
}
```

---

## 🚀 Getting Started / 快速开始

### Prerequisites

- Python ≥ 3.10
- [uv](https://docs.astral.sh/uv/) (recommended package manager)
- CUDA-compatible GPU (optional, for DL/RL training)

### Setup

```bash
# Clone the repository
git clone https://github.com/<your-username>/aisd.git
cd aisd

# Install all dependencies with uv
uv sync

# Activate virtual environment
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # macOS / Linux

# Or run scripts directly without activation
uv run python courses/mv/labs/lab3_orb.py
```

### Quick Start — Review for Exams

```bash
# 1. Open an interactive review hub in your browser
start courses/ml/review/index.html

# 2. Read a storyline narrative
cat courses/rl/notes/week1_rl_intro_storyline.md

# 3. Check math prerequisites
cat courses/math/README.md
```

---

## 🛠️ Utility Scripts / 工具脚本

| Script | Purpose |
|--------|---------|
| `scripts/batch_mineru.py` | Batch convert PDFs to Markdown (MinerU) |
| `scripts/build_vectors.py` | Build vector database for textbook search |
| `scripts/rebuild_db.py` | Rebuild ChromaDB for semantic search |
| `scripts/rebuild_toc.py` | Generate table of contents from PDFs |
| `scripts/search_github_books.py` | Search GitHub for open textbooks |

---

## 📐 Tech Stack / 技术栈

| Category | Tools |
|----------|-------|
| Package Manager | [uv](https://docs.astral.sh/uv/) |
| ML/DL | NumPy, Pandas, Scikit-learn, TensorFlow, PyTorch |
| Computer Vision | OpenCV, MMPretrain, MMDetection |
| NLP | NLTK, Gensim, HuggingFace Transformers |
| RL | Gymnasium, Stable-Baselines3 |
| Document Processing | PyMuPDF, pdfplumber, python-docx, MinerU |
| Search | ChromaDB, Sentence-Transformers, BM25 |

---

## 🎓 Who Is This For? / 适合谁?

- 🧑‍🎓 **Algonquin College AISD students** — current and future cohorts
- 📚 **Self-learners** studying ML, CV, NLP, or RL independently
- 🔍 **Anyone preparing for AI/ML exams** — practice quizzes with explanations
- 🌏 **Chinese-speaking learners** — bilingual notes and storylines (中英双语笔记)
- 🤖 **AI practitioners** — reference implementations and math foundations

---

## 📌 Course Codes Reference / 课程代号

| Code | Course | Semester |
|------|--------|----------|
| CST8507 | Machine Learning / NLP | Winter 2026 |
| CST8508 | Machine Vision | Winter 2026 |
| CST8509 | Reinforcement Learning | Winter 2026 |
| CST8510 | Capstone Project | Winter 2026 |

---

## 🤝 Contributing / 贡献

If you're a fellow student or alumni, feel free to:
- 🐛 Report issues or typos
- 📝 Add quiz questions or improve explanations
- 📖 Contribute storyline notes for missing weeks
- 🌐 Translate content to other languages

---

## 📜 License / 许可

This repository is for **educational purposes only**.
Course slides and official materials remain the property of Algonquin College and their respective instructors.
Student-created notes, code, and review materials are shared under [MIT License](LICENSE).

---

## 🔑 Keywords / 关键词

`Algonquin College` · `AISD` · `AI Software Development` · `Machine Learning` · `Machine Vision` · `Computer Vision` · `NLP` · `Natural Language Processing` · `Reinforcement Learning` · `Deep Learning` · `OpenCV` · `PyTorch` · `TensorFlow` · `Gymnasium` · `Stable-Baselines3` · `DQN` · `SVM` · `CNN` · `RNN` · `LSTM` · `Transformer` · `BERT` · `GPT` · `Naive Bayes` · `K-Means` · `Clustering` · `Object Detection` · `YOLO` · `Gazebo` · `ROS` · `Docker` · `RAG` · `study notes` · `exam review` · `cheat sheet` · `practice quiz` · `course materials` · `学习笔记` · `复习资料` · `速查表` · `练习题`
