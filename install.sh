#!/bin/bash

apt update -y
apt install -y docker docker-compose ffmpeg git

systemctl start docker
systemctl enable docker

mkdir -p app/web/static app/data
cd app

cat > docker-compose.yml << EOF
version: "3"
services:
  web:
    image: tiangolo/uvicorn-gunicorn-fastapi:python3.10
    volumes:
      - ./web:/app
      - ./data:/data
    ports:
      - "80:80"
    command: >
      bash -c "
      pip install whisper ffmpeg-python python-multipart &&
      uvicorn main:app --host 0.0.0.0 --port 80
      "
EOF

docker-compose up -d
