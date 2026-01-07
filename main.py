import tkinter as tk
from tkinter import ttk
from random import randrange
from config import *

dictionary = []

def main():
    dictionary = prepare_word_list(DICTIONARY_FILE)
    word_list = prepare_word_list(WORD_LIST)
    list_size = len(word_list)
    mystery_word = word_list[randrange(list_size)]

    root = tk.Tk()
    root.geometry('500x800')
    root.title(f"{THEME} Wordle")

    guess_grid = ttk.Frame(root)
    guesses = init_guesses(guess_grid)
    guess_grid = configure_grid(guess_grid, guesses)
    guess_grid.pack(fill=tk.X)

    root.mainloop()

def prepare_word_list(list):
    with open(list, "r") as file:
        return file.read().lower().split()
    
def init_guesses(master):
    guesses = []
    for i in range(MAX_GUESSES):
        row = []
        for j in range(WORD_LENGTH):
            row.append(tk.Label(master, height=6))
        guesses.append(row)
    
    return guesses

def configure_grid(root, guesses):
    for i in range(MAX_GUESSES):
        root.rowconfigure(i, weight=1)

    for i in range (WORD_LENGTH):
        root.columnconfigure(i, weight=1)
    
    for i in range(MAX_GUESSES):
        for j in range(WORD_LENGTH):
            guesses[i][j].config(
                font=("Verdanda", 18),
                fg="#000000",
                bg="#FFFFFF"
            )
            guesses[i][j].grid(column=i, row=j, sticky=tk.EW, padx=5, pady=5)
    
    return root

main()