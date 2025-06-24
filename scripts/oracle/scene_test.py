from scripts.utils.dice import d10
from scripts.oracle.event_focus import load_event_focus, resolve_event_focus

def scene_test(chaos, flavor=True):
    roll = d10()
    if roll > chaos:
        return {
            "roll": roll,
            "chaos": chaos,
            "result": "Normal Scene",
            "narration": None if flavor else "Scene proceeds as expected."
        }

    scene_type = "Interrupt Scene" if roll % 2 == 0 else "Altered Scene"
    result = {
        "roll": roll,
        "chaos": chaos,
        "result": scene_type
    }
    
    if scene_type == "Interrupt Scene":
        focus_table = load_event_focus()
        focus = resolve_event_focus(focus_table)
        result["event_focus"] = focus

    if scene_type == "Interrupt Scene" and not flavor:
        result["narration"] = "Scene was interrupted! Generate random event flavor?"
    elif scene_type == "Altered Scene" and not flavor:
        result["narration"] = "Scene is altered. Generate a twist or detail?"

    return result

