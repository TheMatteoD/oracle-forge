import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import config from '../config.js';
import { BackendResponse, createResponseTransformer } from './baseApi';

export interface Adventure {
  id: string;
  name: string;
  world_state?: any;
  player_states?: any;
  active_session?: {
    log?: any[];
    // add other fields as needed
  };
}

export interface WorldEntity {
  name: string;
  description?: string;
  status?: string;
  location?: string;
  faction?: string;
}

export interface WorldState {
  chaos_factor?: number;
  current_scene?: number;
  days_passed?: number;
}

export interface ActiveAdventureResponse {
  active?: string;
}

export interface CreateAdventureRequest {
  name: string;
}

export interface UpdateAdventureRequest {
  name?: string;
}

export const adventureApi = createApi({
  reducerPath: 'adventureApi',
  baseQuery: fetchBaseQuery({ baseUrl: config.SERVER_URL }),
  endpoints: (builder) => ({
    getActiveAdventure: builder.query<ActiveAdventureResponse, void>({
      query: () => '/adventures/active',
      transformResponse: createResponseTransformer<ActiveAdventureResponse>(),
    }),
    listAdventures: builder.query<Adventure[], void>({
      query: () => '/adventures/list',
      transformResponse: createResponseTransformer<Adventure[]>(),
    }),
    getAdventure: builder.query<Adventure, string>({
      query: (id) => `/adventures/${id}`,
      transformResponse: createResponseTransformer<Adventure>(),
    }),
    createAdventure: builder.mutation<Adventure, CreateAdventureRequest>({
      query: (body) => ({
        url: '/adventures',
        method: 'POST',
        body: { data: body },
      }),
      transformResponse: createResponseTransformer<Adventure>(),
    }),
    updateAdventure: builder.mutation<Adventure, { id: string; data: UpdateAdventureRequest }>({
      query: ({ id, data }) => ({
        url: `/adventures/${id}`,
        method: 'PUT',
        body: data,
      }),
      transformResponse: createResponseTransformer<Adventure>(),
    }),
    deleteAdventure: builder.mutation<void, string>({
      query: (id) => ({
        url: `/adventures/${id}`,
        method: 'DELETE',
      }),
      transformResponse: createResponseTransformer<void>(),
    }),
    listCustomMaps: builder.query<string[], string>({
      query: (adventure) => `/adventures/${adventure}/custom_maps`,
      transformResponse: createResponseTransformer<string[]>(),
    }),
    uploadCustomMap: builder.mutation<any, { adventure: string; file: File }>({
      query: ({ adventure, file }) => {
        const formData = new FormData();
        formData.append('file', file);
        return {
          url: `/adventures/${adventure}/upload_custom_map`,
          method: 'POST',
          body: formData,
        };
      },
    }),
    uploadAzgaarMap: builder.mutation<any, { adventure: string; file: File }>({
      query: ({ adventure, file }) => {
        const formData = new FormData();
        formData.append('file', file);
        return {
          url: `/adventures/${adventure}/upload_map`,
          method: 'POST',
          body: formData,
        };
      },
    }),
    getAzgaarMapFile: builder.query<Blob, string>({
      query: (adventure) => ({
        url: `/adventures/${adventure}/map_file`,
        responseHandler: (response) => response.blob(),
      }),
    }),
    checkAzgaarMapExists: builder.query<boolean, string>({
      query: (adventure) => ({
        url: `/adventures/${adventure}/map_file`,
        method: 'HEAD',
      }),
      transformResponse: (_: unknown, meta) => meta?.response?.status === 200,
    }),
    listPlayers: builder.query<any[], string>({
      query: (adventure) => `/adventures/${adventure}/players`,
      transformResponse: createResponseTransformer<any[]>(),
    }),
    createPlayer: builder.mutation<any, { adventure: string; player: any }>({
      query: ({ adventure, player }) => ({
        url: `/adventures/${adventure}/players`,
        method: 'POST',
        body: player,
        headers: { 'Content-Type': 'application/json' },
      }),
      transformResponse: createResponseTransformer<any>(),
    }),
    getPlayer: builder.query<any, { adventure: string; filename: string }>({
      query: ({ adventure, filename }) => `/adventures/${adventure}/players/${filename}`,
      transformResponse: createResponseTransformer<any>(),
    }),
    updatePlayer: builder.mutation<any, { adventure: string; filename: string; data: any }>({
      query: ({ adventure, filename, data }) => ({
        url: `/adventures/${adventure}/players/${filename}`,
        method: 'PUT',
        body: data,
        headers: { 'Content-Type': 'application/json' },
      }),
      transformResponse: createResponseTransformer<any>(),
    }),
    clearActiveAdventure: builder.mutation<any, void>({
      query: () => ({
        url: '/adventures/clear',
        method: 'POST',
      }),
      transformResponse: createResponseTransformer<any>(),
    }),
    // World State Management
    getWorldState: builder.query<WorldState, string>({
      query: (adventure) => `/adventures/${adventure}/world_state`,
      transformResponse: createResponseTransformer<WorldState>(),
    }),
    updateWorldState: builder.mutation<WorldState, { adventure: string; data: WorldState }>({
      query: ({ adventure, data }) => ({
        url: `/adventures/${adventure}/world_state`,
        method: 'POST',
        body: data,
        headers: { 'Content-Type': 'application/json' },
      }),
      transformResponse: createResponseTransformer<WorldState>(),
    }),
    // World Entity Management
    listWorldEntities: builder.query<WorldEntity[], { adventure: string; entityType: string }>({
      query: ({ adventure, entityType }) => ({
        url: `/adventures/${adventure}/world/${entityType}`,
        method: 'GET',
      }),
      transformResponse: (response: any) => {
        return response.data?.entities || [];
      },
    }),
    getWorldEntity: builder.query<WorldEntity, { adventure: string; entityType: string; entityName: string }>({
      query: ({ adventure, entityType, entityName }) => ({
        url: `/adventures/${adventure}/world/${entityType}/${entityName}`,
        method: 'GET',
      }),
      transformResponse: (response: any) => {
        return response.data?.entity || {};
      },
    }),
    createWorldEntity: builder.mutation<WorldEntity, { adventure: string; entityType: string; entityData: WorldEntity }>({
      query: ({ adventure, entityType, entityData }) => ({
        url: `/adventures/${adventure}/world/${entityType}/${entityData.name}`,
        method: 'POST',
        body: { entity_data: entityData },
      }),
      transformResponse: (response: any) => {
        return response.data?.entity || {};
      },
    }),
    updateWorldEntity: builder.mutation<WorldEntity, { adventure: string; entityType: string; entityName: string; entityData: WorldEntity }>({
      query: ({ adventure, entityType, entityName, entityData }) => ({
        url: `/adventures/${adventure}/world/${entityType}/${entityName}`,
        method: 'POST',
        body: { entity_data: entityData },
      }),
      transformResponse: (response: any) => {
        return response.data?.entity || {};
      },
    }),
    deleteWorldEntity: builder.mutation<void, { adventure: string; entityType: string; entityName: string }>({
      query: ({ adventure, entityType, entityName }) => ({
        url: `/adventures/${adventure}/world/${entityType}/${entityName}`,
        method: 'DELETE',
      }),
      transformResponse: (response: any) => {
        return response.data;
      },
    }),
  }),
});

export const {
  useGetActiveAdventureQuery,
  useListAdventuresQuery,
  useGetAdventureQuery,
  useLazyGetAdventureQuery,
  useCreateAdventureMutation,
  useUpdateAdventureMutation,
  useDeleteAdventureMutation,
  useListCustomMapsQuery,
  useUploadCustomMapMutation,
  useUploadAzgaarMapMutation,
  useGetAzgaarMapFileQuery,
  useCheckAzgaarMapExistsQuery,
  useListPlayersQuery,
  useCreatePlayerMutation,
  useGetPlayerQuery,
  useUpdatePlayerMutation,
  useClearActiveAdventureMutation,
  useGetWorldStateQuery,
  useUpdateWorldStateMutation,
  useListWorldEntitiesQuery,
  useGetWorldEntityQuery,
  useCreateWorldEntityMutation,
  useUpdateWorldEntityMutation,
  useDeleteWorldEntityMutation,
} = adventureApi; 