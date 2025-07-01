import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import config from '../config.js';
import { createResponseTransformer } from './baseApi';

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
    // Add other session endpoints here as needed
  }),
});

export const {
  useEndSessionMutation,
} = sessionApi; 