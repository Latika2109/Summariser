import React, { useState, useEffect } from 'react';
import api from '../utils/api';
import './ComparisonComponent.css';

function ComparisonComponent() {
  const [datasets, setDatasets] = useState([]);
  const [dataset1, setDataset1] = useState('');
  const [dataset2, setDataset2] = useState('');
  const [comparison, setComparison] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchDatasets();
  }, []);

  const fetchDatasets = async () => {
    try {
      const response = await api.get('/datasets/');
      setDatasets(response.data);
    } catch (error) {
      console.error('Error fetching datasets:', error);
    }
  };

  const compareDatasets = async () => {
    if (!dataset1 || !dataset2) {
      alert('Please select two datasets to compare');
      return;
    }

    setLoading(true);
    try {
      const response = await api.post('/compare/', {
        dataset1_id: dataset1,
        dataset2_id: dataset2
      });
      setComparison(response.data);
    } catch (error) {
      console.error('Error comparing datasets:', error);
      alert('Failed to compare datasets');
    }
    setLoading(false);
  };

  return (
    <div className="comparison-container">
      <h2>Dataset Comparison</h2>

      <div className="comparison-selector">
        <div className="selector-group">
          <label>Dataset 1:</label>
          <select value={dataset1} onChange={(e) => setDataset1(e.target.value)}>
            <option value="">Select dataset...</option>
            {datasets.map(ds => (
              <option key={ds.id} value={ds.id}>{ds.filename}</option>
            ))}
          </select>
        </div>

        <div className="vs-divider">VS</div>

        <div className="selector-group">
          <label>Dataset 2:</label>
          <select value={dataset2} onChange={(e) => setDataset2(e.target.value)}>
            <option value="">Select dataset...</option>
            {datasets.map(ds => (
              <option key={ds.id} value={ds.id}>{ds.filename}</option>
            ))}
          </select>
        </div>

        <button onClick={compareDatasets} disabled={loading || !dataset1 || !dataset2}>
          {loading ? 'Comparing...' : 'Compare'}
        </button>
      </div>

      {comparison && (
        <div className="comparison-results">
          {/* Summary Cards */}
          <div className="comparison-summary">
            <div className="summary-card">
              <h4>Common Equipment</h4>
              <p className="count">{comparison.comparison.common_equipment}</p>
            </div>
            <div className="summary-card added">
              <h4>Added</h4>
              <p className="count">{comparison.comparison.added_equipment}</p>
            </div>
            <div className="summary-card removed">
              <h4>Removed</h4>
              <p className="count">{comparison.comparison.removed_equipment}</p>
            </div>
          </div>

          {/* Average Changes */}
          <div className="avg-changes">
            <h3>Average Parameter Changes</h3>
            <div className="change-grid">
              <div className="change-item">
                <span>Flowrate:</span>
                <strong className={comparison.comparison.summary.avg_flowrate_change >= 0 ? 'positive' : 'negative'}>
                  {comparison.comparison.summary.avg_flowrate_change >= 0 ? '+' : ''}
                  {comparison.comparison.summary.avg_flowrate_change.toFixed(2)}
                </strong>
              </div>
              <div className="change-item">
                <span>Pressure:</span>
                <strong className={comparison.comparison.summary.avg_pressure_change >= 0 ? 'positive' : 'negative'}>
                  {comparison.comparison.summary.avg_pressure_change >= 0 ? '+' : ''}
                  {comparison.comparison.summary.avg_pressure_change.toFixed(2)}
                </strong>
              </div>
              <div className="change-item">
                <span>Temperature:</span>
                <strong className={comparison.comparison.summary.avg_temperature_change >= 0 ? 'positive' : 'negative'}>
                  {comparison.comparison.summary.avg_temperature_change >= 0 ? '+' : ''}
                  {comparison.comparison.summary.avg_temperature_change.toFixed(2)}
                </strong>
              </div>
            </div>
          </div>

          {/* Significant Changes */}
          {comparison.significant_changes.length > 0 && (
            <div className="significant-changes">
              <h3>Significant Changes ({'>'}10%)</h3>
              <div className="changes-table">
                <table>
                  <thead>
                    <tr>
                      <th>Equipment</th>
                      <th>Flowrate</th>
                      <th>Pressure</th>
                      <th>Temperature</th>
                    </tr>
                  </thead>
                  <tbody>
                    {comparison.significant_changes.map((change, idx) => (
                      <tr key={idx}>
                        <td>{change.equipment_name}</td>
                        <td className={Math.abs(change.flowrate_percent) > 10 ? 'highlight' : ''}>
                          {change.flowrate_percent.toFixed(1)}%
                        </td>
                        <td className={Math.abs(change.pressure_percent) > 10 ? 'highlight' : ''}>
                          {change.pressure_percent.toFixed(1)}%
                        </td>
                        <td className={Math.abs(change.temperature_percent) > 10 ? 'highlight' : ''}>
                          {change.temperature_percent.toFixed(1)}%
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default ComparisonComponent;
