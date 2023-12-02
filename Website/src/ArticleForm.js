// src/ArticleForm.js
import React, { useState } from 'react';
import axios from 'axios';

const ArticleForm = ({ onPredictionUpdate }) => {
  const [articleText, setArticleText] = useState('');
  const [prediction, setPrediction] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePrediction = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await axios.post('http://localhost:5000/predict_movement', {
        article: { text: articleText },
      });

      const newPrediction = response.data.prediction;
      setPrediction(newPrediction);
      onPredictionUpdate && onPredictionUpdate(newPrediction);
    } catch (error) {
      console.error('Error:', error);
      setError('An error occurred while making the prediction.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.header}>Stock Prediction App</h1>
      <div style={styles.articleFormContainer}>
        <textarea
          style={styles.articleTextInput}
          placeholder="Enter article text..."
          value={articleText}
          onChange={(e) => setArticleText(e.target.value)}
        />
        <button style={styles.predictButton} onClick={handlePrediction} disabled={loading}>
          {loading ? 'Predicting...' : 'Predict'}
        </button>
        {error && <p style={styles.errorMessage}>{error}</p>}
        {prediction && <p style={styles.predictionResult}>Prediction: {prediction}</p>}
      </div>
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '100vh',
    backgroundColor: '#000', // Black background
    color: '#fff', // Text color
  },
  header: {
    fontSize: '24px',
    marginBottom: '20px',
  },
  articleFormContainer: {
    width: '300px',
    padding: '20px',
    border: '1px solid #ccc',
    borderRadius: '8px',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
    backgroundColor: '#fff',
  },
  articleTextInput: {
    width: '100%',
    padding: '10px',
    margin: '0 auto 10px auto', 
    border: '1px solid #ccc',
    borderRadius: '4px',
  },
  predictButton: {
    backgroundColor: '#4caf50',
    color: '#fff',
    padding: '10px 15px',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
  },
  predictButtonDisabled: {
    backgroundColor: '#a0a0a0',
    cursor: 'not-allowed',
  },
  errorMessage: {
    color: '#ff3333',
    marginTop: '10px',
  },
  predictionResult: {
    marginTop: '10px',
    fontWeight: 'bold',
  },
};

export default ArticleForm;
