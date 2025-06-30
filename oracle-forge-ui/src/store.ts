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
  },
  // Add middleware for RTK Query here if needed
});

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// Typed version of useDispatch for use in components
export const useAppDispatch = () => useDispatch<AppDispatch>(); 