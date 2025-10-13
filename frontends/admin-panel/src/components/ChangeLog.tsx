import React, { useState } from 'react';
import { ChangelogType } from '../types';

interface ChangeLogEntry {
  date: string;
  type: ChangelogType;
  description: string;
}

interface ChangeLogProps {
  entries: ChangeLogEntry[];
  itemsPerPage?: number;
}

const ChangeLog: React.FC<ChangeLogProps> = ({ entries, itemsPerPage = 4 }) => {
  const [currentPage, setCurrentPage] = useState(0);
  
  const totalPages = Math.ceil(entries.length / itemsPerPage);
  const startIndex = currentPage * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentEntries = entries.slice(startIndex, endIndex);
  
  const goToNextPage = () => {
    if (currentPage < totalPages - 1) {
      setCurrentPage(currentPage + 1);
    }
  };
  
  const goToPreviousPage = () => {
    if (currentPage > 0) {
      setCurrentPage(currentPage - 1);
    }
  };
  const getPillClass = (type: ChangelogType) => {
    switch (type) {
      case ChangelogType.ADMIN_PANEL:
        return 'changelog-pill admin-panel';
      case ChangelogType.BACKEND:
        return 'changelog-pill backend';
      case ChangelogType.INDESIGN_SCRIPT:
        return 'changelog-pill indesign-script';
      default:
        return 'changelog-pill admin-panel';
    }
  };

  return (
    <div className="info-section">
      <h3>Change Log</h3>
      <ul className="changelog-list">
        {currentEntries.map((entry, index) => (
          <li key={startIndex + index}>
            <div className="changelog-header">
              <span className={getPillClass(entry.type)}>{entry.type}</span>
              <span className="changelog-date">{entry.date}</span>
            </div>
            <div className="changelog-description">
              {entry.description}
            </div>
          </li>
        ))}
      </ul>
      
      {totalPages > 1 && (
        <div className="changelog-pagination">
          <button 
            className="pagination-btn"
            onClick={goToPreviousPage}
            disabled={currentPage === 0}
          >
            ← Previous
          </button>
          
          <span className="pagination-info">
            Page {currentPage + 1} of {totalPages}
          </span>
          
          <button 
            className="pagination-btn"
            onClick={goToNextPage}
            disabled={currentPage === totalPages - 1}
          >
            Next →
          </button>
        </div>
      )}
    </div>
  );
};

export default ChangeLog;
export type { ChangeLogEntry };
