#!/bin/bash

# Remove old builds if any
rm -rf dist build cryze_server.egg-info

# increment version
bumpversion patch

# Build the package
python3 setup.py sdist bdist_wheel

# Upload to PyPi
twine upload dist/*