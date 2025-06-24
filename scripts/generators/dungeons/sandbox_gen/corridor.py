import os
from scripts.utils.table_parser import roll_from_yaml

YAML_PATH = os.path.join("vault", "tables", "generators", "dungeons", "sandbox_gen_dungeons.yaml")

def generate():
    return {
        "length": roll("corridor_length"),
        "feature": roll("corridor_features"),
        "feature_location": roll("corridor_feature_location"),
        "end": roll("corridor_end")
    }


def roll(table_id):
    return roll_from_yaml(YAML_PATH, table_id)
