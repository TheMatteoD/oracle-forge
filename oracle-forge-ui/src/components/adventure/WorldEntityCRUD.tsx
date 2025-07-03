import { useState } from "react";
import { 
  useGetActiveAdventureQuery,
  useListWorldEntitiesQuery, 
  useCreateWorldEntityMutation, 
  useUpdateWorldEntityMutation, 
  useDeleteWorldEntityMutation,
  type WorldEntity 
} from "@/api/adventureApi";

interface WorldEntityCRUDProps {
  entityType: 'factions' | 'locations' | 'story_lines' | 'npcs';
  title: string;
  fields: {
    name: string;
    label: string;
    placeholder: string;
  }[];
}

export default function WorldEntityCRUD({ 
  entityType, 
  title, 
  fields 
}: WorldEntityCRUDProps) {
  const [showAdd, setShowAdd] = useState(false);
  const [editEntity, setEditEntity] = useState<string | null>(null);
  const [form, setForm] = useState<WorldEntity>({ name: '', description: '', status: '' });

  // Get the active adventure
  const { data: activeData, isLoading: loadingActive, error: errorActive } = useGetActiveAdventureQuery();
  const adventure = activeData?.active;

  // RTK Query hooks
  const { data: entities = [], isLoading, error, refetch } = useListWorldEntitiesQuery(
    { adventure: adventure!, entityType }, 
    { skip: !adventure }
  );

  const [createEntity, { isLoading: isCreating }] = useCreateWorldEntityMutation();
  const [updateEntity, { isLoading: isUpdating }] = useUpdateWorldEntityMutation();
  const [deleteEntity, { isLoading: isDeleting }] = useDeleteWorldEntityMutation();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleAdd = async () => {
    if (!form.name.trim() || !adventure) return;
    
    try {
      await createEntity({ adventure, entityType, entityData: form }).unwrap();
      setShowAdd(false);
      setForm({ name: '', description: '', status: '' });
      refetch();
    } catch (error) {
      console.error(`Failed to add ${entityType}:`, error);
    }
  };

  const handleEdit = (entity: WorldEntity) => {
    setEditEntity(entity.name);
    setForm(entity);
  };

  const handleUpdate = async () => {
    if (!editEntity || !form.name.trim() || !adventure) return;
    
    try {
      await updateEntity({ adventure, entityType, entityName: editEntity, entityData: form }).unwrap();
      setEditEntity(null);
      setForm({ name: '', description: '', status: '' });
      refetch();
    } catch (error) {
      console.error(`Failed to update ${entityType}:`, error);
    }
  };

  const handleDelete = async (name: string) => {
    if (!window.confirm(`Delete ${entityType.slice(0, -1)} '${name}'?`) || !adventure) return;
    
    try {
      await deleteEntity({ adventure, entityType, entityName: name }).unwrap();
      refetch();
    } catch (error) {
      console.error(`Failed to delete ${entityType}:`, error);
    }
  };

  const resetForm = () => {
    setForm({ name: '', description: '', status: '' });
    setShowAdd(false);
    setEditEntity(null);
  };

  const isLoadingAny = loadingActive || isLoading || isCreating || isUpdating || isDeleting;

  if (loadingActive) return <div className="text-gray-400">Loading...</div>;
  if (errorActive) return <div className="text-red-400">Error loading adventure.</div>;
  if (!adventure) return <div className="text-gray-400">No active adventure.</div>;

  return (
    <div className="mt-4">
      <h4 className="font-semibold">{title}</h4>
      
      {error && <div className="text-red-400 mb-2">Error loading {entityType}.</div>}
      
      {isLoadingAny && <div>Loading...</div>}
      
      <ul className="text-sm list-disc ml-5">
        {entities.map((entity, i) => (
          <li key={i} className="mb-1">
            <span className="font-bold">{entity.name}</span> 
            {entity.status && ` – ${entity.status}`}
            <button 
              className="ml-2 text-blue-400 underline" 
              onClick={() => handleEdit(entity)}
              disabled={isLoadingAny}
            >
              Edit
            </button>
            <button 
              className="ml-2 text-red-400 underline" 
              onClick={() => handleDelete(entity.name)}
              disabled={isLoadingAny}
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
            disabled={isCreating || !form.name.trim()}
            className="bg-green-600 px-3 py-1 rounded text-white"
          >
            {isCreating ? 'Adding...' : 'Add'}
          </button>
          <button 
            onClick={resetForm} 
            className="ml-2 px-3 py-1 rounded bg-gray-600 text-white"
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
            disabled={isUpdating || !form.name.trim()}
            className="bg-blue-600 px-3 py-1 rounded text-white"
          >
            {isUpdating ? 'Updating...' : 'Update'}
          </button>
          <button 
            onClick={resetForm} 
            className="ml-2 px-3 py-1 rounded bg-gray-600 text-white"
          >
            Cancel
          </button>
        </div>
      )}
      
      {!showAdd && !editEntity && (
        <button 
          onClick={() => setShowAdd(true)} 
          className="mt-2 px-3 py-1 rounded bg-blue-600 text-white"
          disabled={isLoadingAny}
        >
          Add {title.slice(0, -1)}
        </button>
      )}
    </div>
  );
} 