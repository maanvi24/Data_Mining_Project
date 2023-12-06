import React, { useState } from 'react';

const Summary = () => {
  const [article, setArticle] = useState('');
  const [numLines, setNumLines] = useState(5); // Default number of lines
  const [generatedSummary, setGeneratedSummary] = useState('');

  const handleGenerateSummary = async () => {
    try {
      const response = await fetch('http://localhost:5001/generate_summary', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          summary: article,
          num_lines: numLines,
        }),
      });

      const data = await response.json();
      setGeneratedSummary(data.generated_summary);
    } catch (error) {
      console.error('Error generating summary:', error);
    }
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
      border: '1px solid #ccc',
      padding: '10px',
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
      <label style={styles.label}>Number of Lines for Summary:</label>
      <input
        style={styles.input}
        type="number"
        value={numLines}
        onChange={(e) => setNumLines(e.target.value)}
      />
      <button style={styles.button} onClick={handleGenerateSummary}>
        Generate Summary
      </button>
      {generatedSummary && (
        <div style={styles.summaryContainer}>
          <h2 style={{ color: '#fff' }}>Generated Summary:</h2>
          <p>{generatedSummary}</p>
        </div>
      )}
    </div>
  );
};

export default Summary;
