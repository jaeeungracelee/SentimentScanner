import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // Import the CSS file

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
      <h1>Sentiment Analysis</h1>
      <form onSubmit={handleSubmit}>
        <input 
          type="text" 
          value={keyword} 
          onChange={handleInputChange} 
          placeholder="Enter keyword" 
        />
        <button type="submit">Analyze</button>
      </form>
      <div className="results" dangerouslySetInnerHTML={{ __html: results }} />
    </div>
  );
}

export default App;
