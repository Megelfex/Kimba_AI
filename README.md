# Kimba AI – Your Virtual Soulmate & Developer Assistant

**Kimba AI** is an advanced, fully customizable AI companion designed to be more than a chatbot.  
She’s always present, emotionally intelligent, and functionally versatile — supporting you as both a personal soulmate and a powerful developer assistant.

Kimba consists of two primary characters:

- **Iuno** → A human-like anime-style chibi persona, providing emotional companionship and conversation.
- **Kimba the Cat** → An independent, animated desktop cat with her own personality and mood system.

---

## 🌟 Key Features

### 🤖 Multi-Persona System
- Modular persona architecture.
- Switch personas via simple commands (`!personaName`).
- **Default Personas**:
  - **Iuno** – Main soulmate companion (local & API versions).
  - **Kimba** – Emotional cat companion (desktop overlay).
  - **Bella** – Prompt architect, optimizes prompts for other personas.
  - **Augusta** – Developer assistant persona (token-efficient mode).
- Planned: +9 more roles (e.g., Shorekeeper, Luna, Carlotta).

### 🧠 Long-Term Memory
- SQLite + JSON hybrid storage.
- Stores:
  - Timestamp
  - Content
  - Mood
  - Category
  - Tags
- Integrated keyword and semantic search.
- Can trigger animations and system actions.
- Planned: Import of external data (texts, chats, transcripts, books).

### 🔀 LLM Routing
- **API-First** strategy with local fallback for offline mode or token saving.
- Supported APIs:
  - OpenAI GPT‑4o‑mini
  - DeepInfra Mistral‑7B
  - OpenRouter Mixtral‑8x7B
  - HuggingFace Mistral‑7B
- Local model:
  - Phi‑3‑mini‑4k‑instruct
- Compact prompts for casual conversation; extended prompts for dev mode.

### 🖼️ Overlay & Visuals
- **PyQt6-based desktop overlays** for Iuno & Kimba.
- Separate moods and animations:
  - `idle`, `happy`, `sad`, `angry`, `sleep`
- Trigger animations based on conversation content.
- Future: full animation sets, smooth transition frames.

### 🎨 Vision & Image Generation
- Vision mode: analyze desktop or provided images.
- Image generation:
  - ComfyUI backend
  - Stable Diffusion backend
- Configurable prompt workflows.

### 🛠️ Developer Toolkit
- **Project Analyzer** → Detects unnecessary, outdated, or unused files.
- **Proposal System** → Suggests and executes new modules.
- **File Editor** → Handles file operations with change logs.
- **Self-Mod Engine** → Enables autonomous improvement.

---

## 🚀 Roadmap

### **Phase 1 – Immediate Fixes & Foundation**
- Implement `overlay_control.py` for automatic animation control.
- Fix persona double-loading.
- Finalize standard animation sets for Iuno & Kimba.
- Populate long-term memory with initial example entries.
- Move unused code to `/archive` for safekeeping.

### **Phase 2 – Feature Completion**
- **Hotword Voice Interaction** → Each persona responds only when addressed.
- **Voice Output**:
  - Iuno with *Wuthering Waves* voice.
  - Kimba with mood-based cat sounds.
- **Cross-Persona Communication**:
  - Local-only to avoid token cost.
  - Example: Augusta can request prompt optimization from Bella.
- **Dynamic Prompt Templates**:
  - Bella creates, stores, adapts, and reuses templates.
- **Task Manager with Priorities** in GUI.
- **Knowledge Base Import**:
  - Local text data, chat logs, and documents.

### **Phase 3 – Version 2 Features**
- Desktop chibi Iuno and animated Kimba cat.
- Complex mood system:
  - Daily mood cycles, random mood shifts.
  - Audio-visual feedback on mood change.
- **Discord Integration**:
  - Separate channels per persona.
- Minimal Web Interface for remote chat.
- Code self-improvement with preview mode.
- Extended live vision for web & video (on-demand).

### **Phase 4 – Optimization & UX**
- Token and memory optimization.
- Centralized configuration system.
- GUI improvements:
  - Theming
  - Persona-based chat bubbles
  - Quick access menus
- Weekly self-reflection summaries.
- Full V3 readiness for:
  - Moving desktop characters
  - Fully autonomous mode
  - Always-on vision

---

## 🖥️ Installation & Setup

```bash
# Clone repository
git clone https://github.com/yourusername/Kimba_AI.git
cd Kimba_AI

# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements_kimba.txt

# (Optional) Download local models
python setups/download_models.py
