const sharedState = {
  load: function() {
    return JSON.parse(sessionStorage.getItem('gameState')) || {
      username: '', letter: '', length: 0, wordsPool: [],
      selectedWords: [], meanings: {}, score: 0
    };
  },
  save: function(state) {
    sessionStorage.setItem('gameState', JSON.stringify(state));
  }
};

const AudioManager = {
  ctx: null,
  init: function() {
    if (!this.ctx) {
      try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        this.ctx = new AudioContext();
      } catch (err) {}
    }
  },
  play: function(type) {
    if (!this.ctx) return;
    if (this.ctx.state === 'suspended') this.ctx.resume();
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    const now = this.ctx.currentTime;
    
    switch(type) {
      case 'click':
        osc.type = 'sine'; osc.frequency.setValueAtTime(150, now); osc.frequency.exponentialRampToValueAtTime(40, now + 0.1);
        gain.gain.setValueAtTime(1, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.1);
        osc.start(now); osc.stop(now + 0.1); break;
      case 'chip':
        osc.type = 'triangle'; osc.frequency.setValueAtTime(300, now); osc.frequency.exponentialRampToValueAtTime(100, now + 0.1);
        gain.gain.setValueAtTime(0.5, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.1);
        osc.start(now); osc.stop(now + 0.1); break;
      case 'success':
        osc.type = 'sine'; osc.frequency.setValueAtTime(440, now); osc.frequency.setValueAtTime(554, now + 0.1);
        gain.gain.setValueAtTime(0, now); gain.gain.linearRampToValueAtTime(0.5, now + 0.05); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.5);
        osc.start(now); osc.stop(now + 0.5); break;
      case 'error':
        osc.type = 'sawtooth'; osc.frequency.setValueAtTime(100, now); osc.frequency.exponentialRampToValueAtTime(50, now + 0.2);
        gain.gain.setValueAtTime(0.5, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.2);
        osc.start(now); osc.stop(now + 0.2); break;
    }
  }
};

document.addEventListener('click', (e) => {
  AudioManager.init();
  if (e.target.closest('.classic-btn')) AudioManager.play('click');
  else if (e.target.closest('.word-chip')) {
    setTimeout(() => {
      if (e.target.closest('.word-chip').classList.contains('wrong')) AudioManager.play('error');
      else AudioManager.play('chip');
    }, 10);
  }
});

const DictionaryLogic = {
  fallback: {
    "abyssal": "Relating to or denoting the depths or bed of the ocean, especially between about 10,000 and 20,000 feet down.",
    "anatomy": "The branch of science concerned with the bodily structure of humans, animals, and other living organisms.",
    "benthic": "Relating to, or occurring at the bottom of a body of water.",
    "catalyst": "A substance that increases the rate of a chemical reaction without itself undergoing any permanent chemical change.",
    "dendrite": "A short branched extension of a nerve cell, along which impulses received from other cells at synapses are transmitted.",
    "electron": "A stable subatomic particle with a charge of negative electricity, found in all atoms.",
    "friction": "The resistance that one surface or object encounters when moving over another.",
    "genetics": "The study of heredity and the variation of inherited characteristics.",
    "herbivore": "An animal that feeds on plants.",
    "isotope": "Each of two or more forms of the same element that contain equal numbers of protons but different numbers of neutrons.",
    "kinetics": "The branch of chemistry or biochemistry concerned with measuring and studying the rates of reactions.",
    "lithosphere": "The rigid outer part of the earth, consisting of the crust and upper mantle.",
    "molecule": "A group of atoms bonded together, representing the smallest fundamental unit of a chemical compound.",
    "nucleus": "The positively charged central core of an atom, consisting of protons and neutrons and containing nearly all its mass.",
    "osmosis": "A process by which molecules of a solvent tend to pass through a semipermeable membrane from a less concentrated solution into a more concentrated one.",
    "pathogen": "A bacterium, virus, or other microorganism that can cause disease.",
    "quantum": "A discrete quantity of energy proportional in magnitude to the frequency of the radiation it represents.",
    "radiation": "The emission of energy as electromagnetic waves or as moving subatomic particles, especially high-energy particles which cause ionization.",
    "symbiosis": "Interaction between two different organisms living in close physical association, typically to the advantage of both.",
    "taxonomy": "The branch of science concerned with classification, especially of organisms; systematics.",
    "universe": "All existing matter and space considered as a whole; the cosmos.",
    "vacuole": "A space or vesicle within the cytoplasm of a cell, enclosed by a membrane and typically containing fluid.",
    "velocity": "The speed of something in a given direction.",
    "wattage": "A measure of electrical power expressed in watts.",
    "chromosome": "A threadlike structure of nucleic acids and protein found in the nucleus of most living cells, carrying genetic information.",
    "mitochondria": "An organelle found in large numbers in most cells, in which the biochemical processes of respiration and energy production occur.",
    "photosynthesis": "The process by which green plants and some other organisms use sunlight to synthesize nutrients from carbon dioxide and water.",
    "thermodynamics": "The branch of physical science that deals with the relations between heat and other forms of energy.",
    "pneumonoultramicroscopicsilicovolcanoconiosis": "An invented word for a lung disease caused by inhaling very fine ash and sand dust; the longest English word.",
    "deoxyribonucleic": "A nucleic acid that is the main constituent of the chromosomes of all organisms (part of DNA).",
    "electromagnetism": "The interaction of electric currents or fields and magnetic fields.",
    "paleontology": "The branch of science concerned with fossil animals and plants.",
    "bioluminescence": "The biochemical emission of light by living organisms such as fireflies and deep-sea fishes.",
    "crystallography": "The branch of science concerned with the structure and properties of crystals.",
    "spectroscopy": "The branch of science concerned with the investigation and measurement of spectra produced when matter interacts with or emits electromagnetic radiation.",
    "neurotransmitter": "A chemical substance that is released at the end of a nerve fiber by the arrival of a nerve impulse, causing the transfer of the impulse to another nerve fiber."
  },
  fetchWords: async function(letter, length) {
    try {
      const pattern = letter.toLowerCase() + "?".repeat(length - 1);
      const res = await fetch(`https://api.datamuse.com/words?sp=${pattern}&topics=science&max=100`);
      let words = await res.json();
      words = words.filter(w => /^[a-zA-Z]+$/.test(w.word)).sort(() => 0.5 - Math.random());
      
      if(words.length > 0) return words.slice(0, 20).map(w => w.word);
      throw new Error("No words");
    } catch {
      let matched = Object.keys(this.fallback).filter(w => w.startsWith(letter.toLowerCase()) && w.length === length);
      if(matched.length < 5) matched = matched.concat(Object.keys(this.fallback).filter(w => w.startsWith(letter.toLowerCase())));
      if(matched.length < 15) matched = matched.concat(Object.keys(this.fallback));
      return [...new Set(matched)].slice(0, 20).sort(() => 0.5 - Math.random());
    }
  },
  fetchMeaning: async function(word) {
    try {
      if(this.fallback[word.toLowerCase()]) return this.fallback[word.toLowerCase()];
      const res = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${word}`);
      const data = await res.json();
      for(let entry of data) for(let meaning of entry.meanings) for(let def of meaning.definitions) if(def.definition) return def.definition;
      throw new Error("No meaning");
    } catch {
      return "A highly specialized scientific term or biological construct heavily studied in standard academic fields.";
    }
  }
};

function initModal() {
  const overlay = document.createElement('div');
  overlay.id = 'modal-overlay';
  overlay.className = 'hidden';
  overlay.innerHTML = `
    <div class="card modal-card" style="max-width: 400px; margin: auto;">
      <h3 id="modal-title">Notice</h3>
      <p id="modal-text"></p>
      <button id="modal-close-btn" class="classic-btn" style="margin-top:20px;">Close</button>
    </div>
  `;
  document.body.appendChild(overlay);
  
  document.getElementById('modal-close-btn').addEventListener('click', () => {
    overlay.classList.add('hidden');
  });
  
  window.showModal = function(title, text) {
    document.getElementById('modal-title').textContent = title;
    document.getElementById('modal-text').textContent = text;
    overlay.classList.remove('hidden');
  }
}

// MULTIPLAYER DYNAMIC INJECTION
const mpRoom = sessionStorage.getItem('mp_room');
const noInjectPages = ['index.html', 'home.html', 'multiplayer-setup.html'];
const isExcluded = noInjectPages.some(p => window.location.pathname.includes(p));

if (mpRoom && !isExcluded) {
  const socketScript = document.createElement('script');
  socketScript.src = "http://localhost:3000/socket.io/socket.io.js";
  socketScript.onload = () => {
    const mpScript = document.createElement('script');
    mpScript.src = "multiplayer.js";
    document.body.appendChild(mpScript);
  };
  document.head.appendChild(socketScript);
}
