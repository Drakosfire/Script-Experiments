actions = """Action Name: Short Sword; Description: Melee Attack: +4 to hit, reach 5 ft., one target. Hit: 6 (1d6 + 2) piercing damage.
Action Name: Spellcasting; Description: Test Goblin Number 5 is a 2nd-level spellcaster. Its spellcasting ability is Charisma (spell save DC 14). It knows the following spells: Acid Splash, Magic Missile, Shield, Feather Fall."""


def parse_actions_from_text(edited_text):
    actions = []
    action_entries = edited_text.strip().split('\n')
    for entry in action_entries:
        parts = entry.split(';')
        action_dict = {
            "name": parts[0].split(": ")[1].strip(),
            "desc": parts[1].split(": ")[1].strip()
        }
        actions.append(action_dict)
    print(actions)
    return actions

def convert_actions_to_html(actions):
    print(actions)
    html_content = ""
    
    for action in actions:
        html_content += f"<dt><em><br><strong>{action['name']}</strong></em> : ‘{action['desc']}’</dt><dd></dd>"
    
    return html_content


actions = parse_actions_from_text(actions)
print(convert_actions_to_html(actions))