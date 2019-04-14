from dictionary_profanity_filter import ProfanityFilter


if __name__ == "__main__":
	profanity_filter = ProfanityFilter()
	print(
		'Filter has {} words'.format(
			len(profanity_filter.get_complete_censor_list())
		)
	)
	profanity_filter.add_words('censorship')
	profanity_filter.add_words(('blocking', ))
	print(profanity_filter.get_extra_censor_list())
	print(
		'Filter has {} words'.format(
			len(profanity_filter.get_complete_censor_list())
		)
	)
	print(profanity_filter.censor('Censorship and blocking'))
	print(profanity_filter.censor('Porn is a restricted word!'))
	print(profanity_filter.is_profane('Porn is a restricted word!'))
