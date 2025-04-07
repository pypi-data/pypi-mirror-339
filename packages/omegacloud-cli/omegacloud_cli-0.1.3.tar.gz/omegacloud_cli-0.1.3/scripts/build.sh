#!/bin/bash

rm -rf dist/
# uv pip freeze > requirements.txt
uv export --no-dev --no-hashes > requirements.txt
pip install -e .
python -m build
twine upload dist/*