# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Databricks UI Components** library - a Python package for creating beautiful dashboards and interactive visualizations in Databricks notebooks and Python environments. The library provides UI components optimized for Databricks' `displayHTML` function.

## Development Commands

### Setup Development Environment
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies with dev extras
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Common Development Tasks
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=db_ui_components --cov-report=term-missing

# Run specific test file
pytest tests/test_chart_component.py

# Run tests with verbose output
pytest -v

# Code formatting (must run before committing)
black db_ui_components/ tests/

# Linting
flake8 db_ui_components/ tests/

# Type checking
mypy db_ui_components/

# Build package
python -m build
```

## Architecture

### Component Hierarchy
1. **BaseComponent** (base_component.py) - Abstract base class for all components
   - Handles HTML generation, CSS styling, JavaScript integration
   - Provides common methods: `render()`, `get_html()`, `get_css()`, `get_js()`

2. **Core Components**:
   - **ChartComponent** - Interactive charts using Plotly (line, bar, pie, scatter, etc.)
   - **TableComponent** - Data tables with search, sort, pagination, CSV download
   - **FilterComponent** - Dynamic filters for data manipulation
   - **Dashboard** - Container for organizing multiple components

3. **Advanced Visualizations** (in `visualization/` directory):
   - SankeyChart, Heatmap, NetworkGraph, TreeMap, BubbleChart
   - Each extends BaseComponent with specialized rendering

4. **Database Integration**:
   - **DatabaseComponent** - Generic database operations
   - **DatabricksDatabase** - Databricks-specific features (SQL, PySpark integration)

### Key Design Patterns
- **Fluent Interface**: Components support method chaining for configuration
- **Template-Based Rendering**: Uses Jinja2 templates for HTML generation
- **Event System**: JavaScript event handling for interactivity
- **Responsive Design**: All components adapt to container size

### Data Flow
1. User provides pandas DataFrame or database query
2. Component processes data and generates configuration
3. Jinja2 renders HTML template with embedded CSS/JS
4. Output is displayed via Databricks' `displayHTML()`

## Important Conventions

### Code Style
- Follow PEP 8 with Black formatting (88 char line length)
- Use type hints for all public methods
- Docstrings in Google style for all public APIs
- No hardcoding - use configuration objects

### Testing
- Every new feature must have tests
- Test files mirror source structure in `tests/` directory
- Use pytest fixtures for common test data
- Aim for >80% code coverage

### Git Workflow
- Branch from `develop` for features: `feature/description`
- Branch from `develop` for fixes: `fix/description`
- All changes require PR with passing CI
- `main` branch is protected - no direct pushes
- Releases are created from `main` via GitHub releases

### CI/CD Pipeline

#### 現在の状態
- **On PR/Push**: Tests run on Python 3.10, 3.11, 3.12
- **develop branch**: Auto-deploys to TestPyPI
- **GitHub Release**: Auto-deploys to production PyPI
- All commits must pass: pytest, black, flake8, mypy

#### 重要なCIコマンド
```bash
# ローカルでCIと同じ環境でテストを実行
pip install -e .
pytest tests/ -v --cov=db_ui_components --cov-report=term-missing

# lintとフォーマットチェック
flake8 db_ui_components/ --extend-ignore=E501
black --check db_ui_components/
mypy db_ui_components/
```

#### リリースプロセス
1. developブランチで開発・テスト
2. PRを作成してmainブランチへマージ
3. GitHub Releaseを作成（タグ: v0.1.0形式）
4. 自動的にPyPIへ公開される

## Databricks-Specific Considerations

1. **displayHTML Compatibility**: All components must generate self-contained HTML
2. **No External Dependencies**: CSS/JS must be embedded, not linked
3. **DataFrame Integration**: Components should accept Spark DataFrames and convert to pandas
4. **Performance**: Consider large datasets - implement pagination/sampling where needed
5. **Security**: Sanitize all user inputs to prevent XSS in generated HTML

## Common Pitfalls to Avoid

1. Don't assume internet connectivity - embed all resources
2. Don't modify global Databricks notebook state
3. Always handle missing/null data gracefully
4. Test with both small and large datasets
5. Ensure components work in both notebooks and standalone Python

## Quick Component Creation Example

```python
from db_ui_components import ChartComponent, TableComponent, Dashboard
import pandas as pd

# Create sample data
df = pd.DataFrame({'x': range(10), 'y': [i**2 for i in range(10)]})

# Create components
chart = ChartComponent(data=df, chart_type='line', x_column='x', y_column='y')
table = TableComponent(data=df, page_size=5)

# Create dashboard
dashboard = Dashboard(title="My Dashboard")
dashboard.add_component(chart, width=8)
dashboard.add_component(table, width=4)

# Display in Databricks
displayHTML(dashboard.render())
```