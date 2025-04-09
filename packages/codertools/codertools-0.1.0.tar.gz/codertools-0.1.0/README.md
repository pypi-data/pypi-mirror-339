# coderTools
code 工具


## 常规操作

### 导出环境
```
uv export --format requirements-txt > requirements.txt
```

### 更新文档
```
mkdocs serve # 预览
mkdocs gh-deploy # 同步到github网站
```

### 运行测试并同步到测试服务
pip install pytest-html
```
uv run pytest --html=/Users/zhaoxuefeng/GitHub/aiworker/html/codetools.html
```

pip install twine
pip install setuptools wheel

python setup.py sdist bdist_wheel
twine upload dist/*

