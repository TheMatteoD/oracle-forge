import { useNavigate } from "react-router-dom";
import { useGetActiveAdventureQuery, useListPlayersQuery } from "@/api/adventureApi";
import type { Player } from '@/types/api';
import CharacterCreator from "./CharacterCreator";

export default function PlayerPanel() {
  const navigate = useNavigate();
  // Get the active adventure
  const { data: activeData, isLoading: loadingActive, error: errorActive } = useGetActiveAdventureQuery();
  const adventure = activeData?.active;
  // Fetch players for the active adventure
  const { data: players = [], isLoading, error, refetch } = useListPlayersQuery(adventure!, { skip: !adventure });

  const handleCharacterCreated = (_newCharacter: Player) => {
    // Refresh the player list
    refetch();
  };

  const handleCharacterClick = (characterName: string) => {
    navigate(`/character/${encodeURIComponent(characterName)}`);
  };

  if (loadingActive || isLoading) {
    return <div className="text-gray-400 text-sm">Loading players...</div>;
  }
  if (errorActive || error) {
    return <div className="text-red-400 text-sm">Error loading players.</div>;
  }
  if (!adventure) {
    return <div className="text-gray-400 text-sm">No active adventure.</div>;
  }

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