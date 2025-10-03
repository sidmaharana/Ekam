import React, { useState } from 'react';
import './App.css';
import DatabaseConnector from './components/DatabaseConnector';
import DocumentUploader from './components/DocumentUploader';
import QueryPanel from './components/QueryPanel';
import ResultsView from './components/ResultsView';
import MetricsDashboard from './components/MetricsDashboard';

function App() {
  const [schema, setSchema] = useState(null);
  const [queryResult, setQueryResult] = useState(null);
  const [ingestionJob, setIngestionJob] = useState(null);
  const [query, setQuery] = useState(''); // Lifted state up

  return (
    <div className="App">
      <header className="App-header">
        <h1>NLP Query Engine</h1>
      </header>
      <main>
        <div className="container">
          <div className="left-panel">
            <DatabaseConnector setSchema={setSchema} />
            <DocumentUploader setIngestionJob={setIngestionJob} />
            <MetricsDashboard schema={schema} ingestionJob={ingestionJob} queryResult={queryResult} />
          </div>
          <div className="right-panel">
            <QueryPanel query={query} setQuery={setQuery} setQueryResult={setQueryResult} />
            <ResultsView queryResult={queryResult} setQuery={setQuery} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;