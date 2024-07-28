import dotenv
import os
import openai
from langchain_community.chat_models.openai import ChatOpenAI
from opensearchpy import OpenSearch
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from .models import ClassifyNews
from news.models import News


def c_news_classify(news_id):
    news = News.objects.get(news_id = news_id)
    title = news.title

    dotenv.load_dotenv()
    # OpenAI API 키 설정
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    # LangChain의 OpenAI LLM 설정
    llm = ChatOpenAI(model_name="gpt-4", openai_api_key=openai.api_key)
    # 프롬프트 템플릿 설정
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="주어진 Context를 보고 답변해주세요. 질문과 관계없는 내용은 포함하지 마세요.\n\nContext: {context}\n\nQuestion: {question}"
    )
    # LLMChain 설정
    llm_chain = LLMChain(llm=llm, prompt=prompt_template)

    dotenv.load_dotenv()

    # 환경 변수에서 값 가져오기
    opensearch_id = os.environ.get("OPENSEARCH_ID")
    opensearch_password = os.environ.get("OPENSEARCH_PASSWORD")
    opensearch_url = os.environ.get("OPENSEARCH_URL")

    # 인증 정보 설정
    opensearch_auth = (opensearch_id, opensearch_password)

    # 인증 정보가 올바르게 설정되었는지 확인
    if None in opensearch_auth or None in (opensearch_id, opensearch_password, opensearch_url):
        raise ValueError("OpenSearch 인증 정보가 설정되지 않았습니다.")

    index_name = 'duck'

    # OpenSearch 클라이언트를 초기화
    opensearch_client = OpenSearch(
        hosts=[opensearch_url],
        http_auth=opensearch_auth,
        use_ssl=True,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False
    )
    
    # 인덱스 이름 설정 (소문자로)
    index_name = 'jihye'
    # 질문을 통해 OpenSearch에서 문서 검색
    

    def search_documents(query):
        search_body = {
            "query": {
                "match": {
                    "text": query
                }
            }
        }
        response = client.search(index=index_name, body=search_body)
        hits = response['hits']['hits']
        return [hit['_source']['text'] for hit in hits]
    
    user_question = (f"'{title}'인 기사에 대해"
                "신뢰도점수를 0~100점 사이로 판별할 것입니다."
                "뉴스판별결과에 따라 점수범위를 정할 것이고,"
                "판별 결과가 '전혀 사실 아님'은 0~20 사이의 점수 ,'대체로 사실 아님'은 21~40 사이의 점수, '절반의 사실'은 41~60 사이의 점수, '대체로 사실'은 61~80 사이의 점수, '사실'은 81~100사이의 점수에서"
                "특정 점수를 결정할 것이고, 범위 내 정확한 점수는 판단근거 요약으로 결정할 것입니다."
                "판단근거 요약이 신뢰할만 하다면 범위내 높은점수를, 신뢰할만하지 않다면 범위내 낮은 점수를 부여해주세요"
                "판단근거 요약 중에 국가기관명이나 연구소가 연구한 결과값이 있다면 좀 더 높은 점수를 부여해주세요"
                "해당 뉴스에 대한 신뢰도점수가 몇점인지 결정해주세요."+\
                "점수는 3자리에 맞춰서 내주세요. 예를 들어 12점이면 012점으로!, "+\
                "형식은 '~점, {판단근거요약을 활용한 점수 결정 근거' 입니다"+\
                "~점으로 시작하는 형식을 따라줘, 다른 문장은 넣지 말아줘")

        # OpenSearch에서 관련 문서 검색
    search_results = search_documents(user_question)
        # 검색된 문서를 하나의 컨텍스트로 합침
    context = " ".join(search_results)
        # LLMChain 실행 및 응답 받기
    response = llm_chain.invoke({"context": context, "question": user_question})

        
    score =  int(response["text"][0:3])
    reason =  response["text"][6:]

    ClassifyNews.objects.create(
            news_id = news,
            score = score,
            reason = reason
    )
