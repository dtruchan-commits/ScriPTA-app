/**
 * ScriPTA Admin Panel Type Definitions
 * 
 * This module contains all TypeScript type definitions used throughout the admin panel.
 * Types are organized by domain and follow TypeScript best practices.
 */

// =============================================================================
// ENUMS - Used for type-safe constants
// =============================================================================

/**
 * Color model types for swatch configurations
 */
export const ColorModel = {
  SPOT: 'SPOT',
  PROCESS: 'PROCESS'
} as const;

export type ColorModel = typeof ColorModel[keyof typeof ColorModel];

/**
 * Color space types for swatch configurations
 */
export const ColorSpace = {
  CMYK: 'CMYK',
  RGB: 'RGB',
  LAB: 'LAB'
} as const;

export type ColorSpace = typeof ColorSpace[keyof typeof ColorSpace];

/**
 * Layer names used in InDesign configurations
 */
export const LayerName = {
  DIELINE: 'DIELINE',
  TECHNICAL: 'TECHNICAL',
  BRAILLE_EMB: 'BRAILLE_EMB',
  TEXT: 'TEXT',
  ACF_HRL: 'ACF_HRL',
  ACF_LRA_VARNISH: 'ACF_LRA_VARNISH',
  DESIGN: 'DESIGN',
  INFOBOX: 'INFOBOX',
  GUIDES: 'GUIDES',
  PANEL: 'PANEL'
} as const;

export type LayerName = typeof LayerName[keyof typeof LayerName];

/**
 * Layer color options
 */
export const LayerColor = {
  GOLD: 'GOLD',
  TEAL: 'TEAL',
  FIESTA: 'FIESTA',
  LIGHT_BLUE: 'LIGHT_BLUE',
  YELLOW: 'YELLOW',
  GREEN: 'GREEN',
  RED: 'RED',
  LAVENDER: 'LAVENDER',
  GRAY: 'GRAY',
  BLUE: 'BLUE'
} as const;

export type LayerColor = typeof LayerColor[keyof typeof LayerColor];

/**
 * Changelog entry types for categorizing changes
 */
export const ChangelogType = {
  ADMIN_PANEL: 'Admin-Panel',
  BACKEND: 'Backend',
  INDESIGN_SCRIPT: 'InDesign-Script'
} as const;

export type ChangelogType = typeof ChangelogType[keyof typeof ChangelogType];

// =============================================================================
// SWATCH CONFIGURATION TYPES
// =============================================================================

/**
 * Individual swatch configuration
 */
export interface SwatchConfig {
  /** Name of the color */
  colorName: string;
  /** Color model type */
  colorModel: ColorModel;
  /** Color space type */
  colorSpace: ColorSpace;
  /** Array of color values */
  colorValues: number[];
}

/**
 * Response type for swatch configuration API
 */
export interface SwatchConfigResponse {
  /** Array of swatch configurations */
  swatches: SwatchConfig[];
}

/**
 * Query parameters for swatch configuration API
 */
export interface SwatchConfigQuery {
  /** Optional color name filter */
  colorName?: string;
}

// =============================================================================
// LAYER CONFIGURATION TYPES
// =============================================================================

/**
 * Individual layer configuration
 */
export interface LayerConfig {
  /** Layer name */
  name: string;
  /** Whether the layer is locked */
  locked: boolean;
  /** Whether the layer should print */
  print: boolean;
  /** Layer color */
  color: string;
}

/**
 * Set of layer configurations with a name
 */
export interface LayerConfigSet {
  /** Configuration set name */
  configName: string;
  /** Array of layer configurations */
  layers: LayerConfig[];
}

/**
 * Response type for layer configuration API (array of sets)
 */
export type LayerConfigResponse = LayerConfigSet[];

/**
 * Query parameters for layer configuration API
 */
export interface LayerConfigQuery {
  /** Optional config name filter */
  configName?: string;
}

// =============================================================================
// TPM CONFIGURATION TYPES
// =============================================================================

/**
 * Technical Packaging Material configuration
 */
export interface TpmConfig {
  /** Unique identifier */
  id: number;
  /** TPM name */
  TPM: string;
  /** Draw dieline setting */
  drawDieline?: string | null;
  /** Draw combination setting */
  drawCombination?: string | null;
  /** Dimension A */
  A?: number | null;
  /** Dimension B */
  B?: number | null;
  /** Dimension H */
  H?: number | null;
  /** Variant name */
  variant?: string | null;
  /** Version number */
  version: number;
  /** Variables list as JSON string */
  variablesList?: string | null;
  /** User who created the record */
  createdBy?: string | null;
  /** Creation date */
  createdAt?: string | null;
  /** User who last modified the record */
  modifiedBy?: string | null;
  /** Last modification date */
  modifiedAt?: string | null;
  /** Package type */
  packType?: string | null;
  /** Description */
  description?: string | null;
  /** Comments */
  comment?: string | null;
  /** Panel list as JSON string */
  panelList?: string | null;
  /** Created timestamp */
  createdTimestamp?: string | null;
  /** Updated timestamp */
  updatedTimestamp?: string | null;
}

/**
 * Response type for TPM configuration API
 */
export interface TpmConfigResponse {
  /** Array of TPM configurations */
  tpms: TpmConfig[];
}

/**
 * Query parameters for TPM configuration API
 */
export interface TpmConfigQuery {
  /** Optional TPM name filter */
  tpmName?: string;
}

// =============================================================================
// API CLIENT TYPES
// =============================================================================

/**
 * Generic API error response
 */
export interface ApiError {
  /** HTTP status code */
  status: number;
  /** Error message */
  message: string;
  /** Additional error details */
  details?: unknown;
}

/**
 * API request configuration
 */
export interface ApiRequestConfig {
  /** Request timeout in milliseconds */
  timeout?: number;
  /** Additional headers */
  headers?: Record<string, string>;
  /** Query parameters */
  params?: Record<string, string | number | boolean>;
}

/**
 * Generic API response wrapper
 */
export interface ApiResponse<T = unknown> {
  /** Response data */
  data: T;
  /** HTTP status code */
  status: number;
  /** Response headers */
  headers: Record<string, string>;
}

// =============================================================================
// COMPONENT STATE TYPES
// =============================================================================

/**
 * Loading states for async operations
 */
export const LoadingState = {
  IDLE: 'idle',
  LOADING: 'loading',
  SUCCESS: 'success',
  ERROR: 'error'
} as const;

export type LoadingState = typeof LoadingState[keyof typeof LoadingState];

/**
 * Generic component state for data fetching
 */
export interface DataState<T> {
  /** Current data */
  data: T | null;
  /** Loading state */
  loading: LoadingState;
  /** Error message if any */
  error: string | null;
  /** Last updated timestamp */
  lastUpdated?: Date;
}

/**
 * Filter state for configuration views
 */
export interface FilterState {
  /** Current filter value */
  value: string;
  /** Whether filter is active */
  isActive: boolean;
  /** Last applied filter */
  lastApplied?: string;
}

// =============================================================================
// DASHBOARD TYPES
// =============================================================================

/**
 * Statistics for dashboard display
 */
export interface DashboardStats {
  /** Number of swatch configurations */
  swatches: number;
  /** Number of layer configuration sets */
  layerConfigs: number;
  /** Number of TPM configurations */
  tpmConfigs: number;
  /** Loading state */
  loading: boolean;
  /** Error message if any */
  error: string | null;
}

/**
 * Navigation menu item
 */
export interface NavItem {
  /** Display label */
  label: string;
  /** Route path */
  path: string;
  /** Icon (emoji or class name) */
  icon: string;
  /** Whether item is currently active */
  active?: boolean;
}

// =============================================================================
// UTILITY TYPES
// =============================================================================

/**
 * Make all properties of T optional recursively
 */
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

/**
 * Extract keys of T that have values assignable to U
 */
export type KeysOfType<T, U> = {
  [K in keyof T]: T[K] extends U ? K : never;
}[keyof T];

/**
 * Make specific properties of T required
 */
export type RequireKeys<T, K extends keyof T> = T & Required<Pick<T, K>>;

/**
 * Omit keys from T and make remaining properties required
 */
export type OmitAndRequire<T, K extends keyof T> = Required<Omit<T, K>>;

// =============================================================================
// FORM TYPES (for future CRUD operations)
// =============================================================================

/**
 * Form field validation state
 */
export interface FieldValidation {
  /** Whether field is valid */
  isValid: boolean;
  /** Validation error message */
  error?: string;
  /** Whether field has been touched */
  touched: boolean;
}

/**
 * Generic form state
 */
export interface FormState<T = Record<string, unknown>> {
  /** Form field values */
  values: T;
  /** Field validation states */
  validation: Record<keyof T, FieldValidation>;
  /** Whether form is currently submitting */
  isSubmitting: boolean;
  /** Whether form is valid overall */
  isValid: boolean;
  /** Form-level error message */
  error?: string;
}

// =============================================================================
// RE-EXPORTS FROM SUBMODULES
// =============================================================================

// Re-export API-specific types
export * from './api';

// Re-export component-specific types
export * from './components';

// All main types are already exported inline above
// No need for duplicate exports