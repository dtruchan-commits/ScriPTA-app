/**
 * React Component Type Definitions
 * 
 * This module contains TypeScript types specific to React components
 * used throughout the admin panel.
 */

import type { ReactNode } from 'react';
import type {
    DataState,
    FilterState,
    LayerConfigSet,
    LoadingState,
    SwatchConfig,
    TpmConfig
} from './index';

// =============================================================================
// COMPONENT PROPS TYPES
// =============================================================================

/**
 * Base props that all components can receive
 */
export interface BaseComponentProps {
  /** Additional CSS class names */
  className?: string;
  /** Inline styles */
  style?: React.CSSProperties;
  /** Test ID for testing */
  testId?: string;
  /** Children elements */
  children?: ReactNode;
}

/**
 * Props for components that handle loading states
 */
export interface LoadingProps {
  /** Current loading state */
  loading: LoadingState;
  /** Loading message */
  loadingMessage?: string;
  /** Custom loading component */
  loadingComponent?: ReactNode;
}

/**
 * Props for components that handle errors
 */
export interface ErrorProps {
  /** Error state */
  error: string | null;
  /** Error retry handler */
  onRetry?: () => void;
  /** Custom error component */
  errorComponent?: ReactNode;
}

/**
 * Combined props for async data components
 */
export interface AsyncDataProps extends LoadingProps, ErrorProps {}

// =============================================================================
// CONFIGURATION VIEW COMPONENT PROPS
// =============================================================================

/**
 * Props for SwatchConfigView component
 */
export interface SwatchConfigViewProps extends BaseComponentProps, AsyncDataProps {
  /** Swatch data */
  data?: DataState<{ swatches: SwatchConfig[] }>;
  /** Filter state */
  filter?: FilterState;
  /** Filter change handler */
  onFilterChange?: (filter: string) => void;
  /** Refresh data handler */
  onRefresh?: () => void;
}

/**
 * Props for LayerConfigView component
 */
export interface LayerConfigViewProps extends BaseComponentProps, AsyncDataProps {
  /** Layer configuration data */
  data?: DataState<LayerConfigSet[]>;
  /** Filter state */
  filter?: FilterState;
  /** Filter change handler */
  onFilterChange?: (filter: string) => void;
  /** Refresh data handler */
  onRefresh?: () => void;
}

/**
 * Props for TpmConfigView component
 */
export interface TpmConfigViewProps extends BaseComponentProps, AsyncDataProps {
  /** TPM configuration data */
  data?: DataState<{ tpms: TpmConfig[] }>;
  /** Filter state */
  filter?: FilterState;
  /** Filter change handler */
  onFilterChange?: (filter: string) => void;
  /** Refresh data handler */
  onRefresh?: () => void;
  /** Expanded row IDs */
  expandedRows?: Set<number>;
  /** Row expansion handler */
  onRowToggle?: (id: number) => void;
}

// =============================================================================
// TABLE COMPONENT PROPS
// =============================================================================

/**
 * Generic table column definition
 */
export interface TableColumn<T> {
  /** Column identifier */
  key: keyof T | string;
  /** Column header label */
  label: string;
  /** Column width */
  width?: string | number;
  /** Whether column is sortable */
  sortable?: boolean;
  /** Custom render function */
  render?: (value: unknown, record: T, index: number) => ReactNode;
  /** CSS class for column */
  className?: string;
}

/**
 * Table component props
 */
export interface TableProps<T> extends BaseComponentProps {
  /** Table data */
  data: T[];
  /** Column definitions */
  columns: TableColumn<T>[];
  /** Loading state */
  loading?: boolean;
  /** Empty state message */
  emptyMessage?: string;
  /** Row key extractor */
  rowKey: keyof T | ((record: T, index: number) => string | number);
  /** Row click handler */
  onRowClick?: (record: T, index: number) => void;
  /** Custom row class name */
  rowClassName?: (record: T, index: number) => string;
}

// =============================================================================
// FILTER COMPONENT PROPS
// =============================================================================

/**
 * Filter input component props
 */
export interface FilterInputProps extends BaseComponentProps {
  /** Current filter value */
  value: string;
  /** Placeholder text */
  placeholder?: string;
  /** Change handler */
  onChange: (value: string) => void;
  /** Submit handler */
  onSubmit: (value: string) => void;
  /** Clear handler */
  onClear: () => void;
  /** Whether filter is currently active */
  isActive?: boolean;
  /** Loading state during filter operation */
  loading?: boolean;
}

// =============================================================================
// NAVIGATION COMPONENT PROPS
// =============================================================================

/**
 * Navigation item for the nav component
 */
export interface NavigationItem {
  /** Display label */
  label: string;
  /** Route path */
  path: string;
  /** Icon (emoji or component) */
  icon: ReactNode;
  /** Whether item is currently active */
  active?: boolean;
  /** Badge content (for notifications) */
  badge?: string | number;
}

/**
 * Navigation component props
 */
export interface NavigationProps extends BaseComponentProps {
  /** Navigation items */
  items: NavigationItem[];
  /** Header content */
  header?: ReactNode;
  /** Footer content */
  footer?: ReactNode;
  /** Whether navigation is collapsed */
  collapsed?: boolean;
  /** Navigation toggle handler */
  onToggle?: () => void;
}

// =============================================================================
// DASHBOARD COMPONENT PROPS
// =============================================================================

/**
 * Statistics card props
 */
export interface StatCardProps extends BaseComponentProps {
  /** Card title */
  title: string;
  /** Statistic value */
  value: string | number;
  /** Card icon */
  icon: ReactNode;
  /** Description text */
  description?: string;
  /** Link URL */
  href?: string;
  /** Link text */
  linkText?: string;
  /** Loading state */
  loading?: boolean;
}

/**
 * Dashboard component props
 */
export interface DashboardProps extends BaseComponentProps {
  /** Statistics data */
  stats?: {
    swatches: number;
    layerConfigs: number;
    tpmConfigs: number;
    loading: boolean;
    error: string | null;
  };
  /** Stats refresh handler */
  onRefreshStats?: () => void;
}

// =============================================================================
// FORM COMPONENT PROPS (for future CRUD operations)
// =============================================================================

/**
 * Form field props
 */
export interface FormFieldProps extends BaseComponentProps {
  /** Field name */
  name: string;
  /** Field label */
  label: string;
  /** Field value */
  value: unknown;
  /** Change handler */
  onChange: (name: string, value: unknown) => void;
  /** Whether field is required */
  required?: boolean;
  /** Whether field is disabled */
  disabled?: boolean;
  /** Field error message */
  error?: string;
  /** Field help text */
  help?: string;
}

/**
 * Form component props
 */
export interface FormProps<T = Record<string, unknown>> extends BaseComponentProps {
  /** Form values */
  values: T;
  /** Form change handler */
  onChange: (values: T) => void;
  /** Form submission handler */
  onSubmit: (values: T) => void | Promise<void>;
  /** Form validation errors */
  errors?: Partial<Record<keyof T, string>>;
  /** Whether form is submitting */
  submitting?: boolean;
  /** Whether form is disabled */
  disabled?: boolean;
  /** Submit button text */
  submitText?: string;
  /** Cancel button text */
  cancelText?: string;
  /** Cancel handler */
  onCancel?: () => void;
}

// =============================================================================
// MODAL/DIALOG COMPONENT PROPS
// =============================================================================

/**
 * Modal component props
 */
export interface ModalProps extends BaseComponentProps {
  /** Whether modal is open */
  open: boolean;
  /** Close handler */
  onClose: () => void;
  /** Modal title */
  title?: string;
  /** Modal size */
  size?: 'small' | 'medium' | 'large' | 'extra-large';
  /** Whether modal can be closed by clicking backdrop */
  closeOnBackdrop?: boolean;
  /** Whether modal can be closed by pressing Escape */
  closeOnEscape?: boolean;
  /** Footer content */
  footer?: ReactNode;
}

// =============================================================================
// HOOK RETURN TYPES
// =============================================================================

/**
 * Return type for data fetching hooks
 */
export interface UseDataResult<T> {
  /** Current data */
  data: T | null;
  /** Loading state */
  loading: boolean;
  /** Error message */
  error: string | null;
  /** Refresh function */
  refresh: () => Promise<void>;
  /** Whether data is stale */
  isStale: boolean;
  /** Last updated timestamp */
  lastUpdated: Date | null;
}

/**
 * Return type for filter hooks
 */
export interface UseFilterResult {
  /** Current filter value */
  filter: string;
  /** Set filter value */
  setFilter: (value: string) => void;
  /** Apply filter */
  applyFilter: () => void;
  /** Clear filter */
  clearFilter: () => void;
  /** Whether filter is active */
  isActive: boolean;
  /** Whether filter is loading */
  loading: boolean;
}

/**
 * Return type for pagination hooks
 */
export interface UsePaginationResult {
  /** Current page */
  currentPage: number;
  /** Total pages */
  totalPages: number;
  /** Items per page */
  pageSize: number;
  /** Total items */
  total: number;
  /** Go to specific page */
  goToPage: (page: number) => void;
  /** Go to next page */
  nextPage: () => void;
  /** Go to previous page */
  previousPage: () => void;
  /** Set page size */
  setPageSize: (size: number) => void;
  /** Whether there's a next page */
  hasNext: boolean;
  /** Whether there's a previous page */
  hasPrevious: boolean;
}

// =============================================================================
// EVENT HANDLER TYPES
// =============================================================================

/**
 * Generic change handler type
 */
export type ChangeHandler<T = string> = (value: T) => void;

/**
 * Generic click handler type
 */
export type ClickHandler<T = Element> = (event: React.MouseEvent<T>) => void;

/**
 * Generic form event handler type
 */
export type FormEventHandler = (event: React.FormEvent<HTMLFormElement>) => void;

/**
 * Generic keyboard event handler type
 */
export type KeyboardEventHandler<T = Element> = (event: React.KeyboardEvent<T>) => void;

// =============================================================================
// UTILITY COMPONENT TYPES
// =============================================================================

/**
 * Render prop pattern type
 */
export type RenderProp<T> = (props: T) => ReactNode;

/**
 * Component with render prop
 */
export interface RenderPropComponent<T> extends Omit<BaseComponentProps, 'children'> {
  /** Render function */
  render: RenderProp<T>;
  /** Alternative children function */
  children?: RenderProp<T>;
}

/**
 * Higher-order component type
 */
export type HOC<P = {}> = <T extends P>(Component: React.ComponentType<T>) => React.ComponentType<T>;

/**
 * Component ref type
 */
export type ComponentRef<T = HTMLElement> = React.RefObject<T> | ((instance: T | null) => void);

// All types are exported inline above