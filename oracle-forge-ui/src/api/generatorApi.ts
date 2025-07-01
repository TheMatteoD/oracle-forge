import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import config from '../config.js';
import { createResponseTransformer } from './baseApi';

export interface Generator {
  name: string;
  // Add other fields as needed
}

export const generatorApi = createApi({
  reducerPath: 'generatorApi',
  baseQuery: fetchBaseQuery({ baseUrl: config.SERVER_URL }),
  endpoints: (builder) => ({
    listGenerators: builder.query<Generator[], { system: string; category?: string }>({
      query: ({ system, category }) =>
        `/generators/${system}${category ? `?category=${category}` : ''}`,
      transformResponse: createResponseTransformer<Generator[]>(),
    }),
    getGenerator: builder.query<Generator, { system: string; name: string }>({
      query: ({ system, name }) => `/generators/${system}/${name}`,
      transformResponse: createResponseTransformer<Generator>(),
    }),
    runGenerator: builder.mutation<any, { system: string; name: string; parameters: Record<string, any> }>({
      query: ({ system, name, parameters }) => ({
        url: `/generators/${system}/${name}/run`,
        method: 'POST',
        body: parameters,
      }),
      transformResponse: createResponseTransformer<any>(),
    }),
  }),
});

export const {
  useListGeneratorsQuery,
  useGetGeneratorQuery,
  useRunGeneratorMutation,
} = generatorApi; 