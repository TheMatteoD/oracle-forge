import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import config from '../config.js';
import { createResponseTransformer } from './baseApi';

export interface OracleTable {
  name: string;
}

export const oracleApi = createApi({
  reducerPath: 'oracleApi',
  baseQuery: fetchBaseQuery({ baseUrl: config.SERVER_URL }),
  endpoints: (builder) => ({
    listTables: builder.query<OracleTable[], { system: string; category?: string }>({
      query: ({ system, category }) =>
        `/oracle/tables/${system}${category ? `?category=${category}` : ''}`,
      transformResponse: createResponseTransformer<OracleTable[]>(),
    }),
    getTable: builder.query<OracleTable, { system: string; name: string }>({
      query: ({ system, name }) => `/oracle/tables/${system}/${name}`,
      transformResponse: createResponseTransformer<OracleTable>(),
    }),
    rollTable: builder.query<any, { system: string; name: string; custom_roll?: number }>({
      query: ({ system, name, custom_roll }) =>
        `/oracle/tables/${system}/${name}/roll${custom_roll ? `?custom_roll=${custom_roll}` : ''}`,
      transformResponse: createResponseTransformer<any>(),
    }),
    yesNo: builder.query<any, { system: string; question?: string }>({
      query: ({ system, question }) =>
        `/oracle/yesno/${system}${question ? `?question=${encodeURIComponent(question)}` : ''}`,
      transformResponse: createResponseTransformer<any>(),
    }),
    sceneCheck: builder.mutation<any, { chaos?: number; flavor?: boolean }>({
      query: (body) => ({
        url: '/oracle/scene',
        method: 'POST',
        body,
      }),
      transformResponse: createResponseTransformer<any>(),
    }),
    meaningOracle: builder.query<any, { system: string; focus?: string }>({
      query: ({ system, focus }) =>
        `/oracle/meaning/${system}${focus ? `?focus=${encodeURIComponent(focus)}` : ''}`,
      transformResponse: createResponseTransformer<any>(),
    }),
  }),
});

export const {
  useListTablesQuery,
  useGetTableQuery,
  useRollTableQuery,
  useYesNoQuery,
  useMeaningOracleQuery,
  useSceneCheckMutation,
} = oracleApi; 