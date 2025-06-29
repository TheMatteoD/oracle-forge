from flask import Blueprint, request, g
import logging
from ..services.oracle import OracleService
from ..utils.responses import APIResponse, handle_service_response
from ..utils.validation import validate_json_body, validate_field

oracle = Blueprint('oracle', __name__)
oracle_service = OracleService()
logger = logging.getLogger(__name__)

@oracle.route("/oracle/yesno", methods=["POST"])
@validate_json_body(required_fields=["question"])
@validate_field("chaos", field_type=int, min_value=1, max_value=9, allow_none=True)
@validate_field("odds", allowed_values=["50/50", "likely", "unlikely"], allow_none=True)
def oracle_yesno():
    """Oracle Yes/No query endpoint"""
    data = g.request_data
    
    question = data.get("question", "").strip()
    odds = data.get("odds", "50/50")
    chaos = data.get("chaos", 5)
    
    # Call service
    result = oracle_service.yes_no_query(question=question, odds=odds, chaos=chaos)
    return handle_service_response(result, "result")

@oracle.route("/oracle/yesno/flavor", methods=["POST"])
@validate_json_body(required_fields=["question", "result"])
def oracle_yesno_flavor():
    """Oracle Yes/No flavor narration endpoint"""
    data = g.request_data
    
    question = data.get("question", "").strip()
    outcome = data.get("result", "").strip()
    event_trigger = data.get("event_trigger", "").strip()
    
    # Call service
    result = oracle_service.yes_no_narration(
        question=question, 
        outcome=outcome, 
        event_trigger=event_trigger
    )
    return handle_service_response(result, "narration")

@oracle.route("/oracle/scene", methods=["POST"])
@validate_field("chaos", field_type=int, min_value=1, max_value=9, allow_none=True)
@validate_field("flavor", field_type=bool, allow_none=True)
def oracle_scene():
    """Oracle Scene test endpoint"""
    data = g.request_data or {}
    
    chaos = data.get("chaos", 5)
    flavor = data.get("flavor", False)
    
    # Call service
    result = oracle_service.scene_test(chaos=chaos, flavor=flavor)
    return handle_service_response(result, "result")

@oracle.route("/oracle/scene/flavor", methods=["POST"])
@validate_json_body(required_fields=["focus"])
def oracle_scene_flavor():
    """Oracle Scene flavor narration endpoint"""
    data = g.request_data
    
    focus = data.get("focus", "").strip()
    expectation = data.get("expectation", "").strip()
    
    # Call service
    result = oracle_service.scene_narration(focus=focus, expectation=expectation)
    return handle_service_response(result, "narration")

@oracle.route("/oracle/meaning", methods=["POST"])
@validate_json_body(required_fields=["question", "table"])
def oracle_meaning():
    """Oracle Meaning query endpoint"""
    data = g.request_data
    
    question = data.get("question", "").strip()
    table = data.get("table", "").strip()
    
    # Call service
    result = oracle_service.meaning_query(question=question, table=table)
    return handle_service_response(result, "result")

@oracle.route("/oracle/meaning/flavor", methods=["POST"])
@validate_json_body(required_fields=["question", "keywords"])
@validate_field("keywords", field_type=list, allow_none=False)
def oracle_meaning_flavor():
    """Oracle Meaning flavor narration endpoint"""
    data = g.request_data
    
    question = data.get("question", "").strip()
    keywords = data.get("keywords", [])
    
    # Call service
    result = oracle_service.meaning_narration(question=question, keywords=keywords)
    return handle_service_response(result, "narration")

@oracle.route("/oracle/meaning/tables", methods=["GET"])
def oracle_meaning_tables():
    """List available oracle meaning tables"""
    # Call service
    result = oracle_service.list_oracle_tables()
    return handle_service_response(result, "tables")
