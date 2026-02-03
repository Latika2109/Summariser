import React, { useState, useEffect } from 'react';
import LoginComponent from './components/LoginComponent';
import UploadComponent from './components/UploadComponent';
import ChartsComponent from './components/ChartsComponent';
import HistoryComponent from './components/HistoryComponent';
import AlertsComponent from './components/AlertsComponent';
import ComparisonComponent from './components/ComparisonComponent';
import BatchUploadComponent from './components/BatchUploadComponent';
import ValidationDashboard from './components/ValidationDashboard';
import HealthDashboard from './components/HealthDashboard';
import ChatWidget from './components/ChatWidget'; // NEW IMPORT
import { DarkModeProvider, useDarkMode } from './components/DarkModeToggle';
import './App.css';

function AppContent() {
  const [user, setUser] = useState(null);
  const [currentView, setCurrentView] = useState('upload');
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(window.innerWidth < 768);
  const { darkMode, toggleDarkMode } = useDarkMode();

  // Handle window resize
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 768) {
        setSidebarCollapsed(true);
      } else {
        setSidebarCollapsed(false);
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  useEffect(() => {
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

  const toggleSidebar = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };

  if (!user) {
    return <LoginComponent onLoginSuccess={handleLoginSuccess} />;
  }

  const getPageTitle = () => {
    const titles = {
      upload: 'Upload Data',
      batch: 'Batch Upload',
      history: 'Dataset History',
      charts: 'Analytics Dashboard',
      alerts: 'Equipment Alerts',
      validation: 'Data Quality',
      health: 'Health & Efficiency',
      compare: 'Dataset Comparison'
    };
    return titles[currentView] || 'Dashboard';
  };

  return (
    <div className="app">
      {/* Sidebar Navigation */}
      <div className={`sidebar ${sidebarCollapsed ? 'collapsed' : ''}`}>
        <div className="sidebar-header">
          <h1 className="app-title">
            {sidebarCollapsed ? 'CEV' : 'Chemical Equipment Visualizer'}
          </h1>
        </div>

        <nav className="sidebar-nav">
          <div className="nav-section">
            {!sidebarCollapsed && <h3 className="nav-section-title">Main</h3>}
            <button
              className={`nav-item ${currentView === 'upload' ? 'active' : ''}`}
              onClick={() => setCurrentView('upload')}
              title="Upload"
            >
              <span className="nav-item-icon">↑</span>
              {!sidebarCollapsed && <span>Upload</span>}
            </button>
            <button
              className={`nav-item ${currentView === 'batch' ? 'active' : ''}`}
              onClick={() => setCurrentView('batch')}
              title="Batch Upload"
            >
              <span className="nav-item-icon">⇈</span>
              {!sidebarCollapsed && <span>Batch Upload</span>}
            </button>
            <button
              className={`nav-item ${currentView === 'history' ? 'active' : ''}`}
              onClick={() => setCurrentView('history')}
              title="History"
            >
              <span className="nav-item-icon">◷</span>
              {!sidebarCollapsed && <span>History</span>}
            </button>
          </div>

          {selectedDataset && (
            <div className="nav-section">
              {!sidebarCollapsed && <h3 className="nav-section-title">Analytics</h3>}
              <button
                className={`nav-item ${currentView === 'charts' ? 'active' : ''}`}
                onClick={() => setCurrentView('charts')}
                title="Charts"
              >
                <span className="nav-item-icon">◫</span>
                {!sidebarCollapsed && <span>Charts</span>}
              </button>
              <button
                className={`nav-item ${currentView === 'alerts' ? 'active' : ''}`}
                onClick={() => setCurrentView('alerts')}
                title="Alerts"
              >
                <span className="nav-item-icon">⚠</span>
                {!sidebarCollapsed && <span>Alerts</span>}
              </button>
              <button
                className={`nav-item ${currentView === 'validation' ? 'active' : ''}`}
                onClick={() => setCurrentView('validation')}
                title="Validation"
              >
                <span className="nav-item-icon">✓</span>
                {!sidebarCollapsed && <span>Validation</span>}
              </button>
              <button
                className={`nav-item ${currentView === 'health' ? 'active' : ''}`}
                onClick={() => setCurrentView('health')}
                title="Health & Efficiency"
              >
                <span className="nav-item-icon">♥</span>
                {!sidebarCollapsed && <span>Health</span>}
              </button>
            </div>
          )}

          <div className="nav-section">
            {!sidebarCollapsed && <h3 className="nav-section-title">Tools</h3>}
            <button
              className={`nav-item ${currentView === 'compare' ? 'active' : ''}`}
              onClick={() => setCurrentView('compare')}
              title="Compare"
            >
              <span className="nav-item-icon">⇄</span>
              {!sidebarCollapsed && <span>Compare</span>}
            </button>
          </div>
        </nav>

        <div className="sidebar-footer">
          {!sidebarCollapsed ? (
            <div className="user-profile">
              <div className="user-avatar">
                {user.username.charAt(0).toUpperCase()}
              </div>
              <div className="user-info">
                <p className="user-name">{user.username}</p>
              </div>
              <button onClick={handleLogout} className="logout-btn">
                Logout
              </button>
            </div>
          ) : (
            <div className="user-profile-collapsed">
              <div className="user-avatar" title={user.username}>
                {user.username.charAt(0).toUpperCase()}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Main Content Area */}
      <div className="main-container">
        <header className="top-header">
          <div className="header-left">
            <button className="sidebar-toggle" onClick={toggleSidebar}>
              {sidebarCollapsed ? '☰' : '←'}
            </button>
            <h2 className="page-title">{getPageTitle()}</h2>
          </div>
          <div className="header-actions">
            <button className="dark-mode-toggle" onClick={toggleDarkMode}>
              {darkMode ? 'Light Mode' : 'Dark Mode'}
            </button>
          </div>
        </header>

        <main className="main-content">
          {currentView === 'upload' && (
            <UploadComponent onUploadSuccess={handleUploadSuccess} />
          )}

          {currentView === 'batch' && (
            <BatchUploadComponent onUploadComplete={() => setCurrentView('history')} />
          )}

          {currentView === 'history' && (
            <HistoryComponent onSelectDataset={handleSelectDataset} />
          )}

          {currentView === 'charts' && selectedDataset && (
            <ChartsComponent dataset={selectedDataset} />
          )}

          {currentView === 'alerts' && selectedDataset && (
            <AlertsComponent datasetId={selectedDataset.id} />
          )}

          {currentView === 'validation' && selectedDataset && (
            <ValidationDashboard datasetId={selectedDataset.id} />
          )}

          {currentView === 'health' && selectedDataset && (
            <HealthDashboard datasetId={selectedDataset.id} />
          )}

          {currentView === 'compare' && (
            <ComparisonComponent />
          )}

          {/* AI Chat Widget */}
          <ChatWidget
            datasetId={selectedDataset?.id}
            navigateTo={(view) => {
              if (view === 'DASHBOARD') setCurrentView('charts');
              else if (view === 'ALERTS') setCurrentView('alerts');
              else if (view === 'HISTORY') setCurrentView('history');
              else if (view === 'HEALTH') setCurrentView('health');
            }}
          />
        </main>
      </div>
    </div>
  );
}

function App() {
  return (
    <DarkModeProvider>
      <AppContent />
    </DarkModeProvider>
  );
}

export default App;
