import React, { useMemo, useEffect } from 'react';
import { useTable } from 'react-table';
import './ResultsView.css';
import ResultChart from './ResultChart'; // Import the new chart component

function ResultsView({ queryResult, setQuery }) {
  useEffect(() => {
    if (queryResult) {
      console.log("Data received by ResultsView:", queryResult);
    }
  }, [queryResult]);

  const { result, query_type, suggestions } = queryResult || {};

  const columns = useMemo(() => {
    if (query_type !== 'sql' || !result || !result.results || !Array.isArray(result.results) || result.results.length === 0) {
      return [];
    }
    return Object.keys(result.results[0]).map(key => ({
      Header: key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
      accessor: key,
    }));
  }, [query_type, result]);

  const data = useMemo(() => {
    if (query_type !== 'sql' || !result || !result.results || !Array.isArray(result.results)) {
      return [];
    }
    return result.results;
  }, [query_type, result]);

  const tableInstance = useTable({ columns, data });
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = tableInstance;

  // Logic to determine if data is chartable and prepare chart data
  const chartData = useMemo(() => {
    if (query_type === 'sql' && data.length > 0 && columns.length === 2) {
      const [labelCol, valueCol] = columns;
      // Check if the value column contains numeric data
      const isNumeric = data.every(row => typeof row[valueCol.accessor] === 'number');

      if (isNumeric) {
        return {
          labels: data.map(row => row[labelCol.accessor]),
          data: data.map(row => row[valueCol.accessor]),
          label: valueCol.Header, // Use the header of the value column as the chart label
          title: `Results for ${labelCol.Header} by ${valueCol.Header}`,
        };
      }
    }
    return null;
  }, [query_type, data, columns]);

  if (!queryResult) {
    return (
      <div className="component">
        <h2>Results View</h2>
        <p>Results will be displayed here.</p>
      </div>
    );
  }

  if (result && result.error) {
    return (
      <div className="component">
        <h2>An Error Occurred</h2>
        <div className="error">{result.error}</div>
      </div>
    );
  }

  const renderSqlResults = () => {
    if (!Array.isArray(result.results)) {
      return <p><i>{result.results || "No results found."}</i></p>;
    }
    if (result.results.length === 0) {
      return <p>Query returned no results.</p>;
    }
    return (
      <table {...getTableProps()}>
        <thead>
          {headerGroups.map(headerGroup => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map(column => (
                <th {...column.getHeaderProps()}>{column.render('Header')}</th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {rows.map(row => {
            prepareRow(row);
            return (
              <tr {...row.getRowProps()}>
                {row.cells.map(cell => (
                  <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    );
  };

  return (
    <div className="component">
      <h2>Results View</h2>
      {queryResult.cache_hit !== undefined && (
        <p className="cache-status">Cache Status: {queryResult.cache_hit ? 'Hit' : 'Miss'}</p>
      )}
      {result && (
        <div>
          <h3>Query Type: {query_type}</h3>
          {query_type === 'sql' && result.generated_sql && (
            <div className="sql-query-box">
              <h4>Generated SQL:</h4>
              <pre>{result.generated_sql}</pre>
            </div>
          )}
          {/* Render Chart if data is suitable */}
          {chartData && <ResultChart chartData={chartData} />}
          
          {query_type === 'sql' && result.results && renderSqlResults()}
          {query_type === 'document' && result.results && (
            <div className="document-results">
              <h4>Document Matches:</h4>
              {result.results.length > 0 ? (
                <ul>
                  {result.results.map((item, index) => (
                    <li key={index} className="document-card">
                      <strong>{item.document_name}</strong> (Similarity: {item.similarity.toFixed(4)})
                      <p>{item.chunk_text}</p>
                    </li>
                  ))}
                </ul>
              ) : (
                <p>No matching documents found.</p>
              )}
            </div>
          )}
        </div>
      )}
      {/* Render Follow-up Suggestions */}
      {suggestions && suggestions.length > 0 && (
        <div className="suggestions-panel">
          <h4>Next Steps:</h4>
          {
            suggestions.map((suggestion, index) => (
              <button key={index} className="suggestion-btn" onClick={() => setQuery(suggestion)}>
                {suggestion}
              </button>
            ))
          }
        </div>
      )}
    </div>
  );
}

export default ResultsView;
