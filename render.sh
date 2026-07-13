#!/usr/bin/env bash
# Render (or preview) the MINTverse documentation site.
#
#   ./render.sh                 # build into _book/
#   ./render.sh --preview       # live-reloading local preview
#   ./render.sh index.qmd       # render a single file
#
# Code cells execute at render time. Results are cached in _freeze/; delete it
# to force a cold render.
set -euo pipefail
cd "$(dirname "$0")"

# Use the project venv rather than whatever python is on PATH.
if [[ -x .venv/bin/python ]]; then
  export QUARTO_PYTHON="$PWD/.venv/bin/python"
fi

# Quarto captures stderr as cell output; keep Hub progress bars out of the pages.
export HF_HUB_DISABLE_PROGRESS_BARS=1
export TQDM_DISABLE=1

if [[ "${1:-}" == "--preview" ]]; then
  shift
  exec quarto preview "$@"
fi

exec quarto render "$@"
