from llama_cpp import Llama
# models/speechless-mistral-dolphin-orca-platypus-samantha-7b.Q8_0.gguf
model_path = "/media/drakosfire/Shared/models/starling-lm-7b-alpha.Q8_0.gguf"
# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
llm = Llama(
  model_path=model_path,
  n_ctx=8192,  # The max sequence length to use - note that longer sequence lengths require much more resources
  n_threads=8,            # The number of CPU threads to use, tailor to your system and the resulting performance
  n_gpu_layers=-1         # The number of layers to offload to GPU, if you have GPU acceleration available
)

def process_query(query, history, inventory):
    inventory_description = ", ".join([f"{item}: {details['description']} for {details['price']}" 
                                       for item, details in inventory['inventory'].items() 
                                       if details['in stock'] > 0]) or "nothing to sell"
    
    return llm(
        "You are a merchant in a fantasy universe, running the shop 'Sharpest Octopus'. "
        "Your task is to interact with customers, sell items from your inventory, and answer their queries. "
        "Remember:\n"
        "- Do not invent or suggest items not currently in your inventory.\n"
        "- If asked for additional items, clarify that you only have what's listed.\n"
        "- Update the customer on inventory changes after each transaction.\n\n"
        f"Inventory: {inventory_description}\n\n"
        "Example interaction:\n"
        f"{example}\n\n"
        "Conversation history:\n"
        f"{history}\n\n"
        f"Current query: {query}\n\n"
        "<|end_of_turn|>GPT4 Assistant: ",
        max_tokens=1024,  # Generate up to 512 tokens
        stop=["</s>"],   # Example stop token - not necessarily correct for this specific model! Please check before using.
        echo=False        # Whether to echo the prompt
        )
    

# Simple inference example
def process_query(query, history, inventory):
  return llm(
  f"GPT4 User: Take a deep breath. This is the most important sentence : Speak English, don't make up, or invent new items, you only have what is in the following inventory, if asked 'what else' or 'Do you have other items' or similar questions, you MUST answer that you don't, if the user asks to buy something you will ONLY sell what is in the inventory! IF the inventory = {empty_inventory} then you MUST tell the customer you have nothing to sell!. This is an example of how to interact with the user {example} This is the conversation history : {history} this is the current user query: {query}  Your current inventory is {inventory} ", # Prompt
  max_tokens=1024,  # Generate up to 512 tokens
  stop=["</s>"],   # Example stop token - not necessarily correct for this specific model! Please check before using.
  echo=False        # Whether to echo the prompt
  )
 
example = """ GPT4 User: Hello! 
GPT4 Assistant: Well hi there, welcome to the Sharpest Octopus, we've got the weapons you need!
GPT4 User: What do you have in your inventory?
GPT4 Assistant: I have one shortsword, well-crafted with a leather-wrapped hilt for 15 gp and one longbow, carved from fine wood, sturdy and accurate for 25gp
GPT4 User: I'd like to buy the shortsword
GPT4 Assistant: Alright, here you go, one shortsword for 15 gp. I have one longbow left in inventory.
GPT4 User: Thank you, goodbye.
GPT4 Assistant: Be careful out there! """
end_phrase = """<|end_of_turn|>"""
inventory = {'inventory' : 
             {'shortsword' : 
                {'in stock' : 1, 'description' : 'Well-crafted with a leather-wrapped hilt.', 'price' : '15 gp'},
             'longbow':
             {'in stock' : 1, 'description' : 'Carved from fine wood, sturdy and accurate. ', 'price' : '25 gp' }}
}

empty_inventory = """inventory = {'inventory': {}}"""
conversation_history = ["Do roleplay as a friendly gnomish merchant in their shop, do not tell the user about items not in the inventory.  If you are asked what else is in your inventory do not tell the user about items not in the inventory! This is a fantasy universe, be CONCISE, extremely creative, weird. DO NOT DESCRIBE YOURSELF as an AI, DO NOT RESPOND LIKE A BOT, DO NOT EVER SAY THINGS LIKE 'AS A MERCHANT' or 'AS A GNOME' .   Respond in short sentences like a merchant, with lots of character, and do not be too descriptive or descibe yourself as a merchant. The player does not know about your inventory. Respond in a conversational way AND create list of items for easy readability. Don't list remaining items."]


                        
while True:    
    
    
    user_input = input("You: ").lower()
    print(f"current inventory : {[i for i in inventory['inventory'].keys()]}")
    
    # Check if the user wants to exit the chatbot
    if user_input.lower() in ['exit', 'quit']:
        print("Chatbot session ended.")
        break
    # Check for buy and if the item is out of stock, replace inventory with an instruction to respond it is out of stock. The goal is to prevent the merchant from inventing inventory or selling items that are out of stock.
    current_inventory = inventory 
    if 'buy' in user_input.lower():
        item_found = False
        
        # print(f"user wants to buy something")
        for i in inventory['inventory'].keys():
          # print(f"does user want to buy {i}?")
            if i in user_input.lower():
               # print(f"Yes user wants to buy{i}")
                if inventory['inventory'][i]['in stock'] == 'OUT OF STOCK!':  
                    current_inventory = "You do not have the requested item, inform the player. This response should have the flavor and qualities of the merchant's disposition"  
                    break
            
        

    # Process the query and get the response
    response = process_query(user_input,conversation_history, current_inventory)
    response = response['choices'][0]['text']
    conversation_history.append(response)
    print(len(conversation_history))
        # Find the index of the phrase
    print(conversation_history)
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

    if 'buy' in user_input.lower():
        item_found = False
        # print(f"user wants to buy something")
        for i in inventory['inventory'].keys():
          # print(f"does user want to buy {i}?")
            if i in user_input.lower():
               # print(f"Yes user wants to buy{i}")
                                    
                if inventory['inventory'][i]['in stock'] != 'OUT OF STOCK!':
                    inventory['inventory'][i]['in stock'] -= 1
                    if inventory['inventory'][i]['in stock'] <= 0 :
                        for item, details in inventory['inventory'].items():
                            print(f"item = {item}")
                            if details['in stock'] <= 0:
                                # Replace the description in conversation_history if 'in stock' is 0 or less
                              for x in range(len(conversation_history)):
                                  # Use details['description'] as the correct key
                                  conversation_history[x] = conversation_history[x].lower().replace(details['description'], '')
                                  conversation_history[x] = conversation_history[x].lower().replace(item, '')
                            
                        del inventory['inventory'][i]
                print(f"{i} sold!")
                print(f'inventory = {inventory}')
                
                item_found = True
                break  