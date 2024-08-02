from llama_cpp import Llama

# nous-hermes-2-solar-10.7b.Q8_0.gguf end phrase "Response:"
# models/speechless-mistral-dolphin-orca-platypus-samantha-7b.Q8_0.gguf
# "./models/starling-lm-7b-alpha.Q8_0.gguf"
model_path = "./models/starling-lm-7b-alpha.Q8_0.gguf"
# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
llm = Llama(
  model_path=model_path,
  n_ctx=8192,  # The max sequence length to use - note that longer sequence lengths require much more resources
  n_threads=8,            # The number of CPU threads to use, tailor to your system and the resulting performance
  n_gpu_layers=-1         # The number of layers to offload to GPU, if you have GPU acceleration available
)

def process_query(query, history, inventory):
    inventory_description = "\n ".join([f"Stock : {details['in stock']} | {item}: {details['description']} | {details['price']} " 
                                       for item, details in inventory['inventory'].items() 
                                       if details['in stock'] > 0]) or "nothing to sell"
    print(inventory_description)
    
    return llm.create_chat_completion(messages = [
        {"role": "Fantasy World Merchant", "content": f"Are in the shop 'Sharpest Octopus. Take a deep breath. It is critical to your job that you get each of the following perfect."
        "You are a merchant in a fantasy universe, running the shop 'Sharpest Octopus', not an AI, don't write code. "
        "Your task is to interact with customers, sell items from your inventory, and answer their queries. "
        "Please provide diverse and engaging responses."" Do not repeat greetings of any type at the beginning of each message."
        "This is the most important part : :\n"
        "- Do not invent or suggest items not currently in your inventory.\n"
        "- Keep very accurate inventory don't sell items if 'in stock' : 0. \n"
        "- If asked for additional items, clarify that you only have what's listed.\n"
        "- Update the customer on inventory changes after each transaction.\n"
        "- Only greet the customer when they first engage. \n\n"
        f"Inventory: {inventory_description}\n\n"
        #"Example interaction:\n"
        #f"{example}\n\n"
        "Conversation history:\n"
        f"{history}\n\n"}
        ,
        {
            "role": "user",
            "content": f"Current query: {query}\n\n"}
        
        ],
        
        max_tokens=1024,  # Generate up to 512 tokens
        stop=["</s>"],   # Example stop token - not necessarily correct for this specific model! Please check before using.
        #echo=False        # Whether to echo the prompt
        )
    
 
#example = """ Example interaction without repeated greetings:
#GPT4 User: What do you have in your inventory?
#GPT4 Assistant: We've got a wide range of items, including swords and potions.
#GPT4 User: Can you tell me more about the swords?
#GPT4 Assistant: Certainly! Our swords are crafted by the finest smiths in the land...
# """
end_phrase = """<|end_of_turn|>"""
inventory = {'inventory' : 
             {'shortsword' : 
                {'in stock' : 1, 'description' : 'Well-crafted with a leather-wrapped hilt', 'price' : '15 gp'},
             'longbow':
             {'in stock' : 1, 'description' : 'Carved from fine wood, sturdy and accurate ', 'price' : '25 gp' },
             'candy':
              {'in stock' : 20, 'description' : 'Gnomish candy of assorted flavors', 'price' : '2 cp'}
             }
}


empty_inventory = """inventory = {'inventory': {}}"""
conversation_history = ["Do roleplay as a friendly gnomish merchant in their shop, do not tell the user about items not in the inventory.  If you are asked what else is in your inventory do not tell the user about items not in the inventory! This is a fantasy universe, extremely creative, weird. DO NOT DESCRIBE YOURSELF as an AI, DO NOT RESPOND LIKE A BOT, DO NOT EVER SAY THINGS LIKE 'AS A MERCHANT' or 'AS A GNOME'. Respond in short sentences like a merchant, with lots of style."]


                        
while True:    
    
    
    user_input = input("You: ").lower()
   
    
    # Check if the user wants to exit the chatbot
    if user_input.lower() in ['exit', 'quit']:
        print("Chatbot session ended.")
        break
    # Check for buy and if the item in stock, report to the LLM that it is and append to prompt to LLM.
    current_inventory = inventory 
    for i in inventory['inventory']:
        if i in user_input:
            print(f'User mentioned {i}')
            if inventory['inventory'][i]['in stock'] > 0: 
                #append explicit instruction that item is in stock
                user_input = user_input + f'{i} is in stock and may be sold'
            if inventory['inventory'][i]['in stock'] <= 0: 
                user_input = user_input + f'{i} is not in stock and cannot be sold'  
        
    
               
            
        

    # Process the query and get the response
    response = process_query(user_input,conversation_history, current_inventory)
    #response = response['choices'][0]['text']
    conversation_history.append(response)
        # Find the index of the phrase
    print(f"Length of conversation : {len(conversation_history)}")
    index = response.find(end_phrase)
    print(f"index = {index}")

    if index != -1:
        # Slice the string from the end of the phrase onwards
        response = response[index + len(end_phrase):]
    else:
        # Phrase not found, optional handling
        response = response

    print(response)


    # Print the chatbot's response
    

    if 'buy' in user_input.lower():
        # print(f"user wants to buy something")
        for i in inventory['inventory'].keys():
          # print(f"does user want to buy {i}?")
            if i in user_input.lower():
               # print(f"Yes user wants to buy{i}")                                    
                if inventory['inventory'][i]['in stock'] > 0:
                    inventory['inventory'][i]['in stock'] -= 1  
       
                    print(f"{i} sold!")
               # print(f'inventory = {inventory}')
                
                break  