import React, { useState, useEffect } from 'react';
import api from '../utils/api';
import './AlertsComponent.css';

function AlertsComponent({ datasetId }) {
  const [alerts, setAlerts] = useState([]);
  const [summary, setSummary] = useState(null);
  const [thresholds, setThresholds] = useState({
    flowrate: { warning: '', critical: '' },
    pressure: { warning: '', critical: '' },
    temperature: { warning: '', critical: '' }
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (datasetId) {
      fetchAlerts();
    }
    fetchThresholds();
  }, [datasetId]);

  const fetchAlerts = async () => {
    try {
      const response = await api.get(`/datasets/${datasetId}/alerts/`);
      setAlerts(response.data.alerts);
      setSummary(response.data.summary);
    } catch (error) {
      console.error('Error fetching alerts:', error);
    }
  };

  const fetchThresholds = async () => {
    try {
      const response = await api.get('/thresholds/');
      const thresholdData = {};
      response.data.forEach(t => {
        thresholdData[t.parameter] = {
          warning: t.warning_threshold || '',
          critical: t.critical_threshold || ''
        };
      });
      setThresholds(prev => ({ ...prev, ...thresholdData }));
    } catch (error) {
      console.error('Error fetching thresholds:', error);
    }
  };

  const saveThreshold = async (parameter) => {
    setLoading(true);
    try {
      await api.post('/thresholds/set/', {
        parameter,
        warning_threshold: parseFloat(thresholds[parameter].warning) || null,
        critical_threshold: parseFloat(thresholds[parameter].critical) || null
      });
      alert('Threshold saved successfully!');
      if (datasetId) {
        fetchAlerts();
      }
    } catch (error) {
      console.error('Error saving threshold:', error);
      alert('Failed to save threshold');
    }
    setLoading(false);
  };

  const updateThreshold = (parameter, type, value) => {
    setThresholds(prev => ({
      ...prev,
      [parameter]: {
        ...prev[parameter],
        [type]: value
      }
    }));
  };

  return (
    <div className="alerts-container">
      <h2>Equipment Alerts</h2>

      {/* Threshold Settings */}
      <div className="threshold-settings">
        <h3>Set Alert Thresholds</h3>
        {['flowrate', 'pressure', 'temperature'].map(param => (
          <div key={param} className="threshold-row">
            <label>{param.charAt(0).toUpperCase() + param.slice(1)}</label>
            <input
              type="number"
              placeholder="Warning"
              value={thresholds[param].warning}
              onChange={(e) => updateThreshold(param, 'warning', e.target.value)}
            />
            <input
              type="number"
              placeholder="Critical"
              value={thresholds[param].critical}
              onChange={(e) => updateThreshold(param, 'critical', e.target.value)}
            />
            <button onClick={() => saveThreshold(param)} disabled={loading}>
              Save
            </button>
          </div>
        ))}
      </div>

      {/* Alert Summary */}
      {summary && (
        <div className="alert-summary">
          <div className="summary-card critical">
            <h4>Critical</h4>
            <p className="count">{summary.critical_alerts}</p>
          </div>
          <div className="summary-card warning">
            <h4>Warning</h4>
            <p className="count">{summary.warning_alerts}</p>
          </div>
          <div className="summary-card normal">
            <h4>Normal</h4>
            <p className="count">{summary.normal}</p>
          </div>
        </div>
      )}
      {/* Alert List */}
      {alerts.length > 0 ? (
        <div className="alerts-list">
          <h3>Active Alerts</h3>
          {alerts.map((alert, index) => (
            <div key={index} className={`alert-item ${alert.level}`}>
              <span className="alert-level">
                {alert.level.toUpperCase()}
              </span>
              <div className="alert-details">
                <strong>{alert.equipment_name}</strong>
                <p>{alert.message}</p>
                <small>Value: {alert.value} | Threshold: {alert.threshold}</small>
              </div>
              <button
                className="root-cause-btn"
                onClick={() => analyzeRootCause(alert)}
              >
                Analyze Root Cause
              </button>
            </div>
          ))}
        </div>
      ) : (
        <p className="no-alerts">No alerts - All equipment operating normally</p>
      )}
    </div>
  );

  async function analyzeRootCause(alertItem) {
    const payload = {
      pressure: alertItem.message.includes('Pressure') ? alertItem.value : 0,
      temperature: alertItem.message.includes('Temperature') ? alertItem.value : 0,
      flowrate: alertItem.message.includes('Flowrate') ? alertItem.value : 0
    };

    try {
      const response = await api.post('/datasets/root_cause/', payload);
      const causes = response.data.causes.join('\n- ');
      window.alert(`AI Root Cause Analysis:\n\nPotential Causes:\n- ${causes}`);
    } catch (error) {
      console.error(error);
      window.alert("Failed to analyze root cause.");
    }
  }
}

export default AlertsComponent;
