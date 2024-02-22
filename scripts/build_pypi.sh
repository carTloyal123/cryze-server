#!/bin/bash
# Get the directory of the script
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
project_dir=$script_dir/..
echo "Script directory: $script_dir"
echo "Project directory: $project_dir"

# Remove old builds if any
rm -rf dist build cryze_server.egg-info

# Build the package
python setup.py sdist bdist_wheel