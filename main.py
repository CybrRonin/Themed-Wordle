import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno, showinfo
from random import randrange
from config import *
from functools import partial

root = tk.Tk()
dictionary = [] # list of words used to verify guesses are actual, English words
word_list = [] # custom word list from which themed mystery words will be selected
guesses = []
buttons = {}
guessed_words = []
guess = 0
letter = 0
mystery_word = ""
THEME = ""

def main():
    setup()

    root.geometry('600x550')
    root.title(f"{THEME} Wordle")

    guess_grid = ttk.Frame(root)
    guesses = init_guesses(guess_grid)
    guess_grid = configure_grid(guess_grid, guesses)
    guess_grid.pack(fill=tk.X)

    keyboard = ttk.Frame(root)
    keyboard = init_buttons(keyboard)
    keyboard.pack()

    root.bind("<Key>", key_handler)

    root.mainloop()

def setup():
    global dictionary, word_list, mystery_word

    dictionary = prepare_word_list(DICTIONARY_FILE)
    word_list = prepare_word_list(WORD_LIST)

    dictionary.extend(word_list) # make sure custom word list is in the dictionary

    list_size = len(word_list)
    mystery_word = word_list[randrange(list_size)].lower()

def prepare_word_list(list):
    global THEME
    with open(list, "r") as file:
        words = file.read().split()
        THEME = words[0]
        return [word.lower() for word in words[1:]]
    
def init_guesses(master):
    for i in range(MAX_GUESSES):
        row = []
        for j in range(WORD_LENGTH):
            row.append(tk.Label(master, height=2))
        guesses.append(row)
    
    return guesses

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

def init_buttons(master):
    keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
             ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
             ["Enter", "Z", "X", "C", "V", "B", "N", "M", "<-"]]
    for i in range(len(keys)):
        row = ttk.Frame(master)
        for j in range(len(keys[i])):
            value = keys[i][j]
            btn = ttk.Button(row, text=value, width=5, command=partial(click_button, value))
            buttons[value.lower()] = btn
            btn.pack(side=tk.LEFT)
        row.pack()

    return master

def click_button(text):
    global guess
    global letter

    if text == "Enter":
        submit_guess()
        return
    if text == "<-":
        if letter > 0:
            letter -= 1
            guesses[guess][letter].config(text = "")
        return
    if letter < 5:
        guesses[guess][letter].config(text = text)
        letter += 1

def submit_guess():
    global dictionary, guessed_words, mystery_word, guess, letter

    # make a copy of the mystery word so I can manipulate it without changing the word
    target = mystery_word 
    style = ttk.Style()
    style.configure("Correct.TButton", background="green", foreground="white")
    style.configure("Misplaced.TButton", background="yellow")
    style.configure("Wrong.TButton", background = "#404040", foreground="white")

    guessed_word = construct_guess()
    if len(guessed_word) < WORD_LENGTH:
        showinfo(message = "Not enough letters")
        return
    
    if guessed_word not in dictionary:
        showinfo(message = "Not in word list")
        return
    
    if guessed_word in guessed_words:
        showinfo(message = "Already guessed")
        return
    
    for i in range(WORD_LENGTH):
        if guessed_word[i] == target [i]:
            guesses[guess][i].config(bg="green", fg="white")
            buttons[guessed_word[i]].config(style = "Correct.TButton")
            # letter is matched up so replace it with a placeholder so it doesn't get compared in the next pass
            guessed_word = guessed_word[:i] + "*" + guessed_word[i+1:]
            target = target[:i] + "*" + target[i+1:]
    
    for i in range(WORD_LENGTH):
        # if letter was correctly matched in the first pass skip it
        if guessed_word[i] == "*":
            continue
        if guessed_word[i] in target:
            guesses[guess][i].config(bg="yellow")
            buttons[guessed_word[i]].config(style = "Misplaced.TButton")
            # We've already flagged any characters that are correctly placed, so it doesn't matter which instance of a character is removed
            # but we do want to remove one in case that letter is repeated
            target = target.replace(guessed_word[i], "*", 1)
        else:
            guesses[guess][i].config(bg="#404040", fg="white")
            btn = buttons[guessed_word[i]]
            if btn.cget("style") != "Misplaced.TButton" and btn.cget("style") != "Correct.TButton":
                btn.config(style = "Wrong.TButton")

    guessed_words.append(guessed_word.lower())
    guess += 1
    letter = 0

    if guessed_word == "*****":
        answer = askyesno(title="Congratulations!", message="You got it! Would you like to try again?")
        print(answer)
        if answer:
            reset()
        else:
            root.destroy()
    elif guess == MAX_GUESSES:
        answer = askyesno(message=f"You lost!\nThe word I was looking for was: {mystery_word}.\nWould you like to try again?")
        if answer:
            reset()
        else:
            root.destroy()
          

def construct_guess():
    global guess
    word = ""
    for i in range(5):
        word+=guesses[guess][i].cget("text")
    return word.lower()

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

def reset():
    global mystery_word, guessed_words, guess, letter

    #reset each label
    for i in range(MAX_GUESSES):
        for j in range(WORD_LENGTH):
            guesses[i][j].config(text="", bg="white", fg="black")

    style = ttk.Style()
    style.configure("Reset.TButton", background="lightgray", foreground="black")

    for button in buttons:
        buttons[button].config(style="Reset.TButton")
    
    list_size = len(word_list)
    mystery_word = word_list[randrange(list_size)].lower()

    guessed_words = []
    guess = 0
    letter = 0

main()