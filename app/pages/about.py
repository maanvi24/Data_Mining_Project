import streamlit as st

# Page title
st.title("About the App")

# Key Features section
st.subheader("Key Features:")
st.markdown("- **Sentiment Analysis:** Understand the emotional tone in the stock-related content.")
st.markdown("- **Relevance Scores:** Evaluate the importance of the information.")
st.markdown("- **Stock Price Prediction:** Get insights into whether the stock prices will go up or down, backed by prediction scores.")

# Live Feed section
st.subheader("Live Feed:")
st.markdown("Experience real-time stock news and predictions. Track the accuracy of our forecasts compared to actual market movements from seven days ago.")

# Summary Page section
st.subheader("Summary Page:")
st.markdown("Simplify intricate stock data with our powerful Summary Page, offering a quick overview of complex information.")

# Platform goal and closing statement
st.markdown("""
We strive to make stock market insights easy and accessible for everyone. Explore our platform to make informed decisions in the dynamic world of stocks!
""")
