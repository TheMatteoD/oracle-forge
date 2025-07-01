import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import config from '../config.js';
import { createResponseTransformer } from './baseApi';

export interface CombatSession {
  id: string;
  // Add other fields as needed
}

export const combatApi = createApi({
  reducerPath: 'combatApi',
  baseQuery: fetchBaseQuery({ baseUrl: config.SERVER_URL }),
  endpoints: (builder) => ({
    listCombatSessions: builder.query<CombatSession[], { adventureId: string }>({
      query: ({ adventureId }) => `/combat/${adventureId}/sessions`,
      transformResponse: createResponseTransformer<CombatSession[]>(),
    }),
    getCombatSession: builder.query<CombatSession, { sessionId: string }>({
      query: ({ sessionId }) => `/combat/sessions/${sessionId}`,
      transformResponse: createResponseTransformer<CombatSession>(),
    }),
    createCombatSession: builder.mutation<CombatSession, { data: any }>({
      query: ({ data }) => ({
        url: '/combat/sessions',
        method: 'POST',
        body: data,
      }),
      transformResponse: createResponseTransformer<CombatSession>(),
    }),
    updateCombatSession: builder.mutation<CombatSession, { sessionId: string; data: any }>({
      query: ({ sessionId, data }) => ({
        url: `/combat/sessions/${sessionId}`,
        method: 'PUT',
        body: data,
      }),
      transformResponse: createResponseTransformer<CombatSession>(),
    }),
    deleteCombatSession: builder.mutation<void, { sessionId: string }>({
      query: ({ sessionId }) => ({
        url: `/combat/sessions/${sessionId}`,
        method: 'DELETE',
      }),
      transformResponse: createResponseTransformer<void>(),
    }),
    rollInitiative: builder.mutation<any, { sessionId: string }>({
      query: ({ sessionId }) => ({
        url: `/combat/sessions/${sessionId}/roll-initiative`,
        method: 'POST',
      }),
      transformResponse: createResponseTransformer<any>(),
    }),
    nextTurn: builder.mutation<any, { sessionId: string }>({
      query: ({ sessionId }) => ({
        url: `/combat/sessions/${sessionId}/next-turn`,
        method: 'POST',
      }),
      transformResponse: createResponseTransformer<any>(),
    }),
  }),
});

export const {
  useListCombatSessionsQuery,
  useGetCombatSessionQuery,
  useCreateCombatSessionMutation,
  useUpdateCombatSessionMutation,
  useDeleteCombatSessionMutation,
  useRollInitiativeMutation,
  useNextTurnMutation,
} = combatApi; 