import inquirer
from colorama import Fore
import sys

def error_letters_length(letters):
    return (Fore.RED + f"letters list should have exactly 12 letters. \"{letters}\" has {len(letters)} letters.")
def error_letters_duplicate(letters):
    return (Fore.RED + f"\"{letters}\" contains duplicate letters. letters list must have 12 distinct letters.")

def letters_validation(letters):
    if len(letters) != 12:
        raise ValueError(error_letters_length(letters))
    if len({char for char in letters}) != 12:
        raise ValueError(error_letters_duplicate(letters))
    return True

def prompt_for_user_selections():
    game_mode = [
    inquirer.List('game_mode',
                    message="Select game mode",
                    choices=[
                        ("New York Times", "nyt"),
                        ("Custom", "manual"),
                    ],
                ),
    ]
    answers = inquirer.prompt(game_mode)

    def letters_validation(answers, current):
        letters = current
        if len(letters) != 12:
            raise inquirer.errors.ValidationError('', reason=(error_letters_length(letters)))
        if len({char for char in letters}) != 12:
            raise inquirer.errors.ValidationError('', reason=(error_letters_duplicate(letters)))
        return True

    def prompt_for_custom_options():
            custom_options = [
            inquirer.Text('letters',
                            message="Enter letters for puzzle",
                            validate=letters_validation
                        ),
            inquirer.List('word_list',
                            message="Select word list",
                            choices=[
                                ("Easy Words", "words_easy"),
                                ("Hard Words", "words_hard"),
                                ("Scrabble Words + Longer Words", "scrabble_plus_long"),
                            ],
                        ),
            ]
            custom_options_answers = inquirer.prompt(custom_options)
            #print(custom_options_answers)
            return custom_options_answers

    if answers["game_mode"] != "nyt":
        answers.update(prompt_for_custom_options())

    return answers

#print(prompt_for_user_selections())