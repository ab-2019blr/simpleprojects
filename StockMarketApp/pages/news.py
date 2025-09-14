# News and research page for StockMarketApp app 

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import base64
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.api_client import fetch_market_news, fetch_global_market_news # Importing read_data function from data package
# Replace missing or invalid image URLs with the default image 
local_image_path = os.path.join(os.path.dirname(__file__),"..","assets","images","stock_market_image.jpg") # Local path to # Encode image as base64 string
with open(local_image_path, "rb") as image_file: 
    encoded_string = base64.b64encode(image_file.read()).decode()   
# Create data URI scheme for image
image_data_uri = f"data:image/jpeg;base64,{encoded_string}"
# Set page configuration
st.set_page_config(page_title="News", layout="centered", page_icon="📰")

st.subheader("Secondary Page: News and Research Page")
st.write("This is the secondary page of the StockMarketApp app. More content can be added here.")

# Add content specific to this page     
# Access shared session state values
# if 'name' in st.session_state and 'age' in st.session_state:
#     st.write(f"Received from main page: Name = {st.session_state['name']}, Age = {st.session_state['age']}")
# else:
#     st.warning("No data yet! Please return to the main page and save details first.")

# st.divider()

df = fetch_market_news(3) # Fetch 3 latest market news articles 
# Show only selected columns and format the date column 
selected_df = df[['title', 'source', 'published_at', 'image_url']].copy()
# Rename the column
selected_df = selected_df.rename(columns={'source': 'Source', 'title': 'Title', 'published_at': 'Date', 'image_url': 'Image'})
# Convert and format the 'date' column to 'YYYY-MM-DD'
selected_df['Date'] = pd.to_datetime(selected_df['Date']).dt.strftime('%d-%m-%Y')
# Display the news articles in a table format    
# st.dataframe(selected_df, hide_index=True)   
# st.success("News displayed successfully!") 

st.divider()

# HTML+CSS to create a ticker with scrolling effect
ticker_html = '''
<style>
.ticker-wrap {
  width: 100%;
  overflow: hidden;
  background-color: black; /* Dark grey background */
  border: 0px solid #ddd;
  white-space: nowrap;
  box-sizing: border-box;
  padding: 10px 0;
}
.ticker-move {
  display: inline-block;
  padding-left: 100%;
  animation: ticker 20s linear infinite;
}
.ticker-item {
  display: inline-block;
  width: auto;
  height: 350px; /* Fixed height for each tile */ 
  padding: 15px 30px;
  font-size: 16px;
  color: #333;
  background-color: #add8e6; /* Light blue background */ 
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
  margin-right: 20px;  /* Space between cards */
  vertical-align: top;
  white-space: normal;  /* Allow multiline content */
  width: 220px;
  box-sizing: border-box;
}
.ticker-item:last-child {
  margin-right: 0;
}
.ticker-item img {
  max-width: 100%;
  height: 100px; /* Adjust the height of thumbnails as needed */
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 10px;
}
.ticker-item strong {
  display: block;
  margin-bottom: 8px;
  font-size: 18px;
}
.ticker-item .source,
.ticker-item .date {
  display: block;
  margin-bottom: 4px;
  font-size: 14px;
  color: #666;
}
@keyframes ticker {
  0% { transform: translate3d(0, 0, 0); }
  100% { transform: translate3d(-100%, 0, 0); }
}
</style>
<div class="ticker-wrap">
  <div class="ticker-move">
'''

# Add each news piece as a tile
for _, row in selected_df.iterrows():
    tile_content = f'''
    <div class="ticker-item">
      <img src="{row.Image}" alt="News Image" onerror="this.style.display='none', this.onerror=null, this.src='{image_data_uri}'"/> <!-- Hide image if not available -->
      <strong>{row.Title}</strong>
      <span class="source">Source: {row.Source}</span>
      <span class="date">Date: {row.Date}</span>
    </div>
    ''' 
    ticker_html += tile_content

ticker_html += '''
  </div>
</div>
'''

# Display the ticker
# st.markdown(ticker_html, unsafe_allow_html=True)
components.html(ticker_html, height=400, scrolling=False)
st.divider()

st.subheader("Global Market News from Alpha Vantage API")
df2 = fetch_global_market_news() # Fetch global market news articles
# st.dataframe(df2, hide_index=True) # Show only selected columns and format the date column
# Pagination Settings
items_per_page = 10
num_pages = (len(df2) - 1) // items_per_page + 1
# Initialize session state page number
if 'page_number' not in st.session_state:
    st.session_state.page_number = 0
# Function to display news tile
def display_tile(row):
    st.markdown(f"##### {row['Title']}")
    st.markdown(f"**Summary:** {row['Summary']}")
    st.markdown(f"**Source:** {row['Source']}")
    st.markdown(f"**Published:** {row['Date']}")
    st.markdown(f"**Read more...** {row['URL']}")
    st.markdown("---")
# Calculate start and end indices for current page
start_idx = st.session_state.page_number * items_per_page
end_idx = min(start_idx + items_per_page, len(df2))
# Display current page tiles vertically
for idx in range(start_idx, end_idx):
    display_tile(df2.iloc[idx])
# Navigation buttons
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("Previous") and st.session_state.page_number > 0:
        st.session_state.page_number -= 1

with col2:
    st.markdown(f"**Page {st.session_state.page_number + 1} of {num_pages}**")

with col3:
    if st.button("Next") and st.session_state.page_number < num_pages - 1:
        st.session_state.page_number += 1

st.success("Global market news displayed successfully!")
st.divider() 