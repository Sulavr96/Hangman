"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
Hangman Game
Student Id: 50509195
Name: Nikesh Bahadur Adhikari
Email: nikesh.adhikari@tuni.fi
Student Id: 150195247
Name: Sulav Rayamajhi
Email: sulav.rayamajhi@tuni.fi
"""

from tkinter import *
import random


class HangMan:
    """
     A classic hangman game where a random word is given with some letters visible to the user. The user has to guess
     the words in given number of chance in order to win the game.
     Number of chances: length of word + 2
    """
    def __init__(self):
        self.__main_window = Tk()
        self.__keys = []
        self.__placeholders = []
        self.__buttons = []
        self.__words = []
        self.__selected_word = ''
        self.__chances = 0
        self.__guessed_word = ''
        self.__game_tips = Label(self.__main_window, text=f'Guess letters for the word')
        self.__game_tips.grid(row=6, column=1)
        self.__start_new_game_button = Button(self.__main_window, text="Start New Game", command=self.reset_frame)
        self.__start_new_game_button.grid(row=7, column=1)
        self.__exit_button = Button(self.__main_window, text="Exit", command=self.stop)
        self.__exit_button.grid(row=7, column=2)

    def set_key_list(self):
        """
        A class method which adds the required keys to render in the virtual keyboard using chr function.
        The unicode for capital letter A is 65 and B is 66 and so on.
        """
        for i in range(65, 65 + 26):
            self.__keys.append(chr(i))

    def set_buttons(self):
        """
        Method to create button objects for each key starting from A to Z.
        """
        for character in self.__keys:
            # Attaching an action to each button.
            def action(x=character):
                return self.pressed_key(x)

            button = Button(self.__main_window, text=character, width=6, command=action,
                            pady=10, padx=10)
            self.__buttons.append(button)

    def add_buttons_to_grid(self):
        """
        Adds button to the grid in a specific position
        """
        row = 1
        col = 1
        for button in self.__buttons:
            if col % 9 == 0:
                col = 1
                row += 1
            button.grid(row=row, column=col, padx=10, pady=10)
            col += 1

    def load_resource(self):
        """
        Loads the required resources for starting the game.
        """
        self.set_key_list()
        self.set_buttons()
        self.add_buttons_to_grid()
        self.get_words_from_file()
        self.set_selected_word()
        self.set_place_holder()
        self.add_placeholders_to_grid()
        self.__main_window.title("Hangman")
        self.__main_window.geometry('1080x500')

    def get_words_from_file(self):
        """
        Method to read the text file containing words and append it to the instance variable __words.
        """
        lines = open('words.txt').readlines()
        for word in lines:
            self.__words.append(str.rstrip(word).upper())

    def set_selected_word(self):
        """
        Method to set words used in the game.
        """

        # Picking up random word from instance variable words.
        self.__selected_word = random.choice(self.__words)

        # Number of chance for each game is selected word + 2.
        self.__chances = len(self.__selected_word) + 2

        self.__guessed_word = ' ' * len(self.__selected_word)
        self.__game_tips.config(text=f'Remaining chances: {self.__chances}')

    def set_place_holder(self):
        """
        Adds the labels that are used to display the selected word.
        """
        random_letter = random.choice(self.__selected_word)
        for letter in self.__selected_word:
            if letter == random_letter:
                label = Label(self.__main_window, text=letter, borderwidth=2, relief="raised", bg="white", padx=10,
                              pady=10)
                self.__placeholders.append(label)
                word_indexes = [pos for pos, char in enumerate(self.__selected_word) if char == random_letter]
                for word_index in word_indexes:
                    self.__guessed_word = self.__guessed_word[:word_index] + random_letter + \
                                          self.__guessed_word[word_index + 1:]
            else:
                label = Label(self.__main_window, borderwidth=2, relief="raised", bg="white", padx=10, pady=10)
                self.__placeholders.append(label)

    def add_placeholders_to_grid(self):
        """
        Renders the labels to the grid.
        """
        row = 0
        col = 0
        for placeholder in self.__placeholders:
            placeholder.grid(row=row, column=col, padx=10, pady=10)
            col += 1

    def check_results(self):
        """
        Checks the results or updates the remaining chances.
        """
        if self.__guessed_word == self.__selected_word:
            self.__game_tips.config(text="You won!", fg="#00FF00")
        else:
            if self.__chances <= 0:
                self.__game_tips.config(text=f'Game Over. The word was {self.__selected_word}', fg="#FF0000")
                self.__guessed_word = ''
            else:
                self.__game_tips.config(text=f'Remaining chances: {self.__chances}')

    def pressed_key(self, key):
        """
        Detects the pressed key in the virtual keyboard and places the key in the label if it's in the selected word
        and deducts the remaining chances.
        :param key:
        """
        found_indexes = [pos for pos, char in enumerate(self.__selected_word) if char == key]

        if len(found_indexes) > 0:
            for word_index in found_indexes:
                self.__placeholders[word_index].config(text=self.__selected_word[word_index])
                self.__chances -= 1
                self.__guessed_word = self.__guessed_word[:word_index] + self.__selected_word[word_index] + \
                                      self.__guessed_word[word_index + 1:]
        else:
            self.__chances -= 1

        self.check_results()

    def empty_resource(self):
        """
        Empties the frame and initializes all the instance variables.
        """
        prev_children = self.__main_window.winfo_children()
        if len(prev_children) > 0:
            for child in prev_children:
                child.destroy()
        self.__game_tips = Label(self.__main_window, text=f'Remaining chances: {self.__chances}')
        self.__game_tips.grid(row=6, column=1)
        self.__start_new_game_button = Button(self.__main_window, text="Start New Game", command=self.reset_frame)
        self.__start_new_game_button.grid(row=7, column=1)
        self.__exit_button = Button(self.__main_window, text="Exit", command=self.stop)
        self.__exit_button.grid(row=7, column=2)
        self.__keys = []
        self.__placeholders = []
        self.__buttons = []
        self.__words = []
        self.__selected_word = ''
        self.__chances = 0
        self.__guessed_word = ''

    def reset_frame(self):
        """
        Resets the main frame and variables to start a new game.
        """
        self.empty_resource()
        self.load_resource()

    def stop(self):
        """
        Ends the execution of the program.
        """
        self.__main_window.destroy()

    def start(self):
        """
        Starts the mainloop by setting window title and size of the window.
        """

        self.load_resource()
        self.__main_window.mainloop()


def main():
    """
    Calls the HangMan class by creating its object.
    """
    ui = HangMan()
    ui.start()


if __name__ == "__main__":
    main()
