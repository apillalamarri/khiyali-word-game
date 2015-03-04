import csv
import random

#a list of all letters in the alphabet
alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

#print alphabet


#open the CSV file with one phrase per line and then randomly select a phrase and set it to upper case
with open ('phrases.csv', 'r') as phrasefile:
	phrase = [line for line in phrasefile]
	answer_mixed=random.choice(phrase)
	answer=answer_mixed.upper().strip()

#build a list of all of the letters in the selected phrase, and identify the unique set of letters in the phrase
all_letters = []
for letter in answer:
	if letter in alphabet:
		all_letters.extend(letter)
unique_letters = set(all_letters)	

print "answer:"
print answer

#Build a dictionary, cipher, whose keys are the unique letters in the phrase (actual letters) and whose values (encoded letters) are randomly selected on two criteria: each encoded letter can only be selected once and the encoded letter cannot be the same as the actual letter
cipher = {}
avail_letters = alphabet
for cipher_letter in unique_letters:
	candidate_letters = [item for item in avail_letters if item not in cipher_letter]
	cipher[cipher_letter] = random.choice(candidate_letters)
	avail_letters=[item for item in avail_letters if item not in cipher[cipher_letter]]
			
print "cipher:"
print cipher

"""Build the encoded phrase by replacing the actual letters with the encoded letters, 
preserving spaces and other punctuation from the original phrase. Sets cur_phrase = the encoded_phrase list.
cur+phrase will be modified as the user guesses correct parts of the cipher
"""
encoded_answer = []
for character in answer:
	if character in alphabet:
		encoded_answer.append(cipher.get(character))
	else:
		encoded_answer.append(character)	
print "encoded_answer:"
print "".join(encoded_answer)
cur_phrase = "".join(encoded_answer)
print "cur_phrase is {0} ".format(cur_phrase)

#Function that handles the user's input
def letter_guess(encoded_letter,decoded_letter, cur_phrase):
	if decoded_letter in cipher.keys():
			
		if cipher[decoded_letter]==encoded_letter:
			cur_phrase = "".join(cur_phrase).replace(encoded_letter,decoded_letter.lower())
			return cur_phrase
	else:
		return "WRONG!"


def add_guess (encoded_letter,decoded_letter,guess_dict):
	if encoded_letter in guess_dict.keys():
		guess_dict[encoded_letter].append(decoded_letter)
	else: 
		guess_dict[encoded_letter] = [decoded_letter]


#Loop that handles the possible choices a user can make, and sends inputs to respective functions		
guess_dict={}

while True:
	
	choice = raw_input('Would you like to "G"uess a letter or "S"olve the puzzle or "Q"uit? ')
	if choice.upper() == 'G':
		keep_guessing = 1
		while keep_guessing:
			encoded_letter = raw_input('Enter the letter you wish to decode: ').upper()
			if (encoded_letter in encoded_answer):
				keep_guessing = 0
				decoded_letter = raw_input('Enter the letter you think is represented by {0}: '.format(encoded_letter)).upper()
				#print letter_guess(encoded_letter,decoded_letter,cur_phrase)
				if decoded_letter in cipher.keys():		
					if cipher[decoded_letter]==encoded_letter:
						cur_phrase = "".join(cur_phrase).replace(encoded_letter,decoded_letter.lower())
						if cur_phrase.upper()==answer:
							print "Your answer, so hot right now!"
							print cur_phrase.upper()+" is correct!"
							break
						else:
							print "cur_phrase is " + cur_phrase
				else:
					print "WRONG!"
					print "cur_phrase is " + cur_phrase
				
				
				
				add_guess(encoded_letter,decoded_letter,guess_dict)
				#print current_phrase(cur_phrase,encoded_letter,decoded_letter)
				print "guess_dict:"
				print guess_dict
				
			elif len(encoded_letter) > 1:
				print "You may only enter one letter at a time. Please try again."
			else:
				print encoded_letter + " is not part of the encoded phrase. Please try again."
			
				
	
	#Handle letter guess
	elif choice.upper() =='S':
	
	#Handle solve
		solution = raw_input('Please enter your solution: ')
		print "Solution:"
		print solution.upper()
		
		if solution.upper() == answer:
			print "Your answer, so hot right now!"
			print solution.upper() + " is correct!"
			break
	elif choice.upper() =='Q':
		print "Kthxbai!"
		break
		
	else:
		print "invalid entry; please try again"
