"""
repair_dictionary_definitions.py
================================
Military-grade dictionary repair engine for Osmosis.
- Fixes truncated definitions cut off by column/page boundaries
- Cleans trailing stray section letters (e.g., '... infection. A')
- Cleans diagram captions & OCR label contamination
- Normalizes punctuation, spaces, and character encoding
- Purges single-character/invalid noise headwords
- Rebuilds dictionary_extracted_final.json, dictionary.json, and core_dictionary.js
"""

import json
import re
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

INPUT_FILE = "dictionary_extracted_final.json"
BACKUP_FILE = "dictionary_extracted_final.bak2.json"

# Complete, authoritative replacements for truncated & contaminated definitions
TARGETED_REPAIRS = {
    "ACCESS CONTROL LIST": (
        "A list of user permissions for a file, folder or other object. It defines what users and groups "
        "can access and what privileges (such as read, write, or execute) they are granted on a computer system or network."
    ),
    "ACID ANHYDRIDE": (
        "A non-metal oxide that reacts with water to form an acidic solution, or an organic compound containing two acyl groups bound to the same oxygen atom with the general formula R-CO-O-CO-R'."
    ),
    "AGRICULTURAL ADVISORY SERVICES": (
        "In agriculture, services that support and facilitate people engaged in agricultural production "
        "to improve the economic and environmental performance of their agricultural holdings and farming practices."
    ),
    "AMORPHOUS CARBON": (
        "A carbon material without long-range crystalline order. Short-range order exists, but with deviations "
        "of the interatomic distances and/or interbonding angles with respect to crystalline graphite or diamond."
    ),
    "AXIS OF SYMMETRY": (
        "A line through a plane or a 2-dimensional (2-D) shape so that each side of this line is a mirror "
        "image of each other. It is a line that divides a shape into two congruent halves."
    ),
    "BAR CHART": (
        "A graphical display of categorical data using rectangular bars with heights or lengths proportional to the values that they represent."
    ),
    "BASE-PAIRING RULE": (
        "The rules of base pairing (or nucleotide pairing) in the formation of nucleic acids (DNA and RNA) with the requirement that adenine must always pair with thymine (or uracil in RNA) and guanine with cytosine, which constitutes the basis of the genetic code."
    ),
    "BOX-AND-WHISKER-PLOT": (
        "A graphical method of displaying the distribution of a dataset based on a five-number summary: minimum, first quartile, median, third quartile, and maximum."
    ),
    "CAULOID": (
        "A stem-like structure found in certain algae and bryophytes that resembles the true stem of higher vascular plants but lacks complex vascular tissue."
    ),
    "CIRCLE GRAPH": (
        "A method of displaying statistical information where a circle is divided into different-sized "
        "sectors by radial lines. The angle and area of each sector is directly proportional to the percentage or frequency of the data category."
    ),
    "EVOLUTIONARY TREE": (
        "A branching diagram or tree showing the evolutionary relationships and common ancestry among various biological species or entities based upon similarities and differences in their physical or genetic characteristics."
    ),
    "FALCIFORM": (
        "Having a curved or sickle-like shape, such as the falciform ligament of the liver."
    ),
    "FLORAL DIAGRAM": (
        "A schematic diagrammatic representation of the cross-section of a flower showing the relative position, number, and arrangement of its floral parts including sepals, petals, stamens, and carpels."
    ),
    "GIBBS ENERGY DIAGRAM": (
        "A graphical plot representing the variation in Gibbs free energy of a thermodynamic system as a function of reaction progress or composition."
    ),
    "ISOPRENE": (
        "A colourless volatile liquid hydrocarbon with the formula CH2=C(CH3)-CH=CH2 (2-methyl-1,3-butadiene). It is the fundamental chemical building block of terpenes and natural rubber."
    ),
    "PISACEOUS": (
        "Having a pea-green colour or resembling peas in appearance."
    ),
    "POROSE": (
        "Characterized by the presence of small openings, pores, or perforations."
    ),
    "POURBAIX DIAGRAM": (
        "A thermodynamic phase diagram that maps out possible stable equilibrium phases of an aqueous electrochemical system in terms of potential (E) and pH."
    ),
    "PYROGALLOL": (
        "An organic compound with the formula C6H3(OH)3 (1,2,3-trihydroxybenzene), appearing as a white crystalline solid and used as a powerful reducing agent and photographic developer."
    ),
    "RUFOUS": (
        "Having a reddish-brown or rust-like colour, frequently used in biological descriptions of plumage, pelage, and botanical specimens."
    ),
    "SALICYLIC ACID": (
        "A lipophilic monohydroxybenzoic acid with the formula C7H6O3 (2-hydroxybenzoic acid), commonly used in medicine, skincare, and as a precursor to aspirin (acetylsalicylic acid)."
    ),
    "AMINO": (
        "A term used to describe an organic chemical compound or radical containing the -NH2 group of atoms, "
        "combined with a non-acidic hydrocarbon radical."
    ),
    "AMINO ACID": (
        "A class of organic compounds with the general formula R-CH(NH2)COOH, in which a carbon atom has bonds "
        "to an amino group (-NH2), a carboxyl group (-COOH), a hydrogen atom (-H) and an organic side chain (-R). "
        "Amino acids are the building blocks of proteins. There are 20 standard amino acids that make up all proteins in living organisms."
    ),
    "ADENOSINE TRIPHOSPHATE, ATP": (
        "A nucleotide molecule with the molecular formula C10H16N5O13P3. It consists of adenine, ribose, and three "
        "phosphate groups. It is the primary energy-carrying molecule in all living cells, supplying energy for muscle contraction, "
        "nerve impulse transmission, and chemical synthesis."
    ),
    "ACETYLATION": (
        "A chemical reaction in which a small molecule called an acetyl group is added to another molecule, "
        "often a protein or organic compound, modifying its chemical properties and biological activity."
    ),
    "ACETONE-CHLOR-HAEMIN TEST": (
        "A forensic and clinical microchemical test used for detecting the presence of blood by crystal formation of haemin."
    ),
    "ACROTONIC": (
        "Describing the development or branching pattern of a plant stem where the most vigorous growth occurs at the apex or upper portion."
    ),
    "ABERRATION": (
        "In optics, any distortion or failure of a lens or mirror to produce an exact, point-for-point image of an object, "
        "including spherical aberration and chromatic aberration where different wavelengths of light focus at different points."
    ),
    "ALLOSYNDESIS": (
        "Pairing of chromosomes derived from different ancestral species during meiosis in an allopolyploid organism."
    ),
    "ALPHA-ADDITION": (
        "A chemical reaction resulting in the formation of two new chemical bonds to the same atom in one of the reactant molecular entities."
    ),
    "ALTERNATE NEWSGROUP": (
        "On Usenet, a user-originated newsgroup hierarchy containing all newsgroups whose name begins with 'alt.', "
        "allowing users to create groups without formal voting procedures."
    ),
    "ALTIMETRY": (
        "The science and technique of measuring altitude or elevation above sea level or planetary terrain, "
        "often using radar or laser instruments from satellites or aircraft."
    ),
    "CURIE-WEISS LAW": (
        "A law relating the magnetic susceptibility chi of a paramagnetic substance to its absolute temperature T: "
        "chi = C / (T - theta), where C is the Curie constant and theta is the Weiss constant."
    ),
    "DISPERSION RELATION": (
        "In physics and wave mechanics, an equation relating the frequency or energy of a wave to its wavelength or wave vector."
    ),
    "DOUBLE PRECISION": (
        "A computer number format that occupies two adjacent storage locations in memory (usually 64 bits), "
        "providing twice the precision of standard single-precision floating-point numbers."
    ),
    "DYNAMIC PROGRAMMING": (
        "An algorithmic technique for solving complex optimization problems by breaking them down into simpler "
        "overlapping subproblems and storing the results of subproblems to avoid redundant computations."
    ),
    "ECCENTRICITY": (
        "In mathematics and astronomy, a parameter that defines the degree to which an orbit or conic section "
        "(such as an ellipse) deviates from being a perfect circle."
    ),
    "ELECTRIC DIPOLE MOMENT": (
        "A measure of the separation of positive and negative electrical charges in a system, calculated as the "
        "product of the charge magnitude and the displacement vector between them."
    ),
    "ELECTROMAGNETIC SPECTRUM": (
        "The entire range of all types of electromagnetic radiation, ordered by frequency or wavelength, "
        "ranging from radio waves and microwaves to infrared, visible light, ultraviolet, X-rays, and gamma rays."
    ),
    "EQUILIBRIUM CONSTANT": (
        "The value of a reaction quotient for a chemical system at chemical equilibrium, expressing the ratio "
        "of product concentrations to reactant concentrations each raised to their stoichiometric coefficients."
    ),
    "FERMI ENERGY": (
        "The highest occupied energy level of electrons in a quantum mechanical system of fermions at absolute zero temperature."
    ),
    "FOURIER TRANSFORM": (
        "A mathematical transform that decomposes any waveform or function of time into the continuous frequencies that make it up."
    ),
    "GREENHOUSE EFFECT": (
        "The process by which greenhouse gases in a planet's atmosphere absorb infrared radiation emitted from the surface, "
        "trapping heat and warming the planetary surface and lower atmosphere."
    ),
    "HEISENBERG UNCERTAINTY PRINCIPLE": (
        "A fundamental principle in quantum mechanics stating that the position and momentum of a particle cannot "
        "both be simultaneously known with arbitrary precision: delta x * delta p >= hbar / 2."
    ),
    "HOMEOSTASIS": (
        "The state of steady internal, physical, and chemical conditions maintained by living organisms despite external environmental changes."
    ),
    "MEIOSIS": (
        "A specialized form of cell division in sexually reproducing organisms that reduces the chromosome number by half, "
        "producing four genetically diverse haploid gamete cells from one diploid parent cell."
    ),
    "MITOSIS": (
        "The process of cell division in eukaryotic cells that replicates the chromosomes and segregates them into two "
        "identical daughter nuclei, essential for growth, repair, and asexual reproduction."
    ),
    "PHOTOSYNTHESIS": (
        "The biological process by which green plants, algae, and cyanobacteria convert light energy into chemical energy, "
        "synthesizing glucose and oxygen from carbon dioxide and water: 6CO2 + 6H2O + light -> C6H12O6 + 6O2."
    ),
    "OXIDATION NUMBER": (
        "A hypothetical charge that an atom would have if all bonds to atoms of different elements were 100% ionic, "
        "used to track electron transfer in oxidation-reduction (redox) reactions."
    ),
    "STANDARD DEVIATION": (
        "A statistical measure of the amount of variation or dispersion of a set of values relative to their arithmetic mean."
    ),
    "THERMODYNAMICS": (
        "The branch of physics and physical chemistry that deals with the relations between heat, work, temperature, and energy."
    )
}

def clean_definition_text(def_text):
    if not def_text:
        return ""
    
    t = def_text.strip()
    
    # 1. Remove non-printable control characters
    t = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', t)
    
    # 2. Strip embedded diagram labels / captions
    t = re.sub(r'(?:Chemical\s+[Ss]tructure\s+of|Neutral\s+Structure\s+of|Zwitter\s+Ion\s+Structure\s+of|Diagram\s+showing).*$', '', t, flags=re.IGNORECASE)
    t = re.sub(r'\b(?:CCN\+|HROOC|CNHH|t2g\s+eg\s+dx2-y2|HCCCOOCCCCCCNHHHNNHNNNNHHHH)\b.*$', '', t)
    t = re.sub(r'\bFig(?:\.|\s+)[I|V|X|0-9]+.*$', '', t)
    
    # 3. Strip trailing stray capital letter (e.g. 'infection. A', 'plastics. A', 'numbers. A')
    t = re.sub(r'([\.\!\?])\s+[A-Z]$', r'\1', t)
    t = re.sub(r'\s+[A-Z]$', '.', t)
    
    # 4. Strip duplicate spaces
    t = re.sub(r'\s+', ' ', t).strip()
    
    # 5. Ensure terminal punctuation
    if t and not t.endswith(('.', '!', '?', '"', "'", ')', ']', ';')):
        t += '.'
        
    return t

def repair_dictionary():
    print(f"Reading {INPUT_FILE}...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        entries = json.load(f)

    print(f"Loaded {len(entries)} entries. Applying repairs and filtering artifacts...")

    repaired_count = 0
    override_count = 0
    clean_entries = []

    for item in entries:
        word = item.get("word", "").strip()
        raw_hw = item.get("raw_headword", "").strip()
        definition = item.get("definition", "").strip()

        # Filter single character artifact headwords (e.g. accidental "a", "b", digits)
        if len(word) <= 1 and not (word.upper() in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"] and len(definition) > 30):
            continue
        if re.match(r'^\d+$', word):
            continue

        # Check Hard Overrides
        norm_key = word.upper().strip()
        matched_override = None
        
        if norm_key in TARGETED_REPAIRS:
            matched_override = TARGETED_REPAIRS[norm_key]
        else:
            for k, val in TARGETED_REPAIRS.items():
                if k == raw_hw.upper() or norm_key.startswith(k) or k.startswith(norm_key):
                    matched_override = val
                    break

        if matched_override:
            item["definition"] = matched_override
            override_count += 1
            repaired_count += 1
            clean_entries.append(item)
            continue

        # General cleaning
        cleaned = clean_definition_text(definition)
        if cleaned != definition:
            item["definition"] = cleaned
            repaired_count += 1
            
        clean_entries.append(item)

    print(f"Applied targeted authoritative overrides to {override_count} entries.")
    print(f"Cleaned and repaired a total of {repaired_count} entries.")
    print(f"Final valid entry count: {len(clean_entries)}")

    # Save to dictionary_extracted_final.json
    with open(INPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(clean_entries, f, indent=2, ensure_ascii=False)
    print(f"Saved repaired data to {INPUT_FILE}")

    # Run build_core_dictionary
    print("\nRebuilding dictionary.json and core_dictionary.js...")
    sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
    from build_core_dictionary import build_core_dictionary
    build_core_dictionary(input_json=INPUT_FILE, output_js="core_dictionary.js", output_json="dictionary.json")
    print("Rebuild COMPLETE!")

if __name__ == "__main__":
    repair_dictionary()
