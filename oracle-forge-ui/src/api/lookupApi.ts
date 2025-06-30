import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import config from '../config.js';

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
    }),
    getEntity: builder.query<LookupEntity, { entityType: LookupEntityType; system: string; name: string }>({
      query: ({ entityType, system, name }) => `/lookup/${entityType}/${system}/${name}`,
    }),
  }),
});

export const {
  useLookupListQuery,
  useGetEntityQuery,
} = lookupApi; 