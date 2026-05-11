const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export const wisdomService = {
  async getTodaysWisdom() {
    const response = await fetch(`${API_BASE_URL}/wisdom/today`);
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Failed to fetch wisdom');
    }
    
    return response.json();
  },
  
  async checkHealth() {
    const response = await fetch(`${API_BASE_URL}/wisdom/health`);
    return response.json();
  }
};
