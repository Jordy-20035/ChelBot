# import requests
# from bs4 import BeautifulSoup

# def fetch_news(url):
#     response = requests.get(url)
#     response.encoding = 'utf-8'
#     soup = BeautifulSoup(response.text, 'html.parser')
#     news_elements = soup.select('.ms-wpContentDivSpace')  
#     news_headlines = [element.get_text(strip=True) for element in news_elements]
#     return news_headlines

# url = 'https://www.csu.ru/news'
# headlines = fetch_news(url)
# print(headlines)



import requests
from bs4 import BeautifulSoup

def fetch_news_items(url):
    response = requests.get(url)
    response.encoding = 'utf-8'  # Ensure proper encoding
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table rows within the specific parent with class 'ms-wpContentDivSpace'
    rows = soup.select('.ms-wpContentDivSpace tr')  # Grab all rows from the parent table

    items = []  # This will store extracted news items

    for row in rows:
        # Find the columns in the current row; we will treat them as table cells
        columns = row.find_all('td')
        
        # Check to ensure that there's enough columns to extract the needed data
        if len(columns) > 8:
            news_item = {}
            # Column with date
            date_column = columns[1].get_text(strip=True) if len(columns) > 1 else None
            title_element = columns[8].find('a')  # Assuming title is in the 9th column
            
            # Filter to only include rows with both date and title found
            if date_column and title_element:
                news_item['date'] = date_column
                news_item['title'] = title_element.get_text(strip=True)
                news_item['link'] = title_element['href']  # Extract the hyperlink
                items.append(news_item)

    return items

# Replace with the actual URL you're scraping
url = 'https://www.csu.ru/news'  
news_items = fetch_news_items(url)

# Assuming you want to print results in a structured format
for item in news_items:
    print(f"Date: {item.get('date')}, Title: {item.get('title')}, Link: {item.get('link')}")