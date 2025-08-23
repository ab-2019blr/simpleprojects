# News and research page for StockMarketApp app 

import streamlit as st

st.subheader("Secondary Page: News and Research Page")
st.write("This is the secondary page of the StockMarketApp app. More content can be added here.")

# Add content specific to this page     
# Access shared session state values
if 'name' in st.session_state and 'age' in st.session_state:
    st.write(f"Received from main page: Name = {st.session_state['name']}, Age = {st.session_state['age']}")
else:
    st.warning("No data yet! Please return to the main page and save details first.")
