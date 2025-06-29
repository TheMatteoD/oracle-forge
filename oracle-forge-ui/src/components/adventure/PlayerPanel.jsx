import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiGet } from '../../api/apiClient';
import CharacterCreator from "./CharacterCreator";

export default function PlayerPanel() {
  const [players, setPlayers] = useState([]);
  const navigate = useNavigate();

  const loadPlayers = async () => {
    try {
      const response = await apiGet('/session/state');
      const data = await response.json();
      setPlayers(data.players || []);
    } catch (error) {
      console.error("Failed to load players:", error);
    }
  };

  useEffect(() => {
    loadPlayers();
  }, []);

  const handleCharacterCreated = (newCharacter) => {
    // Refresh the player list
    loadPlayers();
  };

  const handleCharacterClick = (characterName) => {
    navigate(`/character/${encodeURIComponent(characterName)}`);
  };

  return (
    <div className="space-y-4">
      <div className="bg-gray-800 p-4 rounded shadow">
        <h3 className="text-lg font-semibold mb-2">🧙 Player Status</h3>
        {players.length === 0 ? (
          <p className="text-gray-400 text-sm">No characters yet. Create one below!</p>
        ) : (
          players.map((player) => (
            <div key={player.name} className="border-b border-gray-600 pb-2 mb-2">
              <button
                onClick={() => handleCharacterClick(player.name)}
                className="text-left w-full hover:bg-gray-700 p-2 rounded transition-colors"
              >
                <strong className="text-blue-400 hover:text-blue-300 cursor-pointer">
                  {player.name} 🔍
                </strong> 
                <span className="text-gray-300"> (Lv {player.level}) – HP: {player.derived?.health} | AC: {player.derived?.ac}</span>
              </button>
              {/* Later: Editable stat inputs */}
            </div>
          ))
        )}
      </div>
      
      <CharacterCreator onCharacterCreated={handleCharacterCreated} />
    </div>
  );
}
