/**
 * EndpointListData component that provides API endpoint entries data
 * This component centralizes endpoint data management
 */

export interface EndpointEntry {
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  path: string;
  description: string;
  category: 'Swatch' | 'Layer' | 'TPM' | 'Health';
}

export const getEndpointEntries = (): EndpointEntry[] => {
  return [
    // Health endpoints
    {
      method: 'GET',
      path: '/health',
      description: 'Check backend server health status',
      category: 'Health'
    },
    {
      method: 'GET',
      path: '/health/db',
      description: 'Check database connection health',
      category: 'Health'
    },
    
    // Swatch endpoints
    {
      method: 'GET',
      path: '/get_swatch_config',
      description: 'Retrieve swatch configurations',
      category: 'Swatch'
    },
    {
      method: 'POST',
      path: '/create_swatch_config',
      description: 'Create new swatch configuration',
      category: 'Swatch'
    },
    {
      method: 'PUT',
      path: '/update_swatch_config/{color_name}',
      description: 'Update existing swatch configuration',
      category: 'Swatch'
    },
    {
      method: 'DELETE',
      path: '/delete_swatch_config/{color_name}',
      description: 'Delete swatch configuration',
      category: 'Swatch'
    },
    
    // Layer endpoints
    {
      method: 'GET',
      path: '/get_layer_config',
      description: 'Retrieve layer configurations',
      category: 'Layer'
    },
    {
      method: 'POST',
      path: '/create_layer_config',
      description: 'Create new layer configuration',
      category: 'Layer'
    },
    {
      method: 'PUT',
      path: '/update_layer_config/{config_name}',
      description: 'Update existing layer configuration',
      category: 'Layer'
    },
    {
      method: 'DELETE',
      path: '/delete_layer_config/{config_name}',
      description: 'Delete layer configuration',
      category: 'Layer'
    },
    
    // TPM endpoints
    {
      method: 'GET',
      path: '/get_tpm_config',
      description: 'Retrieve TPM configurations',
      category: 'TPM'
    }
  ];
};

/**
 * Default endpoint data export
 */
export const endpointEntries = getEndpointEntries();