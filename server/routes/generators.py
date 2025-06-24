import os
import pathlib
from flask import Blueprint, request, jsonify
from scripts.generators import generator_driver
from scripts.llm.flavoring import narrate_generation
from scripts.generators.registry import CUSTOM_GENERATORS
import importlib

GENERATORS_ROOT = os.path.join("vault", "tables", "generators")


generators = Blueprint("generators", __name__)


@generators.route("/generators/categories", methods=["GET"])
def list_categories():
    categories = [
        d for d in os.listdir(GENERATORS_ROOT)
        if os.path.isdir(os.path.join(GENERATORS_ROOT, d))
    ]
    return jsonify(categories)


@generators.route("/generators/<category>/files", methods=["GET"])
def list_files(category):
    dir_path = os.path.join(GENERATORS_ROOT, category)
    if not os.path.exists(dir_path):
        return jsonify({"error": "Category not found"}), 404

    files = [f for f in os.listdir(dir_path) if f.endswith(".yaml")]
    return jsonify(files)


@generators.route("/generators/<category>/<filename>/tables", methods=["GET"])
def list_tables(category, filename):
    file_path = os.path.join(GENERATORS_ROOT, category, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    try:
        table_ids = generator_driver.list_table_ids(file_path)
        return jsonify(table_ids)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@generators.route("/generators/custom", methods=["GET"])
def list_custom_generators():
    output = {}
    for category, systems in CUSTOM_GENERATORS.items():
        output[category] = {}
        for system_name, system_data in systems.items():
            output[category][system_name] = {
                "label": system_data["label"],
                "generators": [
                    {"id": gen_id, "label": gen_data["label"]}
                    for gen_id, gen_data in system_data["generators"].items()
                ]
            }
    return jsonify(output)

@generators.route("/generators/custom/<category>/<system>/<generator_id>", methods=["POST"])
def run_custom_generator(category, system, generator_id):
    try:
        system_data = CUSTOM_GENERATORS[category][system]
        gen_entry = system_data["generators"][generator_id]
        module_path, func_name = gen_entry["function"].rsplit(".", 1)
        module = importlib.import_module(module_path)
        func = getattr(module, func_name)
        return jsonify(func())
    except KeyError:
        return jsonify({"error": "Generator not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@generators.route("/generators/roll", methods=["POST"])
def roll_table():
    data = request.get_json()
    category = data.get("category")
    filename = data.get("file")
    table_id = data.get("table_id")

    file_path = os.path.join(GENERATORS_ROOT, category, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    try:
        result = generator_driver.roll_from_yaml(file_path, table_id)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@generators.route("/generators/flavor", methods=["POST"])
def generate_flavor():
    data = request.get_json()
    result = narrate_generation(
        context=data.get("context", ""),
        data=data.get("data", {}),
        category=data.get("category", ""),
        source=data.get("source", "")
    )
    return jsonify({"narration": result})