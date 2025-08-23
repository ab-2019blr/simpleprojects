# Main dashboard page for stock market analysis and monitoring

import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.database import read_data, read_specific_data  # Importing read_data function from data package

# Set page configuration
st.set_page_config(page_title="Dashboard", layout="centered", page_icon="📊")

st.title("Stock Market Dashboard")
st.subheader("Monitor and Analyze Stock Market Data")
st.write("Fetch and display all data from the database.")
# Cache the data reading function to optimize performance
@st.cache_data
def get_data():
    return read_data()

# Add content specific to this page
if st.button("Read Data"):
    df = get_data()
    st.dataframe(df, hide_index=True)  # Display the data in a table format
    st.success("Data displayed successfully!")

# Access specific data example
st.write("Fetch and display specific data from the database.")
name_input = st.text_input("Enter name to fetch specific data (e.g., Alice):") 
if st.button("Fetch Specific Data"):
    if name_input.strip():
        try:
            specific_df = read_specific_data(name_input.strip())
            if not specific_df.empty and (specific_df["name"] == name_input.strip()).any():
                custom_column_names = {'id': 'SL.No.', 'name': 'Name', 'age': 'Age'}  # Define custom column names
                column_order = ['SL.No.', 'Name', 'Age'] # Define the desired column order
                df_renamed = specific_df.rename(columns=custom_column_names)
                df_ordered = df_renamed[column_order] # Reorder the columns in the data frame
                st.dataframe(df_ordered, hide_index=True)  # Display the data in a table format
                st.success(f"Data for '{name_input}' fetched successfully!")
            else:
                st.warning(f"No data found for '{name_input}'.")
        except Exception as e:
            st.error(f"No data found for '{name_input}'. Issue: {e} ")
    else:
        st.warning("Please enter a name to fetch specific data.")
        