import csv
import random

#Handle user's letter guesses
def letter_guess(encoded_letter,decoded_letter, cur_phrase):
	if decoded_letter in cipher.keys():
		if cipher[decoded_letter]==encoded_letter:
			cur_phrase = "".join(cur_phrase).replace(encoded_letter,decoded_letter.lower())
			return cur_phrase
	else:
		return "WRONG!"
		
#Add user's guesses to the guess dictionary
def add_guess (encoded_letter,decoded_letter,guess_dict):
	if encoded_letter in guess_dict.keys():
		guess_dict[encoded_letter].append(decoded_letter)
	else: 
		guess_dict[encoded_letter] = [decoded_letter]


def choose_phrase(phrase_file):
	"Randomly selects a phrase from the phrase_file and sets it to uppercase"
	phrase = [line for line in phrase_file]
	answer_mixed=random.choice(phrase)
	answer=answer_mixed.upper().strip()
	print "answer:"
	print answer
	return answer

def build_cipher(answer, alphabet):
	"builds a set of the unique letters in answer, then builds a cipher for that answer"
	all_letters = []
	for letter in answer:
		if letter in alphabet:
			all_letters.extend(letter)
	unique_letters = set(all_letters)	
	
	#Build a dictionary, cipher, whose keys are the unique letters in the phrase (actual letters) and whose values (encoded letters) are randomly selected on two criteria: each encoded letter can only be selected once and the encoded letter cannot be the same as the actual letter
	cipher = {}
	avail_letters = alphabet
	for cipher_letter in unique_letters:
		candidate_letters = [item for item in avail_letters if item not in cipher_letter]
		cipher[cipher_letter] = random.choice(candidate_letters)
		avail_letters=[item for item in avail_letters if item not in cipher[cipher_letter]]
				
	print "cipher:"
	print cipher
	return cipher
	
def build_encoded_answer(answer, cipher, alphabet):
	"""Build the encoded answer by replacing the actual letters with the encoded letters, preserving spaces and other punctuation from the original phrase. Sets cur_phrase = the encoded_phrase list. cur_phrase will be modified as the user guesses correct parts of the cipher"""
	
	encoded_answer = []
	for character in answer:
		if character in alphabet:
			encoded_answer.append(cipher.get(character))
		else:
			encoded_answer.append(character)	
	print "encoded_answer:"
	print "".join(encoded_answer)
	return "".join(encoded_answer)
	
#cur_phrase = "".join(encoded_answer)
#print "cur_phrase is {0} ".format(cur_phrase)


def handle_valid_guess(encoded_letter, decoded_letter, encoded_answer, cipher, guess_dict, cur_phrase):
	"Add the guess to guess_dict. If it's correct, update cur_phrase. If not, tell the user it's wrong." 
	add_guess(encoded_letter,decoded_letter,guess_dict)
	#print letter_guess(encoded_letter,decoded_letter,cur_phrase)
	if decoded_letter in cipher.keys():
		if cipher[decoded_letter]==encoded_letter:
			print "Yes, " + encoded_letter + " does represent " + decoded_letter + "!"
			cur_phrase = "".join(cur_phrase).replace(encoded_letter,decoded_letter.lower())
		else:
			print "WRONG!"
			print "cur_phrase is " + cur_phrase		
	return cur_phrase		
					
		
def win_play_again(solution):
	"Tell the user that s/he's won and see if s/he wants to play again."
	print "Your answer, so hot right now!"
	print solution.upper() + " is correct!"
	play_again = raw_input('Play again?(Y/N): ').upper()
	while play_again not in ('Y', 'N'):
		play_again = raw_input('Invalid entry. Play again?(Y/N): ').upper()
	if play_again == 'Y':
		return 1
	else:
		return 0
		
def print_guesses(guess_dict):
	"Prints all the user's guesses and how many guesses it took to solve the puzzle"
	count = 0
	print "Encoded letter\tGuesses"
	for k, v in guess_dict.iteritems():
		count = count+1
		print k+":\t\t:",
		print v
	print "You solved this in {0} guesses!".format(count)
	
#a list of all letters in the alphabet
alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

#Intro message to user:
print "Khiyali made up this cool cryptography game when she was six.\nShe'd give me a phrase that was encrypted with a cipher she'd generate\non the fly by assigning each letter to a different letter of the alphabet.\nThen I'd have to guess, e.g. 'Does E mean T?' and when I guessed correctly\nshe'd re-write the encrypted phrase with the decrypted letters in lowercase.\nAt any point, I could guess the phrase if I was ready.\n"
print "Let's play the code game!\n"
#Loop that handles the possible choices a user can make, and sends inputs to respective functions
keep_playing = 1
while keep_playing:
	#Choose a random phrase and encode it with a cipher
	with open ('phrases.csv', 'r') as phrase_file:
		answer = choose_phrase(phrase_file)
	cipher = build_cipher(answer, alphabet)
	encoded_answer = build_encoded_answer(answer, cipher, alphabet)
	cur_phrase = encoded_answer
	
	#initialize the guess dictionary guess_dict, which will store the player's guesses during a given round
	guess_dict={}
	
	choice = ''
	won = 0
	while ((choice != 'Q') and not won and keep_playing):
		#Does the user want to guess a letter, solve the puzzle, or quit?
		choice = raw_input('Would you like to "G"uess a letter or "S"olve the puzzle or "Q"uit? ').upper()
		if choice == 'G':
			#User wants to guess a letter
			keep_guessing = 1
			while keep_guessing:
				encoded_letter = raw_input('Enter the letter you wish to decode: ').upper()
				if len(encoded_letter) > 1:
					print "You may only enter one letter at a time. Please try again."
				elif (encoded_letter in encoded_answer):
					#User has chosen a letter in the code to decode
					keep_guessing = 0
					decoded_letter = raw_input('Enter the letter you think is represented by {0}: '.format(encoded_letter)).upper()
					try:
						if encoded_letter in guess_dict.get(decoded_letter):
							#User has already guessed this combination
							print "You've already guessed that!"
					except:
						#User has made a new guess consisting of letter in the code and its possible value
						cur_phrase = handle_valid_guess(encoded_letter, decoded_letter, encoded_answer, cipher, guess_dict, cur_phrase)
						if cur_phrase.upper()==answer:
							#User has guessed the last value needed to solve the puzzle
							won = 1
							print_guesses(guess_dict)
							keep_playing = win_play_again(answer)
					#print the current state of the guess dictionary
					#print "guess_dict:"
					#print guess_dict
				else:
					#User has chosen a letter to decode that is not part of the encoded phrase
					print encoded_letter + " is not part of the encoded phrase. Please try again."
					print "cur_phrase is " + cur_phrase					
		elif choice =='S':
		#Handle solve
			solution = raw_input('Please enter your solution: ')
			print "Solution:"
			print solution.upper()	
			if solution.upper() == answer:
				won = 1
				keep_playing = win_play_again(answer)
				print_guesses(guess_dict)
		elif choice =='Q':
			keep_playing = 0
			print "Kthxbai!"
			break
		else:
			print "invalid entry; please try again"
