# Complete Lab Workflow

完成课程实验的完整工作流。

## 使用方式

请提供以下信息:
- 课程: ml | mv | nlp | rl
- 实验编号: lab1 | lab2 | lab3 | ...

## 执行步骤

1. **读取工作流**: 读取 `.shared/workflows/complete-lab.md`
2. **定位实验**: 查找 `courses/{course}/labs/` 下的实验文件
3. **分析要求**: 理解实验目标和评分标准
4. **编写代码**: 在 `courses/{course}/code/` 下创建代码
5. **验证结果**: 运行测试确保正确性
6. **生成文档**: 创建答案文档

## 示例

```
/complete-lab ml lab2
```

这将:
1. 读取 `courses/ml/labs/Lab2_*.md`
2. 分析实验要求
3. 在 `courses/ml/code/lab2/` 创建代码
4. 生成 `courses/ml/labs/Lab2AnswerTemplate.md`
