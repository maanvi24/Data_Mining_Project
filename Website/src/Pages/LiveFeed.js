import React, { useState } from 'react';

// Define the LiveFeed component
const LiveFeed = () => {
  // State hooks for managing input, articles, and error
  const [ticker, setTicker] = useState('');
  const [selectedInterval, setSelectedInterval] = useState('1d');
  const [articles, setArticles] = useState([]);
  const [error, setError] = useState('');

  // Function to fetch articles based on user input
  const getArticles = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/get_articles', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ticker, selected_interval: selectedInterval }),
      });

      const result = await response.json();

      if (result.success) {
        setArticles(result.articles);
        setError('');
      } else {
        setArticles([]);
        setError(result.error);
      }
    } catch (error) {
      console.error('Error:', error);
      setArticles([]);
      setError('An error occurred while fetching data.');
    }
  };

  // JSX structure for rendering the component
  return (
    <div className="Livefeed">
      {/* Inline styles for styling purposes */}
      <style>
        {`
          .Livefeed {
            text-align: center;
          }

          .Livefeed-header {
            background-color: #282c34;
            padding: 30px;
            color: white;
          }

          .Livefeed-content {
            margin-top: 20px;
          }

          label {
            margin-right: 10px;
          }

          input,
          select,
          button {
            margin-bottom: 10px;
          }

          /* Style for each article box */
          .article-box {
            border: 1px solid #ccc;
            padding: 10px;
            margin-bottom: 10px;
          }
        `}
      </style>
      {/* Header */}
      <header className="Livefeed-header">
        <h1>Live Feed App</h1>
      </header>
      {/* Content */}
      <div className="Livefeed-content">
        {/* Input and selection elements */}
        <label htmlFor="ticker">Enter Ticker:</label>
        <input
          type="text"
          id="ticker"
          placeholder="Enter Ticker"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
        />

        <label htmlFor="interval">Select Interval:</label>
        <select
          id="interval"
          value={selectedInterval}
          onChange={(e) => setSelectedInterval(e.target.value)}
        >
          <option value="1d">1 Day</option>
          <option value="1w">1 Week</option>
          <option value="1m">1 Month</option>
          <option value="3m">3 Months</option>
          <option value="6m">6 Months</option>
        </select>

        {/* Button to trigger fetching of articles */}
        <button onClick={getArticles}>Get Live Feed</button>

        {/* Display articles */}
        <div id="result">
          {error && <p>Error: {error}</p>}
          {articles.length > 0 && (
            <>
              <h2>Articles:</h2>
              {/* Map over articles and create a styled box for each */}
              {articles.map((article, index) => (
                <div key={index} className="article-box">
                  <p>
                    <strong>{article.title}</strong> - {article.date_published}
                  </p>
                  <p>{article.summary}</p>
                  <p>
                    <a href={article.url} target="_blank" rel="noopener noreferrer">
                      Read More
                    </a>
                  </p>
                </div>
              ))}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

// Export the LiveFeed component
export default LiveFeed;
