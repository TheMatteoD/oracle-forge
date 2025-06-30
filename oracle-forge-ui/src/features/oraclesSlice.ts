import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import type { OracleTable, OracleResult } from '../types/api';

interface OraclesState {
  oracleTables: OracleTable[];
  oracleResult: OracleResult | null;
  loading: boolean;
  error: string | null;
}

const initialState: OraclesState = {
  oracleTables: [],
  oracleResult: null,
  loading: false,
  error: null,
};

const oraclesSlice = createSlice({
  name: 'oracles',
  initialState,
  reducers: {
    setOracleTables(state, action: PayloadAction<OracleTable[]>) {
      state.oracleTables = action.payload;
    },
    setOracleResult(state, action: PayloadAction<OracleResult | null>) {
      state.oracleResult = action.payload;
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
  setOracleTables,
  setOracleResult,
  setLoading,
  setError,
} = oraclesSlice.actions;

export default oraclesSlice.reducer; 