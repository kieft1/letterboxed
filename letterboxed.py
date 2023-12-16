#from english_words import get_english_words_set
#from nltk.corpus import words
import numpy as np
import string
import sys
import json
import os
from datetime import datetime
import nyt_metadata

### OPTIONS ###
# declare longest length to try before finding or giving up on a chain (3 is ok, 4 or higher may take a while)
max_chain_length = 2

# True if max should be set to the best solution found so far, ex. you found a chain of 2, you don't care about finding a chain of 3 anymore
# False if you want to find all chains up to the provided len_max (3 is ok, 4 or higher may take a while)
decreasing_max = False

# word list type (nyt_dictionary,words_easy,words_hard,scrabble_plus_long)
word_list_type = "nyt_dictionary"

# output results to file
save_results = True

### DEFINE PUZZLE ###
date_of_puzzle = "2023-12-16"
letters = "wcmhksobetai"

#create matrix for checking if consecutive letters are on same side of box
letters_matrix = np.array([list(letters[0:3]),list(letters[3:6]),list(letters[6:9]),list(letters[9:12])])
#create list of all letters
letters_list = list(letters)
#get list of letters not in list to remove words that have these letters, they cannot be guesses
letters_not_list = list(set(list(string.ascii_lowercase)) - set(letters_list))

print(letters_list)
print(letters_not_list)

### GET LIST OF WORDS ###
#word_set = get_english_words_set(sources=['web2'],alpha=True,lower=True)
#word_set = words.words()

def load_words(filename):
    with open(filename, 'r') as file:
        words = [line.strip() for line in file]
    return words

def get_word_set(set_name:str):
    if set_name == "scrabble_plus_long":
        # get scrabble word list and larger list just for words longer than 8 char (not in scrabble list)
        word_set = load_words('./words/words_scrabble.txt')
        word_set_long = load_words('./words/wordlist.txt')
        
        for w in word_set_long:
            if len(w) > 8:
                word_set.append(w)
        return word_set
        # could probably save this off into a separate file
    elif set_name == "words_easy":
        return load_words('./words/alice/words_easy.txt')
    elif set_name == "words_hard":
        return load_words('./words/alice/words_hard.txt')
    elif set_name == "nyt_dictionary":
        words_file_path = f"./words/nyt/{date_of_puzzle}.txt"
        if not os.path.isfile(words_file_path):
            nyt_metadata.save_todays_dictionary()
        return load_words(words_file_path)
    else:
        raise ValueError(f"\"{set_name}\" not valid option for word_list_type")

word_set = get_word_set(word_list_type)

word_set = [item.lower() for item in word_set]

# function to determine if word contains any of the letters we can't use
def contains_any_letter(input_string, letters_to_check):
    for letter in letters_to_check:
        if letter in input_string:
            return True
    return False


# if word_set is nyt_dictionary, assume the list is already good as-is
if word_set == "nyt_dictionary":
    word_set_filtered = set(word_set)
    word_set_filtered_2 = word_set_filtered

else:
    # remove words that have letters not in list of provided letters
    # include words only > 2 char in length
    word_set_filtered = set({})
    for w in word_set:
        if not contains_any_letter(w,letters_not_list) and len(w) > 2:
            word_set_filtered.add(w)

    # remove words that have consecutive letters on same side
    word_set_filtered_2 = word_set_filtered.copy()
    for w in word_set_filtered:
        num_prev = -1
        for i,char_to_lookup in enumerate(w):
            row_indices = np.where(letters_matrix == char_to_lookup)[0]
            if row_indices == num_prev:
                word_set_filtered_2.remove(w)
                break
            else:
                num_prev = row_indices

# function to sort words based on how many letters they have left to cover
# ideally we could remove words that don't have any letters in them that we need to still get
# but there might be a puzzle that requires us to add another word out of only used letters to change our ending letter (probably quite rare)
def reorder_words(words, letters):
    def key_function(word):
        return sum(1 for letter in word if letter in letters)
    #sort the words based on the number of matching letters
    sorted_words = sorted(words, key=key_function, reverse=True)
    return sorted_words

if decreasing_max:
    # first sort will just be by length as all letters are left to find
    sorted_word_list = reorder_words(word_set_filtered_2,letters_list).copy()
else:
    # otherwise just sort alpha since all combinations will be checked
    sorted_word_list = sorted(word_set_filtered_2).copy()

#display alpha word list
print(sorted(sorted_word_list))


# function to get list of words that start with the letter we need next
def starting_letter_words(words_to_pick_from: list,starting_letter: str):
    return_list_of_words = []
    for w in words_to_pick_from:
        if w[0] == starting_letter:
            return_list_of_words.append(w)
    #print(return_list_of_words)
    return return_list_of_words

# function to remove letters from the list we still need to get based on the word provided
def remove_letters_from_list(word: str,letters_list: list):
    #remove letters from letters list
    for char in word:
        if char in letters_list:
            letters_list.remove(char)
    return letters_list

### CREATE LISTS ###
# create list starting with each word
list_of_lists = []
for w in sorted_word_list:
    list_of_lists.append([w])


# declare empty list to add chains to
possible_chains = []
possible_chains_string = []

# for each list provided, get possible next words, create another set of lists, and continue until all 12 letters have been used
def create_chains(list_of_lists:list):
    global max_chain_length
    global decreasing_max
    global possible_chains
    for l in list_of_lists:
        remaining_words = sorted_word_list.copy()
        remaining_letters = letters_list.copy()
        for w in l:
            remaining_letters = remove_letters_from_list(w,remaining_letters)
        if len(remaining_letters) == 0:
            print(l)
            if decreasing_max:
                max_chain_length = len(l)
            possible_chains.append(l)
            possible_chains_string.append(' - '.join(l))
        elif len(l) == max_chain_length:
            continue
        else:
            last_letter = l[-1][-1]
            # if looking for shortest chain, reorder the words to get the better options first
            if decreasing_max:
                remaining_words_sorted = reorder_words(remaining_words,remaining_letters)
                for w in l:
                    remaining_words_sorted.remove(w)
                next_words = starting_letter_words(remaining_words_sorted,last_letter)
            # otherwise don't bother reordering the list
            else:
                for w in l:
                    remaining_words.remove(w)
                next_words = starting_letter_words(remaining_words,last_letter)
            l2 = []
            for n in next_words:
                new_list = l.copy()
                new_list.append(n)
                #print(new_list)
                l2.append(new_list)
            #print(l2)
            create_chains(l2)

create_chains(list_of_lists)

#print(possible_chains)

if save_results:
    data = {
        "date_of_puzzle":date_of_puzzle,
        "word_list_type":word_list_type,
        "max_chain_length":max_chain_length,
        "letters":letters_matrix.tolist(),
        "chains":possible_chains,
        "chains_string":possible_chains_string
    }

    directory = fr".\results\{date_of_puzzle}"
    file_path = os.path.join(directory, f"output_{max_chain_length}_{word_list_type}.json")

    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write the dictionary to a JSON file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Results have been saved to: {file_path}")