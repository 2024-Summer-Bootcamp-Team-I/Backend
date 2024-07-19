import os
from google.cloud import language_v1
from google.oauth2 import service_account
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

# .env 파일의 환경 변수를 로드합니다.
load_dotenv()

def create_client():
    # 서비스 계정 키 파일 경로를 환경 변수에서 가져옵니다.
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    )
    client = language_v1.LanguageServiceClient(credentials=credentials)
    return client

def analyze_sentiment(text):
    client = create_client()
    try:
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
        return sentiment.score, sentiment.magnitude
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return None, None




def recommend_similar_articles(article_index, articles, top_n=5):
    contents = [article.content for article in articles]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(contents)
    cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

    similarity_scores = list(enumerate(cosine_similarities[article_index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similar_articles = similarity_scores[1:top_n + 1]

    recommendations = [(articles[i], score) for i, score in similar_articles]
    
    return recommendations
