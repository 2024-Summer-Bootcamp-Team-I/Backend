#!/bin/bash

set -e  # Exit on error

echo "Navigating to the deployment directory..."
cd /home/ubuntu/Backend || exit

echo "Pulling latest changes from Git..."
git pull origin main

echo "Loading Docker image..."
docker load -i fake_news.tar

echo "Stopping existing Docker container..."
docker stop fake_news-container || true

echo "Removing existing Docker container..."
docker rm fake_news-container || true

echo "Running new Docker container..."
docker run -d --name fake_news-container -p 80:80 fake_news:latest

echo "Deployment complete!"
