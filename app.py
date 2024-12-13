# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# from googleapiclient.discovery import build
# import os
# from dotenv import load_dotenv
# from streamlit_lottie import st_lottie  # Import the st_lottie function

# # Load .env variables
# load_dotenv()

# # Access the variables
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

# # Function to load Lottie animations
# def load_lottie_url(url):
#     try:
#         r = requests.get(url)
#         r.raise_for_status()  # Check for HTTP request errors
#         return r.json()  # Returns the JSON data
#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred: {e}")  # Print error for debugging
#         return None

# # Function to search for relevant links using Google Search API
# def search_google(query, api_key, cse_id):
#     service = build("customsearch", "v1", developerKey=api_key)
#     res = service.cse().list(q=query, cx=cse_id).execute()
#     return res['items'][:3] if 'items' in res else []

# # Function to fetch news from the Chelyabinsk State University website
# def fetch_news_items(url):
#     response = requests.get(url)
#     response.encoding = 'utf-8'  # Ensure proper encoding
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     # Find the table rows within the specific parent with class 'ms-wpContentDivSpace'
#     rows = soup.select('.ms-wpContentDivSpace tr')  # Grab all rows from the parent table

#     items = []  # This will store extracted news items

#     for row in rows:
#         # Find the columns in the current row; we will treat them as table cells
#         columns = row.find_all('td')
        
#         # Check to ensure that there's enough columns to extract the needed data
#         if len(columns) > 8:
#             news_item = {}
#             # Column with date
#             date_column = columns[1].get_text(strip=True) if len(columns) > 1 else None
#             title_element = columns[8].find('a')  # Assuming title is in the 9th column
            
#             # Filter to only include rows with both date and title found
#             if date_column and title_element:
#                 news_item['date'] = date_column
#                 news_item['title'] = title_element.get_text(strip=True)
#                 news_item['link'] = title_element['href']  # Extract the hyperlink
#                 items.append(news_item)

#     return items

# # Streamlit Interface
# def main():
#     st.set_page_config(page_title="CSU Info Service", layout="centered")
    
#     # Load a Lottie animation for the header
#     lottie_header_url = "https://lottie.host/eac077c4-86e8-43b1-b41f-142af05db24d/SrwORZwZZV.json"  # Sample Lottie URL
#     lottie_header = load_lottie_url(lottie_header_url)
    
#     if lottie_header:  # Check if loading was successful
#         st_lottie(lottie_header, height=200, key="header_animation")

#     st.title("Chelyabinsk State University Info Service")
#     st.markdown("<h5 style='text-align: center;'>Your one-stop information resource for Chelyabinsk State University</h5>", unsafe_allow_html=True)

#     query = st.text_input("Enter your query about Chelyabinsk State University:", "")

#     if st.button("Search"):
#         if query and GOOGLE_API_KEY and GOOGLE_CSE_ID:
#             with st.spinner("Fetching results..."):
#                 lottie_loading_url = "https://lottie.host/deb5e19c-2dab-4131-a3ba-ed4f79243e27/vcrPpJyhxG.json"  # Sample loading animation
#                 lottie_loading = load_lottie_url(lottie_loading_url)
                
#                 if lottie_loading:  # Check if loading was successful
#                     st_lottie(lottie_loading, height=100, key="loading_animation")  # Show loading animation

#                 relevant_links = search_google(query, GOOGLE_API_KEY, GOOGLE_CSE_ID)
#                 st.subheader("Relevant Links:")

#                 # Load Lottie animation for results
#                 lottie_result_url = "https://lottie.host/d6a993ce-b6f4-46ef-8041-81fedb5fb9dc/nntHvms0Is.json"  # Example URL for result animation
#                 lottie_result = load_lottie_url(lottie_result_url)

#                 if relevant_links:
#                     col1, col2 = st.columns([1, 1])  # Create two columns

#                     # Show the relevant links in the first column
#                     with col1:
#                         for link in relevant_links:
#                             st.markdown(f"- **[{link['title']}]({link['link']})**")

#                     # Show the Lottie animation in the second column (right side)
#                     with col2:
#                         if lottie_result:  # Check if loading was successful
#                             st_lottie(lottie_result, height=100)

#                 else:
#                     st.write("No relevant links found.")

#                 # Fetch and display news headlines
#                 url = 'https://www.csu.ru/news'
#                 news_items = fetch_news_items(url)
                
#                 st.subheader("Recent News Headlines:")
#                 # Show a maximum of 5 headlines with simple summaries
#                 for item in news_items[:5]:
#                     # Simple summarization by truncating titles (customize this as needed)
#                     summary = (item['title'][:50] + '...') if len(item['title']) > 50 else item['title']
#                     st.write(f"**Date:** {item['date']}")
#                     st.write(f"**Title:** {summary} [Read More]({item['link']})")

#         else:
#             st.warning("Please enter a query and ensure API keys are set.")

#         print(news_items)

# if __name__ == "__main__":
#     main()


import streamlit as st
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
from streamlit_lottie import st_lottie  # Import the st_lottie function
from transformers import pipeline

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

# Function to summarize text using Hugging Face's Transformers
def summarize_text(text):
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

# Streamlit Interface
def main():
    st.set_page_config(page_title="CSU Info Service", layout="centered")
    
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
                url = 'https://www.csu.ru/news'
                news_items = fetch_news_items(url)
                
                st.subheader("Recent News Headlines:")
                # Show a maximum of 5 headlines with simple summaries
                headlines = []
                for item in news_items[:5]:
                    # Collecting headlines for summarization
                    headlines.append(item['title'])
                    summary = (item['title'][:50] + '...') if len(item['title']) > 50 else item['title']
                    st.write(f"**Date:** {item['date']}")
                    st.write(f"**Title:** {summary} [Read More]({item['link']})")

                # Generate and display a summary of collected headlines
                if headlines:
                    combined_headlines = ' '.join(headlines)
                    summary = summarize_text(combined_headlines)
                    
                    st.subheader("Summary:")
                    st.write(summary)

        else:
            st.warning("Please enter a query and ensure API keys are set.")

        print(news_items)

if __name__ == "__main__":
    main()