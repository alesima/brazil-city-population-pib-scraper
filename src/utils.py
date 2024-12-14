import re
from colorama import Fore, Style
from unicodedata import normalize


def slugify(text: str):
    """Make an ASCII slug of text"""

    # Make lower case and delete apostrophes from contractions
    slug = re.sub(r"(\w)['’](\w)", r"\1\2", text.lower())

    # Convert runs of non-characters to single hyphens, stripping from ends
    slug = re.sub(r"[\W_]+", "-", slug).strip("-")

    # Replace a few special characters that normalize doesn't handle
    specials = {"æ": "ae", "ß": "ss", "ø": "o"}
    for s, r in specials.items():
        slug = slug.replace(s, r)

    # Normalize the non-ASCII text
    slug = normalize("NFKD", slug).encode("ascii", "ignore").decode()

    # Return the transformed string
    return slug


def log(message, level="info"):
    """Log messages with color depending on the level."""
    if level == "info":
        print(f"{Fore.GREEN}[INFO] {Style.RESET_ALL}{message}")
    elif level == "warning":
        print(f"{Fore.YELLOW}[WARNING] {Style.RESET_ALL}{message}")
    elif level == "error":
        print(f"{Fore.RED}[ERROR] {Style.RESET_ALL}{message}")
