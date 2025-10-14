import React, { useState } from 'react';
import type { EndpointEntry } from './EndpointListData';
import Pagination from './Pagination';

interface EndpointListProps {
  entries: EndpointEntry[];
  itemsPerPage?: number;
}

const EndpointList: React.FC<EndpointListProps> = ({ entries, itemsPerPage = 6 }) => {
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

  const getMethodClass = (method: string) => {
    const baseClass = 'endpoint-method';
    switch (method) {
      case 'GET':
        return `${baseClass} method-get`;
      case 'POST':
        return `${baseClass} method-post`;
      case 'PUT':
        return `${baseClass} method-put`;
      case 'DELETE':
        return `${baseClass} method-delete`;
      default:
        return baseClass;
    }
  };

  return (
    <div className="info-section">
      <h3>Available Endpoints</h3>
      <ul className="endpoint-list">
        {currentEntries.map((entry, index) => (
          <li key={startIndex + index} className="endpoint-item">
            <div className="endpoint-path-with-method">
              <span className={getMethodClass(entry.method)}>{entry.method}</span>
              <code>{entry.path}</code>
            </div>
            <div className="endpoint-description">
              {entry.description}
            </div>
          </li>
        ))}
      </ul>
      
      <Pagination
        currentPage={currentPage}
        totalPages={totalPages}
        onNext={goToNextPage}
        onPrevious={goToPreviousPage}
      />
    </div>
  );
};

export default EndpointList;