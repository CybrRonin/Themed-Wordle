# Themed-Wordle
An attempt to recreate Wordle with words drawn from a smaller sub-list, separate from the dictionary, ensuring each word is related to a given theme (holidays, fandoms, etc.) 

Original dictionary sourced from https://wordslibrary.com/wordle-dictionary-words/

## Why bother? 
Traditional Wordle pulls from the entirety of the English language. You might get lucky and get a word that fits particularly well with a certain topic or time of year, but that's pure luck. This will draw its mystery words from a specifically-designed subset, so you can be certain _every_ word will be appropriate, though it will accept the regular words as guesses, too, to help narrow down. (The provided list likely hints at the time of year I started working on it... before life and the holidays got in the way.)

## How does it work?
You'll need to be able to run Python 3.x. To run it, clone the repo. To set up your custom word list. The very first word represents the theme for the list. Afte that, they'll need to be in a text file, one word per line. Either edit "themed_list.txt" or edit the value of WORD_LIST in "config.py" to point to your text file. At that point, just run main.py and you should see a Tkinter window pop up. From there, it should work just like traditional Wordle: type on the keyboard or use the buttons on the bottom to enter words and make guesses. Any green letters are correct _and_ in the correct position. Yellow letters are part of the mystery word but in thew wrong position. If they're greyed out, they're not part of the word at all.

## Points of improvement
While I did my best to make this as feature complete as I could, there are some definite quality-of-life tweaks that could be added but would've taken the project beyond the 20-40 hours
- Replace labels and buttons with graphical icons. That would significantly improve the visual appeal, especially if you added proper animations to handle tile transitions.
- Expand the dictionary. Even in my limited testing, the list I found online had some rather conspicuous absences, such as "pants" and "panda". I tried to fill them in as I found them, but if those exist, surely there are others, so there's more work that could be done.