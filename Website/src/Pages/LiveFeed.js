
import React, { useState } from 'react';
import axios from 'axios';
document.body.style.backgroundColor = '#033673';
const styles = {
  liveFeedContainer: {
    margin: '20px',
    marginTop: '70px', 
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    marginBottom: '20px',
  },
  label: {
    color: 'white',
    marginBottom: '10px',
  },
  input: {
    marginBottom: '10px',
    padding: '8px',
    border: '1px solid #ccc',
    borderRadius: '4px',
  },
  select: {
    marginBottom: '10px',
    padding: '8px',
  },
  button: {
    marginBottom: '10px',
    padding: '8px',
    cursor: 'pointer',
    transition: 'background-color 0.3s',
    backgroundColor: '#4caf50',
    color: 'white',
    borderRadius: '10px',

  },
  link: {
    color: '#007BFF',
    textDecoration: 'underline',
    cursor: 'pointer',
  },
  errorMessage: {
    color: 'red',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    marginTop: '20px',
  },
  th: {
    border: '1px solid #ddd',
    padding: '8px',
    textAlign: 'left',
    backgroundColor: '#f2f2f2',
  },
  td: {
    border: '1px solid #ddd',
    padding: '8px',
    textAlign: 'left',
  },
};

const LiveFeed = () => {
  const [ticker, setTicker] = useState('');
  const [interval, setInterval] = useState('1d');
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if (name === 'ticker') {
      setTicker(value);
    } else if (name === 'interval') {
      setInterval(value);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Simulate delay for loading
      await new Promise((resolve) => setTimeout(resolve, 1500));

      const response = await axios.post('http://127.0.0.1:5000/get_articles', { ticker, interval });
      setArticles(response.data.articles);
    } catch (error) {
      setError('Error fetching articles. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.liveFeedContainer}>
      <form style={styles.form} onSubmit={handleSubmit}>
        <label style={styles.label}>
          Ticker:
          <input
            type="text"
            name="ticker"
            value={ticker}
            onChange={handleInputChange}
            style={styles.input}
            required
          />
        </label>
        <label style={styles.label}>
          Interval:
          <select name="interval" value={interval} onChange={handleInputChange} style={styles.select}>
            <option value="1d">1 Day</option>
            <option value="1w">1 Week</option>
            <option value="1m">1 Month</option>
            <option value="3m">3 Months</option>
            <option value="6m">6 Months</option>
          </select>
        </label>
        <button type="submit" disabled={loading} style={styles.button}>
          {loading ? 'Loading...' : 'Get Articles'}
        </button>
      </form>

      {error && <p style={styles.errorMessage}>{error}</p>}

      {articles.length > 0 && (
        <table style={styles.table}>
          <thead>
            <tr>
              <th style={styles.th}>URL</th>
              <th style={styles.th}>Date Published</th>
              <th style={styles.th}>Likelihood</th>
              <th style={styles.th}>Model Prediction</th>
              <th style={styles.th}>Actual</th>
              <th style={styles.th}>Open Price</th>
              <th style={styles.th}>Close Price</th>
            </tr>
          </thead>
          <tbody>
            {articles.map((article, index) => (
              <React.Fragment key={index}>
                <tr>
                  <td style={styles.td}>
                    <a href={article.URL} target="_blank" rel="noopener noreferrer" style={styles.link}>
                      Click Here
                    </a>
                  </td>
                  <td style={styles.td}>{article['Date Published']}</td>
                  <td style={styles.td}>{article.Likelihood}</td>
                  <td style={styles.td}>{article['Model Prediction']}</td>
                  <td style={styles.td}>{article.Actual}</td>
                  <td style={styles.td}>{article['Open Price']}</td>
                  <td style={styles.td}>{article['Close Price']}</td>
                </tr>
                <tr>
                  <td colSpan="7" style={{ height: '10px' }}></td>
                </tr>
              </React.Fragment>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default LiveFeed;

