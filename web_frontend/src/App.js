import React, { useState, useEffect } from 'react';
import LoginComponent from './components/LoginComponent';
import UploadComponent from './components/UploadComponent';
import ChartsComponent from './components/ChartsComponent';
import HistoryComponent from './components/HistoryComponent';
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [currentView, setCurrentView] = useState('upload');
  const [selectedDataset, setSelectedDataset] = useState(null);

  useEffect(() => {
    // check if user is already logged in
    const token = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');

    if (token && savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  const handleLoginSuccess = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    setCurrentView('upload');
    setSelectedDataset(null);
  };

  const handleUploadSuccess = (dataset) => {
    setSelectedDataset(dataset);
    setCurrentView('charts');
  };

  const handleSelectDataset = (dataset) => {
    setSelectedDataset(dataset);
    setCurrentView('charts');
  };

  if (!user) {
    return <LoginComponent onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div className="app">
      <nav className="navbar">
        <div className="nav-container">
          <h1 className="app-title">Chemical Equipment Visualizer</h1>
          <div className="nav-links">
            <button
              className={currentView === 'upload' ? 'active' : ''}
              onClick={() => setCurrentView('upload')}
            >
              Upload
            </button>
            <button
              className={currentView === 'history' ? 'active' : ''}
              onClick={() => setCurrentView('history')}
            >
              History
            </button>
            {selectedDataset && (
              <button
                className={currentView === 'charts' ? 'active' : ''}
                onClick={() => setCurrentView('charts')}
              >
                View Data
              </button>
            )}
            <div className="user-info">
              <span>Welcome, {user.username}</span>
              <button onClick={handleLogout} className="logout-btn">
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="main-content">
        {currentView === 'upload' && (
          <UploadComponent onUploadSuccess={handleUploadSuccess} />
        )}

        {currentView === 'history' && (
          <HistoryComponent onSelectDataset={handleSelectDataset} />
        )}

        {currentView === 'charts' && selectedDataset && (
          <ChartsComponent dataset={selectedDataset} />
        )}
      </main>
    </div>
  );
}

export default App;
