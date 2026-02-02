import React, { useEffect, useState } from 'react';
import { Bar, Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import './ChartsComponent.css';

// register chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function ChartsComponent({ dataset }) {
  const [typeChartData, setTypeChartData] = useState(null);
  const [tempChartData, setTempChartData] = useState(null);

  useEffect(() => {
    if (dataset) {
      // prepare type distribution chart
      const types = Object.keys(dataset.type_distribution);
      const counts = Object.values(dataset.type_distribution);

      setTypeChartData({
        labels: types,
        datasets: [
          {
            label: 'Equipment Count',
            data: counts,
            backgroundColor: 'rgba(102, 126, 234, 0.6)',
            borderColor: 'rgba(102, 126, 234, 1)',
            borderWidth: 1,
          },
        ],
      });

      // prepare temperature chart
      const records = dataset.records || [];
      const equipmentNames = records.map(r => r.equipment_name);
      const temperatures = records.map(r => r.temperature);

      setTempChartData({
        labels: equipmentNames,
        datasets: [
          {
            label: 'Temperature (°C)',
            data: temperatures,
            backgroundColor: 'rgba(255, 99, 132, 0.6)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 2,
            fill: false,
          },
        ],
      });
    }
  }, [dataset]);

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
    },
  };

  if (!dataset) {
    return <div className="no-data">No data to display</div>;
  }

  return (
    <div className="charts-container">
      <h2>Data Visualization</h2>

      {/* summary stats */}
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Equipment</h3>
          <p className="stat-value">{dataset.total_equipment}</p>
        </div>
        <div className="stat-card">
          <h3>Avg Flowrate</h3>
          <p className="stat-value">{dataset.avg_flowrate?.toFixed(2)}</p>
        </div>
        <div className="stat-card">
          <h3>Avg Pressure</h3>
          <p className="stat-value">{dataset.avg_pressure?.toFixed(2)}</p>
        </div>
        <div className="stat-card">
          <h3>Avg Temperature</h3>
          <p className="stat-value">{dataset.avg_temperature?.toFixed(2)}</p>
        </div>
      </div>

      {/* charts */}
      <div className="charts-grid">
        <div className="chart-box">
          <h3>Equipment Type Distribution</h3>
          <div className="chart-wrapper">
            {typeChartData && <Bar data={typeChartData} options={chartOptions} />}
          </div>
        </div>

        <div className="chart-box">
          <h3>Temperature by Equipment</h3>
          <div className="chart-wrapper">
            {tempChartData && <Line data={tempChartData} options={chartOptions} />}
          </div>
        </div>
      </div>

      {/* data table */}
      <div className="data-table-container">
        <h3>Equipment Records</h3>
        <div className="table-wrapper">
          <table className="data-table">
            <thead>
              <tr>
                <th>Equipment Name</th>
                <th>Type</th>
                <th>Flowrate</th>
                <th>Pressure</th>
                <th>Temperature</th>
              </tr>
            </thead>
            <tbody>
              {dataset.records?.map((record) => (
                <tr key={record.id}>
                  <td>{record.equipment_name}</td>
                  <td>{record.equipment_type}</td>
                  <td>{record.flowrate}</td>
                  <td>{record.pressure}</td>
                  <td>{record.temperature}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default ChartsComponent;
