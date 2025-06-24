# 🧙‍♂️ Oracle Forge

Oracle Forge is an offline, locally-hosted AI-powered assistant for solo tabletop role-playing games. It combines the improvisational style of Mythic GME 2e with the mechanics of Old-School Essentials (OSE) and a suite of hand-crafted content generators to facilitate dynamic, unscripted adventures.

The application runs as a local web server, providing a responsive user interface for interacting with its various tools without needing an internet connection.

### Development Status

> **Note:** This project is currently in a rapid prototyping phase.
>
> Core features are being actively developed, refined, and sometimes reworked. While the application is functional, the user interface is designed for utility over aesthetics at this stage. The UI/UX is a critical part of the long-term vision but will receive a dedicated focus once the backend functionality is more solidified.

## ✨ Key Features

*   **Mythic-Style Oracles**: Core tools for solo play, including Yes/No questions, scene resolution, and meaning generation, all enhanced with narrative flavor from a local LLM.
*   **Content Lookups**: Quickly search for rules, monster statistics, and spell descriptions from your own curated content vaults.
*   **Pluggable Content Generators**: A flexible system for creating and using custom content generators. Simply add a YAML file to your vault, and it becomes available in the UI.
*   **World-Building Tools**: Integrated with the [Azgaar's Fantasy Map Generator](https://azgaar.github.io/Fantasy-Map-Generator/) for rich, visual world exploration.
*   **100% Offline & Local**: Your data and session logs never leave your machine. The entire application, including the AI model, runs locally.
*   **Modular Architecture**: Built with a Flask backend and React frontend, ensuring a clean separation of concerns and easy extensibility.

## 🛠️ Tech Stack

*   **Backend**: Python, Flask
*   **Frontend**: React, Vite, CSS Modules
*   **AI**: Local LLM integration via [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
*   **Data**: Content is managed through simple YAML and Markdown files.

---

## 🚀 Getting Started

To get Oracle Forge running on your local machine, you will need to set up the backend server, the frontend interface, and configure the application to use your own local LLM and content vault.

### Prerequisites

*   [Python 3.10+](https://www.python.org/)
*   [Node.js and npm](https://nodejs.org/en/)
*   A local LLM in GGUF format (e.g., from [Hugging Face](https://huggingface.co/models?search=gguf))
*   Git

### 1. Installation

First, clone the repository to your local machine:
```bash
git clone <your-repo-url>
cd oracle-forge
```

**Backend Setup:**
```bash
# It is recommended to use a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`

# Install Python dependencies
pip install Flask flask-cors llama-cpp-python
```

**Frontend Setup:**
```bash
cd oracle-forge-ui
npm install
```

### 2. Configuration

Oracle Forge requires a `config/settings.yaml` file and a `vault/` directory at the project root. These are ignored by Git to keep your personal data private.

**Create `config/settings.yaml`:**
Create a file named `settings.yaml` inside a `config` directory. This file tells the application where to find your LLM and sets other parameters.

```yaml
# config/settings.yaml

# Path to your local LLM
model_path: /path/to/your/models/your-llm-v0.1.Q4_K_M.gguf

# The "chaos factor" for the Mythic oracle (1-6, 5 is default)
chaos_factor: 5

# Allowed origins for the frontend (update if your port is different)
cors_origins:
  - "http://localhost:5173"
```

**Set Up Your `vault/` Directory:**
The `vault/` directory is where all your game content (rules, monsters, tables) lives. **Due to the proprietary nature of the original source material, this repository does not include a pre-filled vault.** You will need to create it and populate it with your own data.

I plan to add a full set of example files to the repository in the future. For now, here is the required structure:

```
vault/
├── rules/
│   └── example_rule.md
├── tables/
│   ├── oracle/
│   │   └── example_table.yaml
│   ├── generators/
│   │   └── example_generator.yaml
│   └── monsters.yaml
│   └── spells.yaml
```

*   `rules/`: Contains game rules as Markdown files.
*   `tables/`: Contains YAML files for generators and lookup tables.
*   `monsters.yaml`: YAML file with a list of monster stats.
*   `spells.yaml`: YAML file with a list of spells.

You will need to source and create these files yourself for the application to be fully functional.

**Install Azgaar's Fantasy Map Generator:**
The integrated world map viewer uses [Azgaar's Fantasy Map Generator](https://github.com/Azgaar/Fantasy-Map-Generator). It is not included in this repository and must be installed manually.

1.  Download the project from the [Azgaar's Fantasy Map Generator GitHub page](https://github.com/Azgaar/Fantasy-Map-Generator). You can either clone the repository or download a ZIP archive.
2.  Place the entire project into a folder named `azgaar` inside the `server/` directory.
3.  Ensure the final path to the map generator's main file is `server/azgaar/index.html`.

### 3. Running the Application

1.  **Start the Backend Server:**
    From the project root, with your Python virtual environment activated:
    ```bash
    python main.py
    ```

2.  **Start the Frontend:**
    In a separate terminal, from the `oracle-forge-ui/` directory:
    ```bash
    npm run dev
    ```

You can now access Oracle Forge in your browser at `http://localhost:5173`.

---