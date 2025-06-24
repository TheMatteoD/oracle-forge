import os
from scripts.utils.table_parser import load_yaml as raw_load_yaml, get_table_by_id, roll_on_table


def load_yaml(path):
    """Wrap load_yaml to normalize path and do a basic existence check."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"YAML not found: {path}")
    return raw_load_yaml(path)


def list_table_ids(path):
    """Return a list of table IDs from a generator YAML."""
    data = load_yaml(path)
    return [t.get("id") for t in data.get("tables", []) if "id" in t]


def roll_from_yaml(path, table_id, return_entry=False):
    """Roll on a given table ID from a YAML file."""
    data = load_yaml(path)
    table = get_table_by_id(data, table_id)
    if not table:
        raise ValueError(f"Table with id '{table_id}' not found in {path}.")
    return roll_on_table(table, return_entry)


def get_all_tables(path):
    """Return full table definitions from a YAML file."""
    data = load_yaml(path)
    return data.get("tables", [])
