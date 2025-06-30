import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import type { Session } from '../types/api';

interface SessionsState {
  sessions: Session[];
  activeSession: Session | null;
  loading: boolean;
  error: string | null;
}

const initialState: SessionsState = {
  sessions: [],
  activeSession: null,
  loading: false,
  error: null,
};

const sessionsSlice = createSlice({
  name: 'sessions',
  initialState,
  reducers: {
    setSessions(state, action: PayloadAction<Session[]>) {
      state.sessions = action.payload;
    },
    setActiveSession(state, action: PayloadAction<Session | null>) {
      state.activeSession = action.payload;
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
  setSessions,
  setActiveSession,
  setLoading,
  setError,
} = sessionsSlice.actions;

export default sessionsSlice.reducer; 