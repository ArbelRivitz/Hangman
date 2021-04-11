#############################################################

# FILE : hangman_helper.py

# WRITER : Arbel Rivitz, arbelr, 207904632

# EXERCISE : intro2cs ex4 2017-2018

# DESCRIPTION : Operating a hangman_helper game, using the gui and the assisting functions. That's the implementation of the
# logic behind the game regarding the input from the player, updating the pattern, running another game, suggesting
# hints etc.

#############################################################

import hangman_helper


def update_word_pattern(word, current_pattern, letter):
    """This function take a word, the current shown pattern of this word and show the updated pattern with the places
    this letter appear, if at all"""
    current_pattern = list(current_pattern)
    word = list(word)
    for i in range(len(word)):
        if word[i] == letter:
            current_pattern[i] = letter
    updated_pattern = ''.join(current_pattern)
    return updated_pattern


def run_single_game(words_list):
    """This function runs one game. It includes distinguishing between the different input from the player - whether
    it's a request for a hint or a guess of a letter. When getting a guess, verifying it's validity and then check if
    it's on the pattern and so on. Then, finally it sums up the single run in a case of a win or a loss """
    word = hangman_helper.get_random_word(words_list)
    wrong_guesses_list = []
    current_pattern = '_' * len(word)
    msg = hangman_helper.DEFAULT_MSG

    while len(wrong_guesses_list) < hangman_helper.MAX_ERRORS and current_pattern.count('_') > 0:
        hangman_helper.display_state(current_pattern, len(wrong_guesses_list), wrong_guesses_list, msg)
        type_input, value_input = hangman_helper.get_input()
        if type_input == 2:
            if len(value_input) > 1 or value_input.islower() is False:
                msg = hangman_helper.NON_VALID_MSG
            elif wrong_guesses_list.count(value_input) > 0 or current_pattern.count(value_input) > 0:
                msg = hangman_helper.ALREADY_CHOSEN_MSG + value_input
            elif value_input in word:
                current_pattern = update_word_pattern(word, current_pattern, value_input)
                msg = hangman_helper.DEFAULT_MSG
            else:
                wrong_guesses_list.append(value_input)
                msg = hangman_helper.DEFAULT_MSG
        elif type_input == 1:
            matching_words = filter_words_list(words_list, current_pattern, wrong_guesses_list)
            hint_letter = choose_letter(matching_words, current_pattern)
            msg = hangman_helper.HINT_MSG + hint_letter
            hangman_helper.display_state(current_pattern, len(wrong_guesses_list), wrong_guesses_list, msg)
    if len(wrong_guesses_list) == hangman_helper.MAX_ERRORS:
        msg = hangman_helper.LOSS_MSG + word
    elif current_pattern.count('_') == 0:
        msg = hangman_helper.WIN_MSG
    hangman_helper.display_state(current_pattern, len(wrong_guesses_list), wrong_guesses_list, msg, ask_play=True)


def main():
    """This function handle running the game more than once according to the user input, and uses the load_words
    function to load the words into the run_single_game funcction"""
    words_list = hangman_helper.load_words()
    run_single_game(words_list)
    type_input, value_input = hangman_helper.get_input()
    while type_input == 3 and value_input :
        run_single_game(words_list)
        type_input, value_input = hangman_helper.get_input()


def filter_words_list(words, pattern, wrong_guesses_list):
    """This function filter all of the words from the words list that could fit the current pattern, also due to the
     wrong guesses list"""
    matching_words = []
    for word in words:
        true_values = 0
        if len(pattern) == len(word):
            for letter_index in range(len(word)):
                letter = word[letter_index]
                if (pattern[letter_index] == letter or letter not in wrong_guesses_list) and (pattern.count(letter) \
                        == word.count(letter) or pattern[letter_index] == '_'):
                        true_values += 1
        if true_values == len(word):
            matching_words.append(word)
    return matching_words


CHAR_A = 97


def letter_to_index(letter):
    """
    Return the index of the given letter in an alphabet list.
    """
    return ord(letter.lower()) - CHAR_A


def index_to_letter(index):
    """
    Return the letter corresponding to the given index.
    """
    return chr(index + CHAR_A)


def choose_letter(words, pattern):
    """This function check for the most frequent letters in all of the words from the words list who match the
    current pattern, in order to point out the best hint for a letter from the word"""
    counts_list = []
    for letter_index in range(25):
        sum_per_letter = 0
        letter = index_to_letter(letter_index)
        if pattern.count(letter) == 0:
            for word in words:
                sum_per_letter += word.count(letter)
        counts_list.append(sum_per_letter)
        max_letter_locations = [counts_list.index(max(counts_list))]
        final_letter = index_to_letter(max_letter_locations[0])
    return final_letter


if __name__ == "__main__":
    hangman_helper.start_gui_and_call_main(main)
    hangman_helper.close_gui()
