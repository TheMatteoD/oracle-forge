from scripts.oracle.yes_no import oracle_yes_no
from scripts.oracle.meanings import load_meaning_tables, roll_meaning
from scripts.oracle.scene_test import scene_test
from scripts.llm.flavoring import narrate_event_interrupt, narrate_keywords, narrate_yesno

def handle_yes_no(question, odds="50/50", chaos=5):
    return oracle_yes_no(question, odds, chaos)

def handle_yesno_flavor(question, outcome, event_trigger):
    narration = narrate_yesno(question=question, result=outcome)
    if event_trigger:
        narration += "\n\nThere was an interruption! Generate event flavor with the meaning oracle?"
    return narration

def handle_scene_test(chaos=5, flavor=False):
    result = scene_test(chaos, flavor)
    return result

def handle_scene_flavor(focus, expectation):
    return narrate_event_interrupt(focus, expectation)

def handle_meaning(question, table=None):
    tables = load_meaning_tables(table)
    return roll_meaning(tables)

def handle_meaning_flavor(question, keywords):
    return narrate_keywords(question=question, keywords=keywords)

