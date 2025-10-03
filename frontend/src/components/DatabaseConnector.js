import React, { useState } from 'react';

function DatabaseConnector({ setSchema }) {
  const [connectionString, setConnectionString] = useState('sqlite:///./test.db');
  const [error, setError] = useState(null);
  const [schemaData, setSchemaData] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSchemaData(null);

    try {
      const response = await fetch('/api/ingest/database', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ connection_string: connectionString }),
      });

      const data = await response.json();

      if (response.ok) {
        setSchema(data);
        setSchemaData(data);
      } else {
        setError(data.error || 'An error occurred.');
      }
    } catch (err) {
      setError('Failed to connect to the backend.');
    }
  };

  return (
    <div className="component">
      <h2>Database Connector</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={connectionString}
          onChange={(e) => setConnectionString(e.target.value)}
          placeholder="Enter database connection string"
        />
        <button type="submit">Connect</button>
      </form>
      {error && <div className="error">{error}</div>}
      {schemaData && (
        <div>
          <h3>Discovered Schema:</h3>
          <pre>{JSON.stringify(schemaData, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default DatabaseConnector;