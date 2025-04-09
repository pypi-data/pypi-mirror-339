# 📚 Rdlab Dataset

## Overview
The Rdlab Dataset is a collection of various Khmer datasets useful for research and development (R&D) in Cambodia.
It includes datasets for wild Khmer words, Khmer addresses, and Khmer sentences, all packed and ready for easy loading.

# 📊 Dataset Overview Version 0.0.1

| Dataset Name            | Number of Records |
|--------------------------|-------------------|
| Khmer Address Dataset    | 20,817             |
| Khmer Sentence Dataset   | 211,928            |
| Khmer Word Dataset       | 784,011            |

## Installation

To install this package, run the following command:

```bash
pip install rdlab_dataset
```

## Usage
The module provides three main loaders to easily access the datasets:
- **KhmerWordLoader** — load Khmer word dataset
- **KhmerAddressLoader** — load Khmer address dataset
- **KhmerSentencesLoader** — load Khmer sentence dataset

## Example
### 📚 KhmerWordLoader - Usage
```python

# 1. Import the class
from rdlab_dataset.module import KhmerWordLoader

# 2. Initialize the loader
word_loader = KhmerWordLoader()

# 3. Get all words
all_words = word_loader.get_all_words()
print(all_words)

# 4. Get the first word
first_word = word_loader.get_first_word()
print(first_word)

# 5. Get the first N words (e.g., 5 words)
first_five_words = word_loader.get_n_first_words(5)
print(first_five_words)

# 6. Find if a specific word exists
is_found = word_loader.find_word("សេចក្ដី")
print(is_found)  # True or False

# 7. Check the number of words (using __sizeof__)
number_of_words = word_loader.__sizeof__()
print(number_of_words)

```

### 🏡 KhmerAddressLoader - Usage
```python

# 1. Import the class
from rdlab-dataset.module import KhmerAddressLoader

# 2. Initialize the loader
address_loader = KhmerAddressLoader()

# 3. Get all words
all_addresses = address_loader.get_all_addresses()
print(all_addresses)

# 4. Get the first word
first_address = address_loader.get_first_address()
print(first_address)

# 5. Get the first N words (e.g., 5 words)
first_five_addresses = address_loader.get_n_first_addresses(5)
print(first_five_addresses)

# 6. Find if a specific word exists
is_found = address_loader.find_address("ភ្នំពេញ")
print(is_found)  # True or False

# 7. Check the number of words (using __sizeof__)
number_of_addresses = address_loader.__sizeof__()
print(number_of_addresses)

```

## Features 
- Easy to load datasets (.pkl format) ✅
- Check if a word, address, or sentence exists ✅
- Get all data, first data, or n first items ✅
- Lightweight and fast ✅

## Contributing
Contributions to this module are welcome. Please feel free to fork the repository, make changes, and submit a pull request.

## License
This project is licensed under the Rdlab Community License.
Telegram: 0964060587