import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm.llm_loader import get_llm

def log_to_session(content, session_type="lookup"):
    """Log content to the session log."""
    try:
        from server.state.session_manager import log_event
        log_event(session_type, content)
    except ImportError:
        print(f"Session logging not available: {content}")

def narrate_yesno(question, result, context=None, **kwargs):
    llm = get_llm()

    print("Context for LLM: ")
    print(context)

    prompt = f"""
You are the dungeon master in a fantasy TTRPG.
You're main objective is to narrate the answer to the player's question given the result. 
These are yes and no questions though the results you may be given are yes, no, exceptional yes, or exceptional no.
With a normal yes or no, you would be excpected to keep answers relatively short but provide some flavor and descriptors.
When there is an exceptional result the answer should take the yes and approach, or the no and approach, and add onto the result taking it a step further.
Question: {question}
Answer: {result}
Adventure context: {context}
"""
    response = llm(prompt, max_tokens=500)
    result_text = response["choices"][0]["text"].strip()
    
    # Log to session
    log_to_session(f"Oracle Question: {question}\nResult: {result}\nNarration: {result_text}", "oracle")
    
    return result_text

def narrate_event_interrupt(focus=None, expectation=None, context=None):
    llm = get_llm()
    prompt = f"""
You are the Dungeon Master for a game of Dungeons and Dragons.
Please paint a more colorful picture of the players expected scene without adding anything drastic.
If a Focus is added below than the scene is interuppted and use the focus as the catalyst for the interupting scene the players are now to deal with.
Give lots of details but stay true to the expectation or the new focus if given.
Focus: {focus}
Expectation: {expectation}
Context: {context}

"""
    response = llm(prompt, max_tokens=600)
    result_text = response["choices"][0]["text"].strip()
    
    # Log to session
    log_to_session(f"Event Interrupt - Focus: {focus}\nExpectation: {expectation}\nNarration: {result_text}", "oracle")
    
    return result_text


def narrate_keywords(question, keywords: list, context=None, **kwargs):
    llm = get_llm()

    keyword_str = ", ".join(keywords)

    print("Context for LLM: ")
    print(context)

    prompt = f"""
You are the dungeon master in a fantasy TTRPG.
You're main objective is to interpret the answer to the player's question given random keywords. 
The keywords them selves do not need used in your response but they should inspire the theme of the answer.
A player asked: \"{question}\"
And the oracle generated you these keywords: {keyword_str}. Feel free to use only one if they don't mend well or if one creates a strong narrative.

Keep your response just to answering the question but do so with flavor inspired by the keywords and any of the following context.
{context}
"""
    # response = llm(prompt, max_tokens=250, stop=["\n\n"])
    response = llm(prompt, max_tokens=300) 
    result_text = response["choices"][0]["text"].strip()
    
    # Log to session
    log_to_session(f"Keyword Question: {question}\nKeywords: {keyword_str}\nNarration: {result_text}", "oracle")
    
    return result_text

def narrate_generation(context: str, data: dict, category: str, source: str):
    """
    context: player-supplied intent
    data: generator output dict
    category: e.g. "dungeons"
    source: e.g. "sandbox_gen.room"
    """
    llm = get_llm()

    # Flatten dictionary nicely for prompt
    parts = [f"{k}: {v}" for k, v in data.items()]
    gen_text = "\n".join(parts)

    prompt = f"""
You are the dungeon master in a solo fantasy TTRPG.
The player has just generated some structured content for category "{category}", source "{source}".
The raw results are below, and the player added a context prompt as well.

Player's context: {context}

Generated data:
{gen_text}

Narrate a vivid, immersive, and flavorful version of this result that fits the category.
"""
    response = llm(prompt, max_tokens=500)
    result_text = response["choices"][0]["text"].strip()
    
    # Log to session
    log_to_session(f"Generation - Category: {category}\nContext: {context}\nData: {gen_text}\nNarration: {result_text}", "generator")
    
    return result_text

def narrate_items(items: list, context: str = None, environment: str = None, quality: str = None, theme: str = None, log_session: bool = True):
    """
    Narrate a list of items with LLM-based flavoring.
    
    Args:
        items: List of item dictionaries
        context: Player's context or intent
        environment: Environmental context (forest, desert, etc.)
        quality: Quality level (poor, average, superior, masterwork)
        theme: Thematic context (elven, dwarven, etc.)
        log_session: Whether to log to session (default True)
    """
    llm = get_llm()
    
    # Convert items to readable format
    items_text = []
    for item in items:
        item_desc = f"Name: {item.get('name', 'Unknown')}"
        if item.get('description'):
            item_desc += f"\nDescription: {item['description']}"
        if item.get('category'):
            item_desc += f"\nCategory: {item['category']}"
        if item.get('tags'):
            item_desc += f"\nTags: {', '.join(item['tags'])}"
        if item.get('damage'):
            item_desc += f"\nDamage: {item['damage']}"
        if item.get('damage_type'):
            item_desc += f"\nDamage Type: {item['damage_type']}"
        if item.get('armor_class'):
            item_desc += f"\nArmor Class: {item['armor_class']}"
        if item.get('weight'):
            item_desc += f"\nWeight: {item['weight']}"
        if item.get('cost'):
            item_desc += f"\nCost: {item['cost']}"
        if item.get('properties'):
            item_desc += f"\nProperties: {', '.join(item['properties'])}"
        if item.get('traits'):
            traits_str = []
            for trait in item["traits"]:
                if isinstance(trait, dict):
                    key, val = next(iter(trait.items()))
                    traits_str.append(f"{key}: {val}")
                else:
                    traits_str.append(str(trait))
            item_desc += f"\nTraits: {', '.join(traits_str)}"
        items_text.append(item_desc)
    
    items_str = "\n\n".join(items_text)
    
    # Build context string
    context_parts = []
    if context:
        context_parts.append(f"Player Context: {context}")
    if environment:
        context_parts.append(f"Environment: {environment}")
    if quality:
        context_parts.append(f"Quality: {quality}")
    if theme:
        context_parts.append(f"Theme: {theme}")
    
    context_str = "\n".join(context_parts) if context_parts else "No specific context provided"
    
    prompt = f"""
You are the dungeon master in a fantasy TTRPG.
The player has found or is looking at these items:

{items_str}

Context:
{context_str}

Please provide a vivid, immersive description of these items that incorporates the context provided. 
Make them feel unique and flavorful while staying true to their base properties.
If multiple items are provided, describe them as a cohesive set or collection when appropriate.
Keep descriptions concise but evocative.
"""
    
    response = llm(prompt, max_tokens=600)
    result_text = response["choices"][0]["text"].strip()
    
    # Log to session if requested
    if log_session:
        log_to_session(f"Item Lookup - Context: {context_str}\nItems: {items_str}\nNarration: {result_text}", "lookup")
    
    return result_text

def narrate_monsters(monsters: list, context: str = None, environment: str = None, theme: str = None, log_session: bool = True):
    """
    Narrate a list of monsters with LLM-based flavoring.
    
    Args:
        monsters: List of monster dictionaries
        context: Player's context or intent
        environment: Environmental context (forest, desert, etc.)
        theme: Thematic context (undead, demonic, etc.)
        log_session: Whether to log to session (default True)
    """
    llm = get_llm()
    
    # Convert monsters to readable format
    monsters_text = []
    for monster in monsters:
        monster_desc = f"Name: {monster.get('name', 'Unknown')}"
        if monster.get('description'):
            monster_desc += f"\nDescription: {monster['description']}"
        if monster.get('hit_dice'):
            monster_desc += f"\nHit Dice: {monster['hit_dice']}"
        if monster.get('armor_class'):
            monster_desc += f"\nArmor Class: {monster['armor_class']}"
        if monster.get('attacks'):
            monster_desc += f"\nAttacks: {monster['attacks']}"
        if monster.get('movement'):
            monster_desc += f"\nMovement: {monster['movement']}"
        if monster.get('tags'):
            monster_desc += f"\nTags: {', '.join(monster['tags'])}"
        if monster.get('traits'):
            traits_str = []
            for trait in monster["traits"]:
                if isinstance(trait, dict):
                    key, val = next(iter(trait.items()))
                    traits_str.append(f"{key}: {val}")
                else:
                    traits_str.append(str(trait))
            monster_desc += f"\nTraits: {', '.join(traits_str)}"
        monsters_text.append(monster_desc)
    
    monsters_str = "\n\n".join(monsters_text)
    
    # Build context string
    context_parts = []
    if context:
        context_parts.append(f"Player Context: {context}")
    if environment:
        context_parts.append(f"Environment: {environment}")
    if theme:
        context_parts.append(f"Theme: {theme}")
    
    context_str = "\n".join(context_parts) if context_parts else "No specific context provided"
    
    prompt = f"""
You are the dungeon master in a fantasy TTRPG.
The player has encountered or is looking at these monsters:

{monsters_str}

Context:
{context_str}

Please provide a vivid, immersive description of these monsters that incorporates the context provided.
Make them feel unique and threatening while staying true to their base stats and abilities.
If multiple monsters are provided, describe them as a cohesive group or encounter when appropriate.
Keep descriptions concise but evocative.
"""
    
    response = llm(prompt, max_tokens=600)
    result_text = response["choices"][0]["text"].strip()
    
    # Log to session if requested
    if log_session:
        log_to_session(f"Monster Lookup - Context: {context_str}\nMonsters: {monsters_str}\nNarration: {result_text}", "lookup")
    
    return result_text

def narrate_spells(spells: list, context: str = None, theme: str = None, log_session: bool = True):
    """
    Narrate a list of spells with LLM-based flavoring.
    
    Args:
        spells: List of spell dictionaries
        context: Player's context or intent
        theme: Thematic context (arcane, divine, etc.)
        log_session: Whether to log to session (default True)
    """
    llm = get_llm()
    
    # Convert spells to readable format
    spells_text = []
    for spell in spells:
        spell_desc = f"Name: {spell.get('name', 'Unknown')}"
        if spell.get('description'):
            spell_desc += f"\nDescription: {spell['description']}"
        if spell.get('class'):
            spell_desc += f"\nClass: {spell['class']}"
        if spell.get('level'):
            spell_desc += f"\nLevel: {spell['level']}"
        if spell.get('duration'):
            spell_desc += f"\nDuration: {spell['duration']}"
        if spell.get('range'):
            spell_desc += f"\nRange: {spell['range']}"
        if spell.get('tags'):
            spell_desc += f"\nTags: {', '.join(spell['tags'])}"
        spells_text.append(spell_desc)
    
    spells_str = "\n\n".join(spells_text)
    
    # Build context string
    context_parts = []
    if context:
        context_parts.append(f"Player Context: {context}")
    if theme:
        context_parts.append(f"Theme: {theme}")
    
    context_str = "\n".join(context_parts) if context_parts else "No specific context provided"
    
    prompt = f"""
You are the dungeon master in a fantasy TTRPG.
The player has discovered or is looking at these spells:

{spells_str}

Context:
{context_str}

Please provide a vivid, immersive description of these spells that incorporates the context provided.
Make them feel magical and unique while staying true to their base properties and effects.
If multiple spells are provided, describe them as a cohesive collection or spellbook when appropriate.
Keep descriptions concise but evocative.
"""
    
    response = llm(prompt, max_tokens=600)
    result_text = response["choices"][0]["text"].strip()
    
    # Log to session if requested
    if log_session:
        log_to_session(f"Spell Lookup - Context: {context_str}\nSpells: {spells_str}\nNarration: {result_text}", "lookup")
    
    return result_text

def rewrite_narration(original_narration: str, rewrite_instruction: str, log_session: bool = True):
    """
    Rewrite an existing narration based on user instructions.
    
    Args:
        original_narration: The original narration text
        rewrite_instruction: User's instruction for rewriting
        log_session: Whether to log to session (default True)
    """
    llm = get_llm()
    
    prompt = f"""
You are the dungeon master in a fantasy TTRPG.
The player wants to rewrite the following narration:

Original Narration:
{original_narration}

Rewrite Instruction:
{rewrite_instruction}

Please rewrite the narration according to the instruction while maintaining the same basic information and tone.
"""
    
    response = llm(prompt, max_tokens=600)
    result_text = response["choices"][0]["text"].strip()
    
    # Log to session if requested
    if log_session:
        log_to_session(f"Narration Rewrite - Original: {original_narration}\nInstruction: {rewrite_instruction}\nRewritten: {result_text}", "lookup")
    
    return result_text

def summarize_session_log_llm(prompt):
    llm = get_llm()
    response = llm(prompt, max_tokens=800)
    return response["choices"][0]["text"].strip()
