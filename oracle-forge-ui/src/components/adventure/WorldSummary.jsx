import React, { useEffect, useState } from "react";
import config from "../../config";

const API_BASE = config.SERVER_URL;

export default function WorldSummary() {
  const [world, setWorld] = useState({});

  useEffect(() => {
    fetch(`${API_BASE}/session/state`)
      .then((res) => res.json())
      .then((data) => {
        setWorld(data.world || {});
      });
  }, []);

  return (
    <div className="bg-gray-800 p-4 rounded shadow">
      <h3 className="text-lg font-semibold mb-2">🌍 World Summary</h3>
      <div>
        <strong>Scene:</strong> {world.current_scene} | <strong>Chaos:</strong> {world.chaos_factor}
      </div>

      <div className="mt-3">
        <h4 className="font-semibold">Factions</h4>
        <ul className="text-sm list-disc ml-5">
          {(world.factions || []).map((f, i) => (
            <li key={i}>{f.name} – {f.status}</li>
          ))}
        </ul>
      </div>

      <div className="mt-3">
        <h4 className="font-semibold">Threads</h4>
        <ul className="text-sm list-disc ml-5">
          {(world.threads || []).map((t, i) => (
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
