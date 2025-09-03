// frontend/src/lib/api.ts
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (data: any) => api.post('/api/auth/register', data),
  login: (data: any) => api.post('/api/auth/login', data),
  logout: () => api.post('/api/auth/logout'),
  getMe: () => api.get('/api/auth/me'),
  connectLinkedIn: () => window.location.href = `${API_URL}/api/auth/linkedin`,
};

export const contentAPI = {
  generate: (data: any) => api.post('/api/content/generate', data),
  getVariations: (contentId: string) => api.post('/api/content/variations', { content_id: contentId }),
  schedule: (data: any) => api.post('/api/content/schedule', data),
  publishNow: (contentId: string) => api.post('/api/content/publish-now', { content_id: contentId }),
  getTrending: () => api.get('/api/content/trending-topics'),
  getCalendar: (start: string, end: string) => api.get('/api/content/calendar', { params: { start_date: start, end_date: end } }),
};

export const analyticsAPI = {
  getDashboard: () => api.get('/api/analytics/dashboard'),
  getPostAnalytics: (postId: string) => api.get(`/api/analytics/posts/${postId}/analytics`),
  getTrends: (days: number = 30) => api.get('/api/analytics/trends', { params: { days } }),
  getTopContent: () => api.get('/api/analytics/top-content'),
};

export const userAPI = {
  getProfile: () => api.get('/api/users/profile'),
  updateProfile: (data: any) => api.put('/api/users/profile', data),
  getLinkedInStatus: () => api.get('/api/users/linkedin-status'),
};

export default api;