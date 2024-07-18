from google.cloud import language_v1
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


client = language_v1.LanguageServiceClient()

def analyze_sentiment(text):
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
