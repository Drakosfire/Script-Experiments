import ast

data = """{
    'Demonic Pencil': {
        'Name': 'Demonic Pencil',
        'Type': 'Magical Item',
        'Rarity': 'Uncommon',
        'Value': '250 gp',
        'Properties': ["Writes in any language known to the wielder", "Inks change color based on the writer's emotions", "Inks can be used to cast Invisibility on the writing"],
        'Weight': '0.2 lb',
        'Description': "A sinister-looking pencil with black, iridescent wood and golden accents. Its lead is rumored to be made from the essence of demons, giving it extraordinary power to convey the writer's thoughts.",
        'Quote': "On this pencil's lead, ink flows not only with the writer's hand but with their very soul. It reveals emotions through color, weaving stories that pierce the veil of darkness.",
        'SD Prompt': "A black pencil with golden accents and a hint of red on its lead, as if it has been dipped in the essence of fire. The iridescent wood seems to glow slightly, casting eerie shadows around it."
    }
}"""

try:
    result = ast.literal_eval(data)
    if isinstance(result, dict):
        print("This is a valid dictionary.")
except ValueError:
    print("The string is not a valid dictionary.")