import streamlit as st
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import feedparser
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Access the variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")



# Function to search for relevant links using Google Search API
def search_google(query, api_key, cse_id):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id).execute()
    return res['items'][:3] if 'items' in res else []

# Function to fetch news from the Chelyabinsk State University website
def fetch_news(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # selector based on actual HTML structure
    news_elements = soup.select('.csu_news-feed .csu_news-feed1')  # Example: '.headline'
    news_headlines = [element.get_text(strip=True) for element in news_elements]
    return news_headlines
   
    # news_headlines = []
    # for item in soup.find_all('h3', class_='news-title'):
    #     title = item.get_text()
    #     news_headlines.append(title)
    
    #return news_headlines[:3]  # Limit to three headlines


# Streamlit Interface
def main():
    st.title("Chelyabinsk State University Info Service")

    # # API Keys
    # google_api_key = st.text_input("Enter your Google API Key:", "")
    # google_cse_id = st.text_input("Enter your CSE ID:", "")

    query = st.text_input("Enter your query about Chelyabinsk State University:")

    if st.button("Search"):
        if query and GOOGLE_API_KEY and GOOGLE_CSE_ID:
            # Search for relevant links
            relevant_links = search_google(query, GOOGLE_API_KEY, GOOGLE_CSE_ID)
            st.subheader("Relevant Links:")
            for link in relevant_links:
                st.write(f"[{link['title']}]({link['link']})")

            # Fetch news from the Chelyabinsk State University website
            university_news_url = 'https://www.csu.ru'
            news_headlines = fetch_news(university_news_url)
            st.subheader("Recent News Headlines:")
            for headline in news_headlines:
                st.write("-", headline)


        else:
            st.write("No recent news found.")


if __name__ == "__main__":
    main()