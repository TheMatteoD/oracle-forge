import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import config from '../config.js';
import { BackendResponse, createResponseTransformer } from './baseApi';

export interface Adventure {
  id: string;
  name: string;
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
} = adventureApi; 