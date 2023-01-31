import csv
import random
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox


class MessageBox(tk.Toplevel):
    def __init__(self, correct, answer, possible_answers):
        super().__init__()

        self.focus_set()

        # Set window title
        if correct:
            self.title("Nice!")
            self.message = f"{answer} is correct!"
        else:
            self.title("Not quite...")
            self.correct_answers = "\n  ".join(possible_answers)
            self.message = f"Sorry, {answer} is incorrect.\n\nPossible choices were:\n  {self.correct_answers}"

        # Set window size and placement
        width, height = 300, 200
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        win_x, win_y = ((screen_width / 2) - width / 2
                        ), ((screen_height / 2) - height / 2)
        self.geometry("%dx%d+%d+%d" % (width, height, win_x, win_y))
        self.resizable(0, 0)

        self.bind("<Return>", self.exit_window)

        self.place_widgets()
        self.mainloop()

    def exit_window(self, event):
        self.destroy()
        self.quit()

    def place_widgets(self):
        label_message = tk.Label(
            self, text=self.message, justify="left", font="calibri, 12")
        label_message.pack(anchor="center", expand=True)

        btn_okay = tk.Button(self, text="Okay", width=20, takefocus=1,
                             command=lambda: self.exit_window(event=None), anchor="s", padx=10, justify="center")
        btn_okay.pack(pady=20)


class QuizGame(tk.Tk):
    def __init__(self, csv_file, quiz_type):
        super().__init__()

        # Window properties
        self.title("Quiz Game")
        self.protocol("WM_DELETE_WINDOW", self.end_game)

        # Window size and placement
        width, height = 640, 250
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        win_x, win_y = ((screen_width / 2) - width / 2
                        ), ((screen_height / 2) - height / 2)
        self.geometry("%dx%d+%d+%d" % (width, height, win_x, win_y))
        self.resizable(0, 0)

        # Game data variables
        self.questions_file = csv_file
        self.game_mode = quiz_type
        self.user_answer = tk.StringVar()

        print(f"\n\nQuiz Game started")
        print(f"Using CSV file: {self.questions_file}")
        print(f"Selected game mode: {self.game_mode}")

        # Keep track of questions and correct answers
        self.question_index = 0
        self.questions_correct = 0
        # Used for displaying questions
        self.question_label = 1

        self.running = True
        if self.running:
            # Allow Enter key to submit answer
            self.bind("<Return>", self.submit_question)

            # Build dictionary of questions/answers from CSV file
            self.build_dict()
            self.get_question()

            # Set up and display window
            self.place_widgets()
            self.mainloop()

# Build a dictionary of questions/answers from the CSV file and create a list to index questions
    def build_dict(self):
        self.questions_dict = {}

        # Read from the CSV file (more robust error checking takes place in menu.py)
        try:
            with open(self.questions_file, "r") as csv_file:
                c = csv.reader(csv_file)
                for row in c:
                    self.questions_dict.update({row[0]: row[1::]})
        except FileNotFoundError:
            messagebox.showerror(
                "Error!", "Your CSV file is no longer present.\n\nPlease restart the application and select a CSV file.")

        # Use a list to index and randomly select questions (keys) from the dictionary
        self.question_list = []
        [self.question_list.append(i) for i in self.questions_dict.keys()]

        # Shuffle the list if shuffle game mode
        if self.game_mode == "shuffle":
            random.shuffle(self.question_list)

# Fetch a question from the list and update correct answers
    def get_question(self):

        # check quiz type
        if self.game_mode == "endless":
            self.question = self.question_list[(
                random.randint(0, len(self.question_list) - 1))]

        if self.game_mode == "shuffle":
            if self.question_index < len(self.question_list):
                self.question = self.question_list[self.question_index]
            else:
                self.end_game()

        # display the question
        self.question_text = f"Question {self.question_label}: \n{self.question}"
        self.question_index += 1
        self.question_label += 1

        # populate list of correct answers
        self.correct_answers = []
        [self.correct_answers.append(i.lower().strip())
            for i in self.questions_dict.get(self.question)]

# Check for the correct answer
    def check_answer(self):
        # Correct answer condition
        if self.user_answer.get().lower() in self.correct_answers:
            MessageBox(True, self.user_answer.get(), self.correct_answers)
            self.questions_correct += 1

        # Wrong answer condition
        else:
            MessageBox(False, self.user_answer.get(), self.correct_answers)

# Update the question + answer entry labels
    def update_widgets(self):
        if self.running:
            self.label_question.config(text=self.question_text)
            self.user_answer.set("")
            self.entry_answer.config(textvariable=self.user_answer)
            self.entry_answer.focus()

# Tasks to perform upon submitting the answer
    def submit_question(self, event):
        self.check_answer()
        self.focus_set()
        self.get_question()
        self.update_widgets()

# Set up and place widgets in the application window
    def place_widgets(self):
        # STYLING
        style = ttk.Style()
        style.configure("TButton", font=(
            "calibri", 15), foreground="black", background="white")

        # QUESTION TEXT
        self.label_question = tk.Label(self,
                                       text=self.question_text, font="Arial, 15")
        self.label_question.pack(pady=25, anchor="n")

        # separate frame for buttons, text entry
        frame = tk.Frame(self)
        frame.pack(expand=True, anchor="n")

        # ANSWER ENTRY BOX
        label_answer = tk.Label(frame, text="Answer: ", font="Arial, 10")
        self.entry_answer = ttk.Entry(
            frame, textvariable=self.user_answer, font="Arial, 12", width=32)
        label_answer.grid(row=0, column=0)
        self.entry_answer.grid(row=0, column=1, padx=10, pady=20)
        self.entry_answer.focus()

        # SUBMIT BUTTON
        self.btn_submit = ttk.Button(frame, text="Submit", style="TButton", state=tk.NORMAL,
                                     command=lambda: self.submit_question(event=None))
        self.btn_submit.grid(row=1, columnspan=3)

# Called when 'X' button in window manager is pressed
    def end_game(self):
        self.running = False

        if self.game_mode == "endless":
            self.question_index -= 1

        # display num. of correct answers, will add yes/no dialog in the future
        messagebox.showinfo(
            "Finished", f"You got {self.questions_correct} out of {self.question_index} questions correct!")

        # close the application
        self.destroy()


# used for testing purposes
if __name__ == "__main__":
    t = QuizGame("questions.csv", "shuffle")
