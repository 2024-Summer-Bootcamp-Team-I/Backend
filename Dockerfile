# Python 3.11 기반 이미지를 사용
FROM python:3.11-slim

# Python 환경 설정
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 작업 디렉토리 설정
WORKDIR /Backend

# 필요한 파일들을 복사
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update && \
    apt-get install -y \
    libmagic1 \
    libmagic-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 소스 코드 복사
COPY . .

#로컬에서 도커로 복사하는 코드여서 배포환경에선 오류남 로컬에서 도커올릴때만 사용
#COPY service-account-file.json service-account-file.json
#ENV GOOGLE_APPLICATION_CREDENTIALS=service-account-file.json

# Gunicorn을 사용하여 Django 애플리케이션 실행
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "djangoIteam.wsgi:application"]