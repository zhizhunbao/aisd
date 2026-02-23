# Generate Study Material

从课程内容生成学习材料。

## 使用方式

指定课程和材料类型:
- 课程: ml | mv | nlp | rl
- 类型: notes | quiz | flashcards | summary | lab

## 执行步骤

1. **读取工作流**: `.shared/workflows/generate-study-material.md`
2. **定位资源**: 
   - Slides 流程: 查找 `courses/{course}/slides/` 和 `data/{course}/`
   - Lab 流程: 查找 `courses/{course}/labs/` 和 `courses/{course}/code/lab{N}/`
3. **提取内容**: 分析关键概念
4. **生成材料**: 创建学习内容

## 可用 Skills

- `learning-note_taking`: 笔记整理
- `learning-quiz_generation`: 测验生成
- `learning-quiz_note_taking`: 测验笔记

## 示例

```
/generate-study-material ml notes chapter1
```

```
/generate-study-material nlp quiz lab2
```

```
/generate-study-material nlp lab3
```
