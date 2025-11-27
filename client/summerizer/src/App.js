import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [warning, setWarning] = useState('');

  const validateInput = (inputText) => {
    if (!inputText.trim()) {
      return 'Please enter some text to summarize.';
    }
    if (inputText.length < 50) {
      return 'Text should be at least 50 characters long for better summarization.';
    }
    if (inputText.length > 5000) {
      return 'Text is too long. Please keep it under 5000 characters.';
    }
    return null;
  };

  const summarize = async () => {
    const validationError = validateInput(text);
    if (validationError) {
      setError(validationError);
      return;
    }

    try {
      setLoading(true);
      setError('');
      setWarning('');
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:5000';
      const res = await axios.post(`${apiUrl}/summarize`, { text });
      setSummary(res.data.summary);
      if (res.data.warning) {
        setWarning(res.data.warning);
      }
      // Display LangChain method info if available
      if (res.data.method) {
        const methodInfo = res.data.method === 'langchain_map_reduce' 
          ? `Processed ${res.data.chunks_processed || 0} chunks using map-reduce strategy`
          : 'Processed using LangChain summarization chain';
        console.log('LangChain method:', methodInfo);
      }
    } catch (error) {
      console.error('Summarization error:', error);
      if (error.response) {
        setError(`Server error: ${error.response.data.error || 'Unknown error'}`);
      } else if (error.request) {
        setError('Unable to connect to the server. Please make sure the backend is running.');
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="header">
        <h1 className="main-title">
          <span className="title-text">Rewrite AI</span>
          <span className="title-badge">Powered by LangChain</span>
        </h1>
        <p className="subtitle">Transform your text with intelligent AI-powered summarization</p>
      </div>
      <div className="input-section">
        <textarea
          placeholder="Paste your text here to get started... (minimum 50 characters)"
          value={text}
          onChange={(e) => {
            setText(e.target.value);
            setError(''); 
          }}
          disabled={loading}
        />
        <div className="char-count">
          {text.length}/5000 characters
        </div>
      </div>
      
      <button 
        onClick={summarize} 
        disabled={loading || !text.trim()}
        className={loading ? 'loading' : ''}
      >
        {loading ? 'Rewriting...' : 'Rewrite with AI'}
      </button>
      
      {error && (
        <div className="error">
          <p>{error}</p>
        </div>
      )}
      
      {warning && (
        <div className="warning">
          <p>⚠️ {warning}</p>
        </div>
      )}
      
      {summary && (
        <div className="output">
          <div className="output-header">
            <h3>✨ Rewritten Content</h3>
            <span className="output-badge">AI Generated</span>
          </div>
          <p>{summary}</p>
        </div>
      )}
    </div>
  );
}

export default App;
