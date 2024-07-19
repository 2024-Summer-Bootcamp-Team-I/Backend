import os
from datetime import datetime
import dotenv
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import OpenSearchVectorSearch
from opensearchpy import OpenSearch
from langchain_community.document_loaders import DirectoryLoader
import torch
from transformers import AutoTokenizer, AutoModel
import nltk

# NLTK 데이터 다운로드
nltk.download('averaged_perceptron_tagger')

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

# OpenSearch 클라이언트를 초기화
opensearch_client = OpenSearch(
    hosts=[opensearch_url],
    http_auth=opensearch_auth,
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False
)

class MyEmbeddingModel:
    def __init__(self, model_name):
        # tokenizer와 모델 초기화
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def embed_documents(self, doc):
        # 문서를 임베딩하는 로직 구현
        inputs = self.tokenizer(doc, padding=True, truncation=True, return_tensors="pt", max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
            # 문서의 임베딩을 얻기 위해 마지막 hidden state의 평균을 사용
            embeddings = outputs.last_hidden_state.mean(dim=1).tolist()
        return embeddings

    def embed_query(self, text):
        # 쿼리를 임베딩하는 로직 구현
        inputs = self.tokenizer([text], padding=True, truncation=True, return_tensors="pt", max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
            # 쿼리의 임베딩을 얻기 위해 마지막 hidden state의 평균을 사용
            embedding = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()
        return embedding

# 인덱스 구조 설정
index_body = {
    "settings": {
        "analysis": {
            "tokenizer": {
                "nori_user_dict": {
                    "type": "nori_tokenizer",
                    "decompound_mode": "mixed",
                    "user_dictionary": "user_dic.txt"
                }
            },
            "analyzer": {
                "korean_analyzer": {
                    "filter": [
                        "synonym", "lowercase"
                    ],
                    "tokenizer": "nori_user_dict"
                }
            },
            "filter": {
                "synonym": {
                    "type": "synonym_graph",
                    "synonyms_path": "synonyms.txt"
                }
            }
        }
    }
}

# metadata 추출 및 부여 sys
def create_metadata(docs):
    # add a custom metadata field, such as timestamp
    for idx, doc in enumerate(docs):
        doc.metadata["category"] = ""
        doc.metadata["path"] = "classify_news/news_data.txt"

embed_model_name = "BM-K/KoSimCSE-roberta-multitask"

# metadata 만들기
path = "C:/TecheerSummerBootcamp2024/Backend/classify_news"
loader = DirectoryLoader(path, glob="**/*.txt", show_progress=True)
docs = loader.load()
create_metadata(docs)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=0,
    separators=["\n\n", "\n", "."],
    length_function=len,
)

documents = text_splitter.split_documents(docs)
print(documents)

index_name = 'langchain_rag_test'

# MyEmbeddingModel의 인스턴스를 생성
my_embedding = MyEmbeddingModel(embed_model_name)

vector_db = OpenSearchVectorSearch.from_documents(
    index_name=index_name,
    body=index_body,
    documents=documents,
    embedding=my_embedding,
    opensearch_url=opensearch_url,
    http_auth=opensearch_auth,
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
    bulk_size=1000000,
    timeout=360000
)

vector_db.add_documents(documents, bulk_size=1000000)