from llama_cpp import Llama

model_path = "./models/starling-lm-7b-alpha.Q8_0.gguf"
# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
llm = Llama(
  model_path=model_path,
  n_ctx=8192,  # The max sequence length to use - note that longer sequence lengths require much more resources
  n_threads=8,            # The number of CPU threads to use, tailor to your system and the resulting performance
  n_gpu_layers=-1         # The number of layers to offload to GPU, if you have GPU acceleration available
)


# Simple inference example
def process_query(query, history):
  return llm(
  f"{history} GPT4 User: {query}<|end_of_turn|>GPT4 Assistant:", # Prompt
  max_tokens=512,  # Generate up to 512 tokens
  stop=["</s>"],   # Example stop token - not necessarily correct for this specific model! Please check before using.
  echo=True        # Whether to echo the prompt
  )
 

end_phrase = """<|end_of_turn|>"""
conversation_history = []
while True:
    user_input = input("You: ")
    
    # Check if the user wants to exit the chatbot
    if user_input.lower() in ['exit', 'quit']:
        print("Chatbot session ended.")
        break

    # Process the query and get the response
    response = process_query(user_input,conversation_history)
    response = response['choices'][0]['text']
    conversation_history.append(response)
    print(len(conversation_history))
        # Find the index of the phrase
    index = response.find(end_phrase)
    print(f"index = {index}")

    if index != -1:
        # Slice the string from the end of the phrase onwards
        response = response[index + len(end_phrase):]
    else:
        # Phrase not found, optional handling
        response = response
    


    # Print the chatbot's response
    print(response)