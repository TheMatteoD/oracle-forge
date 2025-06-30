import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import type { GeneratorTable, GeneratorResult } from '../types/api';

interface GeneratorsState {
  generatorTables: GeneratorTable[];
  generatorResult: GeneratorResult | null;
  loading: boolean;
  error: string | null;
}

const initialState: GeneratorsState = {
  generatorTables: [],
  generatorResult: null,
  loading: false,
  error: null,
};

const generatorsSlice = createSlice({
  name: 'generators',
  initialState,
  reducers: {
    setGeneratorTables(state, action: PayloadAction<GeneratorTable[]>) {
      state.generatorTables = action.payload;
    },
    setGeneratorResult(state, action: PayloadAction<GeneratorResult | null>) {
      state.generatorResult = action.payload;
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
  setGeneratorTables,
  setGeneratorResult,
  setLoading,
  setError,
} = generatorsSlice.actions;

export default generatorsSlice.reducer; 