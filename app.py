import streamlit as st
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
from streamlit_lottie import st_lottie  # Import the st_lottie function

# Load .env variables
load_dotenv()

# Access the variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

# Function to load Lottie animations
def load_lottie_url(url):
    try:
        r = requests.get(url)
        r.raise_for_status()  # Check for HTTP request errors
        return r.json()  # Returns the JSON data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")  # Print error for debugging
        return None

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
    news_elements = soup.select('.csu_news-feed .csu_news-feed1')  
    news_headlines = [element.get_text(strip=True) for element in news_elements]
    return news_headlines

# Streamlit Interface
def main():
    st.set_page_config(page_title="CSU Info Service", layout="wide")
    
    # Load a Lottie animation for the header
    lottie_header_url = "https://lottie.host/eac077c4-86e8-43b1-b41f-142af05db24d/SrwORZwZZV.json"  # Sample Lottie URL
    lottie_header = load_lottie_url(lottie_header_url)
    
    if lottie_header:  # Check if loading was successful
        st_lottie(lottie_header, height=200, key="header_animation")

    st.title("Chelyabinsk State University Info Service")
    st.markdown("<h5 style='text-align: center;'>Your one-stop information resource for Chelyabinsk State University</h5>", unsafe_allow_html=True)

    query = st.text_input("Enter your query about Chelyabinsk State University:", "")

    if st.button("Search"):
        if query and GOOGLE_API_KEY and GOOGLE_CSE_ID:
            with st.spinner("Fetching results..."):
                lottie_loading_url = "https://lottie.host/deb5e19c-2dab-4131-a3ba-ed4f79243e27/vcrPpJyhxG.json"  # Sample loading animation
                lottie_loading = load_lottie_url(lottie_loading_url)
                
                if lottie_loading:  # Check if loading was successful
                    st_lottie(lottie_loading, height=100, key="loading_animation")  # Show loading animation

                relevant_links = search_google(query, GOOGLE_API_KEY, GOOGLE_CSE_ID)
                st.subheader("Relevant Links:")

                # Load Lottie animation for results
                lottie_result_url = "https://lottie.host/d6a993ce-b6f4-46ef-8041-81fedb5fb9dc/nntHvms0Is.json"  # Example URL for result animation
                lottie_result = load_lottie_url(lottie_result_url)

                if relevant_links:
                    col1, col2 = st.columns([1, 1])  # Create two columns

                    # Show the relevant links in the first column
                    with col1:
                        for link in relevant_links:
                            st.markdown(f"- **[{link['title']}]({link['link']})**")

                    # Show the Lottie animation in the second column (right side)
                    with col2:
                        if lottie_result:  # Check if loading was successful
                            st_lottie(lottie_result, height=100)

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