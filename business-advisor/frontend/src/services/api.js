import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Main analysis endpoint
export const analyzeBusiness = async (data) => {
  const response = await client.post('/api/analyze', data);
  return response.data;
};

// Market endpoints
export const getCompetitors = async (data) => {
  const response = await client.post('/api/market/competitors', data);
  return response.data;
};

export const getPopulation = async (data) => {
  const response = await client.post('/api/market/population', data);
  return response.data;
};

// Finance endpoint
export const calculateFinance = async (data) => {
  const response = await client.post('/api/finance/calculate', data);
  return response.data;
};

// Business categories
export const getBusinessCategories = async () => {
  const response = await client.get('/api/business/categories');
  return response.data;
};

// Health check
export const getHealth = async () => {
  const response = await client.get('/health');
  return response.data;
};

export const getClusteringResults = async (nClusters = 3) => {
  const response = await client.get('/api/clustering/results', { params: { n_clusters: nClusters } });
  return response.data;
};

export const getBusinessModelMetrics = async () => {
  const response = await client.get('/api/business/model-metrics');
  return response.data;
};

export const predictBusinessSuccess = async (features) => {
  const response = await client.post('/api/business/predict', { features });
  return response.data;
};

export default client;
