import streamlit as st
import requests
from pages import about, live_feed, summary  # Assuming the Predictions Generator content is included in the main script

# Display the content for the home page
st.title("Predictions Generator")

article_text = st.text_area("Enter article text...")

if st.button("Predict"):
    st.write("Predicting...")

    # Flask server URL
    flask_server_url = "http://localhost:5000"

    # Send request to Flask server for prediction
    prediction_response = requests.post(f"{flask_server_url}/predict_movement",
                                       json={"article": {"text": article_text}})
    sentiment_response = requests.post(f"{flask_server_url}/predict_sentiment",
                                      json={"article": {"text": article_text}})
    selectedTopics = [
        'Blockchain',
        'Earnings',
        'IPO',
        'Mergers & Acquisitions',
        'Financial Markets',
        'Energy & Transportation',
        'Finance',
        'Life Sciences',
        'Manufacturing',
        'Real Estate & Construction',
        'Retail & Wholesale',
        'Technology',
    ]
    relevance_responses = {
        topic: requests.post(f"{flask_server_url}/predict_relevance",
                             json={"article": {"text": article_text}, "topic": topic})
        for topic in selectedTopics
    }
    
    # Display prediction and other results
    if prediction_response.status_code == 200:
        prediction_data = prediction_response.json()
        
        # Print prediction data for debugging
       
        
        likelihood = prediction_data.get('likelihood')
        prediction_result = prediction_data.get('prediction')
        
        # Print prediction result and likelihood for debugging
        st.write("Prediction Result:", prediction_result)
    

        if prediction_data.get('prediction') == "up" and likelihood is not None:
            st.write(f"There is a {likelihood} likelihood of the stock going up.")
        elif prediction_data.get('prediction') == "down" and likelihood is not None:
            st.write(f"There is a {likelihood} likelihood of the stock going down.")
        else:
            st.warning("Unable to determine prediction result or likelihood.")

        if sentiment_response.status_code == 200:
            sentiment_data = sentiment_response.json()
            st.write(f"Sentiment Score: {sentiment_data['sentiment']}")

        for topic in selectedTopics:
            if relevance_responses[topic].status_code == 200:
                relevance_data = relevance_responses[topic].json()
                st.write(f"Relevance Score for {topic}: {relevance_data['prediction']}")

        st.success("Prediction completed!")
