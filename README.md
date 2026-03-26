# Word Frequency Indexer

# AI Statement 
 not used for code used it for UI
# Overview

This project implements the foundation of a **Word Frequency Indexer** using a custom-built **Hash Table with chaining**.

This README covers implementation up to:

* Imports & setup
* Core data structure design
* Linked list node (`ChainNode`)


## Setup Instructions

### 1. Install Dependencies

pip install requests

### 2. Run 
``` 
python app.py

```




##  Implemented Components

### 1. Imports

Libraries used:

* re → text processing
* requests → dataset fetching 
* math → hashing
* time → benchmarking
* typing.Optional → type hints

### 2. Data Structure Design

#### ChainNode

A singly linked list node used for handling hash collisions.

#### Attributes:

* word → stores the word
* count → number of occurrences
* line_numbers → list of line indices
* next → pointer to next node

### 3. Key Features

* Custom memory-efficient structure using `__slots__`
* No use of Python dictionaries
* Designed for collision handling using chaining


##  Verification

Test the implementation:
node = ChainNode("example")
print(node.word)

Expected output:     
example
 
## UI 
we have created UI using gradio