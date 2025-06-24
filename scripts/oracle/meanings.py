import os
from scripts.utils.table_parser import load_yaml
from scripts.utils.dice import d100

def load_meaning_tables(selected_file=None, directory="vault/tables/oracle/"):
    tables = []

    # Load specific file if requested
    if selected_file:
        path = os.path.join(directory, selected_file)
        if os.path.exists(path):
            data = load_yaml(path)
            if isinstance(data, list):
                tables.extend(data)
            elif isinstance(data, dict):
                tables.append(data)
        return tables

    # Otherwise, load all valid YAMLs
    for filename in os.listdir(directory):
        if filename.endswith(".yaml") and not filename.startswith("_"):
            path = os.path.join(directory, filename)
            data = load_yaml(path)
            if isinstance(data, list):
                tables.extend(data)
            elif isinstance(data, dict):
                tables.append(data)
    return tables


def roll_meaning(meanings):
    if not meanings:
        raise ValueError("No valid meaning tables loaded.")

    roll1 = d100()
    roll2 = d100()

    table1 = meanings[0]["table"]
    table2 = meanings[1]["table"] if len(meanings) > 1 else table1

    def find_result(table, roll):
        for entry in table:
            rng = entry["range"]
            if isinstance(rng, list):
                if rng[0] <= roll <= rng[-1]:
                    return entry["result"]
            elif isinstance(rng, int):
                if rng == roll:
                    return entry["result"]
        raise ValueError(f"No matching entry for roll {roll}")

    word1 = find_result(table1, roll1)
    word2 = find_result(table2, roll2)

    return {
        "keywords": [word1, word2],
        "rolls": (roll1, roll2)
    }


