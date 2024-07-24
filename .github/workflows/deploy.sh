#!/bin/bash

set -e  # Exit on error

echo "Navigating to the deployment directory..."
cd /home/ubuntu/Backend || exit

echo "Pulling latest changes from Git..."
git pull origin develop

echo "Pulling the latest Docker image..."
docker-compose pull

echo "Stopping and removing existing Docker containers..."
docker-compose down

echo "Starting new Docker containers..."
docker-compose up -d

echo "Deployment complete!"
