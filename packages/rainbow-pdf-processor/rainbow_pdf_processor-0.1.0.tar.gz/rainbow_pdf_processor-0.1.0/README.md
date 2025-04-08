# PDF Processor

一个强大的 PDF 处理工具，用于处理和管理 PDF 文件。

## 功能特性

- PDF 文件处理
- 支持多种操作系统
- 简单易用的 API

## 安装

### 基础安装

```bash
pip install .
```

### 开发环境安装

```bash
pip install ".[dev]"
```

### 测试环境安装

```bash
pip install ".[test]"
```

## 依赖管理

项目使用 `pyproject.toml` 和 `requirements.txt` 进行依赖管理：

- `requirements.txt`: 基础依赖
- `requirements-dev.txt`: 开发依赖
- `requirements-test.txt`: 测试依赖

## 开发指南

### 环境设置

1. 克隆仓库
```bash
git clone <repository-url>
cd pdf-processor
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装开发依赖
```bash
pip install ".[dev]"
```

### 代码规范

项目使用以下工具确保代码质量：

- black: 代码格式化
- isort: import 语句排序
- flake8: 代码风格检查
- mypy: 类型检查

### 运行测试

```bash
pytest
```

## 使用示例

```python
from pdf_processor import PDFProcessor

# 创建处理器实例
processor = PDFProcessor()

# 处理 PDF 文件
processor.process("input.pdf", "output.pdf")
```

## 项目结构

```
pdf-processor/
├── pdf_processor/
│   └── __init__.py
├── tests/
│   └── __init__.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── requirements-test.txt
└── README.md
```

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交改动 (`git commit -m '添加一些特性'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

本项目基于 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 作者

- zhanghanlin - zhanghanlinhs@163.com