import React, { useState } from "react";
import config from "../config";
import Navbar from "../components/core/Navbar";

const API_BASE = config.SERVER_URL;

export default function CombatPage() {
  const [combatState, setCombatState] = useState(null);
  const [combatLog, setCombatLog] = useState([]);
  const [attackerName, setAttackerName] = useState("");
  const [defenderName, setDefenderName] = useState("");

  const startCombat = async () => {
    const res = await fetch(`${API_BASE}/combat/start`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ monsters: ["Acolyte"] })
    });
    const data = await res.json();
    setCombatState(data);
    setCombatLog(["Combat started!"].concat(data.initiative_order.map(n => `Initiative: ${n}`)));
  };

  const performAttack = async () => {
    const attacker = combatState.combat_state[attackerName];
    const defender = combatState.combat_state[defenderName];

    const res = await fetch(`${API_BASE}/combat/attack`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ attacker, defender })
    });
    const data = await res.json();
    setCombatLog(log => [...log, `${data.attacker} attacks ${data.defender}: ${data.hit ? `Hits for ${data.damage}` : "Missed"}`]);
  };

  return (
    <div style={{ background: '#111', color: '#eee', padding: '2em', fontFamily: 'sans-serif' }}>
    <Navbar />
      <h1 className="text-xl font-bold mb-4">Combat Test</h1>
      <button onClick={startCombat} className="px-4 py-2 bg-blue-600 rounded mr-4">Start Combat</button>
      <div className="mt-6">
        <label>Attacker:</label>
        <input
          className="ml-2 text-black px-2"
          value={attackerName}
          onChange={(e) => setAttackerName(e.target.value)}
        />
        <label className="ml-4">Defender:</label>
        <input
          className="ml-2 text-black px-2"
          value={defenderName}
          onChange={(e) => setDefenderName(e.target.value)}
        />
        <button onClick={performAttack} className="ml-4 px-3 py-1 bg-red-600 rounded">Attack</button>
      </div>
      <div className="mt-6 bg-gray-800 p-4 rounded">
        <h2 className="text-lg font-semibold">Combat Log</h2>
        <pre>{combatLog.join("\n")}</pre>
      </div>
    </div>
  );
}
