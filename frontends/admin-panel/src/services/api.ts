import axios from 'axios';
import type {
    ApiError,
    LayerConfigResponse,
    SwatchConfigResponse,
    TPMConfigResponse
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
  static async getTpmConfig(tpmName?: string): Promise<TPMConfigResponse> {
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