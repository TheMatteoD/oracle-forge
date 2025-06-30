import { createAsyncThunk } from '@reduxjs/toolkit';
import { AdventureAPI } from '../api/apiClient';
import type { Adventure } from '../types/api';

// Load all adventures
export const fetchAdventures = createAsyncThunk<Adventure[]>(
  'adventures/fetchAdventures',
  async (_, { rejectWithValue }) => {
    try {
      const response = await AdventureAPI.listAdventures();
      if (response.success && response.data) {
        return response.data as Adventure[];
      } else {
        return rejectWithValue(response.error || 'Failed to fetch adventures');
      }
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch adventures');
    }
  }
);

// Select (fetch) a single adventure by name
export const fetchAdventure = createAsyncThunk<Adventure, string>(
  'adventures/fetchAdventure',
  async (adventureName, { rejectWithValue }) => {
    try {
      const response = await AdventureAPI.getAdventure(adventureName);
      if (response.success && response.data) {
        return response.data as Adventure;
      } else {
        return rejectWithValue(response.error || 'Failed to fetch adventure');
      }
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch adventure');
    }
  }
);

// Create a new adventure
export const createAdventureThunk = createAsyncThunk<Adventure, { name: string }>(
  'adventures/createAdventure',
  async ({ name }, { rejectWithValue, dispatch }) => {
    try {
      const response = await AdventureAPI.createAdventure({
        data: {
          name,
          system: 'dnd5e',
          world_state: {
            npcs: [],
            factions: [],
            locations: [],
            story_lines: []
          },
          players: []
        }
      });
      if (response.success && response.data) {
        // Refresh the adventure list after creation
        dispatch(fetchAdventures());
        return response.data as Adventure;
      } else {
        return rejectWithValue(response.error || 'Failed to create adventure');
      }
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to create adventure');
    }
  }
); 