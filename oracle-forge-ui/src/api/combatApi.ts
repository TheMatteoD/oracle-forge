import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import config from '../config.js';

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
    }),
    getCombatSession: builder.query<CombatSession, { sessionId: string }>({
      query: ({ sessionId }) => `/combat/sessions/${sessionId}`,
    }),
    createCombatSession: builder.mutation<CombatSession, { data: any }>({
      query: ({ data }) => ({
        url: '/combat/sessions',
        method: 'POST',
        body: data,
      }),
    }),
    updateCombatSession: builder.mutation<CombatSession, { sessionId: string; data: any }>({
      query: ({ sessionId, data }) => ({
        url: `/combat/sessions/${sessionId}`,
        method: 'PUT',
        body: data,
      }),
    }),
    deleteCombatSession: builder.mutation<void, { sessionId: string }>({
      query: ({ sessionId }) => ({
        url: `/combat/sessions/${sessionId}`,
        method: 'DELETE',
      }),
    }),
    rollInitiative: builder.mutation<any, { sessionId: string }>({
      query: ({ sessionId }) => ({
        url: `/combat/sessions/${sessionId}/roll-initiative`,
        method: 'POST',
      }),
    }),
    nextTurn: builder.mutation<any, { sessionId: string }>({
      query: ({ sessionId }) => ({
        url: `/combat/sessions/${sessionId}/next-turn`,
        method: 'POST',
      }),
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