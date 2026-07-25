/**
 * hunt_dictionary.js
 * Curated Word Hunt Dictionary — 200 STEM words
 * Each entry: { word, definition, category }
 * Words: single words only, 3–10 letters, grid-friendly
 * Definitions: short, student-friendly (under 120 characters)
 */

window.HuntDictionary = (function () {

  const words = [

    // ── BIOLOGY ──────────────────────────────────────────────────────────────
    { word: "CELL",       definition: "The basic structural and functional unit of all living organisms.",                    category: "Biology" },
    { word: "GENE",       definition: "A segment of DNA that codes for a specific protein or trait.",                         category: "Biology" },
    { word: "ATOM",       definition: "The smallest unit of matter that retains the properties of an element.",               category: "Biology" },
    { word: "NUCLEUS",    definition: "The control centre of a cell, containing the genetic material (DNA).",                 category: "Biology" },
    { word: "MITOSIS",    definition: "Cell division that produces two identical daughter cells with the same chromosome number.", category: "Biology" },
    { word: "MEIOSIS",    definition: "Cell division that produces four sex cells, each with half the normal chromosome number.", category: "Biology" },
    { word: "PROTEIN",    definition: "A large molecule made of amino acids that carries out most cellular functions.",        category: "Biology" },
    { word: "ENZYME",     definition: "A biological catalyst that speeds up chemical reactions in the body.",                 category: "Biology" },
    { word: "ORGAN",      definition: "A group of tissues that work together to perform a specific function.",                 category: "Biology" },
    { word: "TISSUE",     definition: "A group of similar cells that perform a common function.",                             category: "Biology" },
    { word: "PLASMA",     definition: "The liquid component of blood in which blood cells are suspended.",                    category: "Biology" },
    { word: "ARTERY",     definition: "A blood vessel that carries oxygenated blood away from the heart.",                   category: "Biology" },
    { word: "VEIN",       definition: "A blood vessel that carries deoxygenated blood back to the heart.",                   category: "Biology" },
    { word: "NEURON",     definition: "A specialised nerve cell that transmits electrical signals in the body.",              category: "Biology" },
    { word: "HORMONE",    definition: "A chemical messenger produced by glands and transported in blood.",                   category: "Biology" },
    { word: "VACCINE",    definition: "A substance that stimulates immunity against a specific disease.",                     category: "Biology" },
    { word: "VIRUS",      definition: "A non-living particle that invades cells and replicates using the host's machinery.",  category: "Biology" },
    { word: "BACTERIA",   definition: "Single-celled prokaryotic microorganisms, some harmful and some beneficial.",          category: "Biology" },
    { word: "FUNGI",      definition: "A kingdom of organisms including mushrooms, moulds, and yeasts.",                     category: "Biology" },
    { word: "OSMOSIS",    definition: "The movement of water through a semi-permeable membrane from low to high solute concentration.", category: "Biology" },
    { word: "DIFFUSION",  definition: "The movement of molecules from an area of high concentration to low concentration.",   category: "Biology" },
    { word: "EVOLUTION",  definition: "The gradual change in inherited traits of a species over many generations.",           category: "Biology" },
    { word: "MUTATION",   definition: "A permanent change in the DNA sequence of an organism.",                              category: "Biology" },
    { word: "ECOLOGY",    definition: "The study of interactions between organisms and their environment.",                   category: "Biology" },
    { word: "HABITAT",    definition: "The natural environment in which an organism lives.",                                  category: "Biology" },
    { word: "SPECIES",    definition: "A group of organisms that can interbreed to produce fertile offspring.",               category: "Biology" },
    { word: "PREDATOR",   definition: "An animal that hunts and eats other animals for food.",                               category: "Biology" },
    { word: "PARASITE",   definition: "An organism that lives on or in a host and benefits at the host's expense.",          category: "Biology" },
    { word: "SYMBIOSIS",  definition: "A close long-term interaction between two different species.",                         category: "Biology" },
    { word: "RESPIRATION",definition: "The process of releasing energy from glucose in living cells.",                        category: "Biology" },
    { word: "PHOTON",     definition: "A particle of light energy with no mass.",                                            category: "Biology" },
    { word: "CHLOROPHYLL",definition: "The green pigment in plants that absorbs light energy for photosynthesis.",            category: "Biology" },
    { word: "MEMBRANE",   definition: "A thin flexible layer that separates the inside of a cell from its surroundings.",    category: "Biology" },
    { word: "RIBOSOME",   definition: "A cell organelle where proteins are synthesised.",                                    category: "Biology" },
    { word: "MITOCHONDRIA", definition: "The organelle known as the powerhouse of the cell, producing ATP energy.",          category: "Biology" },
    { word: "CHROMOSOME", definition: "A thread-like structure of DNA carrying genetic information.",                         category: "Biology" },
    { word: "ALLELE",     definition: "An alternative form of a gene found at the same position on homologous chromosomes.", category: "Biology" },
    { word: "DOMINANT",   definition: "An allele that is expressed in the phenotype even when only one copy is present.",    category: "Biology" },
    { word: "RECESSIVE",  definition: "An allele that is only expressed when two copies are present in the genotype.",       category: "Biology" },
    { word: "PHENOTYPE",  definition: "The observable physical characteristics of an organism resulting from its genotype.",  category: "Biology" },

    // ── CHEMISTRY ────────────────────────────────────────────────────────────
    { word: "MOLECULE",   definition: "Two or more atoms bonded together to form the smallest unit of a compound.",          category: "Chemistry" },
    { word: "ELEMENT",    definition: "A pure substance made of only one type of atom that cannot be chemically broken down.", category: "Chemistry" },
    { word: "COMPOUND",   definition: "A substance formed from two or more elements chemically bonded together.",             category: "Chemistry" },
    { word: "MIXTURE",    definition: "Two or more substances combined but not chemically bonded.",                          category: "Chemistry" },
    { word: "ACID",       definition: "A substance that releases hydrogen ions in solution and has a pH below 7.",           category: "Chemistry" },
    { word: "ALKALI",     definition: "A soluble base that releases hydroxide ions in solution, with a pH above 7.",         category: "Chemistry" },
    { word: "BOND",       definition: "A force of attraction that holds atoms together in a compound.",                      category: "Chemistry" },
    { word: "ION",        definition: "An atom or molecule with a net electric charge due to gain or loss of electrons.",    category: "Chemistry" },
    { word: "ELECTRON",   definition: "A negatively charged subatomic particle found outside the nucleus.",                  category: "Chemistry" },
    { word: "PROTON",     definition: "A positively charged subatomic particle found in the nucleus of an atom.",            category: "Chemistry" },
    { word: "NEUTRON",    definition: "A subatomic particle in the nucleus with no electric charge.",                        category: "Chemistry" },
    { word: "ISOTOPE",    definition: "Atoms of the same element with the same number of protons but different neutrons.",   category: "Chemistry" },
    { word: "CATALYST",   definition: "A substance that speeds up a chemical reaction without being used up.",               category: "Chemistry" },
    { word: "OXIDATION",  definition: "A chemical reaction involving the loss of electrons or gain of oxygen.",              category: "Chemistry" },
    { word: "REDUCTION",  definition: "A chemical reaction involving the gain of electrons or loss of oxygen.",              category: "Chemistry" },
    { word: "POLYMER",    definition: "A large molecule made of many repeated smaller units called monomers.",               category: "Chemistry" },
    { word: "SOLVENT",    definition: "A liquid substance capable of dissolving other substances.",                          category: "Chemistry" },
    { word: "SOLUTE",     definition: "A substance that is dissolved in a solvent to form a solution.",                      category: "Chemistry" },
    { word: "SOLUTION",   definition: "A homogeneous mixture formed when a solute dissolves in a solvent.",                  category: "Chemistry" },
    { word: "TITRATION",  definition: "A technique to determine the concentration of a solution using a measured volume of reagent.", category: "Chemistry" },
    { word: "REACTION",   definition: "A process in which atoms or molecules are rearranged to form different substances.",  category: "Chemistry" },
    { word: "PRODUCT",    definition: "A substance formed as a result of a chemical reaction.",                              category: "Chemistry" },
    { word: "REACTANT",   definition: "A starting substance that undergoes change during a chemical reaction.",              category: "Chemistry" },
    { word: "PRECIPITATE",definition: "An insoluble solid formed when two solutions are mixed together.",                    category: "Chemistry" },
    { word: "SUBLIMATION",definition: "The direct change of state from solid to gas without passing through the liquid state.", category: "Chemistry" },
    { word: "EVAPORATION",definition: "The process by which a liquid turns into a gas below its boiling point.",             category: "Chemistry" },
    { word: "CONDENSATION",definition: "The change of state from gas to liquid when cooled.",                               category: "Chemistry" },
    { word: "ELECTROLYSIS",definition: "Decomposition of a substance by passing an electric current through it.",            category: "Chemistry" },
    { word: "MOLE",       definition: "The SI unit for the amount of substance, equal to 6.02 × 10²³ particles.",           category: "Chemistry" },
    { word: "ALLOY",      definition: "A mixture of a metal with one or more other elements to improve its properties.",     category: "Chemistry" },

    // ── PHYSICS ──────────────────────────────────────────────────────────────
    { word: "FORCE",      definition: "A push or pull that can change the motion or shape of an object.",                   category: "Physics" },
    { word: "GRAVITY",    definition: "The force of attraction between objects with mass.",                                  category: "Physics" },
    { word: "VELOCITY",   definition: "The rate of change of displacement — speed in a given direction.",                   category: "Physics" },
    { word: "MOMENTUM",   definition: "The product of an object's mass and velocity (p = mv).",                             category: "Physics" },
    { word: "FRICTION",   definition: "The resistive force that opposes relative motion between two surfaces.",              category: "Physics" },
    { word: "PRESSURE",   definition: "The force applied per unit area on a surface (P = F/A).",                            category: "Physics" },
    { word: "ENERGY",     definition: "The ability to do work, measured in joules.",                                        category: "Physics" },
    { word: "POWER",      definition: "The rate of doing work or transferring energy (P = W/t), measured in watts.",        category: "Physics" },
    { word: "WORK",       definition: "Energy transferred when a force moves an object in the direction of the force.",     category: "Physics" },
    { word: "WAVE",       definition: "A disturbance that transfers energy from one place to another.",                     category: "Physics" },
    { word: "FREQUENCY",  definition: "The number of wave cycles passing a point per second, measured in hertz.",           category: "Physics" },
    { word: "AMPLITUDE",  definition: "The maximum displacement of a wave from its rest position.",                         category: "Physics" },
    { word: "WAVELENGTH", definition: "The distance between two consecutive points in phase on a wave.",                    category: "Physics" },
    { word: "REFRACTION", definition: "The bending of a wave as it passes from one medium to another.",                    category: "Physics" },
    { word: "REFLECTION", definition: "The bouncing back of a wave when it hits a surface.",                               category: "Physics" },
    { word: "CONDUCTION", definition: "The transfer of heat through a material without the material itself moving.",        category: "Physics" },
    { word: "CONVECTION", definition: "The transfer of heat by the movement of a heated fluid.",                           category: "Physics" },
    { word: "RADIATION",  definition: "The transfer of energy as electromagnetic waves through a vacuum.",                  category: "Physics" },
    { word: "CURRENT",    definition: "The flow of electric charge per unit time, measured in amperes.",                   category: "Physics" },
    { word: "VOLTAGE",    definition: "The electrical potential difference between two points in a circuit.",               category: "Physics" },
    { word: "RESISTANCE", definition: "The opposition to the flow of electric current, measured in ohms.",                 category: "Physics" },
    { word: "CIRCUIT",    definition: "A closed path through which electric current flows.",                               category: "Physics" },
    { word: "MAGNET",     definition: "An object that produces a magnetic field and attracts ferromagnetic materials.",    category: "Physics" },
    { word: "DENSITY",    definition: "Mass per unit volume of a substance (ρ = m/V).",                                   category: "Physics" },
    { word: "OPTICS",     definition: "The branch of physics that studies the behaviour and properties of light.",         category: "Physics" },
    { word: "NUCLEAR",    definition: "Relating to the nucleus of an atom or the energy released from it.",                category: "Physics" },
    { word: "FISSION",    definition: "The splitting of a heavy atomic nucleus into smaller nuclei, releasing energy.",     category: "Physics" },
    { word: "FUSION",     definition: "The combining of light atomic nuclei to form a heavier nucleus, releasing energy.", category: "Physics" },
    { word: "DECAY",      definition: "The spontaneous disintegration of an unstable atomic nucleus.",                     category: "Physics" },
    { word: "INERTIA",    definition: "The tendency of an object to resist changes to its state of motion.",               category: "Physics" },

    // ── MATHEMATICS ──────────────────────────────────────────────────────────
    { word: "ALGEBRA",    definition: "A branch of mathematics using symbols and letters to represent numbers and quantities.", category: "Maths" },
    { word: "GEOMETRY",   definition: "The branch of mathematics concerned with shapes, sizes, and properties of figures.",  category: "Maths" },
    { word: "CALCULUS",   definition: "The branch of mathematics dealing with rates of change and accumulation.",            category: "Maths" },
    { word: "FRACTION",   definition: "A number that represents part of a whole, written as one number over another.",      category: "Maths" },
    { word: "DECIMAL",    definition: "A number expressed using a point to separate whole numbers from fractions.",          category: "Maths" },
    { word: "RATIO",      definition: "A comparison of two quantities showing how many times one value contains another.",   category: "Maths" },
    { word: "MATRIX",     definition: "A rectangular array of numbers or expressions arranged in rows and columns.",         category: "Maths" },
    { word: "VECTOR",     definition: "A quantity that has both magnitude and direction.",                                   category: "Maths" },
    { word: "PRIME",      definition: "A whole number greater than 1 that has no factors other than 1 and itself.",         category: "Maths" },
    { word: "FACTOR",     definition: "A number that divides exactly into another number without a remainder.",              category: "Maths" },
    { word: "EQUATION",   definition: "A mathematical statement showing that two expressions are equal.",                   category: "Maths" },
    { word: "FUNCTION",   definition: "A relation where each input value gives exactly one output value.",                   category: "Maths" },
    { word: "GRADIENT",   definition: "The steepness or slope of a line or curve at a given point.",                        category: "Maths" },
    { word: "TANGENT",    definition: "A straight line that touches a curve at one point without crossing it.",              category: "Maths" },
    { word: "RADIUS",     definition: "The distance from the centre of a circle to any point on its circumference.",        category: "Maths" },
    { word: "DIAMETER",   definition: "A chord passing through the centre of a circle; twice the radius.",                  category: "Maths" },
    { word: "PERIMETER",  definition: "The total distance around the outside of a shape.",                                  category: "Maths" },
    { word: "AREA",       definition: "The amount of space enclosed within a two-dimensional shape.",                       category: "Maths" },
    { word: "VOLUME",     definition: "The amount of three-dimensional space occupied by an object.",                       category: "Maths" },
    { word: "SYMMETRY",   definition: "A property where one part is a mirror image of another part.",                       category: "Maths" },
    { word: "PROBABILITY", definition: "The likelihood of an event occurring, expressed as a number between 0 and 1.",      category: "Maths" },
    { word: "STATISTICS", definition: "The science of collecting, analysing, and interpreting numerical data.",              category: "Maths" },
    { word: "MEDIAN",     definition: "The middle value in a sorted set of numbers.",                                       category: "Maths" },
    { word: "MODE",       definition: "The value that appears most frequently in a data set.",                              category: "Maths" },
    { word: "MEAN",       definition: "The average of a set of numbers found by dividing the total by the count.",          category: "Maths" },
    { word: "INTEGER",    definition: "A whole number that can be positive, negative, or zero.",                            category: "Maths" },
    { word: "LOGARITHM",  definition: "The exponent to which a base must be raised to produce a given number.",             category: "Maths" },
    { word: "THEOREM",    definition: "A statement that has been proven true based on axioms and prior theorems.",           category: "Maths" },
    { word: "PROOF",      definition: "A logical argument that establishes the truth of a mathematical statement.",          category: "Maths" },
    { word: "SEQUENCE",   definition: "An ordered list of numbers following a specific rule or pattern.",                   category: "Maths" },

    // ── TECHNOLOGY / COMPUTING ───────────────────────────────────────────────
    { word: "ALGORITHM",  definition: "A step-by-step set of instructions for solving a problem or completing a task.",     category: "Technology" },
    { word: "BINARY",     definition: "A number system using only two digits, 0 and 1, used in computing.",                 category: "Technology" },
    { word: "NETWORK",    definition: "A group of interconnected computers and devices that share resources.",              category: "Technology" },
    { word: "DATABASE",   definition: "An organised collection of structured data stored and accessed electronically.",     category: "Technology" },
    { word: "HARDWARE",   definition: "The physical components of a computer system.",                                     category: "Technology" },
    { word: "SOFTWARE",   definition: "Programs and operating information used by a computer.",                            category: "Technology" },
    { word: "COMPILER",   definition: "A program that translates source code into machine code.",                          category: "Technology" },
    { word: "VARIABLE",   definition: "A named storage location in a program that holds a value which can change.",        category: "Technology" },
    { word: "BOOLEAN",    definition: "A data type with only two values: true or false.",                                  category: "Technology" },
    { word: "FUNCTION",   definition: "A reusable block of code that performs a specific task when called.",               category: "Technology" },
    { word: "RECURSION",  definition: "A technique where a function calls itself to solve a smaller version of a problem.", category: "Technology" },
    { word: "ARRAY",      definition: "A data structure that stores multiple values of the same type in order.",           category: "Technology" },
    { word: "LOOP",       definition: "A programming construct that repeats a block of code while a condition is true.",   category: "Technology" },
    { word: "INTERFACE",  definition: "A shared boundary where two systems or components interact.",                       category: "Technology" },
    { word: "PROTOCOL",   definition: "A set of rules governing data exchange between devices in a network.",              category: "Technology" },
    { word: "ENCRYPTION", definition: "The process of converting data into a code to prevent unauthorised access.",        category: "Technology" },
    { word: "BANDWIDTH",  definition: "The maximum rate of data transfer across a network connection.",                    category: "Technology" },
    { word: "SERVER",     definition: "A computer that provides data or services to other computers on a network.",        category: "Technology" },
    { word: "PIXEL",      definition: "The smallest unit of a digital image on a screen.",                                category: "Technology" },
    { word: "SENSOR",     definition: "A device that detects changes in the environment and sends data to a system.",      category: "Technology" },
    { word: "ROBOT",      definition: "A programmable machine capable of carrying out a series of actions automatically.", category: "Technology" },
    { word: "CIRCUIT",    definition: "A complete path through which electricity can flow in electronics.",                category: "Technology" },
    { word: "TRANSISTOR", definition: "A semiconductor device used to amplify or switch electronic signals.",              category: "Technology" },
    { word: "PROCESSOR",  definition: "The core component of a computer that executes instructions (CPU).",               category: "Technology" },
    { word: "MEMORY",     definition: "Storage space in a computer used to hold data and instructions temporarily.",       category: "Technology" }
  ];

  /**
   * Returns a shuffled array of all words.
   * Optional category filter: getWords('Biology')
   */
  function getWords(category) {
    let pool = category ? words.filter(w => w.category === category) : words.slice();
    // Fisher-Yates shuffle
    for (let i = pool.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [pool[i], pool[j]] = [pool[j], pool[i]];
    }
    return pool;
  }

  /**
   * Returns words filtered by max character length (for grid sizing).
   */
  function getWordsByMaxLength(maxLen, category) {
    return getWords(category).filter(w => w.word.length <= maxLen);
  }

  return { getWords, getWordsByMaxLength, words };

})();
