import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import config from '../config.js';

export interface Adventure {
  id: string;
  name: string;
  // Add other fields as needed
}

export interface ActiveAdventureResponse {
  active?: string;
}

export interface CreateAdventureRequest {
  name: string;
  // Add other fields as needed
}

export interface UpdateAdventureRequest {
  name?: string;
  // Add other fields as needed
}

export const adventureApi = createApi({
  reducerPath: 'adventureApi',
  baseQuery: fetchBaseQuery({ baseUrl: config.SERVER_URL }),
  endpoints: (builder) => ({
    getActiveAdventure: builder.query<ActiveAdventureResponse, void>({
      query: () => '/adventures/active',
    }),
    listAdventures: builder.query<Adventure[], void>({
      query: () => '/adventures/list',
    }),
    getAdventure: builder.query<Adventure, string>({
      query: (id) => `/adventures/${id}`,
    }),
    createAdventure: builder.mutation<Adventure, CreateAdventureRequest>({
      query: (body) => ({
        url: '/adventures',
        method: 'POST',
        body,
      }),
    }),
    updateAdventure: builder.mutation<Adventure, { id: string; data: UpdateAdventureRequest }>({
      query: ({ id, data }) => ({
        url: `/adventures/${id}`,
        method: 'PUT',
        body: data,
      }),
    }),
    deleteAdventure: builder.mutation<void, string>({
      query: (id) => ({
        url: `/adventures/${id}`,
        method: 'DELETE',
      }),
    }),
  }),
});

export const {
  useGetActiveAdventureQuery,
  useListAdventuresQuery,
  useGetAdventureQuery,
  useCreateAdventureMutation,
  useUpdateAdventureMutation,
  useDeleteAdventureMutation,
} = adventureApi; 