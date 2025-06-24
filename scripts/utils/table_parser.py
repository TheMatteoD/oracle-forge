import yaml
import random

def load_yaml(path):
    """Load any YAML file and return its parsed object."""
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def roll_dice(dice_str):
    """Roll dice from notation like 'd6', '2d8', or 'd100'."""
    if dice_str.startswith('d'):
        count, sides = 1, int(dice_str[1:])
    else:
        parts = dice_str.lower().split('d')
        count, sides = int(parts[0]), int(parts[1])
    return sum(random.randint(1, sides) for _ in range(count))

def get_table_by_id(data, table_id):
    """Retrieve a specific table from parsed YAML using its 'id' field."""
    tables = data.get('tables', [])
    for table in tables:
        if table.get('id') == table_id:
            return table
    return None

def roll_on_table(table, return_entry=False):
    """Roll on a specific table and return result or full entry."""
    dice = table.get('dice', 'd6')
    roll = roll_dice(dice)
    entries = table.get('entries', [])

    for entry in entries:
        if isinstance(entry, dict) and 'range' in entry:
            start, end = entry['range'][0], entry['range'][-1]
            if start <= roll <= end:
                return entry if return_entry else entry['result']
    return None

def roll_from_yaml(path, table_id, return_entry=False):
    """Load a YAML, retrieve a table by ID, and roll on it."""
    data = load_yaml(path)
    table = get_table_by_id(data, table_id)
    if not table:
        raise ValueError(f"Table with id '{table_id}' not found.")
    return roll_on_table(table, return_entry)
