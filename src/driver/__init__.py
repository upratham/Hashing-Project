from src.Hash import HashTable, ChainNode, tokenize
from src.constants import *
from src.logger import logging
from src.preprocess_text import PreprocessText
logging.getLogger("matplotlib.font_manager").setLevel(logging.WARNING)
ht = HashTable()
raw_text = PreprocessText.load_text()
tokens, lines = PreprocessText.preprocess_text(raw_text)
def run():
   
 
    for line_number, line in enumerate(tokens, start=1):
        for word in tokenize(line):
            ht.insert(word, line_number)


    # Example: print some statistics
    logging.info(f"Total distinct words: {ht._size}")
    logging.info(f"Load factor: {ht.load_factor:.4f}")
    logging.info(f"Collision count: {ht._collisions}")
    logging.info(f"Capacity: {ht._capacity}")

def context_snippet(line_no: int, window: int = 2) -> str:
    start = max(0, line_no - 1 - window)
    end   = min(len(lines), line_no + window)
    snippet = ""
    for i, ln in enumerate(lines[start:end], start=start + 1):
        marker = ">>> " if i == line_no else "    "
        snippet += f"{marker}[{i:>4}] {ln}\n"
    return snippet


def word_search(word: str, show_context: bool, max_ctx: int):
    word = word.strip().lower()
    if not word:
        return "Please enter a word.", ""

    node = ht.search(word)
    if node is None:
        return f'❌  "{word}" was not found in Romeo and Juliet.', ""

    unique_lines = sorted(set(node.line_numbers))
    summary = (
        f"**Word:** `{node.word}`\n"
        f"**Total occurrences:** {node.count}\n"
        f"**Appears on {len(unique_lines)} unique line(s):** "
        + ", ".join(str(l) for l in unique_lines[:50])
        + (" …" if len(unique_lines) > 50 else "")
    )

  
    return summary
if __name__ == "__main__":
    run()
    summary = word_search("love", show_context=True, max_ctx=5)
    print(summary)
   