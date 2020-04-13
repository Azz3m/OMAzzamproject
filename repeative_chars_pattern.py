import re
repeative_chars_pattern = re.compile(r'(\w)\1*',flags=re.UNICODE)
def repeative_characters_removal(text):
    shaped_string = repeative_chars_pattern.sub(r'\1',text).strip()

    return shaped_string
print(repeative_characters_removal("loooooovvvvveeeeeeeeeee hello noooo odofogdfdgffd"))
