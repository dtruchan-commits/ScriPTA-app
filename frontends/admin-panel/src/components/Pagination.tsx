import React from 'react';

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onNext: () => void;
  onPrevious: () => void;
}

/**
 * Reusable pagination component
 */
const Pagination: React.FC<PaginationProps> = ({
  currentPage,
  totalPages,
  onNext,
  onPrevious
}) => {
  if (totalPages <= 1) {
    return null;
  }

  return (
    <div className="changelog-pagination">
      <button 
        className="pagination-btn"
        onClick={onPrevious}
        disabled={currentPage === 0}
      >
        ← Previous
      </button>
      
      <span className="pagination-info">
        Page {currentPage + 1} of {totalPages}
      </span>
      
      <button 
        className="pagination-btn"
        onClick={onNext}
        disabled={currentPage === totalPages - 1}
      >
        Next →
      </button>
    </div>
  );
};

export default Pagination;