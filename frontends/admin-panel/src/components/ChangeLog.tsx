import React from 'react';
import { ChangelogType } from '../types';

interface ChangeLogEntry {
  date: string;
  type: ChangelogType;
  description: string;
}

interface ChangeLogProps {
  entries: ChangeLogEntry[];
}

const ChangeLog: React.FC<ChangeLogProps> = ({ entries }) => {
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
        {entries.map((entry, index) => (
          <li key={index}>
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
    </div>
  );
};

export default ChangeLog;
export type { ChangeLogEntry };
