/**
 * Axios API client configuration with interceptors.
 */

import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';
import { APIErrorResponse } from '@/types';

// Get API URL from environment
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance with default config
export const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  timeout: 30000, // 30s for uploads, can be overridden per request
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding headers
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Add any auth headers here in the future if needed
    // For now, just log the request
    if (process.env.NODE_ENV === 'development') {
      console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error transformation
apiClient.interceptors.response.use(
  (response) => {
    // Return successful responses as-is
    return response;
  },
  (error: AxiosError<APIErrorResponse>) => {
    // Transform API errors into user-friendly messages
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;
      
      let message: string;
      if (typeof data?.detail === 'string') {
        message = data.detail;
        
        // Enhanced error messages for specific security scenarios
        if (message.toLowerCase().includes('pii')) {
          message = '🔒 Security Alert: This image contains personally identifiable information (PII) and cannot be processed for privacy protection.';
        } else if (message.toLowerCase().includes('svg') && message.toLowerCase().includes('security')) {
          message = '⚠️ Security Alert: This SVG file contains potentially malicious content and has been blocked for your safety.';
        } else if (message.toLowerCase().includes('file type') || message.toLowerCase().includes('invalid file')) {
          message = '📄 Invalid File: Please upload PNG, JPG, or SVG files only.';
        } else if (message.toLowerCase().includes('file size') || message.toLowerCase().includes('too large')) {
          message = '📦 File Too Large: Please compress your image to under 10MB.';
        }
      } else if (typeof data?.detail === 'object') {
        // Validation errors from FastAPI
        message = 'Validation error. Please check your input.';
      } else {
        message = `Request failed with status ${status}`;
      }

      // Log error in development
      if (process.env.NODE_ENV === 'development') {
        console.error(`[API Error] ${status}: ${message}`);
      }

      // Create new error with friendly message
      const apiError = new Error(message);
      (apiError as any).status = status;
      (apiError as any).originalError = error;
      return Promise.reject(apiError);
    } else if (error.request) {
      // Request made but no response received
      const networkError = new Error(
        'Unable to connect to server. Please check your connection.'
      );
      (networkError as any).originalError = error;
      return Promise.reject(networkError);
    } else {
      // Something else happened
      return Promise.reject(error);
    }
  }
);

// Helper to set timeout for specific requests
export function createLongTimeoutClient() {
  const client = axios.create({
    ...apiClient.defaults,
    timeout: 60000, // 60s for long-running operations
  });
  
  // Apply same interceptors
  client.interceptors.request = apiClient.interceptors.request;
  client.interceptors.response = apiClient.interceptors.response;
  
  return client;
}
