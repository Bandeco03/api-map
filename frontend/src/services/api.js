import axios from 'axios'

// Backend API base URL
// If VITE_API_URL is empty or not set, use empty string for relative URLs (works with Vite proxy)
// If set to a full URL (e.g., http://localhost:8000), use that for direct connection
const API_BASE_URL = import.meta.env.VITE_API_URL !== undefined
  ? import.meta.env.VITE_API_URL
  : 'http://localhost:8000'

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
      // Adaptar o formato de resposta do banco de dados
      if (response.data && response.data.data) {
        // Check if data is already an object or needs to be parsed
        return typeof response.data.data === 'string'
          ? JSON.parse(response.data.data)
          : response.data.data
      }
      return response.data
    } catch (error) {
      console.error('Error fetching power data:', error)
      throw error
    }
  }

  /**
   * Fetch power data history
   * @param {number} limit - Number of records to fetch
   * @returns {Promise} Historical power data
   */
  async getPowerDataHistory(limit = 100) {
    try {
      const response = await this.client.get(`/api/power-data/history?limit=${limit}`)
      return response.data
    } catch (error) {
      console.error('Error fetching power data history:', error)
      throw error
    }
  }

  /**
   * Trigger immediate data fetch from external API
   * @returns {Promise} Fetched data
   */
  async fetchNow() {
    try {
      const response = await this.client.get('/api/power-data/fetch-now')
      return response.data
    } catch (error) {
      console.error('Error triggering immediate fetch:', error)
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
