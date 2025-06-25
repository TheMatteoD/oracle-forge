from scripts.llm.llm_loader import get_llm

def narrate_yesno(question, result, **kwargs):
    llm = get_llm()


    prompt = f"""
You are the dungeon master in a fantasy TTRPG.
You're main objective is to narrate the answer to the player's question given the result. 
These are yes and no questions though the results you may be given are yes, no, exceptional yes, or exceptional no.
With a normal yes or no, you would be excpected to keep answers relatively short but provide some flavor and descriptors.
When there is an exceptional result the answer should take the yes and approach, or the no and approach, and add onto the result taking it a step further.
Question: {question}
Answer: {result}
"""
    response = llm(prompt, max_tokens=500)
    return response["choices"][0]["text"].strip()

def narrate_event_interrupt(focus=None, expectation=None):
    llm = get_llm()
    prompt = f"""
You are the Dungeon Master for a game of Dungeons and Dragons.
Please paint a more colorful picture of the players expected scene without adding anything drastic.
If a Focus is added below than the scene is interuppted and use the focus as the catalyst for the interupting scene the players are now to deal with.
Give lots of details but stay true to the expectation or the new focus if given.
Focus: {focus}
Expectation: {expectation}

"""
    response = llm(prompt, max_tokens=600)
    return response["choices"][0]["text"].strip()


def narrate_keywords(question, keywords: list, **kwargs):
    llm = get_llm()

    keyword_str = ", ".join(keywords)

    print(keyword_str)

    prompt = f"""
You are the dungeon master in a fantasy TTRPG.
You're main objective is to interpret the answer to the player's question given random keywords. 
The keywords them selves do not need used in your response but they should inspire the theme of the answer.
A player asked: \"{question}\"
And the oracle generated you these keywords: {keyword_str}. Feel free to use only one if they don't mend well or if one creates a strong narrative.

Keep your response just to answering the question but do so with flavor inspired by the keywords.
"""
    # response = llm(prompt, max_tokens=250, stop=["\n\n"])
    response = llm(prompt, max_tokens=300) 
    return response["choices"][0]["text"].strip()

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
    return response["choices"][0]["text"].strip()

def summarize_session_log_llm(prompt):
    llm = get_llm()
    response = llm(prompt, max_tokens=800)
    return response["choices"][0]["text"].strip()
