import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// add token to requests if it exists
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// auth functions
export const register = (username, email, password) => {
  return api.post('/auth/register/', { username, email, password });
};

export const login = (username, password) => {
  return api.post('/auth/login/', { username, password });
};

// dataset functions
export const uploadCSV = (file) => {
  const formData = new FormData();
  formData.append('file', file);

  return api.post('/upload/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const getDatasets = () => {
  return api.get('/datasets/');
};

export const getDataset = (id) => {
  return api.get(`/datasets/${id}/`);
};

export const getChartData = (id) => {
  return api.get(`/datasets/${id}/chart_data/`);
};

export const downloadPDF = (id) => {
  return api.get(`/datasets/${id}/pdf/`, {
    responseType: 'blob',
  });
};

export const downloadExcel = (id) => {
  return api.get(`/datasets/${id}/export_excel/`, {
    responseType: 'blob',
  });
};

export default api;
