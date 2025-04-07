# Development
## Development Install
```
git clone https://spacecruft.org/deepcrayon/ailabeler
cd ailabeler/
python -m venv venv
source venv/bin/activate
pip install -U setuptools pip wheel
pip install -e .
pip install -e .[dev]
```

## Formatting
```
black src/ailabeler/*.py src/ailabeler/lib/*.py
```

## Lint
```
ruff check src/
```

# Build for PyPI
```
pip install -e .[dev]
pip install --upgrade build
python3 -m build
```

# Upload to PyPI
Log into test.pypi.org and pypi.org. Create an API token.
Save token to with formatting to `$HOME/.pypirc`, such as:
```[testpypi]
  username = __token__
  password = pypi-foooooooooooooooooooooooooooooooooooooo
```

Test repo:
```
python3 -m twine upload --repository testpypi dist/*
```

Main repo:
```
python3 -m twine upload dist/*
```

# Release
Move needed files to `dist/` then upload to server.

Upload these files to https://spacecruft.org/deepcrayon/ailabeler/releases
```
ailabeler-VERSION-py3-none-any.whl
ailabeler-VERSION.tar.gz
