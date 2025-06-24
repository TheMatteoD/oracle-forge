from flask import Blueprint, request, jsonify
from scripts.oracle.oracle_driver import (
    handle_yes_no,
    handle_meaning,
    handle_scene_test,
    handle_yesno_flavor,
    handle_meaning_flavor,
    handle_scene_flavor
)

oracle = Blueprint('oracle', __name__)

@oracle.route("/oracle/yesno", methods=["POST"])
def oracle_yesno():
    data = request.get_json()
    result = handle_yes_no(
        question=data.get("question", ""),
        odds=data.get("odds", "50/50"),
        chaos=int(data.get("chaos", 5))
    )
    return jsonify(result)

@oracle.route("/oracle/yesno/flavor", methods=["POST"])
def oracle_yesno_flavor():
    data = request.get_json()
    narration = handle_yesno_flavor(
        question=data.get("question", ""),
        outcome=data.get("result", ""),
        event_trigger=data.get("event_trigger", "")
    )
    return jsonify({"narration": narration})

@oracle.route("/oracle/scene", methods=["POST"])
def oracle_scene():
    data = request.get_json()
    result = handle_scene_test(
        chaos=int(data.get("chaos", 5)),
        flavor=bool(data.get("flavor", False))
    )
    return jsonify(result)

@oracle.route("/oracle/scene/flavor", methods=["POST"])
def oracle_scene_flavor():
    data = request.get_json()
    narration = handle_scene_flavor(
        focus=data.get("focus", ""),
        expectation=data.get("expectation", "")
    )
    return jsonify({"narration": narration})

@oracle.route("/oracle/meaning", methods=["POST"])
def oracle_meaning():
    data = request.get_json()
    result = handle_meaning(
        question=data.get("question", ""),
        table=data.get("table")
    )
    return jsonify(result)

@oracle.route("/oracle/meaning/flavor", methods=["POST"])
def oracle_meaning_flavor():
    data = request.get_json()
    narration = handle_meaning_flavor(
        question=data.get("question", ""),
        keywords=data.get("keywords", [])
    )
    return jsonify({"narration": narration})

@oracle.route("/oracle/meaning/tables", methods=["GET"])
def oracle_meaning_tables():
    import os
    directory = "vault/tables/oracle"
    tables = [
        f for f in os.listdir(directory)
        if f.endswith(".yaml") and not f.startswith("_")
    ]
    return jsonify(tables)
