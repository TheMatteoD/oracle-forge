import { useState } from "react";
import {
  useListAdventuresQuery,
  useCreateAdventureMutation,
  useLazyGetAdventureQuery,
} from "@/api/adventureApi";
import type { Adventure } from '@/api/adventureApi';

interface AdventureSelectorProps {
  onSelect: (adventure: Adventure) => void;
}

export default function AdventureSelector({ onSelect }: AdventureSelectorProps) {
  const { data: adventures = [], isLoading, error, refetch } = useListAdventuresQuery();
  const [createAdventure, { isLoading: isCreating }] = useCreateAdventureMutation();
  const [getAdventure, { isLoading: isSelecting }] = useLazyGetAdventureQuery();
  const [newAdvName, setNewAdvName] = useState("");
  const [selectingId, setSelectingId] = useState<string | null>(null);
  const [selectError, setSelectError] = useState<string | null>(null);

  // Defensive check to ensure adventures is always an array
  const safeAdventures = Array.isArray(adventures) ? adventures : [];

  const handleSelectAdventure = async (adventure: Adventure) => {
    setSelectingId(adventure.id || adventure.name);
    setSelectError(null);
    try {
      const result = await getAdventure(adventure.name).unwrap();
      onSelect(result);
    } catch (e: any) {
      setSelectError(e.data?.error || e.message || 'Failed to activate adventure');
    } finally {
      setSelectingId(null);
    }
  };

  const handleCreateAdventure = async () => {
    if (!newAdvName.trim()) return;
    try {
      await createAdventure({ name: newAdvName.trim() }).unwrap();
      setNewAdvName("");
      refetch();
    } catch (e: any) {
      setSelectError(e.data?.error || e.message || 'Failed to create adventure');
    }
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
          onKeyPress={(e) => e.key === 'Enter' && handleCreateAdventure()}
        />
        <button
          onClick={handleCreateAdventure}
          disabled={isCreating || !newAdvName.trim()}
          className="bg-purple-700 text-white px-4 py-2 rounded"
        >
          {isCreating ? 'Creating...' : 'Create Adventure'}
        </button>
      </div>

      <h2 className="mt-6">📂 Select Adventure</h2>
      {error && <p className="text-red-400">{String(error)}</p>}
      {selectError && <p className="text-red-400">{selectError}</p>}
      {isLoading && <p>Loading adventures...</p>}
      {safeAdventures.length === 0 && !isLoading ? (
        <p>No adventures found. Create one above!</p>
      ) : (
        <ul style={{ listStyle: 'none', paddingLeft: 0 }}>
          {safeAdventures.map((adv) => (
            <li key={adv.id || adv.name} style={{ marginBottom: '0.5em' }}>
              <button
                onClick={() => handleSelectAdventure(adv)}
                disabled={isLoading || isSelecting || selectingId === (adv.id || adv.name)}
                className="bg-gray-700 text-white px-4 py-2 rounded"
              >
                {selectingId === (adv.id || adv.name) ? 'Selecting...' : adv.name}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
} 