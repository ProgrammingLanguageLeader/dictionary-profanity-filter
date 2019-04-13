from typing import List, Sequence
import os
import re

import inflection


class ProfanityFilter:
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
        complete_censor_list.extend([
            inflection.pluralize(word)
            for word in complete_censor_list
        ])
        return list(set(complete_censor_list))

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
            self._extra_censor_list.append(words)
            return
        self._extra_censor_list += list(words)
        self._complete_censor_list.extend([
            inflection.pluralize(word)
            for word in words
        ])
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
