#!/usr/bin/env bash
# Garante que o gunicorn escute na porta do Render
python -m gunicorn commerce.wsgi:application --bind 0.0.0.0:${PORT:-8000}
