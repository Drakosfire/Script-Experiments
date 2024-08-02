from llama_cpp import llama_tokenizer


model_path = "/models/starling-lm-7b-alpha.Q8_0.gguf"

def count_tokens(text):
    tokenizer = llama_tokenizer.from_pretrained(model_path)
    tokens = tokenizer.tokenize(text)
    return len(tokens)

text = """ **Purpose**: Generate a structured inventory entry for a specific item as a Python dictionary. Follow the format provided in the examples below.

**Instructions**:
1. Replace `{item}` with the name of your item, enclosed in single quotes (e.g., `'Magic Wand'`).
2. Ensure your request is formatted as a Python dictionary. Do not add quotation marks around the dictionary's `Quote` value.
3. Items are more expensive than you think, increase the cost.
4. Value should be assigned as an integer of copper pieces (cp), silver pieces (sp), electrum pieces (ep), gold pieces (gp), and platinum pieces (pp). .
5. Use this table for reference on value : 
1 cp 	1 lb. of wheat
2 cp 	1 lb. of flour or one chicken
5 cp 	1 lb. of salt
1 sp 	1 lb. of iron or 1 sq. yd. of canvas
5 sp 	1 lb. of copper or 1 sq. yd. of cotton cloth
1 gp 	1 lb. of ginger or one goat
2 gp 	1 lb. of cinnamon or pepper, or one sheep
3 gp 	1 lb. of cloves or one pig
5 gp 	1 lb. of silver or 1 sq. yd. of linen
10 gp 	1 sq. yd. of silk or one cow
15 gp 	1 lb. of saffron or one ox
50 gp 	1 lb. of gold
500 gp 	1 lb. of platinum

6. Examples of Magical Scroll Value:
    Common: 50-100 gp
    Uncommon: 101-500 gp
    Rare: 501-5000 gp
    Very rare: 5001-50000 gp
    Legendary: 50001+ gp
A scroll's rarity depends on the spell's level:
    Cantrip-1: Common
    2-3: Uncommon
    4-5: Rare
    6-8: Very rare
    9: Legendary

7. Explanation of Mimics:
Mimics are shapeshifting predators able to take on the form of inanimate objects to lure creatures to their doom. In dungeons, these cunning creatures most often take the form of doors and chests, having learned that such forms attract a steady stream of prey.
Imitative Predators. Mimics can alter their outward texture to resemble wood, stone, and other basic materials, and they have evolved to assume the appearance of objects that other creatures are likely to come into contact with. A mimic in its altered form is nearly unrecognizable until potential prey blunders into its reach, whereupon the monster sprouts pseudopods and attacks.
When it changes shape, a mimic excretes an adhesive that helps it seize prey and weapons that touch it. The adhesive is absorbed when the mimic assumes its amorphous form and on parts the mimic uses to move itself.
Cunning Hunters. Mimics live and hunt alone, though they occasionally share their feeding grounds with other creatures. Although most mimics have only predatory intelligence, a rare few evolve greater cunning and the ability to carry on simple conversations in Common or Undercommon. Such mimics might allow safe passage through their domains or provide useful information in exchange for food.

8. 
**Format Example**:
- **Dictionary Structure**:
    ```
    '{item}': {
    'Name': '{item name}',
    'Type': '{item type}',
    'Rarity': '{item rarity},
    'Value': '{item value}',
    'Properties': ['{property1}', '{property2}', ...],
    'Damage': '{damage formula} , 'damage type}',
    'Weight': '{weight}',
    'Description': '{item description}',
    'Quote': '{item quote}',
    'SD Prompt': '{special description for the item}'
}
    ```
- **Input Placeholder**:
    - `{item}`: Replace with the item name, ensuring it's wrapped in single quotes.

**Output Examples**:
1. Cloak of Whispering Shadows Entry:
    ```
    {'Cloak of Whispering Shadows': {
    'Name': 'Cloak of Whispering Shadows',
    'Type': 'Cloak',
    'Rarity': 'Very rare', 
    'Value': '10000 gp',
    'Properties': ['Grants invisibility in dim light or darkness','Allows communication with shadows for gathering information'],
    'Weight': '1 lb',
    'Description': 'A cloak woven from the essence of twilight, blending its wearer into the shadows. Whispers of the past and present linger in its folds, offering secrets to those who listen.',
    'Quote': 'In the embrace of night, secrets surface in the silent whispers of the dark.',
    'SD Prompt': ' decorated with shimmering threads that catch the light to mimic stars.' } }   
    ```
2. Health Potion Entry:
    ```
     {'Health Potion': {
    'Name' : 'Health Portion',
    'Type' : 'Potion',
    'Rarity' : 'Common',
    'Value': '50 gp',
    'Properties': ['Quafable', 'Restores 1d4 + 2 HP upon consumption'],
    'Weight': '0.5 lb',
    'Description': 'Contained within this small vial is a crimson liquid that sparkles when shaken, a life-saving elixir for those who brave the unknown.',
    'Quote': 'To the weary, a drop of hope; to the fallen, a chance to stand once more.',
    'SD Prompt' : ' high quality magnum opus drawing of a vial of bubling red liquid' } }     
    ```
3. Wooden Shield Entry:
    ```
     {'Wooden Shield': {
    'Name' : 'Wooden Shield',
    'Type' : 'Armor, Shield',
    'Rarity': 'Common',
    'Value': '10 gp',
    'Properties': ['+2 AC'],
    'Weight': '6 lb',
    'Description': 'Sturdy and reliable, this wooden shield is a simple yet effective defense against the blows of adversaries.',
    'Quote': 'In the rhythm of battle, it dances - a barrier between life and defeat.',
    'SD Prompt': ' high quality magnum opus drawing of a wooden shield strapped with iron and spikes' } }
    ``` 
4. Magical Helmet of Perception Entry:
    ```
    {'Magical Helmet': {
    'Name' : 'Magical Helmet of Perception',
    'Type' : 'Magical Item (armor, helmet)',
    'Rarity':
    'Value': '25- gp',
    'Properties': ['+ 1 to AC', 'Grants the wearer advantage on perception checks', '+5 to passive perception'],
    'Weight': '3 lb',
    'Description': 'Forged from mystic metals and enchanted with ancient spells, this helmet offers protection beyond the physical realm.',
    'Quote': 'A crown not of royalty, but of unyielding vigilance, warding off the unseen threats that lurk in the shadows.',
    'SD Prompt': 'high quality magnum opus drawing of an ancient elegant helm with a shimmer of magic' } }
    ```
5. Longbow Entry:
    ```
    {'Longbow': {
    'Name': 'Longbow',
    'Type': 'Ranged Weapon (martial, longbow)',
    'Value': '50 gp',
    'Properties': ['2-handed', 'Range 150/600', 'Loading'],
    'Damage': '1d8 + Dex, piercing',
    'Weight': '6 lb',
    'Description': 'With a sleek and elegant design, this longbow is crafted for speed and precision, capable of striking down foes from a distance.',
    'Quote': 'From the shadows it emerges, a silent whisper of steel that pierces the veil of darkness, bringing justice to those who dare to trespass.',
    'SD Prompt' : 'high quality magnum opus drawing of a longbow with a quiver attached' } }
    ```

6. Mace Entry:
    ```
    {'Mace': {
    'Name': 'Mace',
    'Type': 'Melee Weapon (martial, bludgeoning)',
    'Value': '25 gp', 'Properties': ['Bludgeoning', 'One-handed'],
    'Damage': '1d6 + str, bludgeoning',
    'Weight': '6 lb', 
    'Description': 'This mace is a fearsome sight, its head a heavy and menacing ball of metal designed to crush bone and break spirits.', 
    'Quote': 'With each swing, it sings a melody of pain and retribution, an anthem of justice to those who wield it.', 
    'SD Prompt': 'high quality magnum opus drawing of a mace with intricate detailing and an ominous presence' } }
    ```
7. Flying Carpet Entry:
    ```
    {'Flying Carpet': {
    'Name': 'Flying Carpet', 
    'Type': 'Magical Item (transportation)', 
    'Value': '1250 gp', 
    'Properties': ['Flying', 'Personal Flight', 'Up to 2 passengers', Speed : 60 ft], 
    'Weight': '50 lb', 
    'Description': 'This enchanted carpet whisks its riders through the skies, providing a swift and comfortable mode of transport across great distances.', 'Quote': 'Soar above the mundane, and embrace the winds of adventure with this magical gift from the heavens.', 
    'SD Prompt': 'high quality magnum opus drawing of an elegant flying carpet with intricate patterns and colors' } }
    ```
8. Tome of Endless Stories Entry:
    ```
    {'Tome of Endless Stories': {
    'Name': 'Tome of Endless Stories',
    'Type': 'Book',
    'Value': '500 gp',
    'Properties': [
        'Generates a new story or piece of lore each day',
        'Reading a story grants insight or a hint towards solving a problem or puzzle'
    ],
    'Weight': '3 lbs',
    'Description': 'An ancient tome bound in leather that shifts colors like the sunset. Its pages are never-ending, filled with tales from worlds both known and undiscovered.',
    'Quote': 'Within its pages lie the keys to a thousand worlds, each story a doorway to infinite possibilities.',
    'SD Prompt': 'leather-bound with gold and silver inlay, pages appear aged but are incredibly durable, magical glyphs shimmer softly on the cover.' } }    
    ```
9. Ring of Miniature Summoning Entry:
    ```
    {'Ring of Miniature Summoning': {
    'Name': 'Ring of Miniature Summoning',
    'Type': 'Ring',
    'Value': '475 gp',
    'Properties': ['Summons a miniature beast ally once per day', 'Beast follows commands and lasts for 1 hour', 'Choice of beast changes with each dawn'],
    'Weight': '0 lb',
    'Description': 'A delicate ring with a gem that shifts colors. When activated, it brings forth a small, loyal beast companion from the ether.',
    'Quote': 'Not all companions walk beside us. Some are summoned from the depths of magic, small in size but vast in heart.',
    'SD Prompt': 'gemstone with changing colors, essence of companionship and versatility.' } } 
    ``` 

10. Spoon of Tasting Entry:
    ```
    {'Spoon of Tasting': {
    'Name': 'Spoon of Tasting',
    'Type': 'Spoon',
    'Value': '10 gp',
    'Properties': ['When used to taste any dish, it can instantly tell you all the ingredients', 'Provides exaggerated compliments or critiques about the dish'],
    'Weight': '0.2 lb',
    'Description': 'A culinary critic’s dream or nightmare. This spoon doesn’t hold back its opinions on any dish it tastes.',
    'Quote': 'A spoonful of sugar helps the criticism go down.',
    'SD Prompt': 'Looks like an ordinary spoon, but with a mouth that speaks more than you’d expect.' } }
    ```
11. Infinite Scroll Entry: 
    ```
    {'Infinite Scroll': {
    'Name': 'Infinite Scroll',
    'Type': 'Magical Scroll',
    'Value': 'Priceless',
    'Properties': [
        'Endlessly Extends with New Knowledge',
        'Reveals Content Based on Reader’s Need or Desire',
        'Cannot be Fully Transcribed'
    ],
    'Weight': '0.5 lb',
    'Description': 'This scroll appears to be a standard parchment at first glance. However, as one begins to read, it unrolls to reveal an ever-expanding tapestry of knowledge, lore, and spells that seems to have no end. The content of the scroll adapts to the reader’s current quest for knowledge or need, always offering just a bit more beyond what has been revealed.',
    'Quote': 'In the pursuit of knowledge, the horizon is ever receding. So too is the content of this scroll, an endless journey within a parchment’s bounds.',
    'SD Prompt': 'A seemingly ordinary scroll that extends indefinitely, ' } }
    ```
12. Mimic Treasure Chest Entry:
    ```
    'Mimic Treasure Chest': {
    'Name': 'Mimic Treasure Chest',
    'Type': 'Trap',
    'Value': '1000 gp',  # Increased value reflects its dangerous and rare nature
    'Properties': [
        'Deceptively inviting',
        'Springs to life when interacted with',
        'Capable of attacking unwary adventurers'
        ],
    'Weight': '50 lb',  # Mimics are heavy due to their monstrous nature
    'Description': 'At first glance, this chest appears to be laden with treasure, beckoning to all who gaze upon it. However, it harbors a deadly secret: it is a Mimic, a cunning and dangerous creature that preys on the greed of adventurers. With its dark magic, it can perfectly imitate a treasure chest, only to reveal its true, monstrous form when approached. Those who seek to plunder its contents might find themselves in a fight for their lives.',
    'Quote': '"Beneath the guise of gold and riches lies a predator, waiting with bated breath for its next victim."',
    'SD Prompt': 'A seemingly ordinary treasure chest that glimmers with promise. Upon closer inspection, sinister, almost living edges move with malice, revealing its true nature as a Mimic, ready to unleash fury on the unwary.'
    }
    ```

"""
token_count = count_tokens(text)
print(f"Token count: {token_count}")