#!/bin/bash
# Run inside the GitHub Codespace terminal: bash run_containers.sh
set -e
docker network create superkart-net || true

docker build -t superkart-backend ./backend_files
docker build -t superkart-frontend ./frontend_files

docker rm -f superkart-backend superkart-frontend 2>/dev/null || true
docker run -d --name superkart-backend --network superkart-net -p 7860:7860 superkart-backend
docker run -d --name superkart-frontend --network superkart-net -p 8501:8501 \
  -e BACKEND_URL=http://superkart-backend:7860 superkart-frontend

docker ps
