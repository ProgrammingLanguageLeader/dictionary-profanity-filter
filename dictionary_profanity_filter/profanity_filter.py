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
            censor_char: str = '*',
            use_word_cases: bool = False,
    ) -> None:
        self.censor_list = list(custom_censor_list or [])
        self.extra_censor_list = list(extra_censor_list or [])
        self.no_word_boundaries = no_word_boundaries
        self.use_word_cases = use_word_cases
        self.complete_censor_list = []
        self.censor_char = censor_char
        self.morph_analyzer = pymorphy2.MorphAnalyzer()
        if not custom_censor_list:
            self.load_words()
        self.complete_censor_list = self.calc_complete_censor_list()

    def load_words(self) -> None:
        base_dir = os.path.abspath(os.path.dirname(__file__))
        words_file_path = os.path.join(
            base_dir,
            'data',
            'default_list.txt'
        )
        with open(words_file_path, 'r') as words_file:
            self.censor_list = [
                line.strip() for line in words_file.readlines()
            ]

    def calc_complete_censor_list(self) -> List[str]:
        complete_censor_list = []
        complete_censor_list.extend(self.censor_list)
        complete_censor_list.extend(self.extra_censor_list)
        pluralized_words = self.get_words_cases(complete_censor_list)
        complete_censor_list.extend(pluralized_words)
        return list(set(complete_censor_list))

    def get_words_cases(self, words: Sequence[str]) -> List[str]:
        pluralized_words = []
        alphabet_detector = AlphabetDetector()
        if isinstance(words, str):
            words = [words]
        for word in words:
            alphabets = alphabet_detector.detect_alphabet(word)
            if 'LATIN' in alphabets:
                pluralized_words.append(inflection.pluralize(word))
            elif 'CYRILLIC' in alphabets:
                pluralized_words += self.get_cyrillic_word_cases(word)
            else:
                self.logger.warn(
                    'Unsupported language for text: {}'.format(
                        word
                    )
                )
        return pluralized_words

    def get_cyrillic_word_cases(self, word: str) -> List[str]:
        cyrillic_word_cases = []
        parsed_word = self.morph_analyzer.parse(word)[0]
        if self.use_word_cases:
            cyrillic_word_cases += [
                word_form.word for word_form in parsed_word.lexeme
            ]
        parsed_word = parsed_word.inflect({'plur'})
        if self.use_word_cases and parsed_word:
            cyrillic_word_cases += [
                word_form.word for word_form in parsed_word.lexeme
            ]
        elif parsed_word:
            cyrillic_word_cases.append(parsed_word.word)
        return cyrillic_word_cases

    def add_words(self, words: Sequence[str]) -> None:
        if isinstance(words, str):
            words = [words]
        words = list(words)
        self.extra_censor_list += words
        self.complete_censor_list += words
        self.complete_censor_list += self.get_words_cases(words)
        self.complete_censor_list = list(set(self.complete_censor_list))

    def remove_word(self, word: str) -> None:
        self.extra_censor_list.remove(word)
        pluralized_words = self.get_words_cases(word)
        for pluralized_word in pluralized_words:
            self.complete_censor_list.remove(pluralized_word)
        self.complete_censor_list.remove(word)

    def censor(self, input_text: str) -> str:
        censored_text = input_text
        for word in self.complete_censor_list:
            regex_string = r'{0}' if self.no_word_boundaries else r'\b{0}\b'
            regex_string = regex_string.format(word)
            regex = re.compile(regex_string, re.IGNORECASE)
            censored_text = regex.sub(
                self.censor_char * len(word),
                censored_text
            )
        return censored_text

    def is_clean(self, input_text: str) -> bool:
        for word in self.complete_censor_list:
            regex_string = r'{0}' if self.no_word_boundaries else r'\b{0}\b'
            regex_string = regex_string.format(word)
            regex = re.compile(regex_string, re.IGNORECASE)
            if regex.search(input_text):
                return False
        return True

    def is_profane(self, input_text: str) -> bool:
        return not self.is_clean(input_text)
