import axios from 'axios'

// Backend API base URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

/**
 * API service for communicating with the backend
 */
class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }

  /**
   * Fetch power station data from the backend
   * @returns {Promise} Power station data
   */
  async getPowerData() {
    try {
      const response = await this.client.get('/api/power-data')
      return response.data
    } catch (error) {
      console.error('Error fetching power data:', error)
      throw error
    }
  }

  /**
   * Health check endpoint
   * @returns {Promise} Health status
   */
  async healthCheck() {
    try {
      const response = await this.client.get('/health')
      return response.data
    } catch (error) {
      console.error('Error checking health:', error)
      throw error
    }
  }
}

// Export a singleton instance
export default new ApiService()
