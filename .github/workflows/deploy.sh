#!/bin/bash

set -e  # Exit on error

echo "백엔드 폴더로 이동"
cd /home/ubuntu/Backend || exit

echo "Git에서 최신 변경 사항을 가져오기 완료"
git pull origin develop

echo "Docker 이미지를 가져오기"
docker-compose pull

echo "이전 도커 내리기"
docker-compose down

echo "DB 권한, 소유권 변경"

sudo chmod -R 755 /home/ubuntu/Backend/data/db(디렉토리 권한 변경)
sudo chown -R ubuntu:ubuntu /home/ubuntu/Backend/data/db(디렉토리 소유권 변경)

echo "가져온 이미지 도커에 올리기"
docker-compose up -d

echo "배포완료~~"