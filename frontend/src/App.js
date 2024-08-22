import React, { useState } from 'react';
import axios from 'axios';
import SwirlBackground from './SwirlBackground';
import './App.css'; 

function App() {
  const [keyword, setKeyword] = useState('');
  const [results, setResults] = useState('');

  const handleInputChange = (event) => {
    setKeyword(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    axios.post('http://127.0.0.1:5000/analyze', { keyword })
      .then(response => {
        setResults(response.data.reddit_df);
      })
      .catch(error => {
        console.error('There was an error!', error);
      });
  };

  return (
    <div className="App">
    <SwirlBackground />
    <header className="App-header">
      <h1>SentimentScanner</h1>
      <form onSubmit={handleSubmit} className="input-form">
        <textarea
          value={keyword}
          onChange={handleInputChange}
          placeholder="Enter Text Here"
          className="input-box"
          rows="1" // Set an initial number of rows
        />
        <button type="submit" className="submit-button">Analyze</button>
      </form>
      <div className="results" dangerouslySetInnerHTML={{ __html: results }} />
    </header>
  </div>
  );
}

export default App;
