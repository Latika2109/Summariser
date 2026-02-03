import React, { useState, useEffect } from 'react';
import api from '../utils/api';
import './ValidationDashboard.css';

function ValidationDashboard({ datasetId }) {
  const [validation, setValidation] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (datasetId) {
      fetchValidation();
    }
  }, [datasetId]);

  const fetchValidation = async () => {
    setLoading(true);
    try {
      const response = await api.get(`/datasets/${datasetId}/validate/`);
      setValidation(response.data);
    } catch (error) {
      console.error('Error fetching validation:', error);
    }
    setLoading(false);
  };

  if (loading) return <div className="loading">Validating data...</div>;
  if (!validation) return null;

  const getScoreColor = (score) => {
    if (score >= 90) return '#10b981';
    if (score >= 70) return '#f59e0b';
    return '#f5576c';
  };

  return (
    <div className="validation-dashboard">
      <h2>Data Quality Report</h2>

      {/* Quality Score */}
      <div className="quality-score" style={{ borderColor: getScoreColor(validation.quality_score) }}>
        <div className="score-circle" style={{ background: getScoreColor(validation.quality_score) }}>
          <span className="score">{validation.quality_score.toFixed(1)}</span>
          <span className="label">Quality Score</span>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="metrics-grid">
        <div className="metric-card">
          <h4>Total Records</h4>
          <p className="value">{validation.total_records}</p>
        </div>
        <div className="metric-card">
          <h4>Missing Values</h4>
          <p className="value">{validation.missing_values}</p>
        </div>
        <div className="metric-card">
          <h4>Duplicates</h4>
          <p className="value">{validation.duplicate_records}</p>
        </div>
        <div className="metric-card">
          <h4>Outliers</h4>
          <p className="value">{validation.outliers_count}</p>
        </div>
      </div>

      {/* Outlier Details */}
      {validation.details.outliers && validation.details.outliers.length > 0 && (
        <div className="outliers-section">
          <h3>Outlier Analysis</h3>
          {validation.details.outliers.map((outlier, idx) => (
            <div key={idx} className="outlier-card">
              <h4>{outlier.parameter.toUpperCase()}</h4>
              <p>Found {outlier.count} outliers</p>
              <p className="range">
                Valid range: {outlier.lower_bound.toFixed(2)} - {outlier.upper_bound.toFixed(2)}
              </p>
              {outlier.equipment && outlier.equipment.length > 0 && (
                <div className="equipment-list">
                  <strong>Affected equipment:</strong>
                  <ul>
                    {outlier.equipment.map((eq, i) => (
                      <li key={i}>{eq}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Statistics */}
      <div className="statistics-section">
        <h3>Parameter Statistics</h3>
        <div className="stats-grid">
          {Object.entries(validation.details.statistics || {}).map(([param, stats]) => (
            <div key={param} className="stat-card">
              <h4>{param.toUpperCase()}</h4>
              <div className="stat-row">
                <span>Min:</span>
                <strong>{stats.min.toFixed(2)}</strong>
              </div>
              <div className="stat-row">
                <span>Max:</span>
                <strong>{stats.max.toFixed(2)}</strong>
              </div>
              <div className="stat-row">
                <span>Mean:</span>
                <strong>{stats.mean.toFixed(2)}</strong>
              </div>
              <div className="stat-row">
                <span>Std Dev:</span>
                <strong>{stats.std.toFixed(2)}</strong>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ValidationDashboard;
