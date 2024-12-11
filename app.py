import streamlit as st
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

# Load .env variables
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
    news_elements = soup.select('.csu_news-feed .csu_news-feed1')  # Adjust this based on the actual structure
    news_headlines = [element.get_text(strip=True) for element in news_elements]
    return news_headlines

# Streamlit Interface
def main():
    # Page setup
    st.set_page_config(page_title="CSU Info Service", layout="wide")  # Set page title and layout
    st.title("Chelyabinsk State University Info Service")
    

    st.markdown("<h5 style='text-align: center;'>Your one-stop information resource for Chelyabinsk State University</h5>", unsafe_allow_html=True)

    query = st.text_input("Enter your query about Chelyabinsk State University:", "")

    if st.button("Search"):
        if query and GOOGLE_API_KEY and GOOGLE_CSE_ID:
            with st.spinner("Fetching results..."):  # Show spinner while fetching data
                relevant_links = search_google(query, GOOGLE_API_KEY, GOOGLE_CSE_ID)
                st.subheader("Relevant Links:")
                
                # Display relevant links in a visually appealing way
                if relevant_links:
                    for link in relevant_links:
                        st.markdown(f"- **[{link['title']}]({link['link']})**")
                else:
                    st.write("No relevant links found.")

                # Fetch and display news headlines
                university_news_url = 'https://www.csu.ru'
                news_headlines = fetch_news(university_news_url)
                
                st.subheader("Recent News Headlines:")
                if news_headlines:
                    for headline in news_headlines:
                        st.write(f"- {headline}")
                else:
                    st.write("No recent news found.")

        else:
            st.warning("Please enter a query and ensure API keys are set.")

if __name__ == "__main__":
    main()