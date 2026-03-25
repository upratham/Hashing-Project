import re
import requests
import math
import time
from typing import Optional
from src.constants import *
from src.logger import logging
logging.getLogger("matplotlib.font_manager").setLevel(logging.WARNING)

# Node in the chained linked list
class ChainNode:
    """A single node in a singly-linked list used for collision chaining."""
    __slots__ = SLOTS
    

    def __init__(self, word: str):
        self.word: str        = word
        self.count: int       = 0
        self.line_numbers: list = []   # every line number this word appears on
        self.next: Optional["ChainNode"] = None

    def __repr__(self):
        return f"ChainNode(word={self.word!r}, count={self.count})"


# Hash Table implementation
class HashTable:
    """
    Custom hash table with:
      - Polynomial rolling hash function
      - Separate chaining for collision resolution
      - Dynamic resize (doubles capacity when load factor > 0.75)
    """

    _BASE   = BASE          # prime base for polynomial hash
    _MOD    = MOD   # large prime modulus
    _MAX_LF = MAX_LF        # resize threshold


    def __init__(self, capacity: int = 1024):
        self._capacity  = capacity
        self._size      = 0          # number of distinct keys
        self._buckets   = [None] * self._capacity   # array of ChainNode heads
        self._collisions = 0         # cumulative collision counter

    # ── Hash Function ────────────────────────────────────────────────────
    def _hash(self, word: str) -> int:
        """
        Polynomial rolling hash:
            h = (c0·BASE^(n-1) + c1·BASE^(n-2) + … + c_{n-1}) mod MOD
        Then compressed to [0, capacity) via modulo.
        """
        h = 0
        for ch in word:
            h = (h * self._BASE + ord(ch)) % self._MOD
        return h % self._capacity

    # ── Insert / Update ──────────────────────────────────────────────────
    def insert(self, word: str, line_number: int) -> None:
        """Insert a word occurrence.  Creates a new entry or increments count."""
        # Resize before inserting if load factor exceeded
        if self._size / self._capacity >= self._MAX_LF:
            self._resize()

        idx  = self._hash(word)
        node = self._buckets[idx]

        # Walk the chain
        while node is not None:
            if node.word == word:
                node.count += 1
                node.line_numbers.append(line_number)
                return
            node = node.next

        # Word not found → prepend new node
        if self._buckets[idx] is not None:
            self._collisions += 1   # bucket was already occupied

        new_node           = ChainNode(word)
        new_node.count     = 1
        new_node.line_numbers = [line_number]
        new_node.next      = self._buckets[idx]
        self._buckets[idx] = new_node
        self._size        += 1

    #  Search
    def search(self, word: str) -> Optional[ChainNode]:
        """Return the ChainNode for *word*, or None if absent."""
        idx  = self._hash(word.lower().strip())
        node = self._buckets[idx]
        while node:
            if node.word == word.lower().strip():
                return node
            node = node.next
        return None

    #  Delete 
    def delete(self, word: str) -> bool:
        """Remove the entry for *word*.  Returns True if found & removed."""
        idx  = self._hash(word)
        prev = None
        node = self._buckets[idx]
        while node:
            if node.word == word:
                if prev:
                    prev.next = node.next
                else:
                    self._buckets[idx] = node.next
                self._size -= 1
                return True
            prev = node
            node = node.next
        return False

    # Resize 
    def _resize(self) -> None:
        """Double the capacity and rehash all entries."""
        old_buckets    = self._buckets
        self._capacity = self._capacity * 2
        self._buckets  = [None] * self._capacity
        self._size     = 0

        for head in old_buckets:
            node = head
            while node:
                for ln in node.line_numbers:
                    self.insert(node.word, ln)
         
                node = node.next

    # Utility: all entries
    def all_entries(self) -> list:
        """Return a flat list of all ChainNode objects."""
        entries = []
        for head in self._buckets:
            node = head
            while node:
                entries.append(node)
                node = node.next
        return entries

    # Statistics
    @property
    def load_factor(self) -> float:
        return self._size / self._capacity

    @property
    def distinct_words(self) -> int:
        return self._size

    def bucket_distribution(self) -> dict:
        """Count how many buckets have 0, 1, 2, … nodes (for analysis)."""
        dist: dict = {}
        for head in self._buckets:
            depth = 0
            node  = head
            while node:
                depth += 1
                node   = node.next
            dist[depth] = dist.get(depth, 0) + 1
        return dict(sorted(dist.items()))

logging.info("HashTable class defined.")

def tokenize(line: str) -> list:
    """Extract lowercase alphabetic tokens (contractions intact)."""
    return TOKEN_RE.findall(line.lower())

