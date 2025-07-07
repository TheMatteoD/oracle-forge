import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useGetActiveAdventureQuery, useGetPlayerQuery, useUpdatePlayerMutation } from '@/api/adventureApi';
import { skipToken } from '@reduxjs/toolkit/query';

// Helper to deeply clone an object
function deepClone(obj: any) {
  return JSON.parse(JSON.stringify(obj));
}

// Recursive form field renderer
function renderField(key: string, value: any, onChange: (val: any) => void, path: string[] = []) {
  const fieldId = path.concat(key).join('.');
  if (typeof value === 'string') {
    return (
      <input
        type="text"
        className="w-full px-2 py-1 bg-gray-700 border border-gray-600 rounded text-white"
        value={value}
        onChange={e => onChange(e.target.value)}
        id={fieldId}
      />
    );
  }
  if (typeof value === 'number') {
    return (
      <input
        type="number"
        className="w-full px-2 py-1 bg-gray-700 border border-gray-600 rounded text-white"
        value={value}
        onChange={e => onChange(Number(e.target.value))}
        id={fieldId}
      />
    );
  }
  if (typeof value === 'boolean') {
    return (
      <input
        type="checkbox"
        checked={value}
        onChange={e => onChange(e.target.checked)}
        id={fieldId}
      />
    );
  }
  if (Array.isArray(value)) {
    return (
      <div className="space-y-2">
        {value.map((item, idx) => (
          <div key={idx} className="flex items-center space-x-2">
            {renderField(String(idx), item, v => {
              const newArr = [...value];
              newArr[idx] = v;
              onChange(newArr);
            }, path.concat(key))}
            <button
              type="button"
              className="ml-2 px-2 py-1 bg-red-700 text-white rounded"
              onClick={() => {
                const newArr = value.filter((_: any, i: number) => i !== idx);
                onChange(newArr);
              }}
            >Remove</button>
          </div>
        ))}
        <button
          type="button"
          className="px-2 py-1 bg-green-700 text-white rounded"
          onClick={() => onChange([...value, typeof value[0] === 'object' ? deepClone(value[0]) : ''])}
        >Add Item</button>
      </div>
    );
  }
  if (typeof value === 'object' && value !== null) {
    return (
      <div className="space-y-2 border-l-2 border-gray-700 pl-3 bg-gray-800 rounded">
        {Object.entries(value).map(([k, v]) => (
          <div key={k} className="mb-2">
            <label className="block mb-1 font-semibold capitalize">{k.replace(/_/g, ' ')}</label>
            {renderField(k, v, newVal => {
              const newObj = { ...value, [k]: newVal };
              onChange(newObj);
            }, path.concat(key))}
          </div>
        ))}
      </div>
    );
  }
  return <span>Unsupported field</span>;
}

const CharacterPage: React.FC = () => {
  const { characterName } = useParams<{ characterName: string }>();
  const { data: activeData, isLoading: loadingActive, error: errorActive } = useGetActiveAdventureQuery();
  const adventure = activeData?.active;
  const {
    data: player,
    isLoading: loadingPlayer,
    error: errorPlayer,
    refetch,
  } = useGetPlayerQuery(
    adventure && characterName ? { adventure, filename: `${characterName}.yaml` } : skipToken,
    { skip: !adventure || !characterName }
  );
  const [updatePlayer, { isLoading: updating }] = useUpdatePlayerMutation();
  const [editPlayer, setEditPlayer] = useState<any | null>(null);
  const [editError, setEditError] = useState('');
  const [editSuccess, setEditSuccess] = useState('');
  const [playerFilename, setPlayerFilename] = useState<string | null>(null);

  React.useEffect(() => {
    if (player) {
      setEditPlayer(deepClone(player));
      if (player.filename) {
        setPlayerFilename(player.filename);
      }
    }
  }, [player]);

  if (loadingActive || loadingPlayer || !editPlayer) {
    return <div style={{ background: '#111', color: '#eee', padding: '2em', fontFamily: 'sans-serif' }}>Loading character...</div>;
  }
  if (errorActive || errorPlayer) {
    return <div style={{ background: '#111', color: '#f66', padding: '2em', fontFamily: 'sans-serif' }}>Error loading character.</div>;
  }
  if (!adventure || !player) {
    return <div style={{ background: '#111', color: '#eee', padding: '2em', fontFamily: 'sans-serif' }}>Character not found.</div>;
  }

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setEditError('');
    setEditSuccess('');
    try {
      if (!playerFilename) throw new Error('No player filename available');
      await updatePlayer({
        adventure,
        filename: playerFilename,
        data: editPlayer,
      }).unwrap();
      setEditSuccess('Character updated!');
      refetch();
    } catch (err: any) {
      setEditError(err?.data?.error || err?.message || 'Failed to update character');
    }
  };

  return (
    <div style={{ background: '#111', color: '#eee', padding: '2em', fontFamily: 'sans-serif', maxWidth: 700, margin: '0 auto' }}>
      <h1 className="text-2xl font-bold mb-4">Edit Character: {editPlayer.name}</h1>
      <form onSubmit={handleSave} className="space-y-4">
        {Object.entries(editPlayer).map(([key, value]) => (
          <div key={key} className="mb-4">
            <label className="block mb-1 font-semibold capitalize">{key.replace(/_/g, ' ')}</label>
            {renderField(key, value, newVal => setEditPlayer((prev: any) => ({ ...prev, [key]: newVal })))}
          </div>
        ))}
        {editError && <div className="text-red-400 text-sm">{editError}</div>}
        {editSuccess && <div className="text-green-400 text-sm">{editSuccess}</div>}
        <button
          type="submit"
          className="px-4 py-2 bg-blue-700 text-white rounded"
          disabled={updating}
        >
          {updating ? 'Saving...' : 'Save Changes'}
        </button>
      </form>
      <div className="mt-6">
        <h2 className="text-lg font-semibold mb-2">Raw Data</h2>
        <pre className="bg-gray-900 p-3 rounded text-sm overflow-x-auto">{JSON.stringify(editPlayer, null, 2)}</pre>
      </div>
    </div>
  );
};

export default CharacterPage; 