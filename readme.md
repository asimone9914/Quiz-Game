# Python Quiz Game
**THIS APPLICATION IS IN A VERY EARLY STAGE OF DEVELOPMENT**

A simple quiz game built with Python, using the Tkinter library for a GUI.
This application supports custom questions and answers through the use of CSV (comma-separated values) files.

The file can be formatted as such:
```
  1| question, answer1, answer2, answer3
  2| Who plays jack in The Shining?, Jack Nicholson
  3| Where is the Empire State Building located?, New York, New York City
```
> You may notice there are spaces in this file. 
> Normally, this is not the way to format a CSV file.
> But for ease of use and readability, spaces are okay in this program.

# How to use this software:
1. Create or edit a CSV file with your questions and answers
2. From a terminal, run the following: `python start_game.py`

## For Linux users:
If you are on Linux, you will have to install the tkinter module for Python as well as the tkinter package via your package manager.
- Arch: `pacman -S tk` 
- Debian: `apt install python-tk`
- Fedora: `dnf install python3-tkinter`

Ensure that it is working by running `python -m tkinter`

# Recent Changes:
- **added game modes for endless or shuffled quiz**
- added popup dialog box to show correct answers at the end
- fixed some window alignment issues

## Things to fix/add:
- About program button has no function
- add an exit quiz button
- make things look prettier
