import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import type { Player } from '@/types/api';
import CharacterCreator from "./CharacterCreator";

interface PlayerPanelProps {
  adventure: string;
}

export default function PlayerPanel({ adventure }: PlayerPanelProps) {
  const [players, setPlayers] = useState<Player[]>([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const loadPlayers = async () => {
    setLoading(true);
    try {
      if (!adventure) {
        setPlayers([]);
        return;
      }
      // Use the correct endpoint for the adventure
      const response = await fetch(`/adventures/${adventure}/players`);
      const data = await response.json();
      setPlayers(data.data || []);
    } catch (error) {
      console.error("Failed to load players:", error);
      setPlayers([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPlayers();
  }, []);

  const handleCharacterCreated = (_newCharacter: Player) => {
    // Refresh the player list
    loadPlayers();
  };

  const handleCharacterClick = (characterName: string) => {
    navigate(`/character/${encodeURIComponent(characterName)}`);
  };

  return (
    <div className="space-y-4">
      <div className="bg-gray-800 p-4 rounded shadow">
        <h3 className="text-lg font-semibold mb-2">🧙 Player Status</h3>
        {loading ? (
          <p className="text-gray-400 text-sm">Loading players...</p>
        ) : players.length === 0 ? (
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
                <span className="text-gray-300">
                  {player.level && ` (Lv ${player.level})`}
                  {player.stats && (
                    <>
                      {player.stats.health && ` – HP: ${player.stats.health}`}
                      {player.stats.ac && ` | AC: ${player.stats.ac}`}
                    </>
                  )}
                </span>
              </button>
            </div>
          ))
        )}
      </div>
      
      <CharacterCreator onCharacterCreated={handleCharacterCreated} />
    </div>
  );
} 