#!/usr/bin/env bash

# Install uv and use it to install the project dependencies on Render.
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
make install

