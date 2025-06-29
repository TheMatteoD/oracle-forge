import type { 
  APIResponse, 
  PaginatedResponse, 
  APIError, 
  ListRequest,
  CreateEntityRequest,
  UpdateEntityRequest,
  EntityType,
  SystemType
} from '@/types/api';

// Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

// Request configuration
interface RequestConfig {
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  headers?: Record<string, string>;
  body?: any;
  signal?: AbortSignal;
}

// API Client Class
class APIClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  // Private method to make HTTP requests
  private async request<T>(endpoint: string, config: RequestConfig): Promise<APIResponse<T>> {
    const url = `${this.baseURL}${endpoint}`;
    
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...config.headers,
    };

    const requestConfig: RequestInit = {
      method: config.method,
      headers,
      signal: config.signal,
    };

    if (config.body && config.method !== 'GET') {
      requestConfig.body = JSON.stringify(config.body);
    }

    try {
      const response = await fetch(url, requestConfig);
      const data = await this.parseResponse(response);
      
      // Handle rate limiting
      if (response.status === 429) {
        const retryAfter = response.headers.get('Retry-After');
        throw new Error(`Rate limit exceeded. Please try again in ${retryAfter || 'a few'} seconds.`);
      }

      // Handle other HTTP errors
      if (!response.ok) {
        throw new Error(data.error || `HTTP ${response.status}: ${response.statusText}`);
      }

      return data as APIResponse<T>;
    } catch (error) {
      if (error instanceof Error) {
        throw new Error(`API Request failed: ${error.message}`);
      }
      throw new Error('API Request failed: Unknown error');
    }
  }

  // Parse response based on content type
  private async parseResponse(response: Response): Promise<any> {
    const contentType = response.headers.get('content-type');
    
    if (contentType?.includes('application/json')) {
      return await response.json();
    }
    
    return await response.text();
  }

  // Generic CRUD methods
  async get<T>(endpoint: string, signal?: AbortSignal): Promise<APIResponse<T>> {
    return this.request<T>(endpoint, { method: 'GET', signal });
  }

  async post<T>(endpoint: string, data: any, signal?: AbortSignal): Promise<APIResponse<T>> {
    return this.request<T>(endpoint, { method: 'POST', body: data, signal });
  }

  async put<T>(endpoint: string, data: any, signal?: AbortSignal): Promise<APIResponse<T>> {
    return this.request<T>(endpoint, { method: 'PUT', body: data, signal });
  }

  async delete<T>(endpoint: string, signal?: AbortSignal): Promise<APIResponse<T>> {
    return this.request<T>(endpoint, { method: 'DELETE', signal });
  }

  // Health check
  async healthCheck(): Promise<APIResponse<{ status: string; timestamp: string }>> {
    return this.get('/health');
  }

  // Configuration status
  async getConfigStatus(): Promise<APIResponse<any>> {
    return this.get('/config/status');
  }
}

// Create singleton instance
export const apiClient = new APIClient();

// Domain-specific API methods
export class AdventureAPI {
  // Adventures
  static async listAdventures(params?: ListRequest): Promise<PaginatedResponse<any>> {
    const queryParams = new URLSearchParams();
    if (params?.page) queryParams.append('page', params.page.toString());
    if (params?.per_page) queryParams.append('per_page', params.per_page.toString());
    if (params?.search) queryParams.append('search', params.search);
    
    const endpoint = `/adventures${queryParams.toString() ? `?${queryParams}` : ''}`;
    return apiClient.get(endpoint);
  }

  static async getAdventure(id: string): Promise<APIResponse<any>> {
    return apiClient.get(`/adventures/${id}`);
  }

  static async createAdventure(data: CreateEntityRequest<any>): Promise<APIResponse<any>> {
    return apiClient.post('/adventures', data);
  }

  static async updateAdventure(id: string, data: UpdateEntityRequest<any>): Promise<APIResponse<any>> {
    return apiClient.put(`/adventures/${id}`, data);
  }

  static async deleteAdventure(id: string): Promise<APIResponse<void>> {
    return apiClient.delete(`/adventures/${id}`);
  }

  // Sessions
  static async listSessions(adventureId: string): Promise<APIResponse<any[]>> {
    return apiClient.get(`/adventures/${adventureId}/sessions`);
  }

  static async getSession(adventureId: string, sessionId: string): Promise<APIResponse<any>> {
    return apiClient.get(`/adventures/${adventureId}/sessions/${sessionId}`);
  }

  static async createSession(adventureId: string, data: CreateEntityRequest<any>): Promise<APIResponse<any>> {
    return apiClient.post(`/adventures/${adventureId}/sessions`, data);
  }

  static async updateSession(adventureId: string, sessionId: string, data: UpdateEntityRequest<any>): Promise<APIResponse<any>> {
    return apiClient.put(`/adventures/${adventureId}/sessions/${sessionId}`, data);
  }

  static async deleteSession(adventureId: string, sessionId: string): Promise<APIResponse<void>> {
    return apiClient.delete(`/adventures/${adventureId}/sessions/${sessionId}`);
  }

  // World entities (NPCs, Factions, Locations, Story Lines)
  static async listWorldEntities(adventureId: string, entityType: 'npcs' | 'factions' | 'locations' | 'story_lines'): Promise<APIResponse<any[]>> {
    return apiClient.get(`/adventures/${adventureId}/world/${entityType}`);
  }

  static async getWorldEntity(adventureId: string, entityType: 'npcs' | 'factions' | 'locations' | 'story_lines', entityId: string): Promise<APIResponse<any>> {
    return apiClient.get(`/adventures/${adventureId}/world/${entityType}/${entityId}`);
  }

  static async createWorldEntity(adventureId: string, entityType: 'npcs' | 'factions' | 'locations' | 'story_lines', data: CreateEntityRequest<any>): Promise<APIResponse<any>> {
    return apiClient.post(`/adventures/${adventureId}/world/${entityType}`, data);
  }

  static async updateWorldEntity(adventureId: string, entityType: 'npcs' | 'factions' | 'locations' | 'story_lines', entityId: string, data: UpdateEntityRequest<any>): Promise<APIResponse<any>> {
    return apiClient.put(`/adventures/${adventureId}/world/${entityType}/${entityId}`, data);
  }

  static async deleteWorldEntity(adventureId: string, entityType: 'npcs' | 'factions' | 'locations' | 'story_lines', entityId: string): Promise<APIResponse<void>> {
    return apiClient.delete(`/adventures/${adventureId}/world/${entityType}/${entityId}`);
  }

  // Players
  static async listPlayers(adventureId: string): Promise<APIResponse<any[]>> {
    return apiClient.get(`/adventures/${adventureId}/players`);
  }

  static async getPlayer(adventureId: string, playerId: string): Promise<APIResponse<any>> {
    return apiClient.get(`/adventures/${adventureId}/players/${playerId}`);
  }

  static async createPlayer(adventureId: string, data: CreateEntityRequest<any>): Promise<APIResponse<any>> {
    return apiClient.post(`/adventures/${adventureId}/players`, data);
  }

  static async updatePlayer(adventureId: string, playerId: string, data: UpdateEntityRequest<any>): Promise<APIResponse<any>> {
    return apiClient.put(`/adventures/${adventureId}/players/${playerId}`, data);
  }

  static async deletePlayer(adventureId: string, playerId: string): Promise<APIResponse<void>> {
    return apiClient.delete(`/adventures/${adventureId}/players/${playerId}`);
  }
}

export class LookupAPI {
  // Generic lookup method
  static async lookup<T>(entityType: 'items' | 'monsters' | 'spells' | 'rules', system: SystemType, params?: ListRequest): Promise<PaginatedResponse<T>> {
    const queryParams = new URLSearchParams();
    queryParams.append('system', system);
    if (params?.page) queryParams.append('page', params.page.toString());
    if (params?.per_page) queryParams.append('per_page', params.per_page.toString());
    if (params?.search) queryParams.append('search', params.search);
    if (params?.filters) {
      Object.entries(params.filters).forEach(([key, value]) => {
        queryParams.append(key, value.toString());
      });
    }
    
    const endpoint = `/lookup/${entityType}?${queryParams}`;
    return apiClient.get(endpoint);
  }

  static async getEntity<T>(entityType: 'items' | 'monsters' | 'spells' | 'rules', system: SystemType, name: string): Promise<APIResponse<T>> {
    return apiClient.get(`/lookup/${entityType}/${encodeURIComponent(name)}?system=${system}`);
  }

  // Search across all lookup types
  static async searchAll(system: SystemType, query: string, params?: ListRequest): Promise<APIResponse<any>> {
    const queryParams = new URLSearchParams();
    queryParams.append('system', system);
    queryParams.append('q', query);
    if (params?.page) queryParams.append('page', params.page.toString());
    if (params?.per_page) queryParams.append('per_page', params.per_page.toString());
    
    return apiClient.get(`/lookup/search?${queryParams}`);
  }
}

export class OracleAPI {
  static async listTables(system: SystemType, category?: string): Promise<APIResponse<any[]>> {
    const queryParams = new URLSearchParams();
    queryParams.append('system', system);
    if (category) queryParams.append('category', category);
    
    return apiClient.get(`/oracle/tables?${queryParams}`);
  }

  static async getTable(system: SystemType, name: string): Promise<APIResponse<any>> {
    return apiClient.get(`/oracle/tables/${encodeURIComponent(name)}?system=${system}`);
  }

  static async rollTable(system: SystemType, name: string, custom_roll?: number): Promise<APIResponse<any>> {
    const data = custom_roll ? { custom_roll } : {};
    return apiClient.post(`/oracle/tables/${encodeURIComponent(name)}/roll?system=${system}`, data);
  }

  static async yesNo(system: SystemType, question?: string): Promise<APIResponse<any>> {
    const data = question ? { question } : {};
    return apiClient.post(`/oracle/yes-no?system=${system}`, data);
  }

  static async sceneCheck(system: SystemType, scene_context?: string): Promise<APIResponse<any>> {
    const data = scene_context ? { scene_context } : {};
    return apiClient.post(`/oracle/scene-check?system=${system}`, data);
  }

  static async meaningOracle(system: SystemType, focus?: string): Promise<APIResponse<any>> {
    const data = focus ? { focus } : {};
    return apiClient.post(`/oracle/meaning?system=${system}`, data);
  }
}

export class GeneratorAPI {
  static async listGenerators(system: SystemType, category?: string): Promise<APIResponse<any[]>> {
    const queryParams = new URLSearchParams();
    queryParams.append('system', system);
    if (category) queryParams.append('category', category);
    
    return apiClient.get(`/generators?${queryParams}`);
  }

  static async getGenerator(system: SystemType, name: string): Promise<APIResponse<any>> {
    return apiClient.get(`/generators/${encodeURIComponent(name)}?system=${system}`);
  }

  static async runGenerator(system: SystemType, name: string, parameters: Record<string, any>): Promise<APIResponse<any>> {
    return apiClient.post(`/generators/${encodeURIComponent(name)}/run?system=${system}`, { parameters });
  }
}

export class CombatAPI {
  static async listCombatSessions(adventureId: string): Promise<APIResponse<any[]>> {
    return apiClient.get(`/combat/sessions?adventure_id=${adventureId}`);
  }

  static async getCombatSession(sessionId: string): Promise<APIResponse<any>> {
    return apiClient.get(`/combat/sessions/${sessionId}`);
  }

  static async createCombatSession(data: CreateEntityRequest<any>): Promise<APIResponse<any>> {
    return apiClient.post('/combat/sessions', data);
  }

  static async updateCombatSession(sessionId: string, data: UpdateEntityRequest<any>): Promise<APIResponse<any>> {
    return apiClient.put(`/combat/sessions/${sessionId}`, data);
  }

  static async deleteCombatSession(sessionId: string): Promise<APIResponse<void>> {
    return apiClient.delete(`/combat/sessions/${sessionId}`);
  }

  static async rollInitiative(sessionId: string): Promise<APIResponse<any>> {
    return apiClient.post(`/combat/sessions/${sessionId}/initiative`, {});
  }

  static async nextTurn(sessionId: string): Promise<APIResponse<any>> {
    return apiClient.post(`/combat/sessions/${sessionId}/next-turn`, {});
  }
}

// Export all API classes
export { apiClient as default }; 