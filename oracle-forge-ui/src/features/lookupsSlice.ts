import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import type { Item, Monster, Spell, Rule } from '../types/api';

interface LookupsState {
  items: Item[];
  monsters: Monster[];
  spells: Spell[];
  rules: Rule[];
  loading: boolean;
  error: string | null;
}

const initialState: LookupsState = {
  items: [],
  monsters: [],
  spells: [],
  rules: [],
  loading: false,
  error: null,
};

const lookupsSlice = createSlice({
  name: 'lookups',
  initialState,
  reducers: {
    setItems(state, action: PayloadAction<Item[]>) {
      state.items = action.payload;
    },
    setMonsters(state, action: PayloadAction<Monster[]>) {
      state.monsters = action.payload;
    },
    setSpells(state, action: PayloadAction<Spell[]>) {
      state.spells = action.payload;
    },
    setRules(state, action: PayloadAction<Rule[]>) {
      state.rules = action.payload;
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
  setItems,
  setMonsters,
  setSpells,
  setRules,
  setLoading,
  setError,
} = lookupsSlice.actions;

export default lookupsSlice.reducer; 