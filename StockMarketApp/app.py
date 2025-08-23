# Main Streamlit entry point for the StockMarketApp project

import streamlit as st
# Set page configuration
st.set_page_config(page_title="Home", layout="centered", page_icon="🏠")

# Set the page title
st.title("Hello, Streamlit!")

# Add a header
st.header("Welcome to My First Streamlit App")

# Add a subheader
st.subheader("This is a simple example page.")

# Display text
st.write("You can build interactive and beautiful web apps using just Python!")

# Text input widget
name = st.text_input("Enter your name")

# Add a slider widget
age = st.slider("Select your age", 15, 20, 25)
st.write(f"Selected age: {age}")

# Add a button
if st.button("Say Hello"):
    st.session_state['name'] = name
    st.session_state['age'] = age
    st.write(f"Hello, {name}! Your age is {age}.") 
    st.success("Value submitted successfully! Please go to the News page. (see sidebar)")