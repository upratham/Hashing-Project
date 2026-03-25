from datetime import datetime
from pathlib import Path
import re
def find_root() -> Path:
    """Walk up from cwd until pyproject.toml is found."""
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / "pyproject.toml").exists():
            return parent
    return current  # fallback

ROOT = find_root()

# Constants for Hash Table implementation
SLOTS=("word", "count", "line_numbers", "next")
BASE   = 31          # prime base for polynomial hash
MOD    = 1_000_003   # large prime modulus
MAX_LF = 0.75        # resize threshold
STOP_WORDS = set()
TOKEN_RE = re.compile(r"[a-zA-Z]+(?:'[a-zA-Z]+)*") 


# Constants for log configuration
LOG_DIR = 'logs'
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 3

#Constants for Dowanload and preprocess text
GUTENBERG_URL = "https://gutenberg.org/files/1513/1513-0.txt"
START_MARKER = "*** START OF THE PROJECT GUTENBERG EBOOK"
END_MARKER   = "*** END OF THE PROJECT GUTENBERG EBOOK"