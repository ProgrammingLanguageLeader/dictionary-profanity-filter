import unittest

from dictionary_profanity_filter import ProfanityFilter


class TestProfanityFilter(unittest.TestCase):
    def setUp(self):
        self.profanity_filter = ProfanityFilter(use_word_cases=True)

    def test_is_clean(self):
        self.assertEqual(
            self.profanity_filter.is_clean('Шах и мат!'),
            True
        )
        self.assertEqual(
            self.profanity_filter.is_clean('Motherfucker'),
            False
        )

    def test_is_profane(self):
        self.assertEqual(
            self.profanity_filter.is_profane('Говно жопа'),
            True
        )
        self.assertEqual(
            self.profanity_filter.is_profane('Skyrim is amazing'),
            False
        )

    def test_censor(self):
        self.assertEqual(
            self.profanity_filter.censor('This module is great!'),
            'This module is great!'
        )
        self.assertEqual(
            self.profanity_filter.censor('This module is fucking great!'),
            'This module is ******* great!'
        )

    def test_set_censor_char(self):
        self.profanity_filter.censor_char = '#'
        self.assertEqual(
            self.profanity_filter.censor('Fuck you'),
            '#### you'
        )

    def test_add_words(self):
        self.profanity_filter.add_words('kappa')
        self.assertEqual(
            self.profanity_filter.is_clean('Hey Kappa Kappa hey'),
            False
        )

    def test_remove_word(self):
        self.test_add_words()
        self.profanity_filter.remove_word('kappa')
        self.assertEqual(
            self.profanity_filter.is_clean('Hey Kappa Kappa hey'),
            True
        )
