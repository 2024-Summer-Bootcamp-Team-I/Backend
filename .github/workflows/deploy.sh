#!/bin/bash

set -e  # Exit on error

echo "Navigating to the deployment directory..."
cd /home/ubuntu/Backend || exit

echo "Pulling latest changes from Git..."
git pull origin main

echo "Loading Docker image..."
docker load -i myapp.tar

echo "Stopping existing Docker container..."
docker stop myapp-container || true

echo "Removing existing Docker container..."
docker rm myapp-container || true

echo "Running new Docker container..."
docker run -d --name myapp-container -p 80:80 myapp:latest

echo "Deployment complete!"
