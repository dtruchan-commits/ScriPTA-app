import { useEffect, useState } from 'react';
import { ApiService } from '../services/api';
import type { SwatchConfig, SwatchConfigResponse } from '../types';

interface EditableSwatchState {
  [key: string]: {
    isEditing: boolean;
    originalData: SwatchConfig;
    editData: SwatchConfig;
    isSaving: boolean;
    isDeleting: boolean;
  };
}

const SwatchConfigView: React.FC = () => {
  const [swatchData, setSwatchData] = useState<SwatchConfigResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [filterColorName, setFilterColorName] = useState<string>('');
  const [editableStates, setEditableStates] = useState<EditableSwatchState>({});

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
      // Reset editing states when fetching new data
      setEditableStates({});
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch swatch configuration');
    } finally {
      setLoading(false);
    }
  };

  const startEditing = (swatch: SwatchConfig, index: number) => {
    const key = `${swatch.colorName}-${index}`;
    // Ensure color values array has correct number of elements based on color space
    const colorValues = [...swatch.colorValues];
    const requiredLength = swatch.colorSpace === 'RGB' ? 3 : 4;
    
    // Pad with zeros if too short
    while (colorValues.length < requiredLength) {
      colorValues.push(0);
    }
    // Trim if too long
    colorValues.length = requiredLength;
    
    setEditableStates(prev => ({
      ...prev,
      [key]: {
        isEditing: true,
        originalData: swatch,
        editData: { ...swatch, colorValues },
        isSaving: false,
        isDeleting: false
      }
    }));
  };

  const cancelEditing = (swatch: SwatchConfig, index: number) => {
    const key = `${swatch.colorName}-${index}`;
    setEditableStates(prev => {
      const newState = { ...prev };
      delete newState[key];
      return newState;
    });
  };

  const saveChanges = async (swatch: SwatchConfig, index: number) => {
    const key = `${swatch.colorName}-${index}`;
    const editState = editableStates[key];
    if (!editState) return;

    setEditableStates(prev => ({
      ...prev,
      [key]: { ...prev[key], isSaving: true }
    }));

    try {
      const updatedSwatch = await ApiService.updateSwatchConfig(
        editState.originalData.colorName,
        editState.editData
      );

      // Update the local data
      if (swatchData) {
        const newSwatches = [...swatchData.swatches];
        newSwatches[index] = updatedSwatch;
        setSwatchData({ swatches: newSwatches });
      }

      // Clear editing state
      setEditableStates(prev => {
        const newState = { ...prev };
        delete newState[key];
        return newState;
      });

      // Clear any previous errors
      setError(null);
    } catch (err) {
      console.error('Error updating swatch:', err);
      setError(err instanceof Error ? err.message : 'Failed to update swatch configuration');
      setEditableStates(prev => ({
        ...prev,
        [key]: { ...prev[key], isSaving: false }
      }));
    }
  };

  const deleteSwatch = async (swatch: SwatchConfig, index: number) => {
    const key = `${swatch.colorName}-${index}`;
    const editState = editableStates[key];
    if (!editState) return;

    // Show confirmation dialog
    const confirmed = window.confirm(`Are you sure you want to delete the swatch "${swatch.colorName}"? This action cannot be undone.`);
    if (!confirmed) return;

    setEditableStates(prev => ({
      ...prev,
      [key]: { ...prev[key], isDeleting: true }
    }));

    try {
      await ApiService.deleteSwatchConfig(swatch.colorName);

      // Remove the swatch from local data
      if (swatchData) {
        const newSwatches = swatchData.swatches.filter((_, i) => i !== index);
        setSwatchData({ swatches: newSwatches });
      }

      // Clear editing state
      setEditableStates(prev => {
        const newState = { ...prev };
        delete newState[key];
        return newState;
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete swatch configuration');
      setEditableStates(prev => ({
        ...prev,
        [key]: { ...prev[key], isDeleting: false }
      }));
    }
  };

  const updateEditData = (swatch: SwatchConfig, index: number, field: keyof SwatchConfig, value: any) => {
    const key = `${swatch.colorName}-${index}`;
    setEditableStates(prev => ({
      ...prev,
      [key]: {
        ...prev[key],
        editData: {
          ...prev[key].editData,
          [field]: value
        }
      }
    }));
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

  const renderEditableColorName = (swatch: SwatchConfig, index: number) => {
    const key = `${swatch.colorName}-${index}`;
    const editState = editableStates[key];
    
    if (editState?.isEditing) {
      return (
        <input
          type="text"
          value={editState.editData.colorName}
          onChange={(e) => updateEditData(swatch, index, 'colorName', e.target.value)}
          className="edit-input color-name-input"
        />
      );
    }
    
    return <span className="color-name">{swatch.colorName}</span>;
  };

  const renderEditableColorModel = (swatch: SwatchConfig, index: number) => {
    const key = `${swatch.colorName}-${index}`;
    const editState = editableStates[key];
    
    if (editState?.isEditing) {
      return (
        <select
          value={editState.editData.colorModel}
          onChange={(e) => updateEditData(swatch, index, 'colorModel', e.target.value)}
          className="edit-select"
        >
          <option value="SPOT">SPOT</option>
          <option value="PROCESS">PROCESS</option>
        </select>
      );
    }
    
    return (
      <span className={`badge ${swatch.colorModel.toLowerCase()}`}>
        {swatch.colorModel}
      </span>
    );
  };

  const renderEditableColorSpace = (swatch: SwatchConfig, index: number) => {
    const key = `${swatch.colorName}-${index}`;
    const editState = editableStates[key];
    
    if (editState?.isEditing) {
      return (
        <select
          value={editState.editData.colorSpace}
          onChange={(e) => {
            const newColorSpace = e.target.value;
            const currentValues = [...editState.editData.colorValues];
            
            // Adjust color values array based on color space
            let newValues: number[];
            if (newColorSpace === 'RGB') {
              // RGB needs 3 values (R, G, B), convert from 0-100 to 0-255 if coming from CMYK/LAB
              newValues = currentValues.slice(0, 3).map(val => 
                editState.editData.colorSpace !== 'RGB' ? Math.round(val * 2.55) : val
              );
              // Ensure we have exactly 3 values
              while (newValues.length < 3) newValues.push(0);
              newValues.length = 3;
            } else {
              // CMYK and LAB need 4 values, convert from 0-255 to 0-100 if coming from RGB
              newValues = currentValues.slice(0, 4).map(val => 
                editState.editData.colorSpace === 'RGB' ? Math.round(val / 2.55) : val
              );
              // Ensure we have exactly 4 values
              while (newValues.length < 4) newValues.push(0);
              newValues.length = 4;
            }
            
            // Update both color space and values
            setEditableStates(prev => ({
              ...prev,
              [key]: {
                ...prev[key],
                editData: {
                  ...prev[key].editData,
                  colorSpace: newColorSpace as any,
                  colorValues: newValues
                }
              }
            }));
          }}
          className="edit-select"
        >
          <option value="CMYK">CMYK</option>
          <option value="RGB">RGB</option>
          <option value="LAB">LAB</option>
        </select>
      );
    }
    
    return (
      <span className={`badge ${swatch.colorSpace.toLowerCase()}`}>
        {swatch.colorSpace}
      </span>
    );
  };

  const renderEditableColorValues = (swatch: SwatchConfig, index: number) => {
    const key = `${swatch.colorName}-${index}`;
    const editState = editableStates[key];
    
    if (editState?.isEditing) {
      // Determine number of values based on color space
      const numValues = editState.editData.colorSpace === 'RGB' ? 3 : 4;
      const labels = editState.editData.colorSpace === 'RGB' 
        ? ['R', 'G', 'B'] 
        : editState.editData.colorSpace === 'CMYK' 
          ? ['C', 'M', 'Y', 'K'] 
          : ['Value 1', 'Value 2', 'Value 3', 'Value 4'];

      return (
        <div className="color-values-edit">
          {Array.from({ length: numValues }, (_, i) => (
            <input
              key={i}
              type="number"
              min="0"
              max={editState.editData.colorSpace === 'RGB' ? "255" : "100"}
              value={editState.editData.colorValues[i] || 0}
              onChange={(e) => {
                const newValues = [...editState.editData.colorValues];
                const value = parseInt(e.target.value) || 0;
                // RGB values range 0-255, others range 0-100
                const maxValue = editState.editData.colorSpace === 'RGB' ? 255 : 100;
                newValues[i] = Math.max(0, Math.min(maxValue, value));
                updateEditData(swatch, index, 'colorValues', newValues);
              }}
              className="edit-input color-value-input"
              placeholder={labels[i]}
              title={labels[i]}
            />
          ))}
        </div>
      );
    }
    
    return <span className="color-values">{renderColorValues(swatch)}</span>;
  };

  const renderActionButtons = (swatch: SwatchConfig, index: number) => {
    const key = `${swatch.colorName}-${index}`;
    const editState = editableStates[key];
    
    if (editState?.isEditing) {
      return (
        <div className="action-buttons">
          <button
            onClick={() => saveChanges(swatch, index)}
            disabled={editState.isSaving || editState.isDeleting || !editState.editData.colorName.trim()}
            className="save-button"
            title={!editState.editData.colorName.trim() ? "Color name cannot be empty" : ""}
          >
            {editState.isSaving ? 'Saving...' : 'Save'}
          </button>
          <button
            onClick={() => cancelEditing(swatch, index)}
            disabled={editState.isSaving || editState.isDeleting}
            className="cancel-button"
          >
            Cancel
          </button>
          <button
            onClick={() => deleteSwatch(swatch, index)}
            disabled={editState.isSaving || editState.isDeleting}
            className="delete-button"
            title="Delete this swatch permanently"
          >
            {editState.isDeleting ? 'Deleting...' : 'Delete'}
          </button>
        </div>
      );
    }
    
    return (
      <button
        onClick={() => startEditing(swatch, index)}
        className="edit-button"
      >
        Edit
      </button>
    );
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
                  <th>Color Values (RGB: 0-255, Others: 0-100)</th>
                  <th>Color Preview</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {swatchData.swatches.map((swatch, index) => (
                  <tr key={index}>
                    <td>{renderEditableColorName(swatch, index)}</td>
                    <td>{renderEditableColorModel(swatch, index)}</td>
                    <td>{renderEditableColorSpace(swatch, index)}</td>
                    <td>{renderEditableColorValues(swatch, index)}</td>
                    <td className="color-preview">{renderColorPreview(swatch)}</td>
                    <td>{renderActionButtons(swatch, index)}</td>
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