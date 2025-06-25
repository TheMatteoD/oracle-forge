import os
import yaml

BASE_PATH = os.path.join("vault", "adventures")

def load_yaml(path):
    if not os.path.exists(path): return {}
    with open(path, "r") as f:
        return yaml.safe_load(f) or {}

def merge_custom_fields(data):
    if "custom_fields" in data and isinstance(data["custom_fields"], dict):
        for k, v in data["custom_fields"].items():
            if k not in data:
                data[k] = v
        del data["custom_fields"]
    return data

def build_adventure_context(adventure_name):
    base = os.path.join(BASE_PATH, adventure_name)

    # Core files
    world_state = load_yaml(os.path.join(base, "world_state.yaml"))
    player_index = load_yaml(os.path.join(base, "player_states.yaml"))
    session_data = load_yaml(os.path.join(base, "active_session.yaml"))

    # Expand player details
    players = []
    for filename in player_index.get("players", []):
        path = os.path.join(base, "players", filename)
        data = load_yaml(path)
        players.append(merge_custom_fields(data))

    # Expand world references
    def load_entity(folder):
        path = os.path.join(base, "world", folder)
        if not os.path.exists(path): return {}
        return {
            os.path.splitext(f)[0]: merge_custom_fields(load_yaml(os.path.join(path, f)))
            for f in os.listdir(path) if f.endswith(".yaml")
        }

    npcs = load_entity("npcs")
    factions = load_entity("factions")
    locations = load_entity("locations")
    story_lines = load_entity("story_lines")

    return {
        "session": session_data,
        "world": world_state,
        "players": players,
        "npcs": npcs,
        "factions": factions,
        "locations": locations,
        "story_lines": story_lines
    }
