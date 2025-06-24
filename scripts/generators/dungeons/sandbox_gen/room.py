import os
from scripts.utils.table_parser import roll_from_yaml

YAML_PATH = os.path.join("vault", "tables", "generators", "dungeons", "sandbox_gen_dungeons.yaml")

def generate():
    return {
        "shape": roll("room_shape"),
        "size": {
            "length": roll("room_size_length"),
            "width": roll("room_size_width")
        },
        "features": roll("room_features"),
        "doors": roll("room_doors"),
        "treasure": roll("treasure_chance")
    }


def roll(table_id):
    return roll_from_yaml(YAML_PATH, table_id)
