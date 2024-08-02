from loadexllamav2 import MyExllamav2

model_path = "./Speechless-Llama2-Hermes-Orca-Platypus-WizardLM-13B-GPTQ"
allow_download = False

custom_llm = MyExllamav2(model_folder_path=model_path,                  
                       allow_download=allow_download)

prompt = f"This is the most important senctence : It is CRITICAL that this outline format be written EXACTLY AS FOLLOWS!!! Title, 1. Briny Pete Description : only write a concise, visually descriptive, detailed and colorful three to 5 sentences about the appearance of the Briny Pete the focus should be on describing it's visual qualities and it's very important it is CONCISE!, 2. Encounter Location:' A very visually filled and imaginative description of the Briny Pete in Redrook '3. Backstory:' A brief backstory'  '4. Encounter Start' Three distinctly different, very creative and varied possible events to start the encounter, '5. Unexpected Creative Resolutions: ' 3 suggestions for non violent ways the players might engage with the Briny Pete, '6. Enviornmental Events: ' a d20 TABLE list of at least 5 items possible environmental events during the encounter, '7. Loot Table: ' a 1d20 loot TABLE list of at least 5 items that includes valuable loot, wacky loot and some useless but interesting loot. '8. Quest Hook: ' A story hook for a followup quest. You are a VERY compotent, talented, experienced, exacting, perfectionist and wildly creative storyteller and tabletop gamemaster. Your task is to write an outline of a dungeons and dragons location and an encounter with a Briny Pete. Invent names of characters, monsters, and locations as needed.  DO NOT include sub numbers, DO NOT give any additional instructions, reminders, notes, or advice! ONLY WRITE THE OUTLINE! Start with Title!"

# prompt = "Write a three part outline of a dnd adventure"
response = custom_llm._call(prompt)

print(response)

    