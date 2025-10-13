import { useEffect, useState } from 'react';
import { ApiService } from '../services/api';
import type { SwatchConfig, SwatchConfigResponse } from '../types';

const SwatchConfigView: React.FC = () => {
  const [swatchData, setSwatchData] = useState<SwatchConfigResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [filterColorName, setFilterColorName] = useState<string>('');

  const fetchSwatchConfig = async (colorName?: string) => {
    try {
      setLoading(true);
      setError(null);
      const data = await ApiService.getSwatchConfig(colorName || undefined);
      setSwatchData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch swatch configuration');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSwatchConfig();
  }, []);

  const handleFilter = (e: React.FormEvent) => {
    e.preventDefault();
    fetchSwatchConfig(filterColorName.trim());
  };

  const handleClearFilter = () => {
    setFilterColorName('');
    fetchSwatchConfig();
  };

  const renderColorValues = (config: SwatchConfig) => {
    return config.colorValues.join(', ');
  };

  if (loading) {
    return (
      <div className="config-view">
        <h2>Swatch Configuration</h2>
        <div className="loading">Loading swatch data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="config-view">
        <h2>Swatch Configuration</h2>
        <div className="error">Error: {error}</div>
        <button onClick={() => fetchSwatchConfig()}>Retry</button>
      </div>
    );
  }

  return (
    <div className="config-view">
      <h2>Swatch Configuration</h2>
      
      <div className="filter-section">
        <form onSubmit={handleFilter} className="filter-form">
          <input
            type="text"
            placeholder="Filter by color name (e.g., DIELINE)"
            value={filterColorName}
            onChange={(e) => setFilterColorName(e.target.value)}
            className="filter-input"
          />
          <button type="submit" className="filter-button">Filter</button>
          <button type="button" onClick={handleClearFilter} className="clear-button">
            Clear
          </button>
        </form>
      </div>

      <div className="data-section">
        <h3>Results: {swatchData?.swatches.length || 0} swatches</h3>
        
        {swatchData && swatchData.swatches.length > 0 ? (
          <div className="table-container">
            <table className="config-table">
              <thead>
                <tr>
                  <th>Color Name</th>
                  <th>Color Model</th>
                  <th>Color Space</th>
                  <th>Color Values</th>
                </tr>
              </thead>
              <tbody>
                {swatchData.swatches.map((swatch, index) => (
                  <tr key={index}>
                    <td className="color-name">{swatch.colorName}</td>
                    <td>
                      <span className={`badge ${swatch.colorModel.toLowerCase()}`}>
                        {swatch.colorModel}
                      </span>
                    </td>
                    <td>
                      <span className={`badge ${swatch.colorSpace.toLowerCase()}`}>
                        {swatch.colorSpace}
                      </span>
                    </td>
                    <td className="color-values">{renderColorValues(swatch)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="no-data">
            {filterColorName 
              ? `No swatches found for color name "${filterColorName}"`
              : 'No swatch data available'
            }
          </div>
        )}
      </div>
    </div>
  );
};

export default SwatchConfigView;