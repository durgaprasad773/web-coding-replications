import axios from 'axios';

const API_BASE_URL = 'https://pdurgaprasad773.pythonanywhere.com/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    throw new Error(error.response?.data?.error || error.message || 'An error occurred');
  }
);

export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export const getTokenUsage = async () => {
  const response = await api.get('/token-usage');
  return response.data;
};

export const resetSessionTokens = async () => {
  const response = await api.post('/reset-session-tokens');
  return response.data;
};

export const generateReplicas = async (data) => {
  const response = await api.post('/generate-replicas', data);
  return response.data;
};

export const downloadExcel = async (replicas) => {
  const response = await api.post('/download-excel', { replicas }, {
    responseType: 'blob',
  });
  
  // Create blob link and trigger download
  const blob = new Blob([response.data], {
    type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
  });
  
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `web_coding_replicas_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.xlsx`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
};

export const downloadJson = async (data) => {
  const response = await api.post('/download-json', data, {
    responseType: 'blob',
  });
  
  // Create blob link and trigger download
  const blob = new Blob([response.data], { type: 'application/json' });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `web_coding_replicas_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.json`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
};

export default api;
