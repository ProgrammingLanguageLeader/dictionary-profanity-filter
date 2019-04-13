from typing import List, Sequence
import os


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

    def set_censor_char(self, character: str) -> None:
        self._censor_char = character

    def get_censor_list(self) -> List[str]:
        return self._censor_list

    def get_extra_censor_list(self) -> List[str]:
        return self._extra_censor_list

    def add_words(self, words: Sequence[str]) -> None:
        if isinstance(words, str):
            self._extra_censor_list.append(words)
            return
        self._extra_censor_list += list(words)

    def remove_word(self, word: str) -> None:
        self._extra_censor_list.remove(word)

    def censor(self, input_text: str) -> str:
        pass

    def is_clean(self, input_text: str) -> bool:
        pass

    def is_profane(self, input_text: str) -> bool:
        return not self.is_clean(input_text)
