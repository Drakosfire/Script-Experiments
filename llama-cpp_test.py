from llama_cpp import Llama
import ast
import gc
import torch

model_path = "/media/drakosfire/Shared/models/starling-lm-7b-alpha.Q8_0.gguf"

def load_llm(user_input):
  llm = Llama(
  model_path=model_path,
  n_ctx=8192,  # The max sequence length to use - note that longer sequence lengths require much more resources
  n_threads=8,            # The number of CPU threads to use, tailor to your system and the resulting performance
  n_gpu_layers=-1, # The number of layers to offload to GPU, if you have GPU acceleration available
  )
  return llm(
  f"{user_input}", # Prompt
  max_tokens=512,  # Generate up to 512 tokens
  stop=["</s>"],   # Example stop token - not necessarily correct for this specific model! Please check before using.
  echo=False        # Whether to echo the prompt
  )   
query = "Last session, my character, a rogue, successfully sneaked up on an enemy. I heard about something called 'sneak attack' that rogues can do. Can you explain how sneak attack works and what I need to do to use it in our next session?"

response = load_llm(query)

print(response['choices'][0]['text'])