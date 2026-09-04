#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip install -r requirements-dev.txt
[[ -f .env ]] || cp .env.example .env
.venv/bin/python -m compileall -q app.py answer_bot.py core tests
.venv/bin/python -m pytest
printf '\nSetup complete. Run: .venv/bin/python -m streamlit run app.py\n'
