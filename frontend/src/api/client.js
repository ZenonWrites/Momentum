import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(
  (config) => {
    const token = global.authToken;
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const authAPI = {
  onboarding: (data) => apiClient.post('/onboarding/', data),
  login: (data) => apiClient.post('/login/', data),
};

export const profileAPI = {
  get: () => apiClient.get('/profile/'),
  update: (data) => apiClient.patch('/profile/update/', data),
};

export const objectivesAPI = {
  getDailyPlan: () => apiClient.get('/daily-plan/'),
  getList: (date) => apiClient.get(`/objectives/${date ? `?date=${date}` : ''}`),
  update: (id, data) => apiClient.patch(`/objectives/${id}/`, data),
};

export const checkInAPI = {
  submit: (data) => apiClient.post('/daily-checkin/', data),
};

export const tipsAPI = {
  getRandom: () => apiClient.get('/tips/random/'),
};

export const hobbiesAPI = {
  getSuggestion: () => apiClient.get('/suggestions/hobby/'),
  list: () => apiClient.get('/hobbies/'),
  create: (data) => apiClient.post('/hobbies/', data),
};

export const workoutAPI = {
  getPlan: () => apiClient.get('/suggestions/workout/'),
};

export default apiClient;
