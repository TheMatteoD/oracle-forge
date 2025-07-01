import AdventureSelector from "@/components/adventure/AdventureSelector";
import type { Adventure } from "@/api/adventureApi";

interface AdventureSelectorPageProps {
  onAdventureSelected: (adventure: Adventure) => void;
}

export default function AdventureSelectorPage({ onAdventureSelected }: AdventureSelectorPageProps) {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white">
      <h1 className="text-3xl font-bold mb-8">Welcome to Oracle Forge</h1>
      <div className="w-full max-w-md bg-gray-800 p-6 rounded shadow-lg">
        <AdventureSelector onSelect={onAdventureSelected} />
      </div>
    </div>
  );
} 