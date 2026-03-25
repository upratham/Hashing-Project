from src.Hash import HashTable , ChainNode
from src.constants import *
from src.logger import logging
import requests
import re
logging.getLogger("matplotlib.font_manager").setLevel(logging.WARNING)


class PreprocessText:
    """Class to handle downloading and preprocessing text data."""

    @staticmethod
    def download_text(url: str = GUTENBERG_URL) -> str:
        """Download text from the specified URL."""
        logging.info(f"Downloading text from {url}...")
        response = requests.get(GUTENBERG_URL, timeout=30)
        response.raise_for_status()
        logging.info("Download successful.")
        return response.text
    
    @staticmethod
    def preprocess_text(raw_text: str) -> list:
        """Preprocess the raw text by extracting the main content and tokenizing."""
        logging.info("Preprocessing text...")
        # Extract main content between markers
        start_idx = raw_text.find(START_MARKER)
        end_idx   = raw_text.find(END_MARKER)
        if start_idx == -1 or end_idx == -1:
            logging.warning("Start or end marker not found. Using full text.")
            main_text = raw_text
        else:
            main_text = raw_text[start_idx + len(START_MARKER):end_idx]
        
        lines= main_text.splitlines()
        # Tokenize: split on non-alphanumeric characters, convert to lowercase
        tokens = [word.lower() for word in re.split(r'\W+', main_text) if word]
        logging.info(f"Preprocessing complete. Total tokens: {len(tokens)}")
        return tokens,lines
