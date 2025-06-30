import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import type { Adventure } from '../types/api';
import { fetchAdventures, fetchAdventure, createAdventureThunk } from './adventuresThunks';

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
  extraReducers: (builder) => {
    builder
      .addCase(fetchAdventures.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAdventures.fulfilled, (state, action) => {
        state.loading = false;
        state.adventures = action.payload;
      })
      .addCase(fetchAdventures.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string || 'Failed to fetch adventures';
      })
      .addCase(fetchAdventure.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAdventure.fulfilled, (state, action) => {
        state.loading = false;
        state.activeAdventure = action.payload;
      })
      .addCase(fetchAdventure.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string || 'Failed to fetch adventure';
      })
      .addCase(createAdventureThunk.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createAdventureThunk.fulfilled, (state, action) => {
        state.loading = false;
        state.activeAdventure = action.payload;
      })
      .addCase(createAdventureThunk.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string || 'Failed to create adventure';
      });
  },
});

export const {
  setAdventures,
  setActiveAdventure,
  setLoading,
  setError,
} = adventuresSlice.actions;

export default adventuresSlice.reducer; 