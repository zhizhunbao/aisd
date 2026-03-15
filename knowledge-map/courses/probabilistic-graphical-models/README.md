# Probabilistic Graphical Models Knowledge Map

> 来源课程：CMU 10-708 (Eric Xing) · Koller & Friedman《PGM》· Jordan《Introduction to PGM》
> 级别：研究生 Master · 角色：ML 工程师
> 前置课程：`probability` · `statistics` · `machine-learning`

## 课程定位

PGM 用图结构描述高维概率分布的分解，是贝叶斯推断和深度生成模型的理论根基。

| 维度 | Machine Learning (研究生) | PGM (研究生) |
|------|--------------------------|-------------|
| 重点 | 判别模型 + 评估指标 | 概率建模 + 推断算法 |
| 核心方法 | SVM/决策树/神经网络 | 变分推断/MCMC/EM |
| 图 | — | 贝叶斯网络/MRF/因子图 |
| 与 DL 交叉 | CNN/RNN/Transformer | VAE/GAN/扩散模型/能量模型 |

## 主题列表

| 主题 | 文件数 | 状态 | 描述 |
|------|--------|------|------|
| bayesian_networks | 0 | 🔲 planned | 贝叶斯网络：DAG/CPT/d-分离/朴素贝叶斯/HMM |
| markov_random_fields | 0 | 🔲 planned | MRF：势函数/配分函数/CRF/Ising模型/因子图 |
| exact_inference | 0 | 🔲 planned | 精确推断：变量消除/信念传播/联合树/Viterbi |
| variational_inference | 0 | 🔲 planned | 变分推断：均值场/ELBO/EP/摊销推断/随机VI |
| monte_carlo | 0 | 🔲 planned | MCMC：Metropolis-Hastings/Gibbs/HMC/NUTS |
| learning | 0 | 🔲 planned | 学习：MLE/MAP/EM算法/结构学习/PC算法 |
| deep_generative | 0 | 🔲 planned | 深度生成模型：VAE/GAN/Flow/扩散/RBM/EBM |
| causal_inference | 0 | 🔲 planned | 因果推断：do-Calculus/反事实/后门/前门/SCM |
