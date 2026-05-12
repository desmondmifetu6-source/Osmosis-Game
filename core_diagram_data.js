// =====================================================================
// FILE: core_diagram_data.js (The Schematic Library)
// =====================================================================
// Build by Uncle Chen: Because hard-coding is a sign of laziness.
// Add a new entry here, and the engine will handle the rest. No logic changes needed!

const DiagramLibrary = {
  animal: {
    id: 'animal',
    title: 'Zoological Schema (Animal Cell)',
    image: 'diagrams/animal_cell.jpeg',
    labels: [
      "microtubules", "nucleus", "vacuole", "cytoplasm", "golgi complex",
      "vesicles", "lysosome", "centrioles", "mitochondrion",
      "plasma membrane", "ribosomes", "endoplasmic reticulum"
    ],
    aliases: {
      "golgi": "golgi complex",
      "mitochondria": "mitochondrion",
      "membrane": "plasma membrane",
      "ribosome": "ribosomes",
      "er": "endoplasmic reticulum"
    }
  },
  plant: {
    id: 'plant',
    title: 'Botanical Schema (Plant Cell)',
    image: 'diagrams/plant_cell.jpeg',
    labels: [
      "cell wall", "cell membrane", "ribosomes", "golgi apparatus",
      "plastids", "peroxisomes", "amyloplasts", "nucleus",
      "chloroplasts", "rough endoplasmic reticulum",
      "smooth endoplasmic reticulum", "mitochondrion"
    ],
    aliases: {
      "golgi": "golgi apparatus",
      "ribosome": "ribosomes",
      "plastid": "plastids",
      "peroxisome": "peroxisomes",
      "amyloplast": "amyloplasts",
      "chloroplast": "chloroplasts",
      "rough er": "rough endoplasmic reticulum",
      "smooth er": "smooth endoplasmic reticulum",
      "mitochondria": "mitochondrion"
    }
  }
  // Add new diagrams here. For example:
  // human_eye: { ... },
  // solar_system: { ... }
};

if (typeof window !== 'undefined') {
  window.DiagramLibrary = DiagramLibrary;
}
