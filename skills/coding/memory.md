# 编码风格偏好

本项目使用以下编码风格和参考规范。

## 语言偏好
- **Python**: 3.11+
- **JavaScript**: ES6+
- **TypeScript**: TypeScript

## 塽名规范
- **文件名**: snake_case (例如: `user_profile.py`)
- **变量名**: snake_case (例如: `user_name`)
- **常量**: UPPER_SNAKE_CASE (例如: `MAX_retries`)

## 格式化
- **缩进**: 4 空格
- **行长**: 100 字符
- **换行符**: LF (Linux/macOS) 或 CRLF (Windows)

- **文件末尾**: 空行

## 类型提示
- **类型注解**: 使用 Python 3.11+ 类型提示
- **返回类型注解**: 函数必须有返回类型注解
- **参数类型注解**: 复杂参数使用 TypedDict

- **字符串**: 优先使用 f-string，- **集合**: 优先使用 set 或 list
- **None 检查**: 使用 `if value is None:`

## 导入规范
- **标准库**: 优先使用标准库
- **导入顺序**: 标准库 → 第三方库 → 本地模块
- **相对导入**: 使用 `from .module import`
- **避免**: `from module import *`

## 错误处理
- **优先使用异常处理**: 而不是返回值检查
- **记录日志**: 使用 logging 模块
- **自定义异常**: 继承自 Exception 基类

## 测试
- **框架**: pytest
- **覆盖率**: >80%
- **命名**: `test_*.py`
- **位置**: 与源码同级目录

## 文档
- **文档字符串**: 使用 Google 风格
- **类文档**: 包含类名、功能描述、参数、- **函数文档**: 包含参数、- 返回值、- **异常**: 可能抛出的异常
