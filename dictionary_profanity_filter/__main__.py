import sys


if __name__ == "__main__":
	print("This is the main routine.")
	print("It should do something interesting.")

	print("This is the name of the script: ", sys.argv[0])
	print("Number of arguments: ", len(sys.argv))
	print("The arguments are: ", str(sys.argv))
