
import React, { useState } from 'react';
import axios from 'axios';

const ArticleForm = ({ onPredictionUpdate }) => {
  const [articleText, setArticleText] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [sentiment, setSentiment] = useState(null);
  const [relevanceScores, setRelevanceScores] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [likelihoodStatement, setLikelihoodStatement] = useState(null);

  const selectedTopics = [
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
  ];

  const handlePrediction = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await axios.post('http://localhost:5000/predict_movement', {
        article: { text: articleText },
      });

      const newPrediction = response.data.prediction;
      const likelihood = response.data.likelihood;

      setPrediction(newPrediction);
      onPredictionUpdate && onPredictionUpdate(newPrediction);

      // Fetch sentiment and relevance scores for selected topics
      const sentimentResponse = await axios.post('http://localhost:5000/predict_sentiment', {
        article: { text: articleText },
      });

      const relevanceResponses = await Promise.all(
        selectedTopics.map((topic) =>
          axios.post('http://localhost:5000/predict_relevance', {
            article: { text: articleText },
            topic: topic,
          })
        )
      );

      const newSentiment = sentimentResponse.data.sentiment;
      setSentiment(newSentiment);

      const newRelevanceScores = {};
      relevanceResponses.forEach((response, index) => {
        const topic = selectedTopics[index];
        newRelevanceScores[topic] = response.data.prediction;
      });
      setRelevanceScores(newRelevanceScores);

      // Display likelihood information
      const likelihoodStatement = `There is a ${likelihood.toFixed(2)}% likelihood this stock will go ${
        newPrediction === 'up' ? 'up' : 'down'
      } tomorrow.`;
      setLikelihoodStatement(likelihoodStatement);
    } catch (error) {
      console.error('Error:', error);
      setError('An error occurred while making the prediction.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.header}>Predictions Generator</h1>
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
        {prediction && (
          <div>
            <p style={styles.predictionResult}>Prediction: {prediction}</p>
            {likelihoodStatement && <p style={styles.predictionStatement}>{likelihoodStatement}</p>}
          </div>
        )}
        {sentiment && <p style={styles.sentimentScore}>Sentiment Score: {sentiment}</p>}
        {relevanceScores && (
          <div>
            <p style={styles.relevanceScore}>Relevance Scores:</p>
            {selectedTopics.map((topic) => (
              <p key={topic}>{topic}: {relevanceScores[topic]}</p>
            ))}
          </div>
        )}
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
    backgroundColor: '#033673', // Blue background
    color: '#000', // Text color
  },
  header: {
    fontSize: '24px',
    marginBottom: '20px',
    color: '#fff'
  },
  articleFormContainer: {
    width: '500px',
    padding: '20px',
    border: '2px solid #ccc',
    borderRadius: '8px',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
    backgroundColor: '#fff',
  },
  articleTextInput: {
    width: '96%',
    height: '120px',
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
    color: '#000'
  },
  errorMessage: {
    color: '#ff3333',
    marginTop: '10px',
    color: '#000'
  },
  predictionResult: {
    marginTop: '10px',
    fontWeight: 'bold',
  },
  sentimentScore: {
    marginTop: '10px',
    color: '#000',
    fontWeight: 'bold'
  },
  relevanceScore: {
    fontWeight: 'bold',
    marginBottom: '5px',
    color: '#000'
  },
};

export default ArticleForm;

