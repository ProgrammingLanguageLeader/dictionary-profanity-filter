import os


class ProfanityFilter:
    def __init__(
            self,
            custom_censor_list: list = None,
            extra_censor_list: list = None,
            no_word_boundaries: bool = False,
            censor_char: str = '*'
    ) -> None:
        self._censor_list = custom_censor_list or []
        self._extra_censor_list = extra_censor_list or []
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

    def set_censor_char(self, character) -> None:
        self._censor_char = character

    def get_censor_list(self) -> list:
        return self._censor_list

    def get_extra_censor_list(self) -> list:
        return self._extra_censor_list

    def add_word(self, word_list) -> None:
        pass

    def remove_word(self, word) -> None:
        pass

    def censor(self, input_text) -> str:
        pass

    def is_clean(self, input_text) -> bool:
        pass

    def is_profane(self, input_text) -> bool:
        return not self.is_clean(input_text)
