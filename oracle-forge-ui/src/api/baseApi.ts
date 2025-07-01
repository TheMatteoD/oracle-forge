import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import config from '../config.js';

// Backend response wrapper interface - used by all API slices
export interface BackendResponse<T> {
  success: boolean;
  message: string;
  data: T;
}

// Base API configuration that all slices can extend
export const baseApi = createApi({
  reducerPath: 'baseApi',
  baseQuery: fetchBaseQuery({ 
    baseUrl: config.SERVER_URL,
  }),
  endpoints: () => ({}), // Empty endpoints - will be extended by other slices
});

export const createResponseTransformer = <T>() => {
  return (response: BackendResponse<T>): T => response.data;
};

export const createErrorTransformer = (response: any) => {
  if (response?.error?.message) {
    return response.error.message;
  }
  return 'An error occurred';
}; 