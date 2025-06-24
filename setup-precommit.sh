#!/bin/bash
set -e

echo "[INFO] Switching to the root of the git repository..."
cd "$(git rev-parse --show-toplevel)"

if ! command -v python3.11 &>/dev/null; then
    echo "[ERROR] python3.11 is not installed or not in PATH."
    echo "        Please install it manually or via pyenv:"
    echo "        pyenv install 3.11.13 && pyenv global 3.11.13"
    exit 1
fi

if ! command -v pre-commit &>/dev/null; then
    echo "[INFO] pre-commit not found. Installing via pipx..."
    pipx install pre-commit
else
    echo "[INFO] pre-commit is already installed."
fi

echo "[INFO] Installing pre-commit hook..."
pre-commit install

echo "[INFO] Installing commit-msg hook..."
pre-commit install --hook-type commit-msg

echo "[INFO] Pre-installing all hook environments..."
pre-commit install-hooks

echo "[SUCCESS] pre-commit is fully set up and active."
