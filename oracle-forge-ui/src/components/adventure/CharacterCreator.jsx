import React, { useState } from "react";
import { apiPost } from '../../api/apiClient';

export default function CharacterCreator({ onCharacterCreated }) {
  const [characterName, setCharacterName] = useState("");
  const [isCreating, setIsCreating] = useState(false);
  const [error, setError] = useState("");

  const handleCreateCharacter = async (e) => {
    e.preventDefault();
    
    if (!characterName.trim()) {
      setError("Character name is required");
      return;
    }

    setIsCreating(true);
    setError("");

    try {
      const response = await apiPost('/session/character', { name: characterName.trim() });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to create character");
      }

      const result = await response.json();
      setCharacterName("");
      if (onCharacterCreated) {
        onCharacterCreated(result.character);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsCreating(false);
    }
  };

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