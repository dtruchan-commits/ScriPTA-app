import { ChangelogType } from '../types';
import type { ChangeLogEntry } from './ChangeLog';

/**
 * ChangeLogData component that provides changelog entries data
 * This component centralizes changelog data management
 */
export const getChangelogEntries = (): ChangeLogEntry[] => {
  return [
    {
      date: '2025-10-13',
      type: ChangelogType.BACKEND,
      description: 'Added complete CRUD operations for swatch configurations: create, update, and delete endpoints with comprehensive error handling and validation'
    },
    {
      date: '2025-10-13',
      type: ChangelogType.BACKEND,
      description: 'Implemented test suite for swatch CRUD operations with 8 test cases covering success scenarios, error cases, and different color models'
    },
    {
      date: '2025-10-13',
      type: ChangelogType.ADMIN_PANEL,
      description: 'Change Log Component and Data'
    },
    {
      date: '2025-10-13',
      type: ChangelogType.BACKEND,
      description: 'Backend/BD Health Endpoints with Indicators in Admin Panel Dashboard'
    },
    {
      date: '2025-10-13',
      type: ChangelogType.ADMIN_PANEL,
      description: 'Response Models from Types'
    },
    {
      date: '2025-10-13',
      type: ChangelogType.ADMIN_PANEL,
      description: 'Minor Fixes in Naming'
    },
    {
      date: '2025-10-13',
      type: ChangelogType.ADMIN_PANEL,
      description: 'Types and Enums'
    }
  ];
};

/**
 * Default changelog data export
 */
export const changelogEntries = getChangelogEntries();