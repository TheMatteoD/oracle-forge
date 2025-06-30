import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import type { WorldState } from '../types/api';

interface WorldSliceState {
  worldState: WorldState | null;
  loading: boolean;
  error: string | null;
}

const initialState: WorldSliceState = {
  worldState: null,
  loading: false,
  error: null,
};

const worldSlice = createSlice({
  name: 'world',
  initialState,
  reducers: {
    setWorldState(state, action: PayloadAction<WorldState | null>) {
      state.worldState = action.payload;
    },
    setLoading(state, action: PayloadAction<boolean>) {
      state.loading = action.payload;
    },
    setError(state, action: PayloadAction<string | null>) {
      state.error = action.payload;
    },
  },
});

export const {
  setWorldState,
  setLoading,
  setError,
} = worldSlice.actions;

export default worldSlice.reducer; 