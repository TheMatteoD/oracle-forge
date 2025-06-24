import os
from scripts.utils.table_parser import roll_from_yaml
from . import room, corridor

YAML_PATH = os.path.join("vault", "tables", "generators", "dungeons", "sandbox_gen_dungeons.yaml")

def generate():
    return {
        "start_room": room.generate(),
        "first_corridor": corridor.generate(),
        "branch_room": room.generate()
    }


def roll(table_id):
    return roll_from_yaml(YAML_PATH, table_id)
