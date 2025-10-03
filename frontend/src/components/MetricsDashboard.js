import React from 'react';

function MetricsDashboard({ schema, ingestionJob, queryResult }) {
  return (
    <div className="component">
      <h2>Metrics Dashboard</h2>
      {schema && !schema.error && (
        <p>Discovered Tables: {Object.keys(schema).length}</p>
      )}
      {ingestionJob && <p>Last Ingestion Job ID: {ingestionJob}</p>}
      {queryResult && queryResult.cache_hit !== undefined && (
        <p>Last Query Cache: {queryResult.cache_hit ? 'Hit' : 'Miss'}</p>
      )}
    </div>
  );
}

export default MetricsDashboard;