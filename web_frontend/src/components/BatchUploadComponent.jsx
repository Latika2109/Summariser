import React, { useState } from 'react';
import api from '../utils/api';
import './BatchUploadComponent.css';

function BatchUploadComponent({ onUploadComplete }) {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [results, setResults] = useState(null);

  const handleFileSelect = (e) => {
    const selectedFiles = Array.from(e.target.files);
    setFiles(selectedFiles);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFiles = Array.from(e.dataTransfer.files).filter(f => f.name.endsWith('.csv'));
    setFiles(droppedFiles);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const uploadFiles = async () => {
    if (files.length === 0) {
      alert('Please select files to upload');
      return;
    }

    setUploading(true);
    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });

    try {
      const response = await api.post('/batch-upload/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResults(response.data);
      if (onUploadComplete) {
        onUploadComplete();
      }
    } catch (error) {
      console.error('Error uploading files:', error);
      alert('Failed to upload files');
    }
    setUploading(false);
  };

  return (
    <div className="batch-upload-container">
      <h2>Batch Upload</h2>

      <div
        className="drop-zone"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
      >
        <p>Drag and drop CSV files here or</p>
        <input
          type="file"
          multiple
          accept=".csv"
          onChange={handleFileSelect}
          id="batch-file-input"
        />
        <label htmlFor="batch-file-input" className="file-button">
          Choose Files
        </label>
      </div>

      {files.length > 0 && (
        <div className="file-list">
          <h3>Selected Files ({files.length})</h3>
          <ul>
            {files.map((file, idx) => (
              <li key={idx}>
                {file.name} ({(file.size / 1024).toFixed(2)} KB)
              </li>
            ))}
          </ul>
          <button onClick={uploadFiles} disabled={uploading}>
            {uploading ? 'Uploading...' : `Upload ${files.length} Files`}
          </button>
        </div>
      )}

      {results && (
        <div className="upload-results">
          <h3>Upload Results</h3>
          <div className="results-summary">
            <span className="success">{results.successful} Successful</span>
            <span className="failed">{results.failed} Failed</span>
          </div>
          <div className="results-list">
            {results.results.map((result, idx) => (
              <div key={idx} className={`result-item ${result.success ? 'success' : 'error'}`}>
                <span>{result.filename}</span>
                {result.success ? (
                  <span className="status">Uploaded</span>
                ) : (
                  <span className="error-msg">{result.error}</span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default BatchUploadComponent;
