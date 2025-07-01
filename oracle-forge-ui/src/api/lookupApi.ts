import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import config from '../config.js';
import { createResponseTransformer } from './baseApi';

export type LookupEntityType = 'items' | 'monsters' | 'spells' | 'rules';

export interface LookupEntity {
  name: string;
  // Add other fields as needed
}

export const lookupApi = createApi({
  reducerPath: 'lookupApi',
  baseQuery: fetchBaseQuery({ baseUrl: config.SERVER_URL }),
  endpoints: (builder) => ({
    lookupList: builder.query<LookupEntity[], { entityType: LookupEntityType; system: string }>({
      query: ({ entityType, system }) => `/lookup/${entityType}/${system}`,
      transformResponse: createResponseTransformer<LookupEntity[]>(),
    }),
    getEntity: builder.query<LookupEntity, { entityType: LookupEntityType; system: string; name: string }>({
      query: ({ entityType, system, name }) => `/lookup/${entityType}/${system}/${name}`,
      transformResponse: createResponseTransformer<LookupEntity>(),
    }),
  }),
});

export const {
  useLookupListQuery,
  useGetEntityQuery,
} = lookupApi; 