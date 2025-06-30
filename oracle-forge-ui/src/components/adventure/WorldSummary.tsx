import WorldStateSection from './WorldStateSection';
import WorldEntityCRUD from './WorldEntityCRUD';

interface WorldSummaryProps {
  adventure: string;
}

export default function WorldSummary({ adventure }: WorldSummaryProps) {
  if (!adventure) return null;

  return (
    <div className="bg-gray-800 p-4 rounded shadow">
      <WorldStateSection adventure={adventure} />
      
      <WorldEntityCRUD
        adventure={adventure}
        entityType="factions"
        title="Factions"
        fields={[
          { name: 'name', label: 'Name', placeholder: 'Name' },
          { name: 'description', label: 'Description', placeholder: 'Description' },
          { name: 'status', label: 'Status', placeholder: 'Status' }
        ]}
      />
      
      <WorldEntityCRUD
        adventure={adventure}
        entityType="locations"
        title="Locations"
        fields={[
          { name: 'name', label: 'Name', placeholder: 'Name' },
          { name: 'description', label: 'Description', placeholder: 'Description' },
          { name: 'status', label: 'Status', placeholder: 'Status' }
        ]}
      />
      
      <WorldEntityCRUD
        adventure={adventure}
        entityType="story_lines"
        title="Story Lines"
        fields={[
          { name: 'name', label: 'Name', placeholder: 'Name' },
          { name: 'description', label: 'Description', placeholder: 'Description' },
          { name: 'status', label: 'Status', placeholder: 'Status' }
        ]}
      />
      
      <WorldEntityCRUD
        adventure={adventure}
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