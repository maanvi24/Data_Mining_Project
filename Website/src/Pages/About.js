import React from 'react';

function About() {
  const containerStyle = {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'flex-start', // Align items at the start (top) of the container
    minHeight: '100vh', // Use minHeight to ensure the container takes at least the full height of the viewport
    padding: '50px', // Add padding to create space around the content
    boxSizing: 'border-box', // Include padding and border in the element's total width and height
    backgroundColor: '#033673', // Set the background color
  };

  const whiteBannerStyle = {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '10px',
    boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
    textAlign: 'left',
    width: '100%', 
    marginTop: '30px',// Make the banner take the full width of the container
  };

  const headingStyle = {
    marginBottom: '10px',
    color: '#333',
  };

  const paragraphStyle = {
    color: '#666',
  };

  return (
    <div style={containerStyle}>
      <div style={whiteBannerStyle}>
        <h1 style={headingStyle}>About Us</h1>
        <p style={paragraphStyle}>Welcome to our Stock Prediction Platform! Here, you can share articles about different news on the stocks and text on our homepage. We specialize in predicting whether stock prices will go up or down.
        <br /><br />
        Our platform analyzes your submitted content and provides you with:
        <ul>
          <li><strong>Sentiment Score:</strong> Understand the emotional tone in the text.</li>
          <li><strong>Relevance Scores:</strong> Know how important the information is.</li>
          <li><strong>Stock Price Prediction:</strong> Get insights into whether the stock will go up or down, including a prediction score.</li>
        </ul>
        Additionally, we offer a live feature for real-time stock news and predictions. Experience the excitement of tracking our predictions in real-time and observe how accurate our forecasts are when compared to actual market movements from seven days ago.
        <br /><br />
        For a comprehensive understanding, explore our Summary Page, a powerful tool that simplifies intricate stock data. It's all about making stock market insights easy and accessible for everyone, providing a quick overview of complex information.
      </p>
      </div>
    </div>
  );
}

export default About;
