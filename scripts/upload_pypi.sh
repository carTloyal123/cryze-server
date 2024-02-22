#!/bin/bash
# Get the directory of the script
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
project_dir=$script_dir/..
echo "Script directory: $script_dir"
echo "Project directory: $project_dir"

# Remove old builds if any
rm -rf dist build cryze_server.egg-info

# increment version
toml_file=$project_dir/pyproject.toml
echo "TOML file: $toml_file"
current_version=$(cat $toml_file | grep "version" | sed -r s,"^.*=",,)
echo "Current version: $current_version"

# bump version
bump2version --allow-dirty --current-version $current_version patch $toml_file

echo "Building Package"
# Build the package
python setup.py sdist bdist_wheel

echo "Uploading to PyPi"
# Upload to PyPi
twine upload dist/*