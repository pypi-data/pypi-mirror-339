#!/bin/bash
set -e

echo "Building..."
uv build

echo "Publishing..."
uv publish -u $UV_PUBLISH_USERNAME -t $UV_PUBLISH_TOKEN