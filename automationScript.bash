#!/usr/bin/env bash
# Run the Dash app test suite via the project virtual environment.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_ACTIVATE="${SCRIPT_DIR}/quantum/Scripts/activate"
VENV_ACTIVATE_POSIX="${SCRIPT_DIR}/quantum/bin/activate"

# Activate virtual environment (Windows Git Bash or POSIX)
if [[ -f "${VENV_ACTIVATE}" ]]; then
  # shellcheck source=/dev/null
  source "${VENV_ACTIVATE}"
elif [[ -f "${VENV_ACTIVATE_POSIX}" ]]; then
  # shellcheck source=/dev/null
  source "${VENV_ACTIVATE_POSIX}"
else
  echo "Activate script not found at ${VENV_ACTIVATE} or ${VENV_ACTIVATE_POSIX}" >&2
  exit 1
fi

# Prefer the virtualenv's Python explicitly
if [[ -x "${SCRIPT_DIR}/quantum/Scripts/python.exe" ]]; then
  PY_BIN="${SCRIPT_DIR}/quantum/Scripts/python.exe"
elif [[ -x "${SCRIPT_DIR}/quantum/Scripts/python" ]]; then
  PY_BIN="${SCRIPT_DIR}/quantum/Scripts/python"
elif [[ -x "${SCRIPT_DIR}/quantum/bin/python" ]]; then
  PY_BIN="${SCRIPT_DIR}/quantum/bin/python"
else
  PY_BIN="$(command -v python || command -v python3 || command -v python.exe || true)"
fi

if [[ -z "${PY_BIN}" ]]; then
  echo "Python interpreter not found after activating the virtual environment." >&2
  exit 1
fi

cd "${SCRIPT_DIR}"
echo "Running tests with $(${PY_BIN} --version)"

if "${PY_BIN}" -m pytest -q; then
  echo "All tests passed."
  exit 0
else
  echo "Tests failed."
  exit 1
fi
