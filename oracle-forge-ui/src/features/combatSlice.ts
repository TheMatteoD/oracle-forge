import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import type { CombatSession } from '../types/api';

interface CombatState {
  combatSessions: CombatSession[];
  activeCombatSession: CombatSession | null;
  loading: boolean;
  error: string | null;
}

const initialState: CombatState = {
  combatSessions: [],
  activeCombatSession: null,
  loading: false,
  error: null,
};

const combatSlice = createSlice({
  name: 'combat',
  initialState,
  reducers: {
    setCombatSessions(state, action: PayloadAction<CombatSession[]>) {
      state.combatSessions = action.payload;
    },
    setActiveCombatSession(state, action: PayloadAction<CombatSession | null>) {
      state.activeCombatSession = action.payload;
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
  setCombatSessions,
  setActiveCombatSession,
  setLoading,
  setError,
} = combatSlice.actions;

export default combatSlice.reducer; 