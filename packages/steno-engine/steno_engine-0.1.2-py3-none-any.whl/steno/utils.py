import re


# theoretically in the future you could have these be configurable
LITERAL_TAGS = {
    "open": "<literal>",
    "close": "</literal>"
}


def extract_literals(text: str) -> tuple[str, dict]:
    """
    Replaces <literal>...</literal> blocks with placeholders.
    Returns modified text and a mapping of placeholders to original content.
    """
    literals = {}

    def replace(match):
        key = f"LITERAL_{len(literals)}"
        literals[key] = match.group(1)
        return key

    open_tag = LITERAL_TAGS["open"]
    close_tag = LITERAL_TAGS["close"]
    rgx = re.compile(f"""{open_tag}(.*?){close_tag}""", flags=re.DOTALL)
    modified = rgx.sub(replace, text)
    return modified, literals


def restore_literals(text: str, literals: dict, include_tags: bool = False) -> str:
    open_tag = LITERAL_TAGS["open"]
    close_tag = LITERAL_TAGS["close"]
    for key, value in literals.items():
        if include_tags:
            text = text.replace(key, f"{open_tag}{value}{close_tag}")
        else:
            text = text.replace(key, value)
    return text
