import tkinter as tk
from tkinter import ttk
from random import randrange
from config import *
from functools import partial

dictionary = []
guesses = []
guess = 0
letter = 0

def main():
    dictionary = prepare_word_list(DICTIONARY_FILE)
    word_list = prepare_word_list(WORD_LIST)
    list_size = len(word_list)
    mystery_word = word_list[randrange(list_size)]

    root = tk.Tk()
    root.geometry('600x500')
    root.title(f"{THEME} Wordle")

    guess_grid = ttk.Frame(root)
    guesses = init_guesses(guess_grid)
    guess_grid = configure_grid(guess_grid, guesses)
    guess_grid.pack(fill=tk.X)

    keyboard = ttk.Frame(root)
    keyboard = init_buttons(keyboard)
    keyboard.pack()

    root.mainloop()

def prepare_word_list(list):
    with open(list, "r") as file:
        return file.read().lower().split()
    
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
            guesses[i][j].grid(column=i, row=j, sticky=tk.EW, padx=5, pady=5)
    
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
            btn.pack(side=tk.LEFT)
        row.pack()

    return master

def click_button(text):
    print(text)
"""
    if text == "Enter":
        submit_guess()
        return
    if text == "<-":
        if letter > 0:
            letter -= 1
            guesses[guess][letter].config(text = "")
        return
    guesses[guess][letter].config(text = "text")
    letter += 1
"""

def submit_guess():
    pass

main()