// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// API Client with Axios
import axios from 'axios';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response type interfaces based on backend models
export interface SwatchConfig {
  colorName: string;
  colorModel: 'SPOT' | 'PROCESS';
  colorSpace: 'CMYK' | 'RGB' | 'LAB';
  colorValues: number[];
}

export interface SwatchConfigResponse {
  swatches: SwatchConfig[];
}

export interface LayerConfigResponse {
  name: string;
  locked: boolean;
  print: boolean;
  color: string;
}

export interface LayerConfigSetResponse {
  configName: string;
  layers: LayerConfigResponse[];
}

export interface TpmConfig {
  id: number;
  TPM: string;
  drawDieline?: string;
  drawCombination?: string;
  A?: number;
  B?: number;
  H?: number;
  variant?: string;
  version: number;
  variablesList?: string;
  createdBy?: string;
  createdAt?: string;
  modifiedBy?: string;
  modifiedAt?: string;
  packType?: string;
  description?: string;
  comment?: string;
  panelList?: string;
  createdTimestamp?: string;
  updatedTimestamp?: string;
}

export interface TPMConfigResponse {
  tpms: TpmConfig[];
}

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
  static async getLayerConfig(configName?: string): Promise<LayerConfigSetResponse[]> {
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