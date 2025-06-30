import { useState, useEffect } from "react";

interface WorldStateSectionProps {
  adventure: string;
}

interface WorldState {
  chaos_factor?: string;
  current_scene?: string;
  days_passed?: string;
}

export default function WorldStateSection({ adventure }: WorldStateSectionProps) {
  const [world, setWorld] = useState<WorldState>({});
  const [edit, setEdit] = useState(false);
  const [form, setForm] = useState<WorldState>({ 
    chaos_factor: '', 
    current_scene: '', 
    days_passed: '' 
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    if (!adventure) return;
    
    const loadWorldState = async () => {
      try {
        // Note: This endpoint might need to be added to AdventureAPI
        // For now, using direct fetch until we add it
        const response = await fetch(`/adventures/${adventure}/world_state`);
        const data = await response.json();
        
        if (data.success && data.data) {
          setWorld(data.data);
          setForm({
            chaos_factor: data.data.chaos_factor || '',
            current_scene: data.data.current_scene || '',
            days_passed: data.data.days_passed || ''
          });
        } else {
          setError('Failed to load world state.');
        }
      } catch (error) {
        console.error("Error loading world state:", error);
        setError('Failed to load world state.');
      }
    };

    loadWorldState();
  }, [adventure]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSave = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Note: This endpoint might need to be added to AdventureAPI
      // For now, using direct fetch until we add it
      const response = await fetch(`/adventures/${adventure}/world_state`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...world,
          chaos_factor: form.chaos_factor,
          current_scene: form.current_scene,
          days_passed: form.days_passed
        })
      });
      
      const data = await response.json();
      
      if (data.success) {
        setEdit(false);
        setWorld((prev) => ({ ...prev, ...form }));
      } else {
        setError('Failed to save world state.');
      }
    } catch (error) {
      console.error("Error saving world state:", error);
      setError('Failed to save world state.');
    } finally {
      setLoading(false);
    }
  };

  if (!adventure) return null;

  return (
    <div className="bg-gray-800 p-4 rounded shadow">
      <h3 className="text-lg font-semibold mb-2">🌍 World State</h3>
      
      {error && <div className="text-red-400 mb-2">{error}</div>}
      
      {edit ? (
        <div className="space-y-2">
          <div>
            <label>Scene: </label>
            <input 
              name="current_scene" 
              value={form.current_scene} 
              onChange={handleChange} 
              className="bg-gray-700 text-white px-2 py-1 rounded" 
            />
          </div>
          <div>
            <label>Chaos: </label>
            <input 
              name="chaos_factor" 
              value={form.chaos_factor} 
              onChange={handleChange} 
              className="bg-gray-700 text-white px-2 py-1 rounded" 
            />
          </div>
          <div>
            <label>Days Passed: </label>
            <input 
              name="days_passed" 
              value={form.days_passed} 
              onChange={handleChange} 
              className="bg-gray-700 text-white px-2 py-1 rounded" 
            />
          </div>
          <button 
            onClick={handleSave} 
            disabled={loading} 
            className="bg-green-600 px-3 py-1 rounded text-white mt-2"
          >
            {loading ? 'Saving...' : 'Save'}
          </button>
          <button 
            onClick={() => setEdit(false)} 
            className="ml-2 px-3 py-1 rounded bg-gray-600 text-white"
          >
            Cancel
          </button>
        </div>
      ) : (
        <div>
          <div>
            <strong>Scene:</strong> {world.current_scene} | 
            <strong>Chaos:</strong> {world.chaos_factor} | 
            <strong>Days:</strong> {world.days_passed}
          </div>
          <button 
            onClick={() => setEdit(true)} 
            className="mt-2 px-3 py-1 rounded bg-blue-600 text-white"
          >
            Edit
          </button>
        </div>
      )}
    </div>
  );
} 