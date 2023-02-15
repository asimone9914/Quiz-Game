from csv import reader
from random import shuffle, randint
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
        self.width, self.height = 640, 250
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        win_x, win_y = ((screen_width / 2) - self.width / 2
                        ), ((screen_height / 2) - self.height / 2)
        self.geometry("%dx%d+%d+%d" % (self.width, self.height, win_x, win_y))
        self.resizable(0, 0)

        # Game data variables
        self.questions_file = csv_file
        self.game_mode = quiz_type
        self.user_answer = tk.StringVar()

        print(f"\n\n[ QUIZ GAME STARTED ]")
        print(f"Using CSV file: {self.questions_file}")
        print(f"Selected game mode: {self.game_mode}")

        # Keep track of questions and correct answers
        self.question_index = 0
        self.questions_correct = 0

        # Used for displaying question number
        self.question_number = 1

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
                c = reader(csv_file)
                for row in c:
                    self.questions_dict.update({row[0]: row[1::]})
        except FileNotFoundError:
            messagebox.showerror(
                "Error!", "Your CSV file is no longer present.\n\nPlease restart the application and select a CSV file.")

        # Use a list to index and randomly select questions (keys) from the dictionary
        self.question_list = []
        [self.question_list.append(i) for i in self.questions_dict.keys()]

        # Total number of questions;  used with shuffle game mode
        self.total_num_questions = len(self.question_list)

        # Shuffle the list if shuffle game mode
        if self.game_mode == "shuffle":
            shuffle(self.question_list)

# Fetch a question from the list and update correct answers
    def get_question(self):
        if not self.question_index == self.total_num_questions:

            # get random question if endless game mode
            if self.game_mode == "endless":
                self.question = self.question_list[(
                    randint(0, len(self.question_list) - 1))]

            # iterate through the list if shuffle game mode
            if self.game_mode == "shuffle":
                self.question = self.question_list[self.question_index]
                self.question_index += 1

            # populate list of correct answers
            self.correct_answers = []
            [self.correct_answers.append(i.lower().strip())
                for i in self.questions_dict.get(self.question)]
        else:
            self.end_game()

# Check for the correct answer
    def check_answer(self):
        self.question_number += 1
        submitted_answer = self.user_answer.get().strip().lower()

        # function for input sanitization
        def sanitize(answer):
            bad_chars = [",", "-", "/"]
            for x in bad_chars:
                if x == "-":
                    answer = answer.replace(x, " ")
                else:
                    answer = answer.replace(x, "")
            return answer

        # sanitize the correct answers list
        for i in range(len(self.correct_answers)):
            self.correct_answers[i] = sanitize(self.correct_answers[i])

        # sanitize the user submitted answer
        submitted_answer = sanitize(submitted_answer)

        # Correct answer condition
        if submitted_answer.lower() in self.correct_answers:
            MessageBox(True, self.user_answer.get(), self.correct_answers)
            self.questions_correct += 1

        # Wrong answer condition
        else:
            MessageBox(False, self.user_answer.get(), self.correct_answers)

# Update the question + answer entry labels
    def update_widgets(self):
        if self.running:
            self.label_number.config(text=f"Question {self.question_number}")
            self.label_question.config(text=self.question)
            self.update()
            self.size_question()

            self.user_answer.set("")
            self.entry_answer.config(textvariable=self.user_answer)
            self.entry_answer.focus()

# rudimentary function to adjust question if it goes off screen
    def size_question(self):
        # print(
        #    f"\nQuestion label width: {self.label_question.winfo_width()} pixels")

        question_words = self.question.split()
        question_wc = len(question_words)

        mid = (question_wc // 2)

        if self.label_question.winfo_width() > (self.width - 32):
            question_words[mid] = (question_words[mid] + "\n")
            self.question = " ".join(question_words)
            self.label_question.configure(text=self.question)

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

        # QUESTION NUMBER
        self.label_number = tk.Label(self, font="Arial, 12")
        self.label_number.pack(anchor="nw", padx=4)

        # QUESTION TEXT
        self.label_question = tk.Label(self, font="Arial, 15")
        self.label_question.pack(anchor="n", pady=8)

        # separate frame for buttons, text entry
        frame = tk.Frame(self)
        frame.pack(expand=True, anchor="s", pady=20)

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

        self.update_widgets()

# Called when 'X' button in window manager is pressed
    def end_game(self):
        self.running = False

        self.question_number -= 1

        # display num. of correct answers, will add yes/no dialog in the future
        messagebox.showinfo(
            "Finished", f"You got {self.questions_correct} out of {self.question_number} questions correct!")

        # close the application
        self.destroy()


# used for testing purposes
if __name__ == "__main__":
    t = QuizGame("questions.csv", "shuffle")
