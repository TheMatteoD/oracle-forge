import React, { useState, useEffect } from "react";
import type { Player } from '@/types/api';

interface CharacterEditorProps {
  character: Player;
  onCharacterUpdated: (character: Player) => void;
  onCancel: () => void;
}

export default function CharacterEditor({ character, onCharacterUpdated, onCancel }: CharacterEditorProps) {
  const [formData, setFormData] = useState<Player>({} as Player);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (character) {
      setFormData(character);
    }
  }, [character]);

  const handleInputChange = (path: string, value: string | number) => {
    const keys = path.split('.');
    setFormData(prev => {
      const newData = { ...prev };
      let current: any = newData;
      
      for (let i = 0; i < keys.length - 1; i++) {
        if (!current[keys[i]]) {
          current[keys[i]] = {};
        }
        current = current[keys[i]];
      }
      
      current[keys[keys.length - 1]] = value;
      return newData;
    });
  };

  const handleArrayChange = (path: string, index: number, value: string) => {
    const keys = path.split('.');
    setFormData(prev => {
      const newData = { ...prev };
      let current: any = newData;
      
      for (let i = 0; i < keys.length - 1; i++) {
        if (!current[keys[i]]) {
          current[keys[i]] = {};
        }
        current = current[keys[i]];
      }
      
      if (!Array.isArray(current[keys[keys.length - 1]])) {
        current[keys[keys.length - 1]] = [];
      }
      
      current[keys[keys.length - 1]][index] = value;
      return newData;
    });
  };

  const addArrayItem = (path: string) => {
    const keys = path.split('.');
    setFormData(prev => {
      const newData = { ...prev };
      let current: any = newData;
      
      for (let i = 0; i < keys.length - 1; i++) {
        if (!current[keys[i]]) {
          current[keys[i]] = {};
        }
        current = current[keys[i]];
      }
      
      if (!Array.isArray(current[keys[keys.length - 1]])) {
        current[keys[keys.length - 1]] = [];
      }
      
      current[keys[keys.length - 1]].push("");
      return newData;
    });
  };

  const removeArrayItem = (path: string, index: number) => {
    const keys = path.split('.');
    setFormData(prev => {
      const newData = { ...prev };
      let current: any = newData;
      
      for (let i = 0; i < keys.length - 1; i++) {
        current = current[keys[i]];
      }
      
      current[keys[keys.length - 1]].splice(index, 1);
      return newData;
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError("");

    try {
      // Note: This endpoint might need to be added to AdventureAPI
      // For now, using direct fetch until we add it
      const response = await fetch(`/session/character/${encodeURIComponent(character.name)}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ character: formData }),
      });

      if (!response.ok) {
        throw new Error('Failed to update character');
      }

      const result = await response.json();
      if (result.success) {
        onCharacterUpdated(result.data?.character);
      } else {
        console.error("Failed to update character:", result.error);
        throw new Error(result.error || 'Failed to update character');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update character');
    } finally {
      setSaving(false);
    }
  };

  const renderInput = (label: string, path: string, type: string = "text", placeholder: string = "") => (
    <div className="flex justify-between items-center">
      <label className="font-medium">{label}:</label>
      <input
        type={type}
        value={(formData as any)[path] || ""}
        onChange={(e) => handleInputChange(path, e.target.value)}
        placeholder={placeholder}
        className="bg-gray-700 text-white px-2 py-1 rounded text-sm w-24 text-right"
      />
    </div>
  );

  const renderNestedInput = (label: string, path: string, type: string = "text", placeholder: string = "") => {
    const keys = path.split('.');
    let value: any = formData;
    for (const key of keys) {
      value = value?.[key] || "";
    }
    
    return (
      <div className="flex justify-between items-center">
        <label className="font-medium">{label}:</label>
        <input
          type={type}
          value={value}
          onChange={(e) => handleInputChange(path, e.target.value)}
          placeholder={placeholder}
          className="bg-gray-700 text-white px-2 py-1 rounded text-sm w-24 text-right"
        />
      </div>
    );
  };

  const renderArrayInput = (label: string, path: string) => {
    const keys = path.split('.');
    let array: any = formData;
    for (const key of keys) {
      array = array?.[key] || [];
    }
    
    return (
      <div>
        <div className="flex justify-between items-center mb-2">
          <label className="font-medium">{label}:</label>
          <button
            type="button"
            onClick={() => addArrayItem(path)}
            className="bg-blue-600 text-white px-2 py-1 rounded text-xs hover:bg-blue-700"
          >
            + Add
          </button>
        </div>
        <div className="space-y-1">
          {array.map((item: string, index: number) => (
            <div key={index} className="flex items-center gap-2">
              <input
                type="text"
                value={item}
                onChange={(e) => handleArrayChange(path, index, e.target.value)}
                className="bg-gray-700 text-white px-2 py-1 rounded text-sm flex-1"
                placeholder={`${label} ${index + 1}`}
              />
              <button
                type="button"
                onClick={() => removeArrayItem(path, index)}
                className="bg-red-600 text-white px-2 py-1 rounded text-xs hover:bg-red-700"
              >
                ×
              </button>
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="bg-gray-900 p-6 rounded shadow-lg max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold">✏️ Edit Character</h2>
        <div className="space-x-2">
          <button
            onClick={onCancel}
            className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            disabled={saving}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
          >
            {saving ? "Saving..." : "Save Changes"}
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-900 text-red-200 p-3 rounded mb-4">
          Error: {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Basic Info */}
          <div className="bg-gray-800 p-4 rounded">
            <h3 className="text-lg font-semibold mb-3">📋 Basic Information</h3>
            <div className="space-y-3">
              {renderInput("Name", "name")}
              {renderInput("Level", "level", "number")}
              {renderInput("Race", "race")}
              {renderInput("Class", "class")}
              {renderInput("Experience", "experience", "number")}
            </div>
          </div>

          {/* Stats */}
          <div className="bg-gray-800 p-4 rounded">
            <h3 className="text-lg font-semibold mb-3">⚔️ Stats</h3>
            <div className="space-y-3">
              {renderNestedInput("Brawn", "stats.brawn", "number")}
              {renderNestedInput("Agility", "stats.agility", "number")}
              {renderNestedInput("Mind", "stats.mind", "number")}
              {renderNestedInput("Constitution", "stats.constitution", "number")}
            </div>
          </div>

          {/* Derived Stats */}
          <div className="bg-gray-800 p-4 rounded">
            <h3 className="text-lg font-semibold mb-3">🛡️ Derived Stats</h3>
            <div className="space-y-3">
              {renderNestedInput("Health", "derived.health", "number")}
              {renderNestedInput("Armor Class", "derived.ac", "number")}
              {renderNestedInput("Max Weight", "derived.max_weight", "number")}
            </div>
          </div>

          {/* Inventory */}
          <div className="bg-gray-800 p-4 rounded">
            <h3 className="text-lg font-semibold mb-3">💰 Inventory</h3>
            <div className="space-y-3">
              {renderNestedInput("Gold", "inventory.gold", "number")}
              {renderNestedInput("Rations", "inventory.rations", "number")}
              {renderArrayInput("Items", "inventory.items")}
            </div>
          </div>

          {/* Skills */}
          <div className="bg-gray-800 p-4 rounded md:col-span-2">
            <h3 className="text-lg font-semibold mb-3">🎯 Skills</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {renderNestedInput("Foraging", "skills.foraging", "number")}
              {renderNestedInput("Crafting", "skills.crafting", "number")}
              {renderNestedInput("Alchemy", "skills.alchemy", "number")}
              {renderNestedInput("Enchanting", "skills.enchanting", "number")}
              {renderNestedInput("Fishing", "skills.fishing", "number")}
              {renderNestedInput("Cooking", "skills.cooking", "number")}
            </div>
          </div>

          {/* Traits */}
          <div className="bg-gray-800 p-4 rounded md:col-span-2">
            <h3 className="text-lg font-semibold mb-3">✨ Traits</h3>
            {renderArrayInput("Traits", "traits")}
          </div>

          {/* Spells */}
          <div className="bg-gray-800 p-4 rounded md:col-span-2">
            <h3 className="text-lg font-semibold mb-3">🔮 Spells</h3>
            {renderArrayInput("Spells", "spells")}
          </div>

          {/* Conditions */}
          <div className="bg-gray-800 p-4 rounded md:col-span-2">
            <h3 className="text-lg font-semibold mb-3">⚠️ Conditions</h3>
            {renderArrayInput("Conditions", "conditions")}
          </div>

          {/* Notes */}
          <div className="bg-gray-800 p-4 rounded md:col-span-2">
            <h3 className="text-lg font-semibold mb-3">📝 Notes</h3>
            <textarea
              value={(formData as any).notes || ""}
              onChange={(e) => handleInputChange("notes", e.target.value)}
              className="w-full bg-gray-700 text-white p-3 rounded h-32 resize-none"
              placeholder="Character notes..."
            />
          </div>
        </div>
      </form>
    </div>
  );
} 