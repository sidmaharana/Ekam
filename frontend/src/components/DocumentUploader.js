import React, { useState } from 'react';

function DocumentUploader({ setIngestionJob }) {
  const [files, setFiles] = useState([]);
  const [status, setStatus] = useState('');

  const handleFileChange = (e) => {
    setFiles(e.target.files);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (files.length === 0) {
      setStatus('Please select files to upload.');
      return;
    }

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append('files', files[i]);
    }

    setStatus('Uploading...');

    try {
      const response = await fetch('/api/ingest/documents', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setStatus(`Upload successful. Job ID: ${data.job_id}`);
        setIngestionJob(data.job_id);
        // In a real app, you would now poll the /api/ingest/status/{data.job_id} endpoint.
      } else {
        setStatus(`Upload failed: ${data.error || 'Unknown error'}`);
      }
    } catch (err) {
      setStatus('Failed to connect to the backend.');
    }
  };

  return (
    <div className="component">
      <h2>Document Uploader</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" multiple onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
      {status && <div className="status">{status}</div>}
    </div>
  );
}

export default DocumentUploader;