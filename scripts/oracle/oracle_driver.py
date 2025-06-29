from scripts.oracle.yes_no import oracle_yes_no
from scripts.oracle.meanings import load_meaning_tables, roll_meaning
from scripts.oracle.scene_test import scene_test
from scripts.llm.flavoring import narrate_event_interrupt, narrate_keywords, narrate_yesno
from scripts.adventure.context_builder import build_adventure_context
from server.services.session import SessionService

# Create a service instance for use in this module
_session_service = SessionService()

def handle_yes_no(question, odds="50/50", chaos=5):
    return oracle_yes_no(question, odds, chaos)

def handle_yesno_flavor(question, outcome, event_trigger):
    adv = _session_service.get_active_adventure()
    context = build_adventure_context(adv) if adv else None
    narration = narrate_yesno(question=question, result=outcome, context=context)
    if event_trigger:
        narration += "\n\nThere was an interruption! Generate event flavor with the meaning oracle?"
    return narration

def handle_scene_test(chaos=5, flavor=False):
    result = scene_test(chaos, flavor)
    return result

def handle_scene_flavor(focus, expectation):
    adv = _session_service.get_active_adventure()
    context = build_adventure_context(adv) if adv else None
    narration = narrate_event_interrupt(focus, expectation, context=context)
    return narration

def handle_meaning(question, table=None):
    tables = load_meaning_tables(table)
    return roll_meaning(tables)

def handle_meaning_flavor(question, keywords):
    adv = _session_service.get_active_adventure()
    context = build_adventure_context(adv) if adv else None
    narration = narrate_keywords(question=question, keywords=keywords, context=context)
    return narration

