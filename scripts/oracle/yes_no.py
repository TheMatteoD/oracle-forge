from scripts.utils.dice import d100

fate_chart = {
    "Impossible":         [(1, 1, 81), (1, 1, 81), (1, 1, 81), (1, 5, 82), (2, 10, 83), (3, 15, 84), (5, 25, 86), (7, 35, 88), (10, 50, 91)],
    "Nearly Impossible":  [(1, 1, 81), (1, 1, 81), (1, 5, 82), (2, 10, 83), (3, 15, 84), (5, 25, 86), (6, 35, 88), (8, 50, 91), (10, 65, 94)],
    "Very Unlikely":      [(1, 5, 82), (2, 10, 83), (3, 15, 84), (5, 25, 86), (7, 35, 88), (8, 50, 91), (10, 65, 94), (13, 65, 94), (15, 75, 96)],
    "Unlikely":           [(2, 10, 83), (3, 15, 84), (5, 25, 86), (7, 35, 88), (10, 50, 91), (13, 65, 94), (15, 75, 96), (17, 85, 98), (18, 90, 99)],
    "50/50":              [(2, 10, 83), (3, 15, 84), (5, 25, 86), (7, 35, 88), (10, 50, 91), (13, 65, 94), (15, 75, 96), (17, 85, 98), (18, 90, 99)],
    "Likely":             [(3, 15, 84), (5, 25, 86), (7, 35, 88), (10, 50, 91), (13, 65, 94), (15, 75, 96), (17, 85, 98), (18, 90, 99), (19, 95, 100)],
    "Very Likely":        [(5, 25, 86), (7, 35, 88), (10, 50, 91), (13, 65, 94), (15, 75, 96), (17, 85, 98), (18, 90, 99), (19, 95, 100), (20, 99, 'x')],
    "Nearly Certain":     [(7, 35, 88), (10, 50, 91), (13, 65, 94), (15, 75, 96), (17, 85, 98), (18, 90, 99), (19, 95, 100), (20, 99, 'x'), (20, 99, 'x')],
    "Certain":            [(10, 50, 91), (13, 65, 94), (15, 75, 96), (17, 85, 98), (18, 90, 99), (19, 95, 100), (20, 99, 'x'), (20, 99, 'x'), (20, 99, 'x')],
}


def oracle_yes_no(question, odds="50/50", chaos=5):
    if odds not in fate_chart:
        raise ValueError(f"Unknown odds: {odds}")

    roll = d100()

    left, center, right = fate_chart[odds][chaos - 1]
    right = 101 if right == 'x' else right


    if roll <= left:
        result = "Exceptional Yes"
    elif roll <= center:
        result = "Yes"
    elif roll >= right:
        result = "Exceptional No"
    else:
        result = "No"

    # Doubles (11, 22, 33, ..., 99) trigger Random Event if <= chaos * 11
    is_double = (roll % 11 == 0)
    event_trigger = is_double and roll <= (chaos * 11)
    
    return {
        "question": question,
        "odds": odds,
        "chaos": chaos,
        "roll": roll,
        "result": result,
        "event_trigger": ">> Random Event Triggered!" if event_trigger else ""
    }

