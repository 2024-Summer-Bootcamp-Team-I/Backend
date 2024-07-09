from bs4 import BeautifulSoup
import requests
from datetime import datetime
from .models import News

def crawl_news(url):
    news_html = requests.get(url).text
    soup = BeautifulSoup(news_html, 'html.parser')
    
    channel = soup.find('a', class_="media_end_head_top_logo_img light_type _LAZY_LOADING _LAZY_LOADING_INIT_HIDE")
    title = soup.find('h2', class_="media_end_head_headline")
    body = soup.find('div', class_="newsct_article _article_body")
    published_date = soup.find('span', class_="media_end_head_info_datestamp_time _ARTICLE_DATE_TIME")
    
    
    if title and body and published_date:
        news = News(
            channel_id = 1,
            title=title.text,
            content=body.text,
            published_date=published_date.get('data-date-time'),
            
        )
        news.save()
        return news
    else:
        raise ValueError("Missing data in the news")

def crawl_all_news(url):
    list_html = requests.get(url).text
    soup = BeautifulSoup(list_html, 'html.parser')
    news_links = soup.find_all('a', class_="sa_text_title")
    
    for news_link in news_links:
        try:
            crawl_news(news_link.get('href'))
        except Exception as e:
            print(f"Error processing {news_link.get('href')}: {e}")
