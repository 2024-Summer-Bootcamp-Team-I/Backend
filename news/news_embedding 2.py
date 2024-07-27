import os
import dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import OpenSearchVectorSearch
from opensearchpy import OpenSearch
from langchain_community.document_loaders import DirectoryLoader
import torch
from transformers import AutoTokenizer, AutoModel
import nltk

def news_embedding():
    # NLTK 데이터 다운로드
    nltk.download('averaged_perceptron_tagger')
    nltk.download('punkt')

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

    # metadata 만들기
    current_directory = os.path.dirname(__file__)
    path = os.path.join(current_directory)
    loader = DirectoryLoader(path, glob="**/*.txt", show_progress=True)
    docs = loader.load()
    # 메타데이터 넣을 필요 없다고 생각함. 그래서 지움
    #create_metadata(docs)


    embed_model_name = "BM-K/KoSimCSE-roberta-multitask"

    #이게 텍스트 자르는건데 청크사이즈 크게 만들고(취소 작게 하자.) 나누는 기준을 ♣로 하면 됨.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1,
        chunk_overlap=0,
        separators=["♣"],
        length_function=len,
    )

    documents = text_splitter.split_documents(docs)
    print(documents)



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



    #이거때문에 중복 데이터값 저장됨. 그래서 지움. 
    #vector_db.add_documents(documents, bulk_size=1000000)

    response = opensearch_client.count(index=index_name)
    print(f"Number of documents in '{index_name}': {response['count']}")

    # vector DB 초기화
    #response = opensearch_client.indices.delete(index=index_name, ignore=[400, 404])
