# Main dashboard page for stock market analysis and monitoring

import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.database import read_data, read_specific_data, read_nifty_indexes_data, read_nifty_stocks_quotes # Importing read_data function from data package
from data.file_data_processor import read_csv_to_dataframe, read_top_gainers_csv_to_dataframe, read_top_losers_csv_to_dataframe, read_index_valuation_csv_to_dataframe
# Set page configuration
st.set_page_config(page_title="Dashboard", layout="centered", page_icon="📊")

st.title("Stock Market Dashboard")
st.subheader("Nifty Indexes")

@st.cache_data
def get_nifty_indexes_data():
    return read_nifty_indexes_data()
#  Nifty Index Tickers
df = get_nifty_indexes_data()

# HTML+CSS to create a ticker with scrolling effect
ticker_html = '''
<style>
.ticker-wrap {
  width: 100%;
  overflow: hidden;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  white-space: nowrap;
  box-sizing: border-box;
  padding: 10px 0;
}

.ticker-move {
  display: inline-block;
  padding-left: 100%;
  animation: ticker 200s linear infinite;
}

.ticker-item {
  display: inline-block;
  padding: 0 40px;
  font-size: 16px;
  color: #333;
  border-right: 1px solid #ccc;
}

.ticker-item:last-child {
  border-right: none;
}

.positive {
  color: #00C853;
  font-weight: bold;
}

.negative {
  color: #D32F2F;
  font-weight: bold;
}

@keyframes ticker {
  0% { transform: translate3d(0, 0, 0); }
  100% { transform: translate3d(-100%, 0, 0); }
}
</style>

<div class="ticker-wrap">
  <div class="ticker-move">
'''

# Add each Nifty index as a tile
for _, row in df.iterrows():
    # Determine the color class based on percentage change
    percentage = float(row.percentage_change)
    color_class = 'positive' if percentage >= 0 else 'negative'
    tile_content = f'<div class="ticker-item"><strong>{row.index_name}</strong> {row.last_price}  <span class="{color_class}">{row.percentage_change}%</span></div>'
    ticker_html += tile_content

ticker_html += '''
  </div>
</div>
'''

# Render the ticker in Streamlit page
st.markdown(ticker_html, unsafe_allow_html=True)
st.divider()

st.subheader("Nifty Stocks Ticker")
#  Stock tricker scroller
@st.cache_data
def get_nifty_stocks_quotes():
    return read_nifty_stocks_quotes()

nifty_stocks_df = get_nifty_stocks_quotes()

ticker_html_stocks = '''
<style>
.ticker-wrap {
  width: 100%;
  overflow: hidden;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  white-space: nowrap;
  box-sizing: border-box;
  padding: 10px 0;
}

.ticker-move {
  display: inline-block;
  padding-left: 100%;
  animation: ticker 100s linear infinite;
}

.ticker-item {
  display: inline-block;
  padding: 0 40px;
  font-size: 16px;
  color: #333;
  border-right: 1px solid #ccc;
}

.ticker-item:last-child {
  border-right: none;
}

.positive {
  color: #00C853;
  font-weight: bold;
}

.negative {
  color: #D32F2F;
  font-weight: bold;
}

@keyframes ticker {
  0% { transform: translate3d(0, 0, 0); }
  100% { transform: translate3d(-100%, 0, 0); }
}
</style>

<div class="ticker-wrap">
  <div class="ticker-move">
'''

# Add each Nifty stock as a tile
for _, row in nifty_stocks_df.iterrows():
    # Determine the color class based on percentage change
    percentage = float(row.p_change)
    color_class = 'positive' if percentage >= 0 else 'negative'
    tile_content = f'<div class="ticker-item"><strong>{row.symbol}</strong> {row.last_price}  <span class="{color_class}">{row.p_change}%</span></div>'
    ticker_html_stocks += tile_content

ticker_html_stocks += '''
  </div>
</div>
'''

# Render the ticker in Streamlit page
st.markdown(ticker_html_stocks, unsafe_allow_html=True)
st.divider()

#  Nifty Advance Decline Data
# Fetch Nifty Advance Decline data for dashboard page
st.subheader("Nifty Advance Decline Data")
@st.cache_data
def get_nifty_advance_decline_data():
    return read_csv_to_dataframe()

adv_decl_df = get_nifty_advance_decline_data()
# st.dataframe(adv_decl_df, hide_index=True) # Show only selected columns and format the date column

col1, col2 = st.columns([2,1])
with col1:
    # Dropdown filter
    filter_option = st.selectbox(
        "Select Filter:",
        ["Advances", "Declines"],
        key="advance_decline_filter"
    )
with col2:
    # Records per page (default 5)
    records_per_page = st.number_input(
        "Records per page:",
        min_value=5,
        max_value=10,
        value=5,
        step=5
    )
# Filter data based on selection
if filter_option == "Advances":
    filtered_df = adv_decl_df[adv_decl_df['pChange'] > 0].copy()
    st.success(f"Showing {len(filtered_df)} stocks with positive changes")
else:  # Declines
    filtered_df = adv_decl_df[adv_decl_df['pChange'] < 0].copy()
    st.error(f"Showing {len(filtered_df)} stocks with negative changes")

# Sort by pChange in descending order for Advances, ascending for Declines
if filter_option == "Advances":
    filtered_df = filtered_df.sort_values('pChange', ascending=False)
else:
    filtered_df = filtered_df.sort_values('pChange', ascending=True)

# Select specific columns to display
display_columns = [
    'symbol',
    'lastPrice',
    'change',
    'pChange',
    'totalTradedVolume'
]

# Filter to only display selected columns
display_df = filtered_df[display_columns].copy()

# Rename columns for better display
display_df.columns = [
    'Symbol',
    'Last Price',
    'Change',
    'Change %',
    'Volume'
]

# Calculate total pages
total_records = len(display_df)
total_pages = (total_records - 1) // records_per_page + 1 if total_records > 0 else 0

# Initialize session state for page number
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1

# Reset to page 1 if filter changes
if 'last_filter' not in st.session_state:
    st.session_state.last_filter = filter_option
elif st.session_state.last_filter != filter_option:
    st.session_state.current_page = 1
    st.session_state.last_filter = filter_option

# Pagination controls
if total_records > 0:
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
    
    with col1:
        if st.button("⏮️ First", disabled=(st.session_state.current_page == 1)):
            st.session_state.current_page = 1
            st.rerun()
    
    with col2:
        if st.button("◀️ Previous", disabled=(st.session_state.current_page == 1)):
            st.session_state.current_page -= 1
            st.rerun()
    
    with col3:
        st.markdown(f"<center>Page {st.session_state.current_page} of {total_pages}</center>", 
                   unsafe_allow_html=True)
    
    with col4:
        if st.button("Next ▶️", disabled=(st.session_state.current_page == total_pages)):
            st.session_state.current_page += 1
            st.rerun()
    
    with col5:
        if st.button("Last ⏭️", disabled=(st.session_state.current_page == total_pages)):
            st.session_state.current_page = total_pages
            st.rerun()

    # Calculate start and end indices for current page
    start_idx = (st.session_state.current_page - 1) * records_per_page
    end_idx = min(start_idx + records_per_page, total_records)
    
    # Get current page data
    # page_df = display_df.iloc[start_idx:end_idx].reset_index(drop=True)
    page_df = display_df.iloc[start_idx:end_idx].copy()
    # Reset index to start from 1 instead of 0
    page_df.index = range(start_idx + 1, end_idx + 1)


    # Apply color styling to the dataframe
    def color_percentage(val):
        if isinstance(val, (int, float)):
            color = 'green' if val > 0 else 'red' if val < 0 else 'black'
            return f'color: {color}; font-weight: bold'
        return ''
    
    # Style the dataframe
    styled_df = page_df.style.applymap(
        color_percentage,
        subset=['Change %']
    ).format({
        'Last Price': '₹{:.2f}',
        'Change': '{:.2f}',
        'Change %': '{:.2f}%',
        'Volume': '{:,.0f}'
    })

    # Display the styled dataframe
    st.dataframe(
        styled_df,
        use_container_width=True,
        # height=400
    )

    # Show record range
    st.caption(f"Showing records {start_idx + 1} to {end_idx} of {total_records}")

else:
    st.warning("No records found for the selected filter.")
    st.session_state.current_page = 1  # Reset to page 1 if no records found

st.divider()

#  Top Gainers and Losers
st.subheader("Nifty Top Gainers and Losers")
@st.cache_data
def get_nifty_top_gainers_data():
    return read_top_gainers_csv_to_dataframe()

@st.cache_data
def get_nifty_top_losers_data():
    return read_top_losers_csv_to_dataframe()

nifty_top_gainers_df = get_nifty_top_gainers_data()
nifty_top_losers_df = get_nifty_top_losers_data()

display_columns_gainers = [
    'symbol',
    'lastPrice',
    'change',
    'pChange'
]

display_columns_losers = [
    'symbol',
    'lastPrice',
    'change',
    'pChange'
]

nifty_top_gainers_df = nifty_top_gainers_df[display_columns_gainers]
nifty_top_losers_df = nifty_top_losers_df[display_columns_losers]

nifty_top_gainers_df.columns = [
    'Symbol',
    'Last Price',
    'Change',
    'Change %'
]
nifty_top_losers_df.columns = [
    'Symbol',
    'Last Price',
    'Change',
    'Change %'
]
nifty_top_gainers_df.index = range(1, len(nifty_top_gainers_df) + 1)
nifty_top_losers_df.index = range(1, len(nifty_top_losers_df) + 1)

# Style function for gainers (green color)
def style_gainers(val):
    if isinstance(val, (int, float)):
        return 'color: green; font-weight: bold'
    return ''


# Style function for losers (red color)
def style_losers(val):
    if isinstance(val, (int, float)):
        return 'color: red; font-weight: bold'
    return ''

# Apply styling to gainers dataframe
styled_gainers_df = nifty_top_gainers_df.style.applymap(
    style_gainers,
    subset=['Change %']
).format({
    'Last Price': '₹{:.2f}',
    'Change': '{:.2f}',
    'Change %': '{:.2f}%'
})

# Apply styling to losers dataframe
styled_losers_df = nifty_top_losers_df.style.applymap(
    style_losers,
    subset=['Change %']
).format({
    'Last Price': '₹{:.2f}',
    'Change': '{:.2f}',
    'Change %': '{:.2f}%'
})

# nifty_top_gainers_df['Change %'] = nifty_top_gainers_df['Change %'].apply(lambda x: f"{x}%")
# nifty_top_losers_df['Change %'] = nifty_top_losers_df['Change %'].apply(lambda x: f"{x}%")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### Top Gainers")
    st.dataframe(
        styled_gainers_df,
        # nifty_top_gainers_df,
        use_container_width=True,
        # height=400
    )
with col2:
    st.markdown("### Top Losers")
    st.dataframe(
        styled_losers_df,
        # nifty_top_losers_df,
        use_container_width=True,
        # height=400
    )
st.divider()

#  Nifty Index Valuation
st.subheader("Nifty Index Valuation Levels")   
@st.cache_data
def get_nifty_index_valuation_data():
    return read_index_valuation_csv_to_dataframe()

nifty_index_valuation_df = get_nifty_index_valuation_data()
# st.dataframe(nifty_index_valuation_df, hide_index=True) # Show only selected columns and format the date column
# Select specific columns to display
valuation_display_columns = [
    'index',
    'pe',
    'pb',
    'dy'
]
nifty_index_valuation_df = nifty_index_valuation_df[valuation_display_columns]
nifty_index_valuation_df.columns = [
    'Index',
    'P/E Ratio',
    'P/B Ratio',
    'Dividend Yield (%)'    
]
nifty_index_valuation_df.index = range(1, len(nifty_index_valuation_df) + 1)
st.dataframe(
    nifty_index_valuation_df,
    use_container_width=True,
    # height=400
)
st.divider()

#  Heatmap of Stock Performance








##### DUMMY EXAMPLE #####
##### This section demonstrates reading and displaying data from the database #####
# st.write("Fetch and display all data from the database.")
# # Cache the data reading function to optimize performance
# @st.cache_data
# def get_data():
#     return read_data()

# # Add content specific to this page
# if st.button("Read Data"):
#     df = get_data()
#     st.dataframe(df, hide_index=True)  # Display the data in a table format
#     st.success("Data displayed successfully!")

# # Access specific data example
# st.write("Fetch and display specific data from the database.")
# name_input = st.text_input("Enter name to fetch specific data (e.g., Alice):") 
# if st.button("Fetch Specific Data"):
#     if name_input.strip():
#         try:
#             specific_df = read_specific_data(name_input.strip())
#             if not specific_df.empty and (specific_df["name"] == name_input.strip()).any():
#                 custom_column_names = {'id': 'SL.No.', 'name': 'Name', 'age': 'Age'}  # Define custom column names
#                 column_order = ['SL.No.', 'Name', 'Age'] # Define the desired column order
#                 df_renamed = specific_df.rename(columns=custom_column_names)
#                 df_ordered = df_renamed[column_order] # Reorder the columns in the data frame
#                 st.dataframe(df_ordered, hide_index=True)  # Display the data in a table format
#                 st.success(f"Data for '{name_input}' fetched successfully!")
#             else:
#                 st.warning(f"No data found for '{name_input}'.")
#         except Exception as e:
#             st.error(f"No data found for '{name_input}'. Issue: {e} ")
#     else:
#         st.warning("Please enter a name to fetch specific data.")      