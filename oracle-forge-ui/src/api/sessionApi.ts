import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import config from '../config.js';
import { createResponseTransformer } from './baseApi';

export interface LogEntry {
  timestamp: string;
  type: string;
  content: string;
}

export interface AppendLogRequest {
  content: string;
  type?: string;
}

export const sessionApi = createApi({
  reducerPath: 'sessionApi',
  baseQuery: fetchBaseQuery({ baseUrl: config.SERVER_URL }),
  endpoints: (builder) => ({
    endSession: builder.mutation<any, void>({
      query: () => ({
        url: '/session/end',
        method: 'POST',
      }),
      transformResponse: createResponseTransformer<any>(),
    }),
    getSessionLog: builder.query<LogEntry[], void>({
      query: () => '/session/log',
      transformResponse: createResponseTransformer<LogEntry[]>(),
    }),
    appendSessionLog: builder.mutation<LogEntry, AppendLogRequest>({
      query: (body) => ({
        url: '/session/log',
        method: 'POST',
        body,
      }),
      transformResponse: createResponseTransformer<LogEntry>(),
    }),
    // Add other session endpoints here as needed
  }),
});

export const {
  useEndSessionMutation,
  useGetSessionLogQuery,
  useAppendSessionLogMutation,
} = sessionApi; 