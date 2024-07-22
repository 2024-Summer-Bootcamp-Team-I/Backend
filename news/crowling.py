from bs4 import BeautifulSoup
import requests
from .models import News
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration
import os
from .news_embedding import news_embedding

def get_channel_id(channel_name):
    response = requests.post('http://127.0.0.1:8000/api/v1/channels/', json={'name':channel_name})    
    if response.status_code in [200, 201]:
        data = response.json()
        if 'id' in data:
            return data['id']
    raise ValueError("Channel ID not found") 

def init_news_content_text():
    directory = os.path.dirname(__file__)
    
    file_path = os.path.join(directory, "news_content.txt")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("")
    return file_path

def save_news_as_text(content, news_id):
    directory = os.path.dirname(__file__)
    
    file_path = os.path.join(directory, "news_content.txt")
    with open(file_path, "a", encoding="utf-8") as file:
        file.write("♣id:"+str(news_id).zfill(5)+",content:")
        file.write(content+"\n")
    return file_path

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
        )
        news.save()
        save_news_as_text(body.text.strip(), news.news_id)
        return news


def crawl_all_news(url):
    list_html = requests.get(url).text
    soup = BeautifulSoup(list_html, 'html.parser')
    news_links = soup.find_all('a', class_="sa_text_title")
    init_news_content_text()
    for news_link in news_links:
        try:
            news=crawl_news(news_link.get('href'))
            if news:
                print("news있음")
                summarize = summarizer(news.content)
                news.summarize = summarize
                news.save()
                print("요약저장완료")
        except Exception as e:
            print(f"Error processing {news_link.get('href')}: {e}")
    news_embedding()
    

tokenizer = PreTrainedTokenizerFast.from_pretrained('digit82/kobart-summarization')
model = BartForConditionalGeneration.from_pretrained('digit82/kobart-summarization')

def summarizer(text):
    text = text.replace('\n', ' ')

    raw_input_ids = tokenizer.encode(text, return_tensors="pt")
    input_ids = raw_input_ids[0]

    summary_ids = model.generate(input_ids.unsqueeze(0), num_beams=4, max_length=512, eos_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(summary_ids.squeeze().tolist(), skip_special_tokens=True)