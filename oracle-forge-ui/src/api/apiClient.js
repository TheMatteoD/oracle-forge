// Simple centralized API client for Oracle Forge

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

function getHeaders(hasBody = false) {
  const headers = {};
  if (hasBody) {
    headers['Content-Type'] = 'application/json';
  }
  return headers;
}

async function handleResponse(response) {
  const contentType = response.headers.get('content-type');
  let data;
  if (contentType && contentType.includes('application/json')) {
    data = await response.json();
  } else {
    data = await response.text();
  }
  if (!response.ok) {
    throw { status: response.status, data };
  }
  return data;
}

export async function apiGet(endpoint) {
  const res = await fetch(`${API_BASE_URL}${endpoint}`);
  return handleResponse(res);
}

export async function apiPost(endpoint, body) {
  const res = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: 'POST',
    headers: getHeaders(true),
    body: JSON.stringify(body),
  });
  return handleResponse(res);
}

export async function apiPut(endpoint, body) {
  const res = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: 'PUT',
    headers: getHeaders(true),
    body: JSON.stringify(body),
  });
  return handleResponse(res);
}

export async function apiDelete(endpoint) {
  const res = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: 'DELETE',
    headers: getHeaders(),
  });
  return handleResponse(res);
}

// Usage example:
// import { apiGet, apiPost } from '../api/apiClient';
// apiGet('/adventures').then(...).catch(...); 