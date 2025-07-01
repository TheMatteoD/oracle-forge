import React, { useState } from "react";
import type { Player } from '@/types/api';
import { useGetActiveAdventureQuery, useCreatePlayerMutation } from "@/api/adventureApi";

interface CharacterCreatorProps {
  onCharacterCreated: (character: Player) => void;
}

export default function CharacterCreator({ onCharacterCreated }: CharacterCreatorProps) {
  const [characterName, setCharacterName] = useState("");
  const [error, setError] = useState("");
  const { data: activeData, isLoading: loadingActive, error: errorActive } = useGetActiveAdventureQuery();
  const adventure = activeData?.active;
  const [createPlayer, { isLoading: isCreating }] = useCreatePlayerMutation();

  const handleCreateCharacter = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!characterName.trim()) {
      setError("Character name is required");
      return;
    }
    if (!adventure) {
      setError("No active adventure.");
      return;
    }
    setError("");
    try {
      const playerData = { name: characterName.trim() };
      const result = await createPlayer({ adventure, player: playerData }).unwrap();
      setCharacterName("");
      if (onCharacterCreated) {
        onCharacterCreated(result);
      }
    } catch (err: any) {
      setError(err?.data?.error || err?.message || "Failed to create character");
    }
  };

  if (loadingActive) return <div className="text-gray-400 text-sm">Loading...</div>;
  if (errorActive) return <div className="text-red-400 text-sm">Error loading adventure.</div>;
  if (!adventure) return <div className="text-gray-400 text-sm">No active adventure.</div>;

  return (
    <div className="bg-gray-800 p-4 rounded shadow">
      <h3 className="text-lg font-semibold mb-3">➕ Create New Character</h3>
      <form onSubmit={handleCreateCharacter} className="space-y-3">
        <div>
          <label htmlFor="characterName" className="block text-sm font-medium mb-1">
            Character Name
          </label>
          <input
            type="text"
            id="characterName"
            value={characterName}
            onChange={(e) => setCharacterName(e.target.value)}
            className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
            placeholder="Enter character name..."
            disabled={isCreating}
          />
        </div>
        {error && (
          <div className="text-red-400 text-sm">{error}</div>
        )}
        <button
          type="submit"
          disabled={isCreating || !characterName.trim()}
          className="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed"
        >
          {isCreating ? "Creating..." : "Create Character"}
        </button>
      </form>
    </div>
  );
} 