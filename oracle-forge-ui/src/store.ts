import { configureStore } from '@reduxjs/toolkit';
import { useDispatch } from 'react-redux';
// import adventuresReducer from './features/adventures/adventuresSlice'; // To be created

// Placeholder root reducer (add slices here as you create them)
export const store = configureStore({
  reducer: {
    // adventures: adventuresReducer,
    // Add other slices here
  },
  // Add middleware for RTK Query here if needed
});

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// Typed version of useDispatch for use in components
export const useAppDispatch = () => useDispatch<AppDispatch>(); 