from dictionary_profanity_filter.profanity_filter import ProfanityFilter


if __name__ == "__main__":
	profanity_filter = ProfanityFilter()
	print(profanity_filter.get_censor_list())
