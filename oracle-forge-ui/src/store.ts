import { configureStore } from '@reduxjs/toolkit';
import { useDispatch } from 'react-redux';
import adventuresReducer from './features/adventuresSlice';
import playersReducer from './features/playersSlice';
import worldReducer from './features/worldSlice';
import sessionsReducer from './features/sessionsSlice';
import oraclesReducer from './features/oraclesSlice';
import generatorsReducer from './features/generatorsSlice';
import lookupsReducer from './features/lookupsSlice';
import combatReducer from './features/combatSlice';

// Import RTK Query API slices
import { adventureApi } from './api/adventureApi';
import { lookupApi } from './api/lookupApi';
import { oracleApi } from './api/oracleApi';
import { generatorApi } from './api/generatorApi';
import { combatApi } from './api/combatApi';

export const store = configureStore({
  reducer: {
    adventures: adventuresReducer,
    players: playersReducer,
    world: worldReducer,
    sessions: sessionsReducer,
    oracles: oraclesReducer,
    generators: generatorsReducer,
    lookups: lookupsReducer,
    combat: combatReducer,
    // RTK Query reducers
    [adventureApi.reducerPath]: adventureApi.reducer,
    [lookupApi.reducerPath]: lookupApi.reducer,
    [oracleApi.reducerPath]: oracleApi.reducer,
    [generatorApi.reducerPath]: generatorApi.reducer,
    [combatApi.reducerPath]: combatApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(
      adventureApi.middleware,
      lookupApi.middleware,
      oracleApi.middleware,
      generatorApi.middleware,
      combatApi.middleware
    ),
});

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// Typed version of useDispatch for use in components
export const useAppDispatch = () => useDispatch<AppDispatch>(); 