FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /Backend

# 필요한 파일 복사
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
#RUN apt-get update && apt-get install -y libmagic1 libmagic-dev

# 소스 코드 복사
COPY . .

# Google Cloud 서비스 계정 JSON 파일 복사
COPY service-account-file.json service-account-file.json

# 환경 변수 설정
ENV GOOGLE_APPLICATION_CREDENTIALS=service-account-file.json

# 프로젝트 실행 명령어
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]