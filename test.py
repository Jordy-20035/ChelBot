import requests
from bs4 import BeautifulSoup

def fetch_news(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    news_elements = soup.select('.item .news_content')  
    news_headlines = [element.get_text(strip=True) for element in news_elements]
    return news_headlines

url = 'https://iit.csu.ru/news'
headlines = fetch_news(url)
print(headlines)