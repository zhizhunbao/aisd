# 测试生成指令

## Python 测试
- 使用 pytest 框架
- 测试文件命名: `test_*.py`
- 测试函数命名: `test_功能描述`

## 测试覆盖
- 每个函数至少包含正常用例
- 包含边界用例和异常用例
- 使用 fixtures 共享测试数据

## 测试结构
```python
import pytest

class TestClassName:
    """测试类描述"""
    
    def test_normal_case(self):
        """正常用例"""
        pass
    
    def test_edge_case(self):
        """边界用例"""
        pass
    
    def test_error_case(self):
        """异常用例"""
        pass
```

## 参考
- 遵循 `.shared/skills/dev-tdd_guide/` 中的 TDD 指南
- 使用 `.shared/skills/dev-senior_qa/` 中的质量标准
