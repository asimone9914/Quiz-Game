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
        # csv_file = "questions.csv"
        self.questions_file = csv_file
        self.user_answer = tk.StringVar()

        self.question_num = 0
        self.questions_correct = 0

        self.build_dict()
        self.get_question()

        # Set up and display window
        self.place_widgets()
        self.mainloop()

    def build_dict(self):
        self.questions_dict = {}
        try:
            with open(self.questions_file, "r") as csv_file:
                c = csv.reader(csv_file)

                for row in c:
                    self.questions_dict.update({row[0]: row[1::]})
        except FileNotFoundError:
            print("Uh oh, file not found!")

    def get_question(self):
        self.question_num += 1

        question_list = []
        [question_list.append(i) for i in self.questions_dict.keys()]

        self.question = question_list[(
            random.randint(0, len(question_list) - 1))]

        self.question_text = f"Question {self.question_num}: \n{self.question}"

        self.correct_answers = []
        [self.correct_answers.append(i.lower().strip())
         for i in self.questions_dict.get(self.question)]

        # print(self.question, self.correct_answers)

    def check_answer(self):
        if self.user_answer.get().lower() in self.correct_answers:
            messagebox.showinfo(
                "Nice!", f"{self.user_answer.get()} is the correct answer :)")
            self.questions_correct += 1
        else:
            print("u got it wrong lol")

    def place_widgets(self):
        def update_widgets():
            # Function will update Question and Entry with new values
            # after Submit button has been clicked
            label_question.config(text=self.question_text)
            self.user_answer.set("")
            entry_answer.config(textvariable=self.user_answer)

        # STYLING
        style = ttk.Style()
        style.configure("TButton", font=(
            "calibri", 15), foreground="black", background="white")

        # QUESTION TEXT
        label_question = tk.Label(self,
                                  text=self.question_text, font="Arial, 15")
        label_question.pack(pady=25, anchor="n")

        # separate frame for buttons, text entry
        frame = tk.Frame(self)
        frame.pack(expand=True, anchor="n")

        # ANSWER ENTRY BOX
        label_answer = tk.Label(frame, text="Answer: ", font="Arial, 10")
        entry_answer = ttk.Entry(
            frame, textvariable=self.user_answer, font="Arial, 12", width=32)
        label_answer.grid(row=0, column=0)
        entry_answer.grid(row=0, column=1, padx=10, pady=20)

        # SUBMIT BUTTON
        btn_submit = ttk.Button(frame, text="Submit", style="TButton",
                                command=lambda: [self.check_answer(), self.get_question(), update_widgets()])
        btn_submit.grid(row=1, columnspan=3)


t = QuizGame("questions.csv")
