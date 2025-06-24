import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import config from "../config";
import Navbar from '../components/core/Navbar';
import CharacterEditor from '../components/adventure/CharacterEditor';

const API_BASE = config.SERVER_URL;

export default function CharacterPage() {
  const { characterName } = useParams();
  const navigate = useNavigate();
  const [character, setCharacter] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    const loadCharacter = async () => {
      try {
        const response = await fetch(`${API_BASE}/session/character/${encodeURIComponent(characterName)}`);
        if (!response.ok) {
          throw new Error('Character not found');
        }
        const data = await response.json();
        setCharacter(data.character);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (characterName) {
      loadCharacter();
    }
  }, [characterName]);

  const handleCharacterUpdated = (updatedCharacter) => {
    setCharacter(updatedCharacter);
    setIsEditing(false);
  };

  if (loading) {
    return (
      <div style={{ background: '#111', color: '#eee', padding: '2em', fontFamily: 'sans-serif' }}>
        <Navbar />
        <div className="text-center">Loading character...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ background: '#111', color: '#eee', padding: '2em', fontFamily: 'sans-serif' }}>
        <Navbar />
        <div className="text-red-400">Error: {error}</div>
        <button 
          onClick={() => navigate('/adventure')}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Back to Adventure
        </button>
      </div>
    );
  }

  if (!character) {
    return (
      <div style={{ background: '#111', color: '#eee', padding: '2em', fontFamily: 'sans-serif' }}>
        <Navbar />
        <div>Character not found</div>
      </div>
    );
  }

  return (
    <div style={{ background: '#111', color: '#eee', padding: '2em', fontFamily: 'sans-serif' }}>
      <Navbar />
      
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold">🧙 {character.name}</h1>
          <div className="space-x-2">
            <button 
              onClick={() => setIsEditing(!isEditing)}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              {isEditing ? "Cancel Edit" : "✏️ Edit Character"}
            </button>
            <button 
              onClick={() => navigate('/adventure')}
              className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
            >
              ← Back to Adventure
            </button>
          </div>
        </div>

        {isEditing ? (
          <CharacterEditor 
            character={character}
            onCharacterUpdated={handleCharacterUpdated}
            onCancel={() => setIsEditing(false)}
          />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Basic Info */}
            <div className="bg-gray-800 p-6 rounded shadow">
              <h2 className="text-xl font-semibold mb-4">📋 Basic Information</h2>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="font-medium">Level:</span>
                  <span>{character.level}</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-medium">Race:</span>
                  <span>{character.race || 'Not set'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-medium">Class:</span>
                  <span>{character.class || 'Not set'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-medium">Experience:</span>
                  <span>{character.experience}</span>
                </div>
              </div>
            </div>

            {/* Stats */}
            <div className="bg-gray-800 p-6 rounded shadow">
              <h2 className="text-xl font-semibold mb-4">⚔️ Stats</h2>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="font-medium">Brawn:</span>
                  <span>{character.stats?.brawn || 'Not set'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-medium">Agility:</span>
                  <span>{character.stats?.agility || 'Not set'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-medium">Mind:</span>
                  <span>{character.stats?.mind || 'Not set'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-medium">Constitution:</span>
                  <span>{character.stats?.constitution || 'Not set'}</span>
                </div>
              </div>
            </div>

            {/* Derived Stats */}
            <div className="bg-gray-800 p-6 rounded shadow">
              <h2 className="text-xl font-semibold mb-4">🛡️ Derived Stats</h2>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="font-medium">Health:</span>
                  <span>{character.derived?.health || 'Not set'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-medium">Armor Class:</span>
                  <span>{character.derived?.ac || 'Not set'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-medium">Max Weight:</span>
                  <span>{character.derived?.max_weight || 'Not set'}</span>
                </div>
                {character.derived?.initiative && (
                  <div className="flex justify-between">
                    <span className="font-medium">Initiative:</span>
                    <span>{character.derived.initiative}</span>
                  </div>
                )}
              </div>
            </div>

            {/* Inventory */}
            <div className="bg-gray-800 p-6 rounded shadow">
              <h2 className="text-xl font-semibold mb-4">💰 Inventory</h2>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="font-medium">Gold:</span>
                  <span>{character.inventory?.gold || 0}</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-medium">Rations:</span>
                  <span>{character.inventory?.rations || 0}</span>
                </div>
                <div>
                  <span className="font-medium">Items:</span>
                  <ul className="mt-2 space-y-1">
                    {character.inventory?.items?.map((item, index) => (
                      <li key={index} className="text-sm">• {item}</li>
                    )) || <li className="text-gray-400 text-sm">No items</li>}
                  </ul>
                </div>
              </div>
            </div>

            {/* Skills */}
            <div className="bg-gray-800 p-6 rounded shadow md:col-span-2">
              <h2 className="text-xl font-semibold mb-4">🎯 Skills</h2>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {Object.entries(character.skills || {}).map(([skill, value]) => (
                  <div key={skill} className="flex justify-between">
                    <span className="font-medium capitalize">{skill}:</span>
                    <span>{value || 'Not set'}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Traits */}
            {character.traits && character.traits.length > 0 && (
              <div className="bg-gray-800 p-6 rounded shadow md:col-span-2">
                <h2 className="text-xl font-semibold mb-4">✨ Traits</h2>
                <ul className="space-y-2">
                  {character.traits.map((trait, index) => (
                    <li key={index} className="text-sm">• {trait}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Spells */}
            {character.spells && character.spells.length > 0 && (
              <div className="bg-gray-800 p-6 rounded shadow md:col-span-2">
                <h2 className="text-xl font-semibold mb-4">🔮 Spells</h2>
                <ul className="space-y-2">
                  {character.spells.map((spell, index) => (
                    <li key={index} className="text-sm">• {spell}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Conditions */}
            {character.conditions && character.conditions.length > 0 && (
              <div className="bg-gray-800 p-6 rounded shadow md:col-span-2">
                <h2 className="text-xl font-semibold mb-4">⚠️ Conditions</h2>
                <ul className="space-y-2">
                  {character.conditions.map((condition, index) => (
                    <li key={index} className="text-sm">• {condition}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Notes */}
            {character.notes && (
              <div className="bg-gray-800 p-6 rounded shadow md:col-span-2">
                <h2 className="text-xl font-semibold mb-4">📝 Notes</h2>
                <p className="text-sm whitespace-pre-wrap">{character.notes}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
} 