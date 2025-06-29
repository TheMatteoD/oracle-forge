import React, { useEffect, useState } from "react";
import config from "../../config";

const API_BASE = config.SERVER_URL;

function FactionsSection({ adventure }) {
  const [factions, setFactions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showAdd, setShowAdd] = useState(false);
  const [editFaction, setEditFaction] = useState(null);
  const [form, setForm] = useState({ name: '', description: '', status: '' });

  const fetchFactions = () => {
    setLoading(true);
    fetch(`${API_BASE}/adventures/${adventure}/world/factions`)
      .then(res => res.json())
      .then(response => {
        if (response.success) {
          setFactions(response.data || []);
        } else {
          console.error("Failed to fetch factions:", response.error);
          setFactions([]);
        }
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching factions:", error);
        setError('Failed to load factions.');
        setFactions([]);
        setLoading(false);
      });
  };

  useEffect(() => { if (adventure) fetchFactions(); }, [adventure]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleAdd = () => {
    setLoading(true);
    fetch(`${API_BASE}/adventures/${adventure}/world/factions/${encodeURIComponent(form.name)}`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form)
    })
      .then(res => res.json())
      .then(response => {
        if (response.success) {
          setShowAdd(false);
          setForm({ name: '', description: '', status: '' });
          fetchFactions();
        } else {
          console.error("Failed to add faction:", response.error);
          setError('Failed to add faction.');
        }
      })
      .catch(error => {
        console.error("Error adding faction:", error);
        setError('Failed to add faction.');
      });
  };

  const handleEdit = (faction) => {
    setEditFaction(faction.name);
    setForm(faction);
  };

  const handleUpdate = () => {
    setLoading(true);
    fetch(`${API_BASE}/adventures/${adventure}/world/factions/${encodeURIComponent(editFaction)}`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form)
    })
      .then(res => res.json())
      .then(response => {
        if (response.success) {
          setEditFaction(null);
          setForm({ name: '', description: '', status: '' });
          fetchFactions();
        } else {
          console.error("Failed to update faction:", response.error);
          setError('Failed to update faction.');
        }
      })
      .catch(error => {
        console.error("Error updating faction:", error);
        setError('Failed to update faction.');
      });
  };

  const handleDelete = (name) => {
    if (!window.confirm(`Delete faction '${name}'?`)) return;
    setLoading(true);
    fetch(`${API_BASE}/adventures/${adventure}/world/factions/${encodeURIComponent(name)}`, { method: 'DELETE' })
      .then(res => res.json())
      .then(response => {
        if (response.success) {
          fetchFactions();
        } else {
          console.error("Failed to delete faction:", response.error);
          setError('Failed to delete faction.');
        }
      })
      .catch(error => {
        console.error("Error deleting faction:", error);
        setError('Failed to delete faction.');
      });
  };

  return (
    <div className="mt-4">
      <h4 className="font-semibold">Factions</h4>
      {error && <div className="text-red-400 mb-2">{error}</div>}
      {loading && <div>Loading...</div>}
      <ul className="text-sm list-disc ml-5">
        {factions.map((f, i) => (
          <li key={i} className="mb-1">
            <span className="font-bold">{f.name}</span> – {f.status}
            <button className="ml-2 text-blue-400 underline" onClick={() => handleEdit(f)}>Edit</button>
            <button className="ml-2 text-red-400 underline" onClick={() => handleDelete(f.name)}>Delete</button>
          </li>
        ))}
      </ul>
      {showAdd ? (
        <div className="mt-2 space-y-1">
          <input name="name" placeholder="Name" value={form.name} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <input name="description" placeholder="Description" value={form.description} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <input name="status" placeholder="Status" value={form.status} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <button onClick={handleAdd} className="bg-green-600 px-2 py-1 rounded text-white">Add</button>
          <button onClick={() => setShowAdd(false)} className="ml-2 px-2 py-1 rounded bg-gray-600 text-white">Cancel</button>
        </div>
      ) : (
        <button onClick={() => setShowAdd(true)} className="mt-2 px-2 py-1 rounded bg-blue-600 text-white">Add Faction</button>
      )}
      {editFaction && (
        <div className="mt-2 space-y-1">
          <input name="name" placeholder="Name" value={form.name} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <input name="description" placeholder="Description" value={form.description} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <input name="status" placeholder="Status" value={form.status} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <button onClick={handleUpdate} className="bg-green-600 px-2 py-1 rounded text-white">Save</button>
          <button onClick={() => setEditFaction(null)} className="ml-2 px-2 py-1 rounded bg-gray-600 text-white">Cancel</button>
        </div>
      )}
    </div>
  );
}

function LocationsSection({ adventure }) {
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showAdd, setShowAdd] = useState(false);
  const [editLocation, setEditLocation] = useState(null);
  const [form, setForm] = useState({ name: '', description: '', status: '' });

  const fetchLocations = () => {
    setLoading(true);
    fetch(`${API_BASE}/adventures/${adventure}/world/locations`)
      .then(res => res.json())
      .then(response => {
        if (response.success) {
          setLocations(response.data || []);
        } else {
          console.error("Failed to fetch locations:", response.error);
          setLocations([]);
        }
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching locations:", error);
        setError('Failed to load locations.');
        setLocations([]);
        setLoading(false);
      });
  };

  useEffect(() => { if (adventure) fetchLocations(); }, [adventure]);
  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });
  
  const handleAdd = () => {
    setLoading(true);
    fetch(`${API_BASE}/adventures/${adventure}/world/locations/${encodeURIComponent(form.name)}`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form)
    })
      .then(res => res.json())
      .then(response => {
        if (response.success) {
          setShowAdd(false);
          setForm({ name: '', description: '', status: '' });
          fetchLocations();
        } else {
          console.error("Failed to add location:", response.error);
          setError('Failed to add location.');
        }
      })
      .catch(error => {
        console.error("Error adding location:", error);
        setError('Failed to add location.');
      });
  };

  const handleEdit = (loc) => { setEditLocation(loc.name); setForm(loc); };
  
  const handleUpdate = () => {
    setLoading(true);
    fetch(`${API_BASE}/adventures/${adventure}/world/locations/${encodeURIComponent(editLocation)}`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form)
    })
      .then(res => res.json())
      .then(response => {
        if (response.success) {
          setEditLocation(null);
          setForm({ name: '', description: '', status: '' });
          fetchLocations();
        } else {
          console.error("Failed to update location:", response.error);
          setError('Failed to update location.');
        }
      })
      .catch(error => {
        console.error("Error updating location:", error);
        setError('Failed to update location.');
      });
  };

  const handleDelete = (name) => {
    if (!window.confirm(`Delete location '${name}'?`)) return;
    setLoading(true);
    fetch(`${API_BASE}/adventures/${adventure}/world/locations/${encodeURIComponent(name)}`, { method: 'DELETE' })
      .then(res => res.json())
      .then(response => {
        if (response.success) {
          fetchLocations();
        } else {
          console.error("Failed to delete location:", response.error);
          setError('Failed to delete location.');
        }
      })
      .catch(error => {
        console.error("Error deleting location:", error);
        setError('Failed to delete location.');
      });
  };

  return (
    <div className="mt-4">
      <h4 className="font-semibold">Locations</h4>
      {error && <div className="text-red-400 mb-2">{error}</div>}
      {loading && <div>Loading...</div>}
      <ul className="text-sm list-disc ml-5">
        {locations.map((loc, i) => (
          <li key={i} className="mb-1">
            <span className="font-bold">{loc.name}</span> – {loc.status}
            <button className="ml-2 text-blue-400 underline" onClick={() => handleEdit(loc)}>Edit</button>
            <button className="ml-2 text-red-400 underline" onClick={() => handleDelete(loc.name)}>Delete</button>
          </li>
        ))}
      </ul>
      {showAdd ? (
        <div className="mt-2 space-y-1">
          <input name="name" placeholder="Name" value={form.name} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <input name="description" placeholder="Description" value={form.description} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <input name="status" placeholder="Status" value={form.status} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <button onClick={handleAdd} className="bg-green-600 px-2 py-1 rounded text-white">Add</button>
          <button onClick={() => setShowAdd(false)} className="ml-2 px-2 py-1 rounded bg-gray-600 text-white">Cancel</button>
        </div>
      ) : (
        <button onClick={() => setShowAdd(true)} className="mt-2 px-2 py-1 rounded bg-blue-600 text-white">Add Location</button>
      )}
      {editLocation && (
        <div className="mt-2 space-y-1">
          <input name="name" placeholder="Name" value={form.name} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <input name="description" placeholder="Description" value={form.description} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <input name="status" placeholder="Status" value={form.status} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <button onClick={handleUpdate} className="bg-green-600 px-2 py-1 rounded text-white">Save</button>
          <button onClick={() => setEditLocation(null)} className="ml-2 px-2 py-1 rounded bg-gray-600 text-white">Cancel</button>
        </div>
      )}
    </div>
  );
}

function StoryLinesSection({ adventure }) {
  const [storyLines, setStoryLines] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showAdd, setShowAdd] = useState(false);
  const [editStory, setEditStory] = useState(null);
  const [form, setForm] = useState({ name: '', description: '', status: '' });

  const fetchStoryLines = () => {
    setLoading(true);
    fetch(`${API_BASE}/adventures/${adventure}/world/story_lines`)
      .then(res => res.json())
      .then(response => {
        if (response.success) {
          setStoryLines(response.data || []);
        } else {
          console.error("Failed to fetch story lines:", response.error);
          setStoryLines([]);
        }
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching story lines:", error);
        setError('Failed to load story lines.');
        setStoryLines([]);
        setLoading(false);
      });
  };

  useEffect(() => { if (adventure) fetchStoryLines(); }, [adventure]);
  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });
  
  const handleAdd = () => {
    setLoading(true);
    fetch(`${API_BASE}/adventures/${adventure}/world/story_lines/${encodeURIComponent(form.name)}`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form)
    })
      .then(res => res.json())
      .then(response => {
        if (response.success) {
          setShowAdd(false);
          setForm({ name: '', description: '', status: '' });
          fetchStoryLines();
        } else {
          console.error("Failed to add story line:", response.error);
          setError('Failed to add story line.');
        }
      })
      .catch(error => {
        console.error("Error adding story line:", error);
        setError('Failed to add story line.');
      });
  };

  const handleEdit = (story) => { setEditStory(story.name); setForm(story); };
  
  const handleUpdate = () => {
    setLoading(true);
    fetch(`${API_BASE}/adventures/${adventure}/world/story_lines/${encodeURIComponent(editStory)}`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form)
    })
      .then(res => res.json())
      .then(response => {
        if (response.success) {
          setEditStory(null);
          setForm({ name: '', description: '', status: '' });
          fetchStoryLines();
        } else {
          console.error("Failed to update story line:", response.error);
          setError('Failed to update story line.');
        }
      })
      .catch(error => {
        console.error("Error updating story line:", error);
        setError('Failed to update story line.');
      });
  };

  const handleDelete = (name) => {
    if (!window.confirm(`Delete story line '${name}'?`)) return;
    setLoading(true);
    fetch(`${API_BASE}/adventures/${adventure}/world/story_lines/${encodeURIComponent(name)}`, { method: 'DELETE' })
      .then(res => res.json())
      .then(response => {
        if (response.success) {
          fetchStoryLines();
        } else {
          console.error("Failed to delete story line:", response.error);
          setError('Failed to delete story line.');
        }
      })
      .catch(error => {
        console.error("Error deleting story line:", error);
        setError('Failed to delete story line.');
      });
  };

  return (
    <div className="mt-4">
      <h4 className="font-semibold">Story Lines</h4>
      {error && <div className="text-red-400 mb-2">{error}</div>}
      {loading && <div>Loading...</div>}
      <ul className="text-sm list-disc ml-5">
        {storyLines.map((s, i) => (
          <li key={i} className="mb-1">
            <span className="font-bold">{s.name}</span> – {s.status}
            <button className="ml-2 text-blue-400 underline" onClick={() => handleEdit(s)}>Edit</button>
            <button className="ml-2 text-red-400 underline" onClick={() => handleDelete(s.name)}>Delete</button>
          </li>
        ))}
      </ul>
      {showAdd ? (
        <div className="mt-2 space-y-1">
          <input name="name" placeholder="Name" value={form.name} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <input name="description" placeholder="Description" value={form.description} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <input name="status" placeholder="Status" value={form.status} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <button onClick={handleAdd} className="bg-green-600 px-2 py-1 rounded text-white">Add</button>
          <button onClick={() => setShowAdd(false)} className="ml-2 px-2 py-1 rounded bg-gray-600 text-white">Cancel</button>
        </div>
      ) : (
        <button onClick={() => setShowAdd(true)} className="mt-2 px-2 py-1 rounded bg-blue-600 text-white">Add Story Line</button>
      )}
      {editStory && (
        <div className="mt-2 space-y-1">
          <input name="name" placeholder="Name" value={form.name} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <input name="description" placeholder="Description" value={form.description} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <input name="status" placeholder="Status" value={form.status} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <button onClick={handleUpdate} className="bg-green-600 px-2 py-1 rounded text-white">Save</button>
          <button onClick={() => setEditStory(null)} className="ml-2 px-2 py-1 rounded bg-gray-600 text-white">Cancel</button>
        </div>
      )}
    </div>
  );
}

function NPCsSection({ adventure }) {
  const [npcs, setNpcs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showAdd, setShowAdd] = useState(false);
  const [editNpc, setEditNpc] = useState(null);
  const [form, setForm] = useState({ name: '', description: '', status: '', location: '', faction: '' });

  const fetchNpcs = () => {
    setLoading(true);
    fetch(`${API_BASE}/adventures/${adventure}/world/npcs`)
      .then(res => res.json())
      .then(response => {
        if (response.success) {
          setNpcs(response.data || []);
        } else {
          console.error("Failed to fetch NPCs:", response.error);
          setNpcs([]);
        }
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching NPCs:", error);
        setError('Failed to load NPCs.');
        setNpcs([]);
        setLoading(false);
      });
  };

  useEffect(() => { if (adventure) fetchNpcs(); }, [adventure]);
  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });
  
  const handleAdd = () => {
    setLoading(true);
    fetch(`${API_BASE}/adventures/${adventure}/world/npcs/${encodeURIComponent(form.name)}`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form)
    })
      .then(res => res.json())
      .then(response => {
        if (response.success) {
          setShowAdd(false);
          setForm({ name: '', description: '', status: '', location: '', faction: '' });
          fetchNpcs();
        } else {
          console.error("Failed to add NPC:", response.error);
          setError('Failed to add NPC.');
        }
      })
      .catch(error => {
        console.error("Error adding NPC:", error);
        setError('Failed to add NPC.');
      });
  };

  const handleEdit = (npc) => { setEditNpc(npc.name); setForm(npc); };
  
  const handleUpdate = () => {
    setLoading(true);
    fetch(`${API_BASE}/adventures/${adventure}/world/npcs/${encodeURIComponent(editNpc)}`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form)
    })
      .then(res => res.json())
      .then(response => {
        if (response.success) {
          setEditNpc(null);
          setForm({ name: '', description: '', status: '', location: '', faction: '' });
          fetchNpcs();
        } else {
          console.error("Failed to update NPC:", response.error);
          setError('Failed to update NPC.');
        }
      })
      .catch(error => {
        console.error("Error updating NPC:", error);
        setError('Failed to update NPC.');
      });
  };

  const handleDelete = (name) => {
    if (!window.confirm(`Delete NPC '${name}'?`)) return;
    setLoading(true);
    fetch(`${API_BASE}/adventures/${adventure}/world/npcs/${encodeURIComponent(name)}`, { method: 'DELETE' })
      .then(res => res.json())
      .then(response => {
        if (response.success) {
          fetchNpcs();
        } else {
          console.error("Failed to delete NPC:", response.error);
          setError('Failed to delete NPC.');
        }
      })
      .catch(error => {
        console.error("Error deleting NPC:", error);
        setError('Failed to delete NPC.');
      });
  };

  return (
    <div className="mt-4">
      <h4 className="font-semibold">NPCs</h4>
      {error && <div className="text-red-400 mb-2">{error}</div>}
      {loading && <div>Loading...</div>}
      <ul className="text-sm list-disc ml-5">
        {npcs.map((npc, i) => (
          <li key={i} className="mb-1">
            <span className="font-bold">{npc.name}</span> – {npc.status}
            <button className="ml-2 text-blue-400 underline" onClick={() => handleEdit(npc)}>Edit</button>
            <button className="ml-2 text-red-400 underline" onClick={() => handleDelete(npc.name)}>Delete</button>
          </li>
        ))}
      </ul>
      {showAdd ? (
        <div className="mt-2 space-y-1">
          <input name="name" placeholder="Name" value={form.name} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <input name="description" placeholder="Description" value={form.description} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <input name="status" placeholder="Status" value={form.status} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <input name="location" placeholder="Location" value={form.location} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <input name="faction" placeholder="Faction" value={form.faction} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <button onClick={handleAdd} className="bg-green-600 px-2 py-1 rounded text-white">Add</button>
          <button onClick={() => setShowAdd(false)} className="ml-2 px-2 py-1 rounded bg-gray-600 text-white">Cancel</button>
        </div>
      ) : (
        <button onClick={() => setShowAdd(true)} className="mt-2 px-2 py-1 rounded bg-blue-600 text-white">Add NPC</button>
      )}
      {editNpc && (
        <div className="mt-2 space-y-1">
          <input name="name" placeholder="Name" value={form.name} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <input name="description" placeholder="Description" value={form.description} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <input name="status" placeholder="Status" value={form.status} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <input name="location" placeholder="Location" value={form.location} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <input name="faction" placeholder="Faction" value={form.faction} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded mr-2" />
          <button onClick={handleUpdate} className="bg-green-600 px-2 py-1 rounded text-white">Save</button>
          <button onClick={() => setEditNpc(null)} className="ml-2 px-2 py-1 rounded bg-gray-600 text-white">Cancel</button>
        </div>
      )}
    </div>
  );
}

export default function WorldSummary({ adventure }) {
  const [world, setWorld] = useState({});
  const [edit, setEdit] = useState(false);
  const [form, setForm] = useState({ chaos_factor: '', current_scene: '', days_passed: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    if (!adventure) return;
    fetch(`${API_BASE}/adventures/${adventure}/world_state`)
      .then((res) => res.json())
      .then((data) => {
        setWorld(data || {});
        setForm({
          chaos_factor: data.chaos_factor || '',
          current_scene: data.current_scene || '',
          days_passed: data.days_passed || ''
        });
      })
      .catch(() => setError('Failed to load world state.'));
  }, [adventure]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSave = () => {
    setLoading(true);
    setError(null);
    fetch(`${API_BASE}/adventures/${adventure}/world_state`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...world,
        chaos_factor: form.chaos_factor,
        current_scene: form.current_scene,
        days_passed: form.days_passed
      })
    })
      .then((res) => res.json())
      .then((data) => {
        setEdit(false);
        setLoading(false);
        setWorld((prev) => ({ ...prev, ...form }));
      })
      .catch(() => {
        setError('Failed to save world state.');
        setLoading(false);
      });
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
            <input name="current_scene" value={form.current_scene} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded" />
          </div>
          <div>
            <label>Chaos: </label>
            <input name="chaos_factor" value={form.chaos_factor} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded" />
          </div>
          <div>
            <label>Days Passed: </label>
            <input name="days_passed" value={form.days_passed} onChange={handleChange} className="bg-gray-700 text-white px-2 py-1 rounded" />
          </div>
          <button onClick={handleSave} disabled={loading} className="bg-green-600 px-3 py-1 rounded text-white mt-2">{loading ? 'Saving...' : 'Save'}</button>
          <button onClick={() => setEdit(false)} className="ml-2 px-3 py-1 rounded bg-gray-600 text-white">Cancel</button>
        </div>
      ) : (
        <div>
          <div>
            <strong>Scene:</strong> {world.current_scene} | <strong>Chaos:</strong> {world.chaos_factor} | <strong>Days:</strong> {world.days_passed}
          </div>
          <button onClick={() => setEdit(true)} className="mt-2 px-3 py-1 rounded bg-blue-600 text-white">Edit</button>
        </div>
      )}

      <FactionsSection adventure={adventure} />
      <LocationsSection adventure={adventure} />
      <StoryLinesSection adventure={adventure} />
      <NPCsSection adventure={adventure} />

      <div className="mt-3">
        <h4 className="font-semibold">Story Lines</h4>
        <ul className="text-sm list-disc ml-5">
          {(world.story_lines || []).map((t, i) => (
            <li key={i}>{t.name} ({t.status})</li>
          ))}
        </ul>
      </div>

      <div className="mt-3">
        <h4 className="font-semibold">Locations</h4>
        <ul className="text-sm list-disc ml-5">
          {(world.adventure_locations || []).map((loc, i) => (
            <li key={i}>{loc.name} – {loc.status}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
