# Neuromorphic Artificial Insect — SNN with STDP in a Pygame World 🐜🧠

A Python neuromorphic prototype where a virtual insect explores a 2D environment to find food.  
Behavior emerges from a **Spiking Neural Network (SNN)** with **STDP synaptic plasticity**: eight directional “olfactory” sensors modulate motor neurons, and through repeated trials the agent refines its foraging strategy. A **Pygame** interface provides real-time visualization of movement, spikes, and learning dynamics.

---

## ✨ Key Features
- **Brian2 SNN core** with event-driven STDP and tunable parameters.  
- **Eight directional sensory channels** (olfaction) → motor command mapping.  
- **Autonomous navigation** in a noisy 2D world; agent learns efficient trajectories to food.  
- **Real-time GUI** (Pygame): world state, agent pose, and optional diagnostics.  
- **Learning analytics**: spike activity, synaptic weight trends, and behavior evolution.  

---

## 🧩 Architecture (Conceptual)
- **Sensors:** 8 olfactory rays sampling food intensity; signals encoded as Poisson rates.  
- **Processing:** Spiking interneurons with **STDP** adjust input→motor synapses online.  
- **Motor Layer:** Left/Right (or multi-directional) neurons compete to set velocity/turn.  
- **Feedback:** Reward linked to proximity/consumption events; weights adapt continually.  

---

## 🎯 What This Demonstrates
- Emergent behavior from **local learning rules** (no backprop, no labels).  
- **Embodied intelligence**: sensing → spiking → action → new sensory state → learning.  
- A clean sandbox for testing **neuromorphic control** and **sensorimotor loops**.

---

## 🔧 Configurable Elements
- STDP constants (A_plus, A_minus, τ), weight caps, and learning windows.  
- Sensor geometry (ray count, spread, range) and environment noise.  
- Motor mapping (from spiking rates to linear/ang. velocity) and reward shaping.  

---

## 📊 Visualization & Metrics
- Spike raster and firing summaries over learning episodes.  
- Synaptic weight trajectories highlighting which inputs drive actions.  
- Behavioral improvements (time-to-food, path efficiency) across trials.  

---

## 🗺️ Roadmap
- Optional **eligibility traces** and **neuromodulator-gated plasticity**.  
- Obstacles, distractors, and multi-food tasks.  
- Curriculum learning (progressively harder mazes).  
- Exportable logs for offline analysis (CSV/Parquet).  

---

## 📚 Citation
If this project helps your research or teaching, you can cite it like this:

> Matteini, F. *Neuromorphic Artificial Insect — SNN with STDP (Brian2 + Pygame).* 2025.  

---

## 👤 Author & Contacts
**Filippo Matteini** — Pianist, AI Engineer, Neuromorphic Computing (Independent Researcher)  

- 🎹 YouTube (Dexteris): [@dexteris27](https://www.youtube.com/@dexteris27)  
- 💼 LinkedIn: [Filippo Matteini](https://www.linkedin.com/in/filippo-matteini-29554a355)  
- 🖥️ GitHub: [Fil952701](https://github.com/Fil952701)

---

## 📝 License
MIT License — free to use, modify, and build upon with attribution.

---

## 🔖 Hashtags
#NeuromorphicComputing #SpikingNeuralNetworks #STDP #Brian2 #Pygame #ReinforcementLearning #EmbodiedAI #ComputationalNeuroscience #BioInspiredAI #Python 🐍
