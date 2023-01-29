import csv
import random
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox


class QuizGame(tk.Tk):
    def __init__(self, csv_file):
        super().__init__()

        # Window properties
        self.title("Quiz Game")
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        # Window size and placement
        width, height = 640, 250
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        win_x, win_y = ((screen_width / 2) - width / 2
                        ), ((screen_height / 2) - height / 2)
        self.geometry("%dx%d+%d+%d" % (width, height, win_x, win_y))
        self.resizable(0, 0)

        # Game data variables
        self.questions_file = csv_file
        self.user_answer = tk.StringVar()

        # Keep track of questions and correct answers
        self.question_num = 0
        self.questions_correct = 0

        # Allow Enter key to submit answer
        self.bind("<Return>", self.submit_question)

        # Build dictionary of questions/answers from CSV file
        self.build_dict()
        self.get_question()

        # Set up and display window
        self.place_widgets()
        self.mainloop()

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

# Fetch a random question from the question list and update correct answers
    def get_question(self):
        self.question_num += 1

        self.question = self.question_list[(
            random.randint(0, len(self.question_list) - 1))]

        self.question_text = f"Question {self.question_num}: \n{self.question}"

        self.correct_answers = []
        [self.correct_answers.append(i.lower().strip())
         for i in self.questions_dict.get(self.question)]

# Check for the correct answer
    def check_answer(self):
        if self.user_answer.get().lower() in self.correct_answers:
            messagebox.showinfo(
                "Nice!", f"{self.user_answer.get()} is the correct answer :)")
            self.questions_correct += 1
        else:
            # Wrong answer condition
            pass

# Update the question + answer entry labels
    def update_widgets(self):
        self.label_question.config(text=self.question_text)
        self.user_answer.set("")
        self.entry_answer.config(textvariable=self.user_answer)

# Tasks to perform upon submitting the answer
    def submit_question(self, event):
        self.check_answer()
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

        # SUBMIT BUTTON
        btn_submit = ttk.Button(frame, text="Submit", style="TButton", takefocus=1,
                                command=lambda: self.submit_question(event=None))
        btn_submit.grid(row=1, columnspan=3)


"""
# used for testing purposes
if __name__ == "__main__":
    t = QuizGame("questions.csv")
"""
