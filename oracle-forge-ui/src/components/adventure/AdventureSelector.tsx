import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { useAppDispatch } from "@/store";
import { fetchAdventures, fetchAdventure, createAdventureThunk } from "@/features/adventuresThunks";
import type { Adventure } from '@/types/api';
import type { RootState } from '@/store';

interface AdventureSelectorProps {
  onSelect: (adventure: Adventure) => void;
}

export default function AdventureSelector({ onSelect }: AdventureSelectorProps) {
  const dispatch = useAppDispatch();
  const adventures = useSelector((state: RootState) => state.adventures.adventures);
  const loading = useSelector((state: RootState) => state.adventures.loading);
  const error = useSelector((state: RootState) => state.adventures.error);
  const [newAdvName, setNewAdvName] = useState("");

  useEffect(() => {
    dispatch(fetchAdventures());
  }, [dispatch]);

  const selectAdventure = async (adventure: Adventure) => {
    // Dispatch thunk to fetch and set active adventure
    const resultAction = await dispatch(fetchAdventure(adventure.name));
    if (fetchAdventure.fulfilled.match(resultAction)) {
      onSelect(resultAction.payload);
    } else {
      // Optionally handle error
      // (error is already in Redux state)
    }
  };

  const createAdventure = async () => {
    if (!newAdvName.trim()) return;
    const resultAction = await dispatch(createAdventureThunk({ name: newAdvName.trim() }));
    if (createAdventureThunk.fulfilled.match(resultAction)) {
      setNewAdvName("");
      onSelect(resultAction.payload);
    }
    // Error is handled in Redux state
  };

  return (
    <div>
      <h2>🎲 Create New Adventure</h2>
      <div style={{ marginBottom: '1em' }}>
        <input
          type="text"
          value={newAdvName}
          onChange={(e) => setNewAdvName(e.target.value)}
          placeholder="Enter adventure name"
          style={{ marginRight: '1em', padding: '0.5em' }}
          onKeyPress={(e) => e.key === 'Enter' && createAdventure()}
        />
        <button 
          onClick={createAdventure} 
          disabled={loading || !newAdvName.trim()}
          className="bg-purple-700 text-white px-4 py-2 rounded"
        >
          {loading ? 'Creating...' : 'Create Adventure'}
        </button>
      </div>

      <h2 className="mt-6">📂 Select Adventure</h2>
      {error && <p className="text-red-400">{error}</p>}
      {loading && <p>Loading adventures...</p>}
      {adventures.length === 0 && !loading ? (
        <p>No adventures found. Create one above!</p>
      ) : (
        <ul style={{ listStyle: 'none', paddingLeft: 0 }}>
          {adventures.map((adv) => (
            <li key={adv.id || adv.name} style={{ marginBottom: '0.5em' }}>
              <button
                onClick={() => selectAdventure(adv)}
                disabled={loading}
                className="bg-gray-700 text-white px-4 py-2 rounded"
              >
                {adv.name}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
} 