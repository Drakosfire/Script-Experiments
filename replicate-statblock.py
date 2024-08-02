import replicate
import ast
import gc
import os

api_key = os.getenv('REPLICATE_API_TOKEN')


model_path = "meta/meta-llama-3-70b-instruct"
def load_llm(user_input):
  input = {"prompt" : f" {prompt_instructions} the item is {user_input}","max_tokens":1250}
  output = replicate.run(model_path,
  input=input
  
    )
  return output
  

def call_llm_and_cleanup(user_input):
    # Call the LLM and store its output
    llm_output = "".join(load_llm(user_input))
    print("".join(llm_output))
    gc.collect()
  
    # llm_output is still available for use here
    
    return llm_output

def convert_to_dict(string):
  # Evaluate if string is dictionary literal
    try: 
        result = ast.literal_eval(string)
        if isinstance(result, dict):
            print("Item dictionary is valid")
            return result
        # If not, modify by attempting to add brackets to where they tend to fail to generate.
        else: 
            modified_string = '{' + string
            if isinstance(modified_string, dict):  
                return modified_string
            modified_string = string + '}'
            if isinstance(modified_string, dict):  
                return modified_string
            modified_string = '{' + string + '}'
            if isinstance(modified_string, dict):  
                return modified_string
    except (ValueError, SyntaxError) :
        print("Dictionary not valid")
        return None
  

# Instructions past 4 are not time tested and may need to be removed.
### Meta prompted : 
prompt_instructions = """ 
**Purpose**: ONLY Generate a structured json following the provided format. The job is to generate a balance, creative, interesting monster statblock in the rule style of Dungeons and Dragons. You do not need to stick strictly to the abilities and spells of the game, if it fits the style and flavor of the user input, get weird, scary, or silly with the details. 
Anytime you are inventing new ideas they need explicit and clear description and explanation. 
Example that is not specific or clear : gaining a new ability or effect for 1 minute.
Example that is specific : gaining a +2 to perception.
Example that is specific : gaining the enlarged status for 1 minute.

You will also be writing a paragraph of interesting text describing the visual appearance and qualities of the subject. Then a brief stable diffusion image generation prompt. Include the type and subtype in the image prompt.


Image Generation Prompt Examples :
"A hooded stout dwarf necromancer, in black robes, emanating evil magic "
"A black and tan battle dog with spike collar, hackles up and ready to strike"
"a tanned human barbarian with bleeding red axes"
"a magical zombie tiger, colorful and decaying"
1. Only output the json file structure starting with {, DO NOT say anything like "Here is a generated monster statblock in the style of Dungeons and Dragons:"
2.Review and stick closely to this table.

Monster Statistics by Challenge Rating
| CR | XP | Prof. Bonus | Armor Class | Hit Points | Attack Bonus | Damage/Round | Save DC | Prob. of Spell | Num. of Spells | Level of Spells | Prob. of Legendary Actions | Num. of Legendary Actions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 10 | 2 | 10-13 | 1-3 | 3 | 0-1 | 13 | 0% | 0 | - | 0% | 0 |
| 1/8 | 25 | 2 | 10-13 | 2-7 | 3 | 2-3 | 13 | 05% | 1 | 1st | 0% | 0 |
| 1/4 | 50 | 2 | 10-13 | 4-8 | 3 | 4-5 | 13 | 10% | 2 | 1st | 0% | 0 |
| 1/2 | 100 | 2 | 10-13 | 5-11 | 3 | 6-8 | 13 | 15% | 3 | 1st | 0% | 0 |
| 1 | 200 | 2 | 10-13 | 8-20 | 3 | 9-14 | 13 | 15% | 4 | 1st | 0% | 0 |
| 2 | 450 | 2 | 11-13 | 15-30 | 3 | 15-20 | 13 | 20% | 5 | 2nd | 0% | 0 |
| 3 | 700 | 2 | 11-13 | 25-50 | 4 | 21-26 | 13 | 25% | 6 | 2nd |05% | 1 |
| 4 | 1100 | 2 | 11-14 | 35-75 | 5 | 27-32 | 14 | 30% | 7 | 2nd | 10% | 1 |
| 5 | 1800 | 3 | 12-15 | 45-95 | 6 | 33-38 | 15 | 50% | 8 | 3rd | 10% | 1 |
| 6 | 2300 | 3 | 12-15 | 60-110 | 6 | 39-44 | 15 | 60% | 9 | 3rd | 15% | 2 |
| 7 | 2900 | 3 | 12-15 | 70-140 | 6 | 45-50 | 15 | 75% | 10 | 3rd | 20% | 2 |
| 8 | 3900 | 3 | 13-16 | 80-160 | 7 | 51-56 | 16 | 90% | 11 | 4th | 20% | 3 |
| 9 | 5000 | 4 | 13-16 | 105-205 | 7 | 57-62 | 16 | 90% | 12 | 4th | 20% | 3 |
| 10 | 5900 | 4 | 14-17 | 206-220 | 7 | 63-68 | 16 | 100% | 13 | 4th | 30% | 3 |
| 11 | 7200 | 4 | 14-17 | 221-235 | 8 | 69-74 | 17 | 100% | 14 | 5th | 40% | 3 |
| 12 | 8400 | 4 | 14-17 | 236-250 | 8 | 75-80 | 18 | 100% | 15 | 6th | 60% | 4 |
| 13 | 10000 | 5 | 15-18 | 251-265 | 8 | 81-86 | 18 | 100% | 16 | 7th | 80% | 4 |
| 14 | 11500 | 5 | 15-18 | 266-280 | 8 | 87-92 | 18 | 100% | 17 | 7th | 100% | 4 |
| 15 | 13000 | 5 | 15-18 | 281-295 | 8 | 93-98 | 18 | 100% | 18 | 8th | 100% | 5 |
| 16 | 15000 | 5 | 15-18 | 296-310 | 9 | 99-104 | 18 | 100% | 19 | 8th | 100% | 5 |
| 17 | 18000 | 6 | 16-19 | 311-325 | 10 | 105-110 | 19 | 100% | 20 | 8th | 100% | 5 |
| 18 | 20000 | 6 | 16-19 | 326-340 | 10 | 111-116 | 19 | 100% | 21 | 9th | 100% | 5 |
| 19 | 22000 | 6 | 16-19 | 341-355 | 10 | 117-122 | 19 | 100% | 22 | 9th | 100% | 5 |
| 20 | 25000 | 6 | 16-19 | 356-400 | 10 | 123-140 | 19 | 100% | 23 | 9th | 100% | 5 |
| 21 | 33000 | 7 | 16-19 | 401-445 | 11 | 141-158 | 20 | 100% | 24 | 9th | 100% | 5 |
| 22 | 41000 | 7 | 16-19 | 446-490 | 11 | 159-176 | 20 | 100% | 25 | 9th | 100% | 5 |
| 23 | 50000 | 7 | 16-19 | 491-535 | 11 | 177-194 | 20 | 100% | 26 | 9th | 100% | 5 |
| 24 | 62000 | 7 | 16-19 | 536-580 | 11 | 195-212 | 21 | 100% | 27 | 9th | 100% | 5 |
| 25 | 75000 | 8 | 16-19 | 581-625 | 12 | 213-230 | 21 | 100% | 28 | 9th | 100% | 5 |
| 26 | 90000 | 8 | 16-19 | 626-670 | 12 | 231-248 | 21 | 100% | 29 | 9th | 100% | 5 |
| 27 | 105000 | 8 | 16-19 | 671-715 | 13 | 249-266 | 22 | 100% | 30 | 9th | 100% | 5 |
| 28 | 120000 | 8 | 16-19 | 716-760 | 13 | 267-284 | 22 | 100% | 31 | 9th | 100% | 5 |
| 29 | 135000 | 9 | 16-19 | 760-805 | 13 | 285-302 | 22 | 100% | 32 | 9th | 100% | 5 |
| 30 | 155000 | 9 | 16-19 | 805-850 | 14 | 303-320 | 23 | 100% | 33 | 9th | 100% | 5 |
3. At lower Challenge Rating ie 0,1/8, 1/4, 1/2, the monster MUST have less than 
2. 

Output format : 
{
  "name": "",
  "type": "",
  "subtype": "",
  "alignment": "",
  "armor_class": ,
  "hit_points": ,
  "hit_dice": "",
  "speed": {
    "walk": ,
    "other_speed_type":
  },
  "abilities": {
    "str": ,
    "dex": ,
    "con": ,
    "int": ,
    "wis": ,
    "cha":
  },
  "saving_throws": {
    "str": ,
    "dex": ,
    "wis":
  },
  "skills": {
    "perception": ,
    "other_skill_type":
  },
  "senses": {
    "darkvision": ,
    "other_sense_type":
  },
  "languages": "",
  "challenge_rating": ,
  "xp": ,
  "actions": [
    {
      "name": "",
      "desc": ""
    }
  ],
  "spells": {
    "at_will": [
      {
        "name": "",
        "level": ,
        "desc": ""
      }
    ],
    "x/day each": [
      {
        "name": "",
        "level": ,
        "desc": ""
      }
    ],
    "spell_slots": {
      "1st_level": ,
      "2nd_level": ,
      "3rd_level": ,
      "4th_level": ,
      "5th_level": ,
      "6th_level": ,
      "7th_level": ,
      "8th_level": ,
      "9th_level":
    }
  },
  "legendary_actions": {
    "actions": ,
    "options": [
      {
        "name": "",
        "desc": ""
      }
    ]
  },
  "description":"",
  "sd prompt":""
}
"""
output = call_llm_and_cleanup("The Flavor Lich, a wonderfully strange creature that prusued eternal life in the pursuit of becoming the perfect eternal pizza chef")
user_monster = convert_to_dict(output)

mon_name = user_monster['name']
mon_speed = user_monster['speed']
print(mon_name)
print(mon_speed)
print(type(mon_speed))