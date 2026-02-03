import React, { useState, useEffect } from 'react';
import api from '../utils/api';
import './HealthDashboard.css';

function HealthDashboard({ datasetId }) {
  const [healthData, setHealthData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (datasetId) {
      fetchHealthAnalysis();
    }
  }, [datasetId]);

  const fetchHealthAnalysis = async () => {
    setLoading(true);
    try {
      const response = await api.get(`/datasets/${datasetId}/health_analysis/`);
      setHealthData(response.data);
    } catch (error) {
      console.error('Error fetching health analysis:', error);
    }
    setLoading(false);
  };

  if (loading) return <div className="loading">Analyzing Equipment Health...</div>;
  if (!healthData.length) return <div className="no-data">No health data available</div>;

  // Split for layout
  const criticalItems = healthData.filter(i => i.status === 'Critical');
  const warningItems = healthData.filter(i => i.status === 'Warning');
  const goodItems = healthData.filter(i => i.status === 'Good');

  // Sort by power index descending for "Efficiency" list
  const powerSorted = [...healthData].sort((a, b) => b.power_index - a.power_index).slice(0, 10);

  return (
    <div className="health-dashboard">
      <div className="health-header">
        <h2>Health & Efficiency Analytics</h2>
        <p>Real-time equipment condition monitoring and power index analysis</p>
      </div>

      <div className="health-grid">
        {/* Left: Health Heatmap */}
        <div className="heatmap-card">
          <h3>Equipment Health Heatmap</h3>
          <p className="subtitle">Visualizing deviation from optimal parameters</p>

          <div className="heatmap-container">
            {healthData.map((item) => (
              <div
                key={item.id}
                className={`heat-cell ${item.status.toLowerCase()}`}
                title={`Flow: ${item.flowrate} | Press: ${item.pressure} | Temp: ${item.temperature}`}
              >
                <span className="heat-val">{item.health_score}</span>
                <span className="heat-label">{item.name}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Right: High Power Consumers */}
        <div className="efficiency-card">
          <h3>Power Intensity Index</h3>
          <p className="subtitle">Top energy consumers (Flow × Pressure)</p>

          <div className="efficiency-list">
            {powerSorted.map((item) => (
              <div key={item.id} className="power-item">
                <div className="power-info">
                  <h4>{item.name}</h4>
                  <span>{item.type}</span>
                </div>
                <div className="power-val">
                  <span className="p-index">{item.power_index.toFixed(0)}</span>
                  <span className="p-label">Hydraulic Power</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default HealthDashboard;
