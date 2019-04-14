# Dictionary Profanity Filter

[![Build Status](https://travis-ci.com/ProgrammingLanguageLeader/dictionary-profanity-filter.svg?token=NAXdZ3urs2rzWv4x9zhq&branch=master)](https://travis-ci.com/ProgrammingLanguageLeader/dictionary-profanity-filter)
[![PyPI version](https://badge.fury.io/py/dictionary-profanity-filter.svg)](https://badge.fury.io/py/dictionary-profanity-filter)

Python module for profanity filtering using dictionaries. 
It supports English and Russian languages out-of-the-box.

## Requirements
- Python 3.5 or higher

## How to install
Use the following command to install the package using pip:
```bash
pip install dictionary-profanity-filter
```

## How to use
Here are several examples of the module usage:

- Creating ProfanityFilter instance:

```python
from dictionary_profanity_filter import ProfanityFilter
profanity_filter = ProfanityFilter()
```

- Adding custom words to censor:

```python
profanity_filter.add_words(['censorship', 'blocking'])
profanity_filter.censor('I hate censorship and blocking!')
# Output: 'I hate ********** and ********!'
```

- Detect bad words in the text:

```python
profanity_filter.is_clean('Porn is a restricted word')
# Output: False
```

- Removing word from custom dictionary:
 
```python
profanity_filter.remove_word('blocking')
profanity_filter.censor('I hate censorship and blocking!')
# Output: 'I hate ********** and blocking!'
```

## TODO
- [ ] Write documentation
- [x] Write tests
