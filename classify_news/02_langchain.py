import openai
import os
import dotenv
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


# OpenAI API 키 설정
openai.api_key1 = os.environ.get("OPENAI_API_KEY")
openai.api_key2 = os.environ.get("OPENAI_API_KEY")

# LangChain의 OpenAI LLM 설정
llm1 = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai.api_key1)
llm2 = ChatOpenAI(model_name="gpt-4", openai_api_key=openai.api_key2)

# 프롬프트 템플릿 설정
prompt_template = PromptTemplate(
    input_variables=["question"],
    template="You are a helpful assistant. Answer the following question: {question}"
)

# LLMChain 설정
llm_chain = LLMChain(llm=llm1, prompt=prompt_template)

# 질문 정의
question = "Hello, how can I use GPT API with Python? in korean"

# LLMChain 실행 및 응답 받기
response = llm_chain.run(question)
print(response)