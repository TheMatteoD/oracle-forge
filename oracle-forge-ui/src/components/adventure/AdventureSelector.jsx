import React, { useEffect, useState } from "react";
import config from "../../config";

const API_BASE = config.SERVER_URL;

export default function AdventureSelector({ onSelect }) {
  const [adventures, setAdventures] = useState([]);
  const [newAdvName, setNewAdvName] = useState("");

  useEffect(() => {
    fetch(`${API_BASE}/adventures/list`)
      .then((res) => res.json())
      .then((response) => {
        if (response.success) {
          setAdventures(response.data || []);
        } else {
          console.error("Failed to fetch adventures:", response.error);
          setAdventures([]);
        }
      })
      .catch((error) => {
        console.error("Error fetching adventures:", error);
        setAdventures([]);
      });
  }, []);

  const selectAdventure = async (adventure) => {
    try {
      const response = await fetch(`${API_BASE}/adventures/select/${adventure}`, { method: "POST" });
      const result = await response.json();
      if (result.success) {
        onSelect(adventure);
      } else {
        console.error("Failed to select adventure:", result.error);
      }
    } catch (error) {
      console.error("Error selecting adventure:", error);
    }
  };

  const createAdventure = async () => {
    if (!newAdvName) return;
    await selectAdventure(newAdvName);
    setAdventures([...adventures, newAdvName]);
    setNewAdvName("");
  };

  return (
    <div>
      <h2>🎲 Create New Adventure</h2>
      <input
        type="text"
        value={newAdvName}
        onChange={(e) => setNewAdvName(e.target.value)}
        placeholder="Enter adventure name"
        style={{ marginRight: '1em', padding: '0.5em' }}
      />
      <button onClick={createAdventure} className="bg-purple-700 text-white px-4 py-2 rounded">
        Create Adventure
      </button>

      <h2 className="mt-6">📂 Select Adventure</h2>
      <ul style={{ listStyle: 'none', paddingLeft: 0 }}>
        {adventures.map((adv) => (
          <li key={adv} style={{ marginBottom: '0.5em' }}>
            <button
              onClick={() => selectAdventure(adv)}
              className="bg-gray-700 text-white px-4 py-2 rounded"
            >
              {adv}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
