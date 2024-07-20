from opensearchpy import OpenSearch
from sklearn.metrics.pairwise import cosine_similarity
import torch


client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    http_auth=("admin", "A769778aa!"),
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)

index_name = 'langchain_rag_test'


def calc_similarity(vector1, vector2):
    vector1 = torch.tensor([vector1])
    vector2 = torch.tensor([vector2])
    similarity = cosine_similarity(vector1, vector2)
    return similarity[0][0]


def get_vector_by_news_id(news_id):
    search_body = {
        "query": {
            "match_all": {}
        }
    }
    response = client.search(index=index_name, body=search_body)
    hit = response['hits']['hits'][news_id-1]
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
    for index, hit in enumerate(hits):
        db_news_vector = hit['_source']['vector_field']
        similarity = calc_similarity(db_news_vector, target_news_vector)
        if similarity >= 0.78:
            similar_news_ids.append(index+1)
    return similar_news_ids

