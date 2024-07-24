from bs4 import BeautifulSoup
import requests

from news.models import News


# --- SNU 내 뉴스 기사 크롤링 함수 ---
def get_channel_id(channel_name):
    response = requests.post('http://127.0.0.1:8000/api/v1/channels/', json={'name':channel_name})    
    if response.status_code in [200, 201]:
        data = response.json()
        if 'id' in data:
            return data['id']
    raise ValueError("Channel ID not found") 

def crawl_news(url):
    news_html = requests.get(url).text
    soup = BeautifulSoup(news_html, 'html.parser')
    
    channel = soup.find('img', class_="media_end_head_top_logo_img light_type _LAZY_LOADING _LAZY_LOADING_INIT_HIDE")
    title = soup.find('h2', class_="media_end_head_headline")
    body = soup.find('div', class_="newsct_article _article_body")
    published_date = soup.find('span', class_="media_end_head_info_datestamp_time _ARTICLE_DATE_TIME")
    channel_name = channel.get('alt')
    channel_id = get_channel_id(channel_name)
    img = soup.find('img', id='img1', class_="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE")
    img_src = None
    if img is not None:
        img_src = img.get('data-src')
        
    if News.objects.filter(title=title.text.strip()).exists():
        print("있는 기사임")
        return
    else:
        news = News(
            channel_id = channel_id,
            title = title.text.strip(),
            content = body.text.strip(),
            published_date=published_date.get('data-date-time'),
            img = img_src,
            url = url,
            type = 'c'
        )
        news.save()
        
        return news
    






