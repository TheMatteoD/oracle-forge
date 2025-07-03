import { useState, useEffect } from "react";
import { useGetActiveAdventureQuery, useGetWorldStateQuery, useUpdateWorldStateMutation, type WorldState } from "@/api/adventureApi";

export default function WorldStateSection() {
  const [edit, setEdit] = useState(false);
  const [form, setForm] = useState<WorldState>({ 
    chaos_factor: 0, 
    current_scene: 0, 
    days_passed: 0 
  });
  
  // Get the active adventure
  const { data: activeData, isLoading: loadingActive, error: errorActive } = useGetActiveAdventureQuery();
  const adventure = activeData?.active;
  
  // RTK Query hooks
  const { data: world, isLoading, error } = useGetWorldStateQuery(adventure!, { skip: !adventure });
  const [updateWorldState, { isLoading: isUpdating }] = useUpdateWorldStateMutation();
  
  // Update form when world data changes
  useEffect(() => {
    if (world) {
      setForm({
        chaos_factor: world.chaos_factor || 0,
        current_scene: world.current_scene || 0,
        days_passed: world.days_passed || 0
      });
    }
  }, [world]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.type === 'number' ? parseInt(e.target.value) || 0 : e.target.value;
    setForm({ ...form, [e.target.name]: value });
  };

  const handleSave = async () => {
    if (!adventure) return;
    try {
      await updateWorldState({ adventure, data: form }).unwrap();
      setEdit(false);
    } catch (error) {
      console.error("Error saving world state:", error);
    }
  };

  if (loadingActive || isLoading) return <div className="text-gray-400">Loading world state...</div>;
  if (errorActive || error) return <div className="text-red-400">Error loading world state.</div>;
  if (!adventure) return <div className="text-gray-400">No active adventure.</div>;

  return (
    <div className="bg-gray-800 p-4 rounded shadow">
      <h3 className="text-lg font-semibold mb-2">🌍 World State</h3>
      
      {edit ? (
        <div className="space-y-2">
          <div>
            <label>Scene: </label>
            <input 
              name="current_scene" 
              type="number"
              value={form.current_scene} 
              onChange={handleChange} 
              className="bg-gray-700 text-white px-2 py-1 rounded" 
            />
          </div>
          <div>
            <label>Chaos: </label>
            <input 
              name="chaos_factor" 
              type="number"
              value={form.chaos_factor} 
              onChange={handleChange} 
              className="bg-gray-700 text-white px-2 py-1 rounded" 
            />
          </div>
          <div>
            <label>Days Passed: </label>
            <input 
              name="days_passed" 
              type="number"
              value={form.days_passed} 
              onChange={handleChange} 
              className="bg-gray-700 text-white px-2 py-1 rounded" 
            />
          </div>
          <button 
            onClick={handleSave} 
            disabled={isUpdating} 
            className="bg-green-600 px-3 py-1 rounded text-white mt-2"
          >
            {isUpdating ? 'Saving...' : 'Save'}
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
            <strong>Scene:</strong> {world?.current_scene || 0} | 
            <strong>Chaos:</strong> {world?.chaos_factor || 0} | 
            <strong>Days:</strong> {world?.days_passed || 0}
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