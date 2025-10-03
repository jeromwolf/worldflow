/**
 * Application Configuration
 */

// API Base URL - use environment variable in production, fallback to localhost in development
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const config = {
  apiUrl: API_BASE_URL,
}
