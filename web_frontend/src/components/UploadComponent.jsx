import React, { useState } from 'react';
import { uploadCSV } from '../utils/api';
import './UploadComponent.css';

function UploadComponent({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    setUploading(true);
    setError('');

    try {
      const response = await uploadCSV(file);
      onUploadSuccess(response.data);
      setFile(null);
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload Equipment Data</h2>

      <div
        className={`drop-zone ${dragActive ? 'active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          id="file-input"
          style={{ display: 'none' }}
        />

        <label htmlFor="file-input" className="file-label">
          {file ? (
            <div className="file-info">
              <span className="file-icon">📄</span>
              <span className="file-name">{file.name}</span>
            </div>
          ) : (
            <div className="upload-prompt">
              <span className="upload-icon">⬆️</span>
              <p>Drag and drop CSV file here or click to browse</p>
            </div>
          )}
        </label>
      </div>

      {error && <div className="error-message">{error}</div>}

      <button
        onClick={handleUpload}
        disabled={!file || uploading}
        className="upload-btn"
      >
        {uploading ? 'Uploading...' : 'Upload CSV'}
      </button>
    </div>
  );
}

export default UploadComponent;
