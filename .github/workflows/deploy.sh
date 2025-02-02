#!/bin/bash

set -e  # Exit on error

echo "백엔드 폴더로 이동"
cd /home/ubuntu/Backend || { echo "Failed to cd to /home/ubuntu/Backend"; exit 1; }

echo "Git에서 최신 변경 사항을 가져오기"
git pull origin develop || { echo "Failed to pull from Git"; exit 1; }

echo "Docker 이미지를 가져오기"
docker pull dlaehddus18/fake_news:v1|| { echo "Failed to pull Docker images"; exit 1; }

echo "이전 도커 내리기"
docker-compose down || { echo "Failed to bring down Docker containers"; exit 1; }

echo "DB 권한, 소유권 변경"
sudo chmod -R 755 /home/ubuntu/Backend/data/db || { echo "Failed to change permissions"; exit 1; }
sudo chown -R ubuntu:ubuntu /home/ubuntu/Backend/data/db || { echo "Failed to change ownership"; exit 1; }
sudo chmod 755 /etc/letsencrypt /etc/letsencrypt/archive /etc/letsencrypt/live
sudo chown root:root /etc/letsencrypt /etc/letsencrypt/archive /etc/letsencrypt/live
sudo chmod 644 /etc/letsencrypt/archive/fakenew.site/*.pem
sudo chown root:root /etc/letsencrypt/archive/fakenew.site/*.pem
sudo chmod 644 /etc/letsencrypt/archive/fakenew.site/*.pem
sudo chown root:root /etc/letsencrypt/archive/fakenew.site/*.pem



echo "가져온 이미지 도커에 올리기"
docker-compose up -d || { echo "Failed to bring up Docker containers"; exit 1; }

sudo tail -f /var/log/nginx/error.log

echo "컨테이너 상태 확인"
docker ps || { echo "Failed to list running Docker containers"; exit 1; }

echo "배포완료~~"