import { useEffect, useState } from "react";
import { AdventureAPI } from '@/api/apiClient';
import type { Adventure } from '@/types/api';

interface AdventureSelectorProps {
  onSelect: (adventure: Adventure) => void;
}

export default function AdventureSelector({ onSelect }: AdventureSelectorProps) {
  const [adventures, setAdventures] = useState<Adventure[]>([]);
  const [newAdvName, setNewAdvName] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadAdventures();
  }, []);

  const loadAdventures = async () => {
    try {
      const response = await AdventureAPI.listAdventures();
      if (response.success && response.data) {
        // Extract adventure names from the response
        const adventureNames = response.data.map((adv: Adventure) => adv.name);
        setAdventures(response.data);
      } else {
        console.error("Failed to fetch adventures:", response.error);
        setAdventures([]);
      }
    } catch (error) {
      console.error("Error fetching adventures:", error);
      setAdventures([]);
    }
  };

  const selectAdventure = async (adventure: Adventure) => {
    setLoading(true);
    try {
      const response = await AdventureAPI.getAdventure(adventure.name);
      
      if (response.success) {
        onSelect(adventure);
      } else {
        console.error("Failed to select adventure:", response.error);
      }
    } catch (error) {
      console.error("Error selecting adventure:", error);
    } finally {
      setLoading(false);
    }
  };

  const createAdventure = async () => {
    if (!newAdvName.trim()) return;
    
    setLoading(true);
    try {
      const response = await AdventureAPI.createAdventure({
        data: {
          name: newAdvName,
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
      
      if (response.success) {
        setAdventures([...adventures, response.data]);
        setNewAdvName("");
        // Optionally select the new adventure
        onSelect(response.data);
      } else {
        console.error("Failed to create adventure:", response.error);
      }
    } catch (error) {
      console.error("Error creating adventure:", error);
    } finally {
      setLoading(false);
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
      {adventures.length === 0 ? (
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