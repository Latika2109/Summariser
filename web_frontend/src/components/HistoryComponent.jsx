import React, { useEffect, useState } from 'react';
import { getDatasets, downloadPDF, downloadExcel } from '../utils/api';
import './HistoryComponent.css';

function HistoryComponent({ onSelectDataset }) {
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDatasets();
  }, []);

  const fetchDatasets = async () => {
    try {
      const response = await getDatasets();
      setDatasets(response.data);
    } catch (err) {
      setError('Failed to load history');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = async (datasetId, filename) => {
    try {
      const response = await downloadPDF(datasetId);

      // create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `report_${filename}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      alert('Failed to download PDF');
    }
  };

  const handleDownloadExcel = async (datasetId, filename) => {
    try {
      const response = await downloadExcel(datasetId);

      // create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `dataset_${filename}.xlsx`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      alert('Failed to download Excel');
    }
  };

  if (loading) {
    return <div className="loading">Loading history...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="history-container">
      <h2>Upload History (Last 5)</h2>

      {datasets.length === 0 ? (
        <p className="no-history">No uploads yet</p>
      ) : (
        <div className="history-grid">
          {datasets.map((dataset) => (
            <div key={dataset.id} className="history-card">
              <div className="card-header">
                <h3>{dataset.filename}</h3>
                <span className="upload-date">
                  {new Date(dataset.uploaded_at).toLocaleString()}
                </span>
              </div>

              <div className="card-stats">
                <div className="stat-item">
                  <span className="stat-label">Total Equipment:</span>
                  <span className="stat-value">{dataset.total_equipment}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Avg Flowrate:</span>
                  <span className="stat-value">{dataset.avg_flowrate?.toFixed(2)}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Avg Pressure:</span>
                  <span className="stat-value">{dataset.avg_pressure?.toFixed(2)}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Avg Temperature:</span>
                  <span className="stat-value">{dataset.avg_temperature?.toFixed(2)}</span>
                </div>
              </div>

              <div className="card-actions">
                <button
                  onClick={() => onSelectDataset(dataset)}
                  className="view-btn"
                >
                  View Details
                </button>
                <button
                  onClick={() => handleDownloadPDF(dataset.id, dataset.filename)}
                  className="pdf-btn"
                >
                  Download PDF
                </button>
                <button
                  onClick={() => handleDownloadExcel(dataset.id, dataset.filename)}
                  className="excel-btn"
                >
                  Export Excel
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default HistoryComponent;
