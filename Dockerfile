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

# 소스 코드 복사
COPY . .

# Gunicorn을 사용하여 Django 애플리케이션 실행
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "djangoIteam.wsgi:application"]
