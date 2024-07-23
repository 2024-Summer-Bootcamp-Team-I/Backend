#!/bin/bash

# Navigate to the deployment directory
cd /home/ubuntu/Backend || exit

# Pull latest changes from Git
git pull origin main

# Load Docker image and run container
docker load -i myapp.tar
docker stop myapp-container || true
docker rm myapp-container || true
docker run -d --name myapp-container -p 80:80 myapp:latest
