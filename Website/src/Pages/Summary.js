import React, { useState } from 'react';
 
const Summary = () => {
  const [article, setArticle] = useState('');
  const [maxLength, setMaxLength] = useState(500); // Default max length
  const [minLength, setMinLength] = useState(10); // Default min length
  const [numSentences, setNumSentences] = useState(2); // Default number of sentences
  const [generatedSummary, setGeneratedSummary] = useState('');
  const [error, setError] = useState(null);
 
  const handleGenerateSummary = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/generate_summary', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          summary: article,
          max_length: maxLength,
          min_length: minLength,
          num_sentences: numSentences,
        }),
      });
 
      if (!response.ok) {
        throw new Error('Failed to generate summary');
      }
 
      const data = await response.json();
      setGeneratedSummary(data.generated_summary);
      setError(null); // Reset any previous errors
    } catch (error) {
      console.error('Error generating summary:', error);
      setGeneratedSummary(''); // Reset the summary on error
      setError('Error generating summary. Please try again.'); // Set an error message
    }
  };
 
  const styles = {
    container: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      padding: '20px',
      backgroundColor: '#333',
      color: '#fff',
    },
    header: {
      fontSize: '24px',
      marginBottom: '20px',
    },
    textarea: {
      width: '100%',
      height: '150px',
      padding: '10px',
      marginBottom: '20px',
      border: '1px solid #ccc',
      borderRadius: '4px',
      resize: 'vertical',
    },
    label: {
      fontSize: '16px',
      marginBottom: '5px',
    },
    input: {
      width: '50px',
      padding: '8px',
      margin: '0 0 10px 0',
      border: '1px solid #ccc',
      borderRadius: '4px',
    },
    button: {
      padding: '10px',
      backgroundColor: '#007bff',
      color: '#fff',
      border: 'none',
      borderRadius: '4px',
      cursor: 'pointer',
    },
    summaryContainer: {
      marginTop: '20px',
      textAlign: 'left', // Adjusted for better readability
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