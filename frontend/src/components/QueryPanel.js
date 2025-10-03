import React, { useState } from 'react';

function QueryPanel({ query, setQuery, setQueryResult }) {
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setQueryResult(null); // Clear previous results

    try {
      const response = await fetch('/api/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      const data = await response.json();

      if (response.ok) {
        setQueryResult(data);
      } else {
        setError(data.error || 'An error occurred.');
      }
    } catch (err) {
      setError('Failed to connect to the backend.');
    }
  };

  return (
    <div className="component">
      <h2>Query Panel</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={query} // Use prop
          onChange={(e) => setQuery(e.target.value)} // Use prop
          placeholder="Enter your natural language query"
        ></textarea>
        <button type="submit">Submit Query</button>
      </form>
      {error && <div className="error">{error}</div>}
    </div>
  );
}

export default QueryPanel;
