from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import os

# --- txt 저장 함수 ---
def init_news_content_text():
    directory = os.path.dirname(__file__)
    
    file_path = os.path.join(directory, "snu_content.txt")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("")
    return file_path

def save_news_as_text(title, score, summary):
    directory = os.path.dirname(__file__)
    
    file_path = os.path.join(directory, "snu_content.txt")
    with open(file_path, "a", encoding="utf-8") as file:
        file.write("{뉴스제목:"+title+",판단결과:"+score+",판단근거요약:"+summary+"}\n")
    return file_path

def snu_crawl(snu_num):
    # --- snu 동적 크롤링 세팅 ---
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)  # 임시 대기 시간을 늘려서 안정성 확보
    wait = WebDriverWait(driver, 20) 


    url = f"https://factcheck.snu.ac.kr/facts/show?id={snu_num}"
    driver.get(url)
        
    try:
        # 판별결과
        el = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.jsx-1319828163.fact-dial-label-text')))

        # 기사 제목
        article_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.jsx-1319828163.score_check_articles-container')))

        # 팩트체크 요약
        summary_elements = driver.find_elements(By.CSS_SELECTOR, 'div.jsx-1319828163.fact-check-summary-body ul li')
        summary_text = "\n".join([element.text for element in summary_elements])

        # 파일에 저장
        save_news_as_text(article_title.text, el.text, summary_text)

    except Exception as e:
        print(f"Error occurred for ID {snu_num}: {e}")
        
    # 알림 처리
    try:
        alert = Alert(driver)
        alert.accept()  # 알림이 나타나면 수락
    except Exception:
        pass  # 알림이 없으면 그냥 넘어감

    driver.quit()