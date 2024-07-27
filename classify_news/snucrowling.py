from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from save_txt import init_news_content_text, save_news_as_text

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(5)

wait = WebDriverWait(driver, 20) 


driver.get("https://factcheck.snu.ac.kr/facts/show?id=5390")

#판별결과
el = driver.find_element(By.CSS_SELECTOR, 'div.jsx-1319828163.fact-dial-label-text')

#기사 제목
article_title = driver.find_element(By.CSS_SELECTOR, 'div.jsx-1319828163.score_check_articles-container')

#팩트체크 요약
summary_elements = driver.find_elements(By.CSS_SELECTOR, 'div.jsx-1319828163.fact-check-summary-body ul li')
summary_text = "\n".join([element.text for element in summary_elements])


init_news_content_text()
save_news_as_text(article_title.text, el.text, summary_text)

driver.quit()