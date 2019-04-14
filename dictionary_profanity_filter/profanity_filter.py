from typing import List, Sequence
import os
import re
import logging

from alphabet_detector import AlphabetDetector
import inflection
import pymorphy2


class ProfanityFilter:
    logger = logging.getLogger('dictionary_profanity_filter')
    logger.setLevel('INFO')
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(handler)

    def __init__(
            self,
            custom_censor_list: Sequence[str] = None,
            extra_censor_list: Sequence[str] = None,
            no_word_boundaries: bool = False,
            censor_char: str = '*'
    ) -> None:
        self._censor_list = list(custom_censor_list or [])
        self._extra_censor_list = list(extra_censor_list or [])
        self._no_word_boundaries = no_word_boundaries
        self._complete_censor_list = []
        self._censor_char = censor_char
        self._morph_analyzer = pymorphy2.MorphAnalyzer()
        if not custom_censor_list:
            self._load_words()
        self._complete_censor_list = self._calc_complete_censor_list()

    def _load_words(self) -> None:
        base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..')
        )
        words_file_path = os.path.join(
            base_dir,
            'data',
            'default_list.txt'
        )
        with open(words_file_path, 'r') as words_file:
            self._censor_list = [
                line.strip() for line in words_file.readlines()
            ]

    def _calc_complete_censor_list(self) -> List[str]:
        complete_censor_list = []
        complete_censor_list.extend(self._censor_list)
        complete_censor_list.extend(self._extra_censor_list)
        pluralized_words = self._pluralize_words(complete_censor_list)
        complete_censor_list.extend(pluralized_words)
        return list(set(complete_censor_list))

    def _pluralize_words(self, words: Sequence[str]) -> List[str]:
        pluralized_words = []
        alphabet_detector = AlphabetDetector()
        if isinstance(words, str):
            words = [words]
        for word in words:
            alphabets = alphabet_detector.detect_alphabet(word)
            if 'LATIN' in alphabets:
                pluralized_words.append(inflection.pluralize(word))
            elif 'CYRILLIC' in alphabets:
                parsed_word = self._morph_analyzer.parse(word)[0]
                inflected_word = parsed_word.inflect({'plur'})
                if inflected_word:
                    pluralized_words.append(inflected_word.word)
            else:
                self.logger.warn(
                    'Unsupported language for text: {}'.format(
                        word
                    )
                )
        return pluralized_words

    def set_censor_char(self, character: str) -> None:
        self._censor_char = character

    def get_censor_list(self) -> List[str]:
        return self._censor_list

    def get_extra_censor_list(self) -> List[str]:
        return self._extra_censor_list

    def get_complete_censor_list(self) -> List[str]:
        return self._complete_censor_list

    def add_words(self, words: Sequence[str]) -> None:
        if isinstance(words, str):
            words = [words]
        self._extra_censor_list += list(words)
        self._complete_censor_list += self._pluralize_words(words)
        self._complete_censor_list = list(set(self._complete_censor_list))

    def remove_word(self, word: str) -> None:
        self._extra_censor_list.remove(word)
        for pluralized_word in inflection.pluralize(word):
            self._complete_censor_list.remove(pluralized_word)
        self._complete_censor_list.remove(word)

    def censor(self, input_text: str) -> str:
        censored_text = input_text
        for word in self._complete_censor_list:
            regex_string = r'{0}' if self._no_word_boundaries else r'\b{0}\b'
            regex_string = regex_string.format(word)
            regex = re.compile(regex_string, re.IGNORECASE)
            censored_text = regex.sub(
                self._censor_char * len(word),
                censored_text
            )
        return censored_text

    def is_clean(self, input_text: str) -> bool:
        for word in self._complete_censor_list:
            regex_string = r'{0}' if self._no_word_boundaries else r'\b{0}\b'
            regex_string = regex_string.format(word)
            regex = re.compile(regex_string, re.IGNORECASE)
            if re.match(regex, input_text):
                return False
        return True

    def is_profane(self, input_text: str) -> bool:
        return not self.is_clean(input_text)
