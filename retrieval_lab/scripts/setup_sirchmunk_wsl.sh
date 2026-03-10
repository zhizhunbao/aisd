#!/usr/bin/env bash
set -euo pipefail

ROOT="/mnt/c/Users/40270/OneDrive/Desktop/workspace/aisd"
WORK="$ROOT/retrieval_lab/data/search_data/sirchmunk/work"
BIN="$WORK/bin"
VENV="$WORK/.venv"
TMP_DIR="$(mktemp -d)"
UV_BIN="$HOME/.local/bin/uv"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

mkdir -p "$BIN"

RG_URL="https://github.com/BurntSushi/ripgrep/releases/download/15.1.0/ripgrep-15.1.0-x86_64-unknown-linux-musl.tar.gz"
RGA_URL="https://github.com/phiresky/ripgrep-all/releases/download/v0.10.10/ripgrep_all-v0.10.10-x86_64-unknown-linux-musl.tar.gz"

cd "$TMP_DIR"
curl -L "$RG_URL" -o rg.tar.gz
curl -L "$RGA_URL" -o rga.tar.gz

tar -xzf rg.tar.gz
cp "ripgrep-15.1.0-x86_64-unknown-linux-musl/rg" "$BIN/rg"
chmod +x "$BIN/rg"

tar -xzf rga.tar.gz
cp "ripgrep_all-v0.10.10-x86_64-unknown-linux-musl/rga" "$BIN/rga"
cp "ripgrep_all-v0.10.10-x86_64-unknown-linux-musl/rga-preproc" "$BIN/rga-preproc"
chmod +x "$BIN/rga" "$BIN/rga-preproc"

if [ ! -f "$VENV/bin/activate" ]; then
  rm -rf "$VENV"
  if [ ! -x "$UV_BIN" ]; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
  fi
  "$UV_BIN" venv "$VENV"
fi

"$UV_BIN" pip install --python "$VENV/bin/python" -e "$ROOT/.github/sirchmunk"

echo "Prepared Sirchmunk WSL environment"
echo "WORK=$WORK"
echo "BIN=$BIN"
echo "VENV=$VENV"
"$UV_BIN" --version
"$BIN/rg" --version
"$BIN/rga" --version
