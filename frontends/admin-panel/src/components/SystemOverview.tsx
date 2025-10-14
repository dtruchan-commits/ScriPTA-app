import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { ApiService } from '../services/api';
import ChangeLog from './ChangeLog';
import { changelogEntries } from './ChangeLogData';
import EndpointList from './EndpointList';
import { endpointEntries } from './EndpointListData';

const SystemOverview: React.FC = () => {
  const [stats, setStats] = useState({
    swatches: 0,
    layerConfigs: 0,
    tpmConfigs: 0,
    loading: true,
    error: null as string | null
  });



  const [systemStatus, setSystemStatus] = useState({
    backendOnline: false,
    databaseConnected: false,
    loading: true,
    error: null as string | null
  });

  const checkSystemStatus = async (isInitialLoad = false) => {
    try {
      // Only show loading state on initial load to avoid flickering during periodic checks
      if (isInitialLoad) {
        setSystemStatus(prev => ({ ...prev, loading: true, error: null }));
        setStats(prev => ({ ...prev, loading: true, error: null }));
      }
      
      // Check if backend is online
      const isBackendOnline = await ApiService.checkBackendHealth();
      
      let isDatabaseConnected = false;
      let systemError = null;
      
      if (isBackendOnline) {
        // Check database connection only if backend is online
        isDatabaseConnected = await ApiService.checkDatabaseHealth();
        if (!isDatabaseConnected) {
          systemError = 'Database connection failed. Some features may not work properly.';
        }
      } else {
        systemError = 'Backend server is not responding. Please check if the server is running.';
      }
      
      setSystemStatus({
        backendOnline: isBackendOnline,
        databaseConnected: isDatabaseConnected,
        loading: false,
        error: systemError
      });
      
      // Only fetch stats if both backend and database are working
      if (isBackendOnline && isDatabaseConnected) {
        // Fetch all configs to get counts
        const [swatchData, layerData, tpmData] = await Promise.all([
          ApiService.getSwatchConfig().catch(() => ({ swatches: [] })),
          ApiService.getLayerConfig().catch(() => []),
          ApiService.getTpmConfig().catch(() => ({ tpms: [] }))
        ]);

        setStats({
          swatches: swatchData.swatches?.length || 0,
          layerConfigs: layerData.length || 0,
          tpmConfigs: tpmData.tpms?.length || 0,
          loading: false,
          error: null
        });
      } else {
        // Set stats to not loading but don't fetch data if there are system issues
        setStats(prev => ({
          ...prev,
          loading: false
        }));
      }
    } catch (error) {
      setSystemStatus(prev => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Failed to check system status'
      }));
      setStats(prev => ({
        ...prev,
        loading: false
      }));
    }
  };

  useEffect(() => {
    // Initial check
    checkSystemStatus(true);
    
    // Set up periodic checking every 10 seconds
    const interval = setInterval(() => {
      checkSystemStatus(false);
    }, 10000);
    
    // Cleanup interval on component unmount
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="system-overview">
      <div className="system-overview-header">
        <h2>System Overview</h2>
      </div>

      <div className="system-status">
        <h3>System Status</h3>
        <div className="status-indicators">
          <div className="status-item">
            <span className="status-label">Backend Server:</span>
            <span className={`status-indicator ${systemStatus.loading ? 'loading' : systemStatus.backendOnline ? 'online' : 'offline'}`}>
              {systemStatus.loading ? 'Checking...' : systemStatus.backendOnline ? 'Online' : 'Offline'}
            </span>
          </div>
          <div className="status-item">
            <span className="status-label">Database:</span>
            <span className={`status-indicator ${systemStatus.loading ? 'loading' : !systemStatus.backendOnline ? 'unknown' : systemStatus.databaseConnected ? 'connected' : 'disconnected'}`}>
              {systemStatus.loading ? 'Checking...' : !systemStatus.backendOnline ? 'Unknown' : systemStatus.databaseConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>
        </div>
        {systemStatus.error && (
          <div className="system-error-message">
            <h4>System Issue Detected</h4>
            <p>{systemStatus.error}</p>
          </div>
        )}
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-content">
            <h3>Swatch Configurations</h3>
            <div className="stat-number">
              {stats.loading ? '...' : stats.swatches}
            </div>
            <p>Color configurations for InDesign</p>
            <Link to="/swatches" className="stat-link">
              View Swatches →
            </Link>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-content">
            <h3>Layer Configurations</h3>
            <div className="stat-number">
              {stats.loading ? '...' : stats.layerConfigs}
            </div>
            <p>Layer settings and properties</p>
            <Link to="/layers" className="stat-link">
              View Layers →
            </Link>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-content">
            <h3>TPM Configurations</h3>
            <div className="stat-number">
              {stats.loading ? '...' : stats.tpmConfigs}
            </div>
            <p>Technical Packaging Material data</p>
            <Link to="/tpm" className="stat-link">
              View TPMs →
            </Link>
          </div>
        </div>
      </div>

      <div className="system-overview-info">

        <EndpointList entries={endpointEntries} />

                <ChangeLog entries={changelogEntries} />
      </div>
    </div>
  );
};

export default SystemOverview;