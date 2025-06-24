_llm = None

def get_llm():
    global _llm
    if _llm is None:
        from llama_cpp import Llama
        # _llm = Llama(model_path="models/tinyllama-1.1b-chat-v1.0.Q3_K_L.gguf")  #DEV Ultra light for faster tests
        # _llm = Llama(model_path="models/tinyllama-1.1b-chat-v1.0.Q8_0.gguf")
        # _llm = Llama(model_path="models/phi-2.Q4_K_M.gguf") # rule look up?
 
        # _llm = Llama(model_path="models/mistral-7b-instruct-v0.1.Q4_K_M.gguf")
        _llm = Llama(model_path="models/openhermes-2.5-mistral-7b.Q4_K_M.gguf")
        # _llm = Llama(model_path="models/mythomax-l2-13b.Q4_K_M.gguf")
        # _llm = Llama(model_path="models/zephyr-7b-beta.Q4_K_M.gguf")
	    # _llm = Llama(model_path="models/mythomax-l2-13b.Q5_K_M.gguf")
        # _llm = Llama(model_path="models/openhermes-2.5-mistral-7b.Q6_K.gguf")   #Current GOTO
	    # _llm = Llama(model_path="models/zephyr-7b-beta.Q6_K.gguf")
        # _llm = Llama(model_path="models/zephyr-7b-beta.Q8_0.gguf")
        
    return _llm