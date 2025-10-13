import axios from 'axios';
import type {
  ApiError,
  LayerConfigResponse,
  SwatchConfigResponse,
  TpmConfigResponse
} from '../types';

// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// API Client with Axios
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor for consistent error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const apiError: ApiError = {
      status: error.response?.status || 0,
      message: error.response?.data?.detail || error.message || 'Unknown error occurred',
      details: error.response?.data
    };
    return Promise.reject(apiError);
  }
);

// API Service Functions
export class ApiService {
  // Backend Health Check
  static async checkBackendHealth(): Promise<boolean> {
    try {
      const response = await apiClient.get('/', { timeout: 3000 });
      return response.status === 200;
    } catch (error) {
      console.warn('Backend health check failed:', error);
      return false;
    }
  }

  // Database Health Check (mocked for now)
  static async checkDatabaseHealth(): Promise<boolean> {
    try {
      // TODO: Replace with actual database health check endpoint when implemented
      // For now, we'll mock it by checking if we can fetch any data
      const response = await apiClient.get('/get_swatch_config', { 
        params: { limit: 1 }, 
        timeout: 5000 
      });
      return response.status === 200;
    } catch (error) {
      console.warn('Database health check failed:', error);
      return false;
    }
  }

  // Swatch Configuration API
  static async getSwatchConfig(colorName?: string): Promise<SwatchConfigResponse> {
    try {
      const params = colorName ? { colorName } : {};
      const response = await apiClient.get('/get_swatch_config', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching swatch config:', error);
      throw error;
    }
  }

  // Layer Configuration API
  static async getLayerConfig(configName?: string): Promise<LayerConfigResponse> {
    try {
      const params = configName ? { configName } : {};
      const response = await apiClient.get('/get_layer_config', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching layer config:', error);
      throw error;
    }
  }

  // TPM Configuration API
  static async getTpmConfig(tpmName?: string): Promise<TpmConfigResponse> {
    try {
      const params = tpmName ? { tpmName } : {};
      const response = await apiClient.get('/get_tpm_config', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching TPM config:', error);
      throw error;
    }
  }
}

export default ApiService;