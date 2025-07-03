import WorldStateSection from './WorldStateSection';
import WorldEntityCRUD from './WorldEntityCRUD';

export default function WorldSummary() {
  return (
    <div className="bg-gray-800 p-4 rounded shadow">
      <WorldStateSection />
      
      <WorldEntityCRUD
        entityType="factions"
        title="Factions"
        fields={[
          { name: 'name', label: 'Name', placeholder: 'Name' },
          { name: 'description', label: 'Description', placeholder: 'Description' },
          { name: 'status', label: 'Status', placeholder: 'Status' }
        ]}
      />
      
      <WorldEntityCRUD
        entityType="locations"
        title="Locations"
        fields={[
          { name: 'name', label: 'Name', placeholder: 'Name' },
          { name: 'description', label: 'Description', placeholder: 'Description' },
          { name: 'status', label: 'Status', placeholder: 'Status' }
        ]}
      />
      
      <WorldEntityCRUD
        entityType="story_lines"
        title="Story Lines"
        fields={[
          { name: 'name', label: 'Name', placeholder: 'Name' },
          { name: 'description', label: 'Description', placeholder: 'Description' },
          { name: 'status', label: 'Status', placeholder: 'Status' }
        ]}
      />
      
      <WorldEntityCRUD
        entityType="npcs"
        title="NPCs"
        fields={[
          { name: 'name', label: 'Name', placeholder: 'Name' },
          { name: 'description', label: 'Description', placeholder: 'Description' },
          { name: 'status', label: 'Status', placeholder: 'Status' },
          { name: 'location', label: 'Location', placeholder: 'Location' },
          { name: 'faction', label: 'Faction', placeholder: 'Faction' }
        ]}
      />
    </div>
  );
} 