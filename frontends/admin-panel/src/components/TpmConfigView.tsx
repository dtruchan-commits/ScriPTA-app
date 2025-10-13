import { useEffect, useState } from 'react';
import type { TPMConfigResponse, TpmConfig } from '../services/api';
import { ApiService } from '../services/api';

const TpmConfigView: React.FC = () => {
  const [tpmData, setTpmData] = useState<TPMConfigResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [filterTpmName, setFilterTpmName] = useState<string>('');
  const [expandedRows, setExpandedRows] = useState<Set<number>>(new Set());

  const fetchTpmConfig = async (tpmName?: string) => {
    try {
      setLoading(true);
      setError(null);
      const data = await ApiService.getTpmConfig(tpmName || undefined);
      setTpmData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch TPM configuration');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTpmConfig();
  }, []);

  const handleFilter = (e: React.FormEvent) => {
    e.preventDefault();
    fetchTpmConfig(filterTpmName.trim());
  };

  const handleClearFilter = () => {
    setFilterTpmName('');
    fetchTpmConfig();
  };

  const toggleRowExpansion = (id: number) => {
    const newExpanded = new Set(expandedRows);
    if (newExpanded.has(id)) {
      newExpanded.delete(id);
    } else {
      newExpanded.add(id);
    }
    setExpandedRows(newExpanded);
  };

  const renderTpmDetails = (tpm: TpmConfig) => {
    const isExpanded = expandedRows.has(tpm.id);
    
    return (
      <tr key={tpm.id} className={`tpm-row ${isExpanded ? 'expanded' : ''}`}>
        <td colSpan={8}>
          <div className="tpm-summary" onClick={() => toggleRowExpansion(tpm.id)}>
            <div className="tpm-header">
              <span className="expand-icon">{isExpanded ? '▼' : '▶'}</span>
              <strong className="tpm-name">{tpm.TPM}</strong>
              <span className="tpm-id">ID: {tpm.id}</span>
              <span className="tpm-version">v{tpm.version}</span>
            </div>
            <div className="tpm-basic-info">
              {tpm.description && <span className="description">{tpm.description}</span>}
              {tpm.packType && <span className="pack-type">Pack: {tpm.packType}</span>}
            </div>
          </div>
          
          {isExpanded && (
            <div className="tpm-expanded-details">
              <div className="details-grid">
                <div className="detail-section">
                  <h5>Dimensions</h5>
                  <div className="dimension-values">
                    {tpm.A && <span>A: {tpm.A}</span>}
                    {tpm.B && <span>B: {tpm.B}</span>}
                    {tpm.H && <span>H: {tpm.H}</span>}
                  </div>
                </div>

                <div className="detail-section">
                  <h5>Drawing Settings</h5>
                  <div className="drawing-values">
                    {tpm.drawDieline && <span>Dieline: {tpm.drawDieline}</span>}
                    {tpm.drawCombination && <span>Combination: {tpm.drawCombination}</span>}
                  </div>
                </div>

                <div className="detail-section">
                  <h5>Metadata</h5>
                  <div className="metadata-values">
                    {tpm.variant && <span>Variant: {tpm.variant}</span>}
                    {tpm.createdBy && <span>Created by: {tpm.createdBy}</span>}
                    {tpm.modifiedBy && <span>Modified by: {tpm.modifiedBy}</span>}
                  </div>
                </div>

                <div className="detail-section">
                  <h5>Timestamps</h5>
                  <div className="timestamp-values">
                    {tpm.createdAt && <span>Created: {new Date(tpm.createdAt).toLocaleDateString()}</span>}
                    {tpm.modifiedAt && <span>Modified: {new Date(tpm.modifiedAt).toLocaleDateString()}</span>}
                  </div>
                </div>

                {tpm.variablesList && (
                  <div className="detail-section full-width">
                    <h5>Variables List</h5>
                    <div className="variables-content">
                      <pre>{tpm.variablesList}</pre>
                    </div>
                  </div>
                )}

                {tpm.panelList && (
                  <div className="detail-section full-width">
                    <h5>Panel List</h5>
                    <div className="panel-content">
                      <pre>{tpm.panelList}</pre>
                    </div>
                  </div>
                )}

                {tpm.comment && (
                  <div className="detail-section full-width">
                    <h5>Comments</h5>
                    <div className="comment-content">
                      {tpm.comment}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </td>
      </tr>
    );
  };

  if (loading) {
    return (
      <div className="config-view">
        <h2>TPM Configuration</h2>
        <div className="loading">Loading TPM data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="config-view">
        <h2>TPM Configuration</h2>
        <div className="error">Error: {error}</div>
        <button onClick={() => fetchTpmConfig()}>Retry</button>
      </div>
    );
  }

  return (
    <div className="config-view">
      <h2>TPM Configuration</h2>
      
      <div className="filter-section">
        <form onSubmit={handleFilter} className="filter-form">
          <input
            type="text"
            placeholder="Filter by TPM name"
            value={filterTpmName}
            onChange={(e) => setFilterTpmName(e.target.value)}
            className="filter-input"
          />
          <button type="submit" className="filter-button">Filter</button>
          <button type="button" onClick={handleClearFilter} className="clear-button">
            Clear
          </button>
        </form>
      </div>

      <div className="data-section">
        <h3>Results: {tpmData?.tpms.length || 0} TPM configurations</h3>
        
        {tpmData && tpmData.tpms.length > 0 ? (
          <div className="table-container">
            <table className="config-table tpm-table">
              <tbody>
                {tpmData.tpms.map((tpm) => renderTpmDetails(tpm))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="no-data">
            {filterTpmName 
              ? `No TPM configurations found for name "${filterTpmName}"`
              : 'No TPM configuration data available'
            }
          </div>
        )}
      </div>
    </div>
  );
};

export default TpmConfigView;