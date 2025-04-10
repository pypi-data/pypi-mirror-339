import re

RESET = "\033[0m"

_STYLES = {
    "bold": "\033[1m",
    "dim": "\033[2m",
    "italic": "\033[3m",       # not supported in all terminals
    "underline": "\033[4m",
    "blink": "\033[5m",
    "reverse": "\033[7m",
    "hidden": "\033[8m",
    "strikethrough": "\033[9m",
}

_COLORS = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "default": "\033[39m",
}

_BRIGHT_COLORS = {
    "bright_black": "\033[90m",
    "bright_red": "\033[91m",
    "bright_green": "\033[92m",
    "bright_yellow": "\033[93m",
    "bright_blue": "\033[94m",
    "bright_magenta": "\033[95m",
    "bright_cyan": "\033[96m",
    "bright_white": "\033[97m",
}

_BG_COLORS = {
    "bg_black": "\033[40m",
    "bg_red": "\033[41m",
    "bg_green": "\033[42m",
    "bg_yellow": "\033[43m",
    "bg_blue": "\033[44m",
    "bg_magenta": "\033[45m",
    "bg_cyan": "\033[46m",
    "bg_white": "\033[47m",
    "bg_default": "\033[49m",
}

_BRIGHT_BG_COLORS = {
    "bg_bright_black": "\033[100m",
    "bg_bright_red": "\033[101m",
    "bg_bright_green": "\033[102m",
    "bg_bright_yellow": "\033[103m",
    "bg_bright_blue": "\033[104m",
    "bg_bright_magenta": "\033[105m",
    "bg_bright_cyan": "\033[106m",
    "bg_bright_white": "\033[107m",
}

# combine all codes into a single dictionary
_CODE_MAP = {}
_CODE_MAP.update(_STYLES)
_CODE_MAP.update(_COLORS)
_CODE_MAP.update(_BRIGHT_COLORS)
_CODE_MAP.update(_BG_COLORS)
_CODE_MAP.update(_BRIGHT_BG_COLORS)
_CODE_MAP["reset"] = RESET

def style(text: str) -> str:
    def replace_token(match):
        token = match.group(1)
        # look up the token in the code map; if not found, leave it unchanged.
        return _CODE_MAP.get(token, match.group(0))
    
    # replace all token occurrences in the input text.
    styled = re.sub(r'\{([^}]+)\}', replace_token, text)
    if not styled.endswith(RESET):
        styled += RESET
    return styled

# test
if __name__ == '__main__':
    sample = style("{bright_blue}Hello {red}World!")
    print("Styled text output:")
    print(sample)