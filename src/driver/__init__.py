from src.Hash import HashTable, ChainNode, tokenize
from src.constants import *
from src.logger import logging
from src.preprocess_text import PreprocessText
logging.getLogger("matplotlib.font_manager").setLevel(logging.WARNING)

def run():
    # Download and preprocess text
    raw_text = PreprocessText.download_text()
    tokens   = PreprocessText.preprocess_text(raw_text)
    # Create hash table and insert tokens
    hash_table = HashTable()
    for line_number, line in enumerate(tokens, start=1):
        for word in tokenize(line):
            hash_table.insert(word, line_number)


    # Example: print some statistics
    logging.info(f"Total distinct words: {hash_table._size}")
    logging.info(f"Load factor: {hash_table.load_factor:.4f}")
    logging.info(f"Collision count: {hash_table._collisions}")
    logging.info(f"Capacity: {hash_table._capacity}")
  
    return 