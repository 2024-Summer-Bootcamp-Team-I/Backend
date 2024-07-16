import openai
import dotenv
import os

dotenv.load_dotenv()


# OpenAI API 키 설정
openai.api_key = os.environ.get("OPENAI_API_KEY")

# GPT-4 모델에 요청 보내기
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how can I use GPT API with Python? in korean"}
    ],
    max_tokens=350,  # 응답에서 생성할 최대 토큰 수
    temperature=0.1  # 텍스트 생성의 창의성 수준
)

# 응답 출력
print(response['choices'][0]['message']['content'].strip())
