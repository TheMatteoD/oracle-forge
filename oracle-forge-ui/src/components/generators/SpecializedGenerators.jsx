import React, { useEffect, useState } from "react";
import { apiGet, apiPost } from '../../api/apiClient';


export default function SpecializedGenerators() {
  const [generators, setGenerators] = useState({});
  const [results, setResults] = useState({});
  const [flavorInputs, setFlavorInputs] = useState({});
  const [flavorResults, setFlavorResults] = useState({});
  const [flavorLoading, setFlavorLoading] = useState({});

  useEffect(() => {
    apiGet('/generators/custom')
      .then(setGenerators);
  }, []);

  const runGenerator = async (category, system, id) => {
    const res = await apiPost('/generators/custom', { category, system, id });
    const data = await res.json();
    const key = `${category}:${system}:${id}`;
    setResults((prev) => ({ ...prev, [key]: data }));
  };

  const generateFlavor = async (category, system, id) => {
    const key = `${category}:${system}:${id}`;
    const context = flavorInputs[key] || "";
    const data = results[key];

    setFlavorLoading((prev) => ({ ...prev, [key]: true }));
    try {
      const res = await apiPost('/generators/flavor', {
        context,
        data,
        category,
        source: `${system}.${id}`
      });
      const json = await res.json();
      setFlavorResults((prev) => ({ ...prev, [key]: json.narration }));
    } catch (error) {
      console.error("Failed to generate flavor:", error);
    } finally {
      setFlavorLoading((prev) => ({ ...prev, [key]: false }));
    }
  };

  return (
    <div className="mt-10">
      <h2 className="text-lg font-bold mb-4">Specialized Generators</h2>
      {Object.keys(generators).map((category) => (
        <div key={category} className="mb-6">
          <h3 className="text-md font-semibold capitalize">{category}</h3>
          {Object.entries(generators[category]).map(([system, sysData]) => (
            <div key={system} className="ml-4 mb-4">
              <h4 className="font-medium">{sysData.label}</h4>
              {sysData.generators.map((gen) => {
                const key = `${category}:${system}:${gen.id}`;
                return (
                  <div key={gen.id} className="mb-6">
                    <button
                      className="px-3 py-1 bg-green-700 text-white rounded"
                      onClick={() => runGenerator(category, system, gen.id)}
                    >
                      Generate {gen.label}
                    </button>

                    {results[key] && (
                      <div className="mt-2">
                        <pre className="bg-gray-100 p-3 rounded border border-gray-300">
                          {JSON.stringify(results[key], null, 2)}
                        </pre>

                        <textarea
                          className="mt-2 w-full border p-2"
                          rows={3}
                          placeholder="Add flavor context (optional)..."
                          value={flavorInputs[key] || ""}
                          onChange={(e) =>
                            setFlavorInputs((prev) => ({
                              ...prev,
                              [key]: e.target.value,
                            }))
                          }
                        />
                        <button
                          className="mt-2 px-3 py-1 bg-purple-700 text-white rounded"
                          onClick={() => generateFlavor(category, system, gen.id)}
                        >
                          Generate Flavor
                        </button>
                        {flavorLoading[key] && (
                          <div className="loader mt-1 text-sm italic text-gray-600">Generating narration...</div>
                        )}
                        {flavorResults[key] && (
                          <div className="mt-2 p-3 bg-white border rounded shadow">
                            <strong>Narration:</strong>
                            <p className="mt-1 whitespace-pre-wrap">{flavorResults[key]}</p>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}
