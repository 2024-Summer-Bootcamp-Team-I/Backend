import os
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
        file.write("{뉴스제목:"+title+",점수:"+score+",판단근거요약:"+summary+"}\n")
    return file_path
