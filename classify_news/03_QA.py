import dotenv
import os
import openai
from langchain_community.chat_models.openai import ChatOpenAI
from opensearchpy import OpenSearch
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

dotenv.load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.environ.get("OPENAI_API_KEY")

# LangChain의 OpenAI LLM 설정
llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai.api_key)

# 프롬프트 템플릿 설정
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="주어진 Context를 보고 답변해주세요. 질문과 관계없는 내용은 포함하지 마세요.\n\nContext: {context}\n\nQuestion: {question}"
)

# LLMChain 설정
llm_chain = LLMChain(llm=llm, prompt=prompt_template)

client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    http_auth=("admin", "A769778aa!"),
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)

# 인덱스 이름 설정 (소문자로)
index_name = 'langchain_rag_test'


# 질문을 통해 OpenSearch에서 문서 검색
def search_documents(query):
    search_body = {
        "query": {
            "match": {
                "content": query
            }
        }
    }
    response = client.search(index=index_name, body={"query": {"match_all": {}}})
    hits = response['hits']['hits']
    return [hit['_source']['text'] for hit in hits]


# 메인 로직
if __name__ == "__main__":
    user_question = "가장 최신 기사 알려줘"

    # OpenSearch에서 관련 문서 검색
    search_results = search_documents(user_question)

    # 검색된 문서를 하나의 컨텍스트로 합침
    context = " ".join(search_results)

    # LLMChain 실행 및 응답 받기
    response = llm_chain.invoke({"context": context, "question": user_question})

    print("Answer:", response["text"])