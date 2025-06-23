import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

export const createShortURL = (data) => {
  return axios.post(`${API_BASE}/shorturls`, data);
};

export const getShortURLStats = (shortcode) => {
  return axios.get(`${API_BASE}/shorturls/${shortcode}`);
};
