Dictionary Profanity Filter
==========================

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
```python
from dictionary_profanity_filter import ProfanityFilter

profanity_filter = ProfanityFilter()
profanity_filter.add_words(['censorship', 'blocking'])
profanity_filter.censor('I hate censorship and blocking!')
# Output: 'I hate ********** and ********!'

profanity_filter.is_clean('Porn is a restricted word')
# Output: False

profanity_filter.remove_word('blocking')
profanity_filter.censor('I hate censorship and blocking!')
# Output: 'I hate ********** and blocking!'
```

## TODO
- [ ] Write documentation
- [ ] Write tests
