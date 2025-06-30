import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import config from '../config.js';

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
    }),
    getGenerator: builder.query<Generator, { system: string; name: string }>({
      query: ({ system, name }) => `/generators/${system}/${name}`,
    }),
    runGenerator: builder.mutation<any, { system: string; name: string; parameters: Record<string, any> }>({
      query: ({ system, name, parameters }) => ({
        url: `/generators/${system}/${name}/run`,
        method: 'POST',
        body: parameters,
      }),
    }),
  }),
});

export const {
  useListGeneratorsQuery,
  useGetGeneratorQuery,
  useRunGeneratorMutation,
} = generatorApi; 