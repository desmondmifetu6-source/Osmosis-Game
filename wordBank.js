/**
 * wordBank.js
 * A static, hardcoded dictionary structure mapping every letter (A-Z)
 * to an array of scientifically relevant words and their definitions.
 * This acts as the primary source of truth for the game rounds.
 */
const wordBank = {
  A: [
    { word: "atom", definition: "Smallest unit of matter" },
    { word: "angle", definition: "Space between two intersecting lines" },
    { word: "axis", definition: "A line used as a reference for measurement" },
    { word: "astronomy", definition: "The scientific study of stars, planets, and the universe" },
    { word: "algorithm", definition: "A set of rules to be followed in calculations" }
  ],
  B: [
    { word: "binary", definition: "A system using only 0 and 1" },
    { word: "balance", definition: "A state where forces are equal" },
    { word: "battery", definition: "A device that stores and supplies energy" },
    { word: "biology", definition: "The scientific study of life and living organisms" },
    { word: "buoyancy", definition: "The upward force exerted by a fluid that opposes weight" }
  ],
  C: [
    { word: "cell", definition: "Basic unit of life" },
    { word: "circuit", definition: "A path through which electricity flows" },
    { word: "code", definition: "Instructions written for a computer" },
    { word: "chemistry", definition: "The study of matter and its interactions" },
    { word: "catalyst", definition: "A substance that speeds up a chemical reaction" }
  ],
  D: [
    { word: "data", definition: "Information used for analysis" },
    { word: "density", definition: "Mass per unit volume" },
    { word: "digit", definition: "A single number from 0 to 9" },
    { word: "dna", definition: "Molecule that carries genetic instructions" },
    { word: "dynamics", definition: "The branch of mechanics concerned with motion" }
  ],
  E: [
    { word: "energy", definition: "Ability to do work" },
    { word: "element", definition: "A pure substance made of one type of atom" },
    { word: "engine", definition: "A machine that converts energy into motion" },
    { word: "electron", definition: "A subatomic particle with a negative charge" },
    { word: "ecology", definition: "The study of interactions among organisms and their environment" }
  ],
  F: [
    { word: "force", definition: "A push or pull on an object" },
    { word: "field", definition: "An area influenced by a force" },
    { word: "frame", definition: "A structure that supports something" },
    { word: "friction", definition: "The resistance encountered when moving over a surface" },
    { word: "fossil", definition: "Remains or impressions of prehistoric plants or animals" }
  ],
  G: [
    { word: "gravity", definition: "The force that attracts bodies toward the center of the earth" },
    { word: "genetics", definition: "The study of heredity and inherited characteristics" },
    { word: "galaxy", definition: "A system of millions or billions of stars" },
    { word: "geometry", definition: "The branch of mathematics concerned with shape, size, and space" },
    { word: "geology", definition: "The science deals with the earth's physical structure and substance" }
  ],
  H: [
    { word: "hypothesis", definition: "A proposed explanation made on the basis of limited evidence" },
    { word: "habitat", definition: "The natural home or environment of an organism" },
    { word: "hardware", definition: "The physical components of a computer system" },
    { word: "hormone", definition: "Chemical messengers traveling in the blood" },
    { word: "helium", definition: "A light, colorless gas often used in balloons" }
  ],
  I: [
    { word: "inertia", definition: "A property of matter to resist an accelerating force" },
    { word: "ion", definition: "An atom or molecule with a net electric charge" },
    { word: "isotope", definition: "Forms of the same element with different neutron numbers" },
    { word: "immunology", definition: "The study of the immune system" },
    { word: "integer", definition: "A whole number, not a fraction" }
  ],
  J: [
    { word: "joule", definition: "The SI unit of work or energy" },
    { word: "jupiter", definition: "The largest planet in the solar system" },
    { word: "joint", definition: "A point at which parts of an artificial structure are joined" },
    { word: "jet", definition: "A rapid stream of liquid or gas forced out of a small opening" },
    { word: "java", definition: "A high-level, class-based, object-oriented programming language" }
  ],
  K: [
    { word: "kinetics", definition: "The study of rates of chemical processes" },
    { word: "kelvin", definition: "The SI base unit of thermodynamic temperature" },
    { word: "kingdom", definition: "A taxonomic category of the highest rank" },
    { word: "keratin", definition: "A fibrous protein forming the main structural constituent of hair/feathers" },
    { word: "kinematics", definition: "The branch of mechanics studying motion without forces" }
  ],
  L: [
    { word: "lithosphere", definition: "The rigid outer part of the earth" },
    { word: "laser", definition: "A device producing a narrow beam of concentrated light" },
    { word: "logic", definition: "Reasoning conducted according to strict principles of validity" },
    { word: "lipid", definition: "Fatty acids or their derivatives insoluble in water" },
    { word: "lunar", definition: "Relating to the moon" }
  ],
  M: [
    { word: "molecule", definition: "A group of atoms bonded together" },
    { word: "mass", definition: "A coherent body of matter with no definite shape" },
    { word: "momentum", definition: "The quantity of motion of a moving body" },
    { word: "mutation", definition: "A change in the DNA sequence" },
    { word: "magnetism", definition: "Physical phenomena arising from the force between magnets" }
  ],
  N: [
    { word: "nucleus", definition: "The positively charged central core of an atom" },
    { word: "neuron", definition: "A specialized cell transmitting nerve impulses" },
    { word: "nebula", definition: "A cloud of gas and dust in outer space" },
    { word: "neutron", definition: "A subatomic particle without an electric charge" },
    { word: "network", definition: "A group or system of interconnected people or things" }
  ],
  O: [
    { word: "osmosis", definition: "Solvent molecules passing through a semipermeable membrane" },
    { word: "orbit", definition: "The curved path of a celestial object or spacecraft" },
    { word: "oxygen", definition: "A chemical element that constitutes 21 percent of the atmosphere" },
    { word: "optics", definition: "The scientific study of sight and the behavior of light" },
    { word: "organism", definition: "An individual animal, plant, or single-celled life form" }
  ],
  P: [
    { word: "physics", definition: "The branch of science concerned with the nature and properties of matter and energy" },
    { word: "photon", definition: "A particle representing a quantum of light" },
    { word: "planet", definition: "A celestial body moving in an elliptical orbit around a star" },
    { word: "protein", definition: "Nitrogenous organic compounds essential for all living organisms" },
    { word: "pathogen", definition: "A bacterium, virus, or other microorganism that can cause disease" }
  ],
  Q: [
    { word: "quantum", definition: "A discrete quantity of energy" },
    { word: "quark", definition: "Any of a number of subatomic particles carrying a fractional electric charge" },
    { word: "quadrant", definition: "Each of four parts of a plane, sphere, space, or body divided by two lines at right angles" },
    { word: "quotient", definition: "A result obtained by dividing one quantity by another" },
    { word: "quasar", definition: "A massive and extremely remote celestial object emitting large amounts of energy" }
  ],
  R: [
    { word: "radiation", definition: "The emission of energy as electromagnetic waves" },
    { word: "robot", definition: "A machine resembling a human being and able to replicate certain movements" },
    { word: "rna", definition: "Ribonucleic acid, present in all living cells" },
    { word: "refraction", definition: "The fact or phenomenon of light being deflected in passing obliquely through a medium" },
    { word: "rocket", definition: "A vehicle propelled by exhaust gas from a rocket engine" }
  ],
  S: [
    { word: "science", definition: "The systematic study of the physical and natural world" },
    { word: "species", definition: "A group of living organisms consisting of similar individuals capable of exchanging genes" },
    { word: "software", definition: "The programs and other operating information used by a computer" },
    { word: "spectrum", definition: "A band of colors, as seen in a rainbow, produced by separation of the components of light" },
    { word: "symbiosis", definition: "Interaction between two different organisms living in close physical association" }
  ],
  T: [
    { word: "taxonomy", definition: "The branch of science concerned with classification" },
    { word: "theorem", definition: "A general proposition not self-evident but proved by a chain of reasoning" },
    { word: "telescope", definition: "An optical instrument designed to make distant objects appear nearer" },
    { word: "temperature", definition: "The degree or intensity of heat present in a substance or object" },
    { word: "thermodynamics", definition: "The branch of physical science that deals with the relations between heat and other forms of energy" }
  ],
  U: [
    { word: "universe", definition: "All existing matter and space considered as a whole" },
    { word: "ultraviolet", definition: "Electromagnetic radiation with a wavelength from 10 nm to 400 nm" },
    { word: "uranium", definition: "A chemical element with the symbol U, a radioactive metal" },
    { word: "ultrasound", definition: "Sound or other vibrations having an ultrasonic frequency" },
    { word: "urethane", definition: "A synthetic crystalline compound used in the manufacture of plastics" }
  ],
  V: [
    { word: "velocity", definition: "The speed of something in a given direction" },
    { word: "vacuole", definition: "A space or vesicle within the cytoplasm of a cell" },
    { word: "vacuum", definition: "A space entirely devoid of matter" },
    { word: "variable", definition: "A data item that may take on more than one value during the runtime of a program" },
    { word: "vector", definition: "A quantity having direction as well as magnitude" }
  ],
  W: [
    { word: "wattage", definition: "A measure of electrical power expressed in watts" },
    { word: "wavelength", definition: "The distance between successive crests of a wave" },
    { word: "weather", definition: "The state of the atmosphere at a place and time" },
    { word: "weight", definition: "A body's relative mass or the quantity of matter contained by it" },
    { word: "web", definition: "A complex system of interconnected elements (e.g., World Wide Web)" }
  ],
  X: [
    { word: "x-ray", definition: "An electromagnetic wave of high energy and very short wavelength" },
    { word: "xenon", definition: "A chemical element, a heavy, colorless, and odorless noble gas" },
    { word: "xerophyte", definition: "A plant that needs very little water" },
    { word: "xylem", definition: "The vascular tissue in plants that conducts water and dissolved nutrients" },
    { word: "x-axis", definition: "The principal or horizontal axis of a system of coordinates" }
  ],
  Y: [
    { word: "y-axis", definition: "The secondary or vertical axis of a system of coordinates" },
    { word: "yield", definition: "The amount of an agricultural or industrial product produced" },
    { word: "yttrium", definition: "A chemical element, a silvery-metallic transition metal" },
    { word: "yolk", definition: "The yellow part of an egg, containing nutrients" },
    { word: "year", definition: "The time taken by a planet to make one revolution around the sun" }
  ],
  Z: [
    { word: "zoology", definition: "The scientific study of the behavior, structure, classification, and distribution of animals" },
    { word: "zinc", definition: "A chemical element, a slightly brittle metal at room temperature" },
    { word: "zygote", definition: "A diploid cell resulting from the fusion of two haploid gametes" },
    { word: "zenith", definition: "The time at which something is most powerful or successful" },
    { word: "zero", definition: "No quantity or number; naught" }
  ]
};

/**
 * Returns a random letter key from the wordBank.
 * @returns {string} One of the letters A-Z
 */
function getRandomLetter() {
  const letters = Object.keys(wordBank);
  const randomIndex = Math.floor(Math.random() * letters.length);
  return letters[randomIndex];
}

/**
 * Returns all word objects for a designated letter.
 * @param {string} letter - A letter from A-Z
 * @returns {Array} An array of objects: {word, definition}
 */
function getWordsByLetter(letter) {
  if (!letter || typeof letter !== 'string') return [];
  const upperLetter = letter.toUpperCase();
  return wordBank[upperLetter] || [];
}

/**
 * Shuffles words of a specific letter and returns up to the specified limit without duplicates.
 * @param {string} letter - A letter from A-Z
 * @param {number} limit - The maximum number of words to return (default 12)
 * @returns {Array} Shuffled array of specific word objects capped by the limit
 */
function getRoundWords(letter, limit = 12) {
  const allWordsForLetter = getWordsByLetter(letter);
  if (!allWordsForLetter || allWordsForLetter.length === 0) {
    return [];
  }
  
  // Clone to avoid side effects
  const clonedWords = [...allWordsForLetter];
  
  // Fisher-Yates Shuffle
  for (let i = clonedWords.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [clonedWords[i], clonedWords[j]] = [clonedWords[j], clonedWords[i]];
  }
  
  // Ensure we don't return more duplicated words, picking the top `limit` distinct elements.
  // We remove duplicates just in case there are identical words in the bank by mistake.
  const distinctWords = [];
  const trackingSet = new Set();
  
  for (const obj of clonedWords) {
    if (!trackingSet.has(obj.word.toLowerCase())) {
      trackingSet.add(obj.word.toLowerCase());
      distinctWords.push(obj);
      if (distinctWords.length === limit) {
        break;
      }
    }
  }

  return distinctWords;
}

// Export for varying environments
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    wordBank,
    getRandomLetter,
    getWordsByLetter,
    getRoundWords
  };
} else if (typeof window !== 'undefined') {
  window.STEMDictionary = {
    wordBank,
    getRandomLetter,
    getWordsByLetter,
    getRoundWords
  };
}
