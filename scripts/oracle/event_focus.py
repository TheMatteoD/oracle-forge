from scripts.utils.table_parser import load_yaml, roll_on_table

def load_event_focus(path="vault/tables/oracle/event_focus.yaml"):
    data = load_yaml(path)
    return data[0]["table"]

def resolve_event_focus(table):
    # Instead of returning only .get("result"), return the full matched dict
    import random
    roll = random.randint(1, 100)
    for entry in table:
        start, end = entry["range"][0], entry["range"][-1]
        if start <= roll <= end:
            return {
                "roll": roll,
                "result": entry["result"],
                "description": entry.get("description", "")
            }
    return {"roll": roll, "result": "Unknown", "description": ""}

