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
# print three word chain results as they are found, makes it a bit slower
print_results_option = False

# word list type (nyt_dictionary,words_easy,words_hard,scrabble_plus_long)
word_list_type = "nyt_dictionary"

# output results to file
save_results = True

### DEFINE PUZZLE ###
date_of_puzzle = "2023-12-16"
letters = "wcmhksobetai"

letters_list_separated = [letters[0:3],letters[3:6],letters[6:9],letters[9:12]]
#create matrix for checking if consecutive letters are on same side of box
letters_matrix = np.array([list(letters[0:3]),list(letters[3:6]),list(letters[6:9]),list(letters[9:12])])
#create list of all letters
letters_list = list(letters)
#get list of letters not in list to remove words that have these letters, they cannot be guesses
letters_not_list = list(set(list(string.ascii_lowercase)) - set(letters_list))

print(f"date_of_puzzle: {date_of_puzzle}")
print(f"letters_list: {letters_list_separated}")

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

sorted_word_list = sorted(word_set_filtered_2).copy()

#display alpha word list
#print(sorted(sorted_word_list))


### START GETTING RESULTS ###

def print_optional(p):
    if print_results_option:
        print(p)

### THREE WORD CHAINS IN ONE STEP ###

# leaving this solution in here, but it's about 5x slower than the two plus one approach
def three_word_solutions(word_list:list,letters_list:list):
    letters_set = set(letters_list)
    results = [
        [word1 , word2 , word3]
        for word1 in word_list
        for word2 in word_list
        for word3 in word_list
        #if word1 != word2 and word2 != word3 and word3 != word1
        if word1[-1] == word2[0]
        if word2[-1] == word3[0]
        if not letters_set - (set(word1) | set(word2) | set(word3))
    ]
    return results

### THREE WORD CHAINS WITH TWO THEN ONE ###

# create list of two words with letters contained and letters remaining
def two_word_combinations(word_list:list,letters_list:list):
    results = [
        {
            "word1":word1,
            "word2":word2,
            "letters_contained":list(set(word1) | set(word2)),
            "letters_remaining":list(set(letters_list) - (set(word1) | set(word2)))
        }
        for word1 in word_list
        for word2 in word_list
        if word1 != word2
        if word1[-1] == word2[0]
    ]
    return results

# create list of single words with letters contained and letters remaining
def one_word_list(word_list:list,letters_list:list):
    results = [
        {
            "word" : word,
            "letters_contained" : list(set(word)),
            "letters_remaining" : list(set(letters_list)-set(word))
        }
        for word in word_list
        ]
    return results

# combine two word combinations with one word that satisfies letters list
def two_plus_one_combinations(two_word_combinations:list,one_word_list:list,order:string):
    results = []
    if order == "two_then_one":
        for tw in two_word_combinations:
            for ow in one_word_list:
                if tw["word2"][-1] == ow["word"][0] \
                and not (set(tw["letters_remaining"]) - set(ow["letters_contained"])) \
                and not (tw["word2"] == ow["word"]):
                    results.append([tw["word1"],tw["word2"],ow["word"]])
                    print_optional([tw["word1"],tw["word2"],ow["word"]])
    # one then two is a little slower
    elif order == "one_then_two":
        for ow in one_word_list:
            for tw in two_word_combinations:
                if ow["word"][-1] == tw["word1"][0] \
                and not (set(ow["letters_remaining"]) - set(tw["letters_contained"])) \
                and not (ow["word"] == tw["word1"]):
                    results.append([ow["word"],tw["word1"],tw["word2"]])
                    print_optional([ow["word"],tw["word1"],tw["word2"]])
    return results

# start to get results
start_time = datetime.now()
print(f"start time: {start_time}")

twc = two_word_combinations(sorted_word_list,letters_list)
owl = one_word_list(sorted_word_list,letters_list)

# get solutions for one and two word chains
one_word_chains = [[ow["word"]] for ow in owl if ow["letters_remaining"] == []]
two_word_chains = [[tw["word1"],tw["word2"]] for tw in twc if tw["letters_remaining"] == []]

# get solutions for three word chains
# only try for two word chains that aren't already solutions by themselves, since two word chains would finish your game
two_word_non_chains = [tw for tw in twc if not tw["letters_remaining"] == []]
three_word_chains = two_plus_one_combinations(two_word_non_chains,owl,"two_then_one")

# convert chain lists to single strings
possible_chains_1 = [' - '.join(p) for p in one_word_chains]
possible_chains_2 = [' - '.join(p) for p in two_word_chains]
possible_chains_3 = [' - '.join(p) for p in three_word_chains]

# end of getting results
end_time = datetime.now()

print(f"end_time: {end_time}")
print(f"duration: {(end_time - start_time)}")
print(f"one word chains: {len(one_word_chains)}")
print(f"two word chains: {len(two_word_chains)}")
print(f"three word chains: {len(three_word_chains)}")

if save_results:
    data = {
        "date_of_puzzle":date_of_puzzle,
        "letters":letters_list_separated,
        "word_list_type":word_list_type,
        "start_time":start_time,
        "end_time":end_time,
        "duration":(end_time - start_time),
        "one word chains":len(one_word_chains),
        "two word chains":len(two_word_chains),
        "three word chains":len(three_word_chains),
        "chains_1":possible_chains_1,
        "chains_2":possible_chains_2,
        "chains_3":possible_chains_3
    }

    directory = fr".\results\{date_of_puzzle}"
    file_path = os.path.join(directory, f"output_all_{word_list_type}.json")

    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write the dictionary to a JSON file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4, default=str)

    print(f"Results have been saved to: {file_path}")