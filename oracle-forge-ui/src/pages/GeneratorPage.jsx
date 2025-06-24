import React from "react";
import Navbar from "../components/core/Navbar";
import GenericGenerators from "../components/generators/GenericGenerators";
import SpecializedGenerators from "../components/generators/SpecializedGenerators";

export default function GeneratorPage() {
  return (
    <div style={{ background: '#111', color: '#eee', padding: '2em', fontFamily: 'sans-serif' }}>
      <Navbar />
      <h1 className="text-xl font-bold mb-4">Generator Testing</h1>
      <GenericGenerators />
      <SpecializedGenerators />
    </div>
  );
}
