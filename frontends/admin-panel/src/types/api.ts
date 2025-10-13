/**
 * API Service Type Definitions
 * 
 * This module contains types specific to the API service layer,
 * separate from the main domain types.
 */

import type {
    LayerConfigSet,
    SwatchConfig,
    TpmConfig
} from './index';

// =============================================================================
// API SERVICE METHOD TYPES
// =============================================================================

/**
 * Parameters for swatch configuration API calls
 */
export interface GetSwatchConfigParams {
  colorName?: string;
}

/**
 * Parameters for layer configuration API calls
 */
export interface GetLayerConfigParams {
  configName?: string;
}

/**
 * Parameters for TPM configuration API calls
 */
export interface GetTpmConfigParams {
  tpmName?: string;
}

// =============================================================================
// API SERVICE INTERFACE
// =============================================================================

/**
 * Interface defining all API service methods
 */
export interface IApiService {
  /**
   * Fetch swatch configurations
   */
  getSwatchConfig(params?: GetSwatchConfigParams): Promise<{ swatches: SwatchConfig[] }>;
  
  /**
   * Fetch layer configurations
   */
  getLayerConfig(params?: GetLayerConfigParams): Promise<LayerConfigSet[]>;
  
  /**
   * Fetch TPM configurations
   */
  getTpmConfig(params?: GetTpmConfigParams): Promise<{ tpms: TpmConfig[] }>;
}

// =============================================================================
// HTTP CLIENT TYPES
// =============================================================================

/**
 * HTTP methods supported by the API
 */
export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';

/**
 * HTTP request configuration
 */
export interface HttpRequestConfig {
  method: HttpMethod;
  url: string;
  params?: Record<string, string | number | boolean>;
  data?: unknown;
  headers?: Record<string, string>;
  timeout?: number;
}

/**
 * HTTP response structure
 */
export interface HttpResponse<T = unknown> {
  data: T;
  status: number;
  statusText: string;
  headers: Record<string, string>;
}

// =============================================================================
// ERROR HANDLING TYPES
// =============================================================================

/**
 * API error types
 */
export const ApiErrorType = {
  NETWORK_ERROR: 'NETWORK_ERROR',
  TIMEOUT_ERROR: 'TIMEOUT_ERROR',
  SERVER_ERROR: 'SERVER_ERROR',
  CLIENT_ERROR: 'CLIENT_ERROR',
  UNKNOWN_ERROR: 'UNKNOWN_ERROR'
} as const;

export type ApiErrorType = typeof ApiErrorType[keyof typeof ApiErrorType];

/**
 * Enhanced API error with categorization
 */
export interface EnhancedApiError {
  type: ApiErrorType;
  status?: number;
  message: string;
  details?: unknown;
  timestamp: Date;
  endpoint?: string;
}

// =============================================================================
// VALIDATION TYPES
// =============================================================================

/**
 * API response validation result
 */
export interface ValidationResult<T> {
  isValid: boolean;
  data?: T;
  errors?: string[];
}

/**
 * Schema validator function type
 */
export type SchemaValidator<T> = (data: unknown) => ValidationResult<T>;

// =============================================================================
// CACHING TYPES
// =============================================================================

/**
 * Cache entry structure
 */
export interface CacheEntry<T> {
  data: T;
  timestamp: Date;
  expiresAt: Date;
  key: string;
}

/**
 * Cache configuration
 */
export interface CacheConfig {
  ttl: number; // Time to live in milliseconds
  maxEntries: number;
  enabled: boolean;
}

// =============================================================================
// REQUEST INTERCEPTOR TYPES
// =============================================================================

/**
 * Request interceptor function
 */
export type RequestInterceptor = (config: HttpRequestConfig) => HttpRequestConfig | Promise<HttpRequestConfig>;

/**
 * Response interceptor function
 */
export type ResponseInterceptor<T = unknown> = (response: HttpResponse<T>) => HttpResponse<T> | Promise<HttpResponse<T>>;

/**
 * Error interceptor function
 */
export type ErrorInterceptor = (error: EnhancedApiError) => EnhancedApiError | Promise<never>;

// =============================================================================
// RETRY MECHANISM TYPES
// =============================================================================

/**
 * Retry configuration
 */
export interface RetryConfig {
  attempts: number;
  delay: number;
  backoff: 'linear' | 'exponential';
  retryCondition: (error: EnhancedApiError) => boolean;
}

/**
 * Retry state
 */
export interface RetryState {
  attempt: number;
  maxAttempts: number;
  nextDelay: number;
  error?: EnhancedApiError;
}

// All types are already exported inline above