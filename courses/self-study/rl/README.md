# RL Self-Study | 强化学习自学

RLHF 是 LLM 训练的核心技术，RL 比以往更重要。

---

## Books (1)

| Book | Key | Chapters | Sections |
|------|-----|----------|----------|
| Reinforcement Learning: An Introduction (2nd) | sutton | 17 | 155 |

---

## Lecture Slides (1)

| Course | Key | Lectures | Source |
|--------|-----|----------|--------|
| David Silver RL Course (UCL) | david_silver | 10 | [YouTube Playlist](https://www.youtube.com/watch?v=2pWv7GOvuf0&list=PLMZdRRhAoLnKFxZlmFoFp0uHVvN2PSE9T) |

### David Silver Lectures

| File | Topic |
|------|-------|
| L1-intro_RL.pdf | Introduction to Reinforcement Learning |
| L2-MDP.pdf | Markov Decision Processes |
| L3-dynamic-programming.pdf | Planning by Dynamic Programming |
| L4-model-free-prediction.pdf | Model-Free Prediction |
| L5-model-free-control.pdf | Model-Free Control |
| L6-value-function-approximation.pdf | Value Function Approximation |
| L7-policy-gradient-methods.pdf | Policy Gradient Methods |
| L8-integrating-learning-and-planning.pdf | Integrating Learning and Planning |
| L9-exploration-and-exploitation.pdf | Exploration and Exploitation |
| L10-games.pdf | Classic Games |

---

## 目录结构

```
rl/
├── _sources/
│   └── sutton_barto_rl_intro.pdf → sutton_sections/
├── david_silver_lectures/
│   ├── L1-intro_RL.pdf
│   ├── L2-MDP.pdf
│   ├── ...
│   └── L10-games.pdf
```

每个 `*_sections/` 包含 `toc.json` + `chXX/sec_*.pdf`。

---

## 为什么现在学 RL 更重要

1. **RLHF** - ChatGPT/Claude 训练核心
2. **AlphaFold** - 蛋白质结构预测
3. **机器人** - 运动控制、操作
4. **游戏 AI** - Dota 2, StarCraft

---

## 推荐资源

| 资源 | 链接 |
|------|------|
| David Silver Lectures | `david_silver_lectures/` (local) / [YouTube](https://www.youtube.com/watch?v=2pWv7GOvuf0&list=PLMZdRRhAoLnKFxZlmFoFp0uHVvN2PSE9T) |
| David Silver Course Page | https://www.davidsilver.uk/teaching/ |
| OpenAI Spinning Up | https://spinningup.openai.com/ |
| Berkeley CS285 | https://rail.eecs.berkeley.edu/deeprlcourse/ |

---

## 参考

- [Sutton & Barto Official](http://incompleteideas.net/book/the-book-2nd.html)
- [DeepMind RL Course](https://www.deepmind.com/learning-resources)
