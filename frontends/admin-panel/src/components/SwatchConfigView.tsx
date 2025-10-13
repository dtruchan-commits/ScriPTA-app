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
      
      // Check if backend is online
      const isBackendOnline = await ApiService.checkBackendHealth();
      if (!isBackendOnline) {
        throw new Error('Backend server is not responding. Please check if the server is running.');
      }
      
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

  const renderColorPreview = (config: SwatchConfig) => {
    let backgroundColor = '#ffffff';
    
    // Handle CMYK color values
    if (config.colorSpace === 'CMYK' && config.colorValues.length >= 4) {
      const [c, m, y, k] = config.colorValues;
      
      // Convert CMYK to RGB approximation
      const r = 255 * (1 - c / 100) * (1 - k / 100);
      const g = 255 * (1 - m / 100) * (1 - k / 100);
      const b = 255 * (1 - y / 100) * (1 - k / 100);
      
      backgroundColor = `rgb(${Math.round(r)}, ${Math.round(g)}, ${Math.round(b)})`;
    }
    // Handle RGB color values
    else if (config.colorSpace === 'RGB' && config.colorValues.length >= 3) {
      const [r, g, b] = config.colorValues;
      backgroundColor = `rgb(${r}, ${g}, ${b})`;
    }
    // Handle LAB or other color spaces - show a placeholder pattern
    else {
      backgroundColor = 'linear-gradient(45deg, #ccc 25%, transparent 25%, transparent 75%, #ccc 75%), linear-gradient(45deg, #ccc 25%, transparent 25%, transparent 75%, #ccc 75%)';
    }

    return (
      <div 
        className="color-preview-circle"
        style={{
          width: '24px',
          height: '24px',
          borderRadius: '50%',
          border: '1px solid #ccc',
          background: backgroundColor,
          backgroundSize: '4px 4px',
          backgroundPosition: '0 0, 2px 2px',
          display: 'inline-block'
        }}
        title={`${config.colorName}: ${config.colorValues.join(', ')}`}
      />
    );
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
                  <th>Color Preview</th>
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
                    <td className="color-preview">{renderColorPreview(swatch)}</td>
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