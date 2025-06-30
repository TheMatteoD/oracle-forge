import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import type { Adventure } from '../types/api';
// Async logic will be handled by RTK Query going forward

interface AdventuresState {
  adventures: Adventure[];
  activeAdventure: Adventure | null;
  loading: boolean;
  error: string | null;
}

const initialState: AdventuresState = {
  adventures: [],
  activeAdventure: null,
  loading: false,
  error: null,
};

const adventuresSlice = createSlice({
  name: 'adventures',
  initialState,
  reducers: {
    setAdventures(state, action: PayloadAction<Adventure[]>) {
      state.adventures = action.payload;
    },
    setActiveAdventure(state, action: PayloadAction<Adventure | null>) {
      state.activeAdventure = action.payload;
    },
    setLoading(state, action: PayloadAction<boolean>) {
      state.loading = action.payload;
    },
    setError(state, action: PayloadAction<string | null>) {
      state.error = action.payload;
    },
  },
  // No extraReducers needed; async handled by RTK Query
});

export const {
  setAdventures,
  setActiveAdventure,
  setLoading,
  setError,
} = adventuresSlice.actions;

export default adventuresSlice.reducer; 