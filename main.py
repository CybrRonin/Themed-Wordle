import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno, showinfo
from random import randrange
from config import *
from functools import partial

root = tk.Tk()
dictionary = []      # list of words used to verify guesses are actual, English words
word_list = []      # custom word list from which themed mystery words will be selected
guesses = []        # list lists made up of the various labels that display the characters for displaying the words in each guess
buttons = {}        # Dictionary mappping labels that represent keyboard keys to a grid of buttons at the bottom of the screen
guessed_words = []  # List for tracking the words that have already been guessed (a check not even official Wordle provides)
guess = 0           # tracks how many guesses have been made so far
letter = 0          # tracks who many letters have been entered in the current guess
mystery_word = ""   # stores the mystery word (i.e. the one we're trying to guess)
THEME = ""          # a string storing the theme for the collection of words being drawn from; used to update the title on the title bar

def main():
    # initialize the game window
    setup()

    root.geometry('600x550')
    root.title(f"{THEME} Wordle")

    # set up the grid of labels for guessses in its own frame for convenience and pack it into the game window
    guess_grid = ttk.Frame(root)
    guesses = init_guesses(guess_grid)
    guess_grid = configure_grid(guess_grid, guesses)
    guess_grid.pack(fill=tk.X)

    # set up the grid of buttons representing the virtual keyboard at the bottom of the game window and pack that onto the screen
    keyboard = ttk.Frame(root)
    keyboard = init_buttons(keyboard)
    keyboard.pack()

    # With the virtual keyboard set up, it's time to handle physical keyboard input
    root.bind("<Key>", key_handler)

    root.mainloop()

# builds the lists for the dictionary, the word list to draw from, 
# and selects a mystry word from that list to guess
def setup():
    global dictionary, word_list, mystery_word

    dictionary = prepare_word_list(DICTIONARY_FILE)
    word_list = prepare_word_list(WORD_LIST, True)

    dictionary.extend(word_list) # ensures the custom word list is in the dictionary

    list_size = len(word_list)
    mystery_word = word_list[randrange(list_size)].lower()

# takes a text file and converts it to a list of individual words
# if "containsTheme" is true, the first entry is assigned as the game's theme before 
# using the rest of the file to contruct the word list.
def prepare_word_list(list, containsTheme=False):
    global THEME
    start = 0
    with open(list, "r") as file:
        words = file.read().split()
        if containsTheme:
            THEME = words[0]
            start = 1
        return [word.lower() for word in words[start:]]

# initialize the matrix of labels, each row representing a word of WORD_LENGTH (default 5)
# characters, in a list containing MAX_GUESSES (default 6) words 
def init_guesses(master):
    for i in range(MAX_GUESSES):
        row = []
        for j in range(WORD_LENGTH):
            row.append(tk.Label(master, height=2))
        guesses.append(row)
    
    return guesses

# Take initialized label matrix and construct a grid that the labels can then be
# slotted into in order to be displayed correctly
def configure_grid(master, guesses):
    for i in range(MAX_GUESSES):
        master.rowconfigure(i, weight=1)

    for i in range (WORD_LENGTH):
        master.columnconfigure(i, weight=1)
    
    for i in range(MAX_GUESSES):
        for j in range(WORD_LENGTH):
            guesses[i][j].config(
                font=("Verdanda", 18),
                fg="#000000",
                bg="#FFFFFF"
            )
            guesses[i][j].grid(row=i, column=j, sticky=tk.EW, padx=5, pady=5)
    
    return master

# Generate rows of buttons representing a virtual keyboard, packing each row of
# buttons into its own frame (left-to-right) which, in turn, is packed into the 
# master frame provided (top-to-bottom)
def init_buttons(master):
    # List of keys to be used for virtual keyboard, divided into rows, 
    # w/ Enter and backspace added to the bottom row, mimicking the official layout
    KEYS = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
             ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
             ["Enter", "Z", "X", "C", "V", "B", "N", "M", "<-"]]
    for i in range(len(KEYS)):
        row = ttk.Frame(master)
        for j in range(len(KEYS[i])):
            value = KEYS[i][j]
            btn = ttk.Button(row, text=value, width=5, command=partial(click_button, value))
            buttons[value.lower()] = btn
            btn.pack(side=tk.LEFT)
        row.pack()

    return master

# callback function for handling the click events of the keyboard buttons
def click_button(text):
    global guess
    global letter

    if text == "Enter":
        submit_guess()
        return
    if text == "<-":
        # As long as a letter has been input, back up one spot and reset the 
        # text value to erase that character
        if letter > 0:
            letter -= 1
            guesses[guess][letter].config(text = "")
        return
    if letter < 5:
        guesses[guess][letter].config(text = text)
        letter += 1

# Attempts to submit the current word as a guess about what the mystery word might be
def submit_guess():
    global dictionary, guessed_words, mystery_word, guess, letter

    # make a copy of the mystery word so I can manipulate it without changing the word
    target = mystery_word 

    # Establish the styles for the various button states:
    # Correct - Letter is not only in the mystery word, but it's in the right position
    # Misplaced - Letter is in the mystery word, but not in that slot
    # Wrong - Letter isn't part of the mystery word, at all
    style = ttk.Style()
    style.configure("Correct.TButton", background="green", foreground="white")
    style.configure("Misplaced.TButton", background="yellow")
    style.configure("Wrong.TButton", background = "#404040", foreground="white")

    # construct the guessed word from the current grid state and comfirm it's long enough
    guessed_word = construct_guess()
    if len(guessed_word) < WORD_LENGTH:
        showinfo(message = "Not enough letters")
        return
    
    # verify the word exists in the dictionary
    if guessed_word not in dictionary:
        showinfo(message = "Not in word list")
        return
    
    # confirm word hasn't already been guessed
    # (Note: This isn't actually a feature of vanilla Wordle but it feels like a good
    # quality-of-life update, even if you can easily verify for yourself by checking
    # the grid)
    if guessed_word in guessed_words:
        showinfo(message = "Already guessed")
        return

    # Confirmed valid guess, so track the word as a guess before we make any changes to the string
    guessed_words.append(guessed_word.lower())

    # iterate through and check if any letters are in their correct slots
    for i in range(WORD_LENGTH):
        if guessed_word[i] == target [i]:
            guesses[guess][i].config(bg="green", fg="white")
            buttons[guessed_word[i]].config(style = "Correct.TButton")
            # letter is matched up so replace it with a placeholder so it doesn't get compared in the next pass
            guessed_word = guessed_word[:i] + "*" + guessed_word[i+1:]
            target = target[:i] + "*" + target[i+1:]
    
    # With exact matches sorted, check if any remaingng letters exist in the word, anywhere
    for i in range(WORD_LENGTH):
        # if letter was correctly matched in the first pass skip it
        if guessed_word[i] == "*":
            continue
        # if letter is part of the mystery word, update the label and button colors accordingly
        if guessed_word[i] in target:
            guesses[guess][i].config(bg="yellow")
            buttons[guessed_word[i]].config(style = "Misplaced.TButton")
            # We've already flagged any characters that are correctly placed, so it doesn't matter which instance of a character is removed
            # but we do want to remove one in case that letter is repeated
            target = target.replace(guessed_word[i], "*", 1)
        # letter isn't part of the mystery word, so gray out the label and button to 
        # make that easier to see
        else:
            guesses[guess][i].config(bg="#404040", fg="white")
            btn = buttons[guessed_word[i]]
            if btn.cget("style") != "Misplaced.TButton" and btn.cget("style") != "Correct.TButton":
                btn.config(style = "Wrong.TButton")
    # guess was successfully submitted so increment the counter (row) and reset to the 
    # first letter position in preparation to start the next word
    guess += 1
    letter = 0

    # if every letter was replaced with a placeholder we have a perfect match.
    # Display a popup declaring victory and asking if they'd like to go again.
    if guessed_word == "*****":
        answer = askyesno(title="Congratulations!", message="You got it! Would you like to try again?")
        print(answer)
        if answer:
            reset()
        else:
            root.destroy()
    # if this executes, we've run out of guesses without finding the correct word.
    # Dispaly a popup revealing the word and asking if they'd like to try again
    elif guess == MAX_GUESSES:
        answer = askyesno(message=f"You lost!\nThe word I was looking for was: {mystery_word}.\nWould you like to try again?")
        if answer:
            reset()
        else:
            root.destroy()
          
# iterate through the row representing the current guess, combining each of their labels
# into a single word which is returned (in lower case for ease of comparison)
def construct_guess():
    global guess
    word = ""
    for i in range(5):
        word+=guesses[guess][i].cget("text")
    return word.lower()

# Keyboard event handler 
# Redirects key inputs to corresponding click events already implemented
def key_handler(event):
    if event.char.upper() >= "A" and event.char.upper() <= "Z":
        click_button(event.char.upper())
        return
    if event.keysym == "Return" or event.keysym == "KP_Enter":
        click_button("Enter")
        return
    if event.keysym == "BackSpace":
        click_button("<-")
        return

# Reset the game state in preparation to start another round
def reset():
    global mystery_word, guessed_words, guess, letter

    # reset each label to its initial state
    for i in range(MAX_GUESSES):
        for j in range(WORD_LENGTH):
            guesses[i][j].config(text="", bg="white", fg="black")

    # reset each of the keyboard buttons to their original style
    style = ttk.Style()
    style.configure("Reset.TButton", background="lightgray", foreground="black")

    for button in buttons:
        buttons[button].config(style="Reset.TButton")
    
    # Lastly, select a new mystery word and reset the guessed words list
    # and guess/letter counters
    list_size = len(word_list)
    mystery_word = word_list[randrange(list_size)].lower()

    guessed_words = []
    guess = 0
    letter = 0

main()