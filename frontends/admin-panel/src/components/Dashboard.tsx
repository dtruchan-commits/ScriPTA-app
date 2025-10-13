import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { ApiService } from '../services/api';

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState({
    swatches: 0,
    layerConfigs: 0,
    tpmConfigs: 0,
    loading: true,
    error: null as string | null
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setStats(prev => ({ ...prev, loading: true, error: null }));
        
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
      } catch (error) {
        setStats(prev => ({
          ...prev,
          loading: false,
          error: error instanceof Error ? error.message : 'Failed to load statistics'
        }));
      }
    };

    fetchStats();
  }, []);

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Dashboard</h2>
        <p>Welcome to the ScriPTA Configuration Management System</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">🎨</div>
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
          <div className="stat-icon">📋</div>
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
          <div className="stat-icon">📦</div>
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

      {stats.error && (
        <div className="error-message">
          <h4>Error loading statistics</h4>
          <p>{stats.error}</p>
        </div>
      )}

      <div className="dashboard-info">
        <div className="info-section">
          <h3>About ScriPTA</h3>
          <p>
            ScriPTA is a REST API for managing Technical Packaging Material Data and 
            InDesign Swatch and Layer Configurations. This admin panel provides a 
            user-friendly interface to view and manage configuration data.
          </p>
        </div>

        <div className="info-section">
          <h3>Available Endpoints</h3>
          <ul className="endpoint-list">
            <li><code>GET /get_swatch_config</code> - Retrieve swatch configurations</li>
            <li><code>GET /get_layer_config</code> - Retrieve layer configurations</li>
            <li><code>GET /get_tpm_config</code> - Retrieve TPM configurations</li>
          </ul>
        </div>

        <div className="info-section">
          <h3>Features</h3>
          <ul className="feature-list">
            <li>✅ Read access to all configuration types</li>
            <li>🔍 Filtering capabilities for all endpoints</li>
            <li>📊 Real-time data loading with error handling</li>
            <li>📱 Responsive design for all devices</li>
            <li>🔄 Future: CRUD operations (Create, Update, Delete)</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;