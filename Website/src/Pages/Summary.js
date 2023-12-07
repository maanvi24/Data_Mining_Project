

import React, { useState } from 'react';

const Summary = () => {
  const [article, setArticle] = useState('');
  const [maxLength, setMaxLength] = useState('');
  const [minLength, setMinLength] = useState('');
  const [numSentences, setNumSentences] = useState('');
  const [generatedSummary, setGeneratedSummary] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerateSummary = async () => {
    try {
      setLoading(true);

      const response = await fetch('http://127.0.0.1:5000/generate_summary', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          summary: article,
          max_length: parseInt(maxLength), // Parse as integer
          min_length: parseInt(minLength), // Parse as integer
          num_sentences: parseInt(numSentences), // Parse as integer
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate summary');
      }

      const data = await response.json();

      if (!data.generated_summary) {
        setError('No summary generated. Please check your input.');
      } else {
        setGeneratedSummary(data.generated_summary);
        setError(null);
      }
    } catch (error) {
      console.error('Error generating summary:', error);
      setGeneratedSummary('');
      setError('Error generating summary. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const styles = {
    container: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '100vh',
      backgroundColor: '#033673',
      color: '#fff',
    },
    header: {
      fontSize: '24px',
      marginBottom: '20px',
      color: '#fff',
    },
    textarea: {
      width: '80%',
      height: '150px',
      padding: '10px',
      margin: '10px 0',
      border: '1px solid #ccc',
      borderRadius: '4px',
    },
    label: {
      fontSize: '16px',
      marginBottom: '5px',
      color: '#fff',
    },
    input: {
      width: '50px',
      padding: '8px',
      margin: '0 0 10px 0',
      border: '1px solid #ccc',
      borderRadius: '4px',
    },
    button: {
      backgroundColor: '#4caf50',
      color: '#fff',
      padding: '10px 15px',
      border: 'none',
      borderRadius: '4px',
      cursor: 'pointer',
    },
    summaryContainer: {
      marginTop: '10px',
      padding: '10px',
      fontWeight: 'bold',
      color: '#fff',
    },
    loadingOverlay: {
      position: 'absolute',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
      zIndex: 1,
      color: '#fff',
    },
    error: {
      color: 'red',
      marginTop: '10px',
    },
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.header}>Summary Generator</h1>
      <textarea
        style={styles.textarea}
        placeholder="Enter your article here..."
        value={article}
        onChange={(e) => setArticle(e.target.value)}
      ></textarea>
      <label style={styles.label}>Max Length for Summary:</label>
      <input
        style={styles.input}
        type="number"
        value={maxLength}
        onChange={(e) => setMaxLength(e.target.value)}
      />
      <label style={styles.label}>Min Length for Summary:</label>
      <input
        style={styles.input}
        type="number"
        value={minLength}
        onChange={(e) => setMinLength(e.target.value)}
      />
      <label style={styles.label}>Number of Sentences for Summary:</label>
      <input
        style={styles.input}
        type="number"
        value={numSentences}
        onChange={(e) => setNumSentences(e.target.value)}
      />
      <button style={styles.button} onClick={handleGenerateSummary}>
        Generate Summary
      </button>

      {loading && (
        <div style={styles.loadingOverlay}>
          <p>Loading...</p>
        </div>
      )}

      {error && <p style={styles.error}>{error}</p>}

      {generatedSummary && (
        <div style={styles.summaryContainer}>
          <h2>Generated Summary:</h2>
          <p>{generatedSummary}</p>
        </div>
      )}
    </div>
  );
};

export default Summary;

