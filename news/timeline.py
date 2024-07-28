from opensearchpy import OpenSearch
from sklearn.metrics.pairwise import cosine_similarity
import torch
import dotenv
import os


dotenv.load_dotenv()

# 환경 변수에서 값 가져오기
opensearch_id = os.environ.get("OPENSEARCH_ID")
opensearch_password = os.environ.get("OPENSEARCH_PASSWORD")
opensearch_url = os.environ.get("OPENSEARCH_URL")

# 인증 정보 설정
opensearch_auth = (opensearch_id, opensearch_password)

index_name = 'duck'

# OpenSearch 클라이언트를 초기화
client = OpenSearch(
    hosts=[opensearch_url],
    http_auth=opensearch_auth,
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False
)


def calc_similarity(vector1, vector2):
    vector1 = torch.tensor([vector1])
    vector2 = torch.tensor([vector2])
    similarity = cosine_similarity(vector1, vector2)
    return similarity[0][0]


def get_vector_by_news_id(news_id):
    search_body = {
        "query": {
            "match": {
                "text": "id:" + str(news_id).zfill(5)
            }
        }
    }
    response = client.search(index=index_name, body=search_body)
    hit = response['hits']['hits'][0]
    return hit['_source']['vector_field']


def get_similar_news_ids(news_id):
    similar_news_ids = []
    query = {
        "query": {
            "match_all": {}
        }
    }
    response = client.search(index=index_name, body=query)
    target_news_vector = get_vector_by_news_id(news_id)
    hits = response['hits']['hits']
    for hit in hits:
        db_news_vector = hit['_source']['vector_field']
        db_news_id = hit['_source']['text'][4:9]
        similarity = calc_similarity(db_news_vector, target_news_vector)
        if similarity >= 0.78:
            similar_news_ids.append(int(db_news_id))
    return similar_news_ids

