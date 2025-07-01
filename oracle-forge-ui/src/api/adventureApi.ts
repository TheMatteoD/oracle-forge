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
} = adventureApi; 