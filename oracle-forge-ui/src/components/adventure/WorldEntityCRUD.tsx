import { useState, useEffect } from "react";
import { AdventureAPI } from '@/api/apiClient';

interface WorldEntity {
  name: string;
  description?: string;
  status?: string;
  location?: string;
  faction?: string;
}

interface WorldEntityCRUDProps {
  adventure: string;
  entityType: 'factions' | 'locations' | 'story_lines' | 'npcs';
  title: string;
  fields: {
    name: string;
    label: string;
    placeholder: string;
  }[];
}

export default function WorldEntityCRUD({ 
  adventure, 
  entityType, 
  title, 
  fields 
}: WorldEntityCRUDProps) {
  const [entities, setEntities] = useState<WorldEntity[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showAdd, setShowAdd] = useState(false);
  const [editEntity, setEditEntity] = useState<string | null>(null);
  const [form, setForm] = useState<WorldEntity>({ name: '', description: '', status: '' });

  const fetchEntities = async () => {
    setLoading(true);
    try {
      const response = await AdventureAPI.listWorldEntities(adventure, entityType);
      
      if (response.success && response.data) {
        setEntities(response.data);
      } else {
        console.error(`Failed to fetch ${entityType}:`, response.error);
        setEntities([]);
      }
    } catch (error) {
      console.error(`Error fetching ${entityType}:`, error);
      setError(`Failed to load ${entityType}.`);
      setEntities([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { 
    if (adventure) fetchEntities(); 
  }, [adventure, entityType]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleAdd = async () => {
    if (!form.name.trim()) return;
    
    setLoading(true);
    try {
      const response = await AdventureAPI.createWorldEntity(adventure, entityType, {
        data: form
      });
      
      if (response.success) {
        setShowAdd(false);
        setForm({ name: '', description: '', status: '' });
        fetchEntities();
      } else {
        console.error(`Failed to add ${entityType}:`, response.error);
        setError(`Failed to add ${entityType}.`);
      }
    } catch (error) {
      console.error(`Error adding ${entityType}:`, error);
      setError(`Failed to add ${entityType}.`);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (entity: WorldEntity) => {
    setEditEntity(entity.name);
    setForm(entity);
  };

  const handleUpdate = async () => {
    if (!editEntity || !form.name.trim()) return;
    
    setLoading(true);
    try {
      const response = await AdventureAPI.updateWorldEntity(adventure, entityType, editEntity, {
        data: form
      });
      
      if (response.success) {
        setEditEntity(null);
        setForm({ name: '', description: '', status: '' });
        fetchEntities();
      } else {
        console.error(`Failed to update ${entityType}:`, response.error);
        setError(`Failed to update ${entityType}.`);
      }
    } catch (error) {
      console.error(`Error updating ${entityType}:`, error);
      setError(`Failed to update ${entityType}.`);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (name: string) => {
    if (!window.confirm(`Delete ${entityType.slice(0, -1)} '${name}'?`)) return;
    
    setLoading(true);
    try {
      const response = await AdventureAPI.deleteWorldEntity(adventure, entityType, name);
      
      if (response.success) {
        fetchEntities();
      } else {
        console.error(`Failed to delete ${entityType}:`, response.error);
        setError(`Failed to delete ${entityType}.`);
      }
    } catch (error) {
      console.error(`Error deleting ${entityType}:`, error);
      setError(`Failed to delete ${entityType}.`);
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setForm({ name: '', description: '', status: '' });
    setShowAdd(false);
    setEditEntity(null);
  };

  return (
    <div className="mt-4">
      <h4 className="font-semibold">{title}</h4>
      
      {error && <div className="text-red-400 mb-2">{error}</div>}
      
      {loading && <div>Loading...</div>}
      
      <ul className="text-sm list-disc ml-5">
        {entities.map((entity, i) => (
          <li key={i} className="mb-1">
            <span className="font-bold">{entity.name}</span> 
            {entity.status && ` – ${entity.status}`}
            <button 
              className="ml-2 text-blue-400 underline" 
              onClick={() => handleEdit(entity)}
            >
              Edit
            </button>
            <button 
              className="ml-2 text-red-400 underline" 
              onClick={() => handleDelete(entity.name)}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
      
      {showAdd && (
        <div className="mt-2 space-y-1">
          {fields.map((field) => (
            <input
              key={field.name}
              name={field.name}
              placeholder={field.placeholder}
              value={(form as any)[field.name] || ''}
              onChange={handleChange}
              className="bg-gray-700 text-white px-2 py-1 rounded mr-2"
            />
          ))}
          <button 
            onClick={handleAdd} 
            disabled={loading || !form.name.trim()}
            className="bg-green-600 px-2 py-1 rounded text-white"
          >
            Add
          </button>
          <button 
            onClick={resetForm} 
            className="ml-2 px-2 py-1 rounded bg-gray-600 text-white"
          >
            Cancel
          </button>
        </div>
      )}
      
      {editEntity && (
        <div className="mt-2 space-y-1">
          {fields.map((field) => (
            <input
              key={field.name}
              name={field.name}
              placeholder={field.placeholder}
              value={(form as any)[field.name] || ''}
              onChange={handleChange}
              className="bg-gray-700 text-white px-2 py-1 rounded mr-2"
            />
          ))}
          <button 
            onClick={handleUpdate} 
            disabled={loading || !form.name.trim()}
            className="bg-green-600 px-2 py-1 rounded text-white"
          >
            Save
          </button>
          <button 
            onClick={resetForm} 
            className="ml-2 px-2 py-1 rounded bg-gray-600 text-white"
          >
            Cancel
          </button>
        </div>
      )}
      
      {!showAdd && !editEntity && (
        <button 
          onClick={() => setShowAdd(true)} 
          className="mt-2 px-2 py-1 rounded bg-blue-600 text-white"
        >
          Add {title.slice(0, -1)}
        </button>
      )}
    </div>
  );
} 