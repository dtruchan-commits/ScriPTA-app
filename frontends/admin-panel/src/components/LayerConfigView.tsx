import { useEffect, useState } from 'react';
import { ApiService } from '../services/api';
import type { LayerConfig, LayerConfigResponse } from '../types';

const LayerConfigView: React.FC = () => {
  const [layerData, setLayerData] = useState<LayerConfigResponse>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [filterConfigName, setFilterConfigName] = useState<string>('');

  const fetchLayerConfig = async (configName?: string) => {
    try {
      setLoading(true);
      setError(null);
      
      // Check if backend is online
      const isBackendOnline = await ApiService.checkBackendHealth();
      if (!isBackendOnline) {
        throw new Error('Backend server is not responding. Please check if the server is running.');
      }
      
      const data = await ApiService.getLayerConfig(configName || undefined);
      setLayerData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch layer configuration');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLayerConfig();
  }, []);

  const handleFilter = (e: React.FormEvent) => {
    e.preventDefault();
    fetchLayerConfig(filterConfigName.trim());
  };

  const handleClearFilter = () => {
    setFilterConfigName('');
    fetchLayerConfig();
  };

  const renderLayerTable = (layers: LayerConfig[]) => {
    return (
      <table className="layer-table">
        <thead>
          <tr>
            <th>Layer Name</th>
            <th>Locked</th>
            <th>Print Layer</th>
            <th>Layer Color</th>
          </tr>
        </thead>
        <tbody>
          {layers.map((layer, index) => (
            <tr key={index}>
              <td className="layer-name">{layer.name}</td>
              <td>
                <span className={`status-badge ${layer.locked ? 'locked' : 'unlocked'}`}>
                  {layer.locked ? '🔒 Locked' : '🔓 Unlocked'}
                </span>
              </td>
              <td>
                <input 
                  type="checkbox" 
                  checked={layer.print} 
                  readOnly
                  className="print-checkbox"
                />
              </td>
              <td>
                <span className={`color-badge ${layer.color.toLowerCase().replace('_', '-')}`}>
                  {layer.color}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  if (loading) {
    return (
      <div className="config-view">
        <h2>Layer Configuration</h2>
        <div className="loading">Loading layer data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="config-view">
        <h2>Layer Configuration</h2>
        <div className="error">Error: {error}</div>
        <button onClick={() => fetchLayerConfig()}>Retry</button>
      </div>
    );
  }

  return (
    <div className="config-view">
      <h2>Layer Configuration</h2>
      
      <div className="filter-section">
        <form onSubmit={handleFilter} className="filter-form">
          <input
            type="text"
            placeholder="Filter by config name (e.g., default, FoldingBox)"
            value={filterConfigName}
            onChange={(e) => setFilterConfigName(e.target.value)}
            className="filter-input"
          />
          <button type="submit" className="filter-button">Filter</button>
          <button type="button" onClick={handleClearFilter} className="clear-button">
            Clear
          </button>
        </form>
      </div>

      <div className="data-section">
        <h3>Results: {layerData.length} configuration sets</h3>
        
        {layerData.length > 0 ? (
          <div className="config-sets">
            {layerData.map((configSet, index) => (
              <div key={index} className="config-set">
                <h4 className="config-name">
                  {configSet.configName}
                  <span className="layer-count">({configSet.layers.length} layers)</span>
                </h4>
                <div className="table-container">
                  {renderLayerTable(configSet.layers)}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="no-data">
            {filterConfigName 
              ? `No layer configurations found for config name "${filterConfigName}"`
              : 'No layer configuration data available'
            }
          </div>
        )}
      </div>
    </div>
  );
};

export default LayerConfigView;