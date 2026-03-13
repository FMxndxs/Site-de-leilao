#!/usr/bin/env bash
# Garante que o gunicorn escute na porta do Render
# --worker-tmp-dir /dev/shm: evita falha em filesystem read-only do Render
# --workers 1: startup mais rápido para o health check
python -m gunicorn commerce.wsgi:application \
  --bind 0.0.0.0:${PORT:-10000} \
  --workers 1 \
  --worker-tmp-dir /dev/shm \
  --timeout 120
