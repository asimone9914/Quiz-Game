import tkinter as tk
import tkinter.ttk as ttk
import pathlib
import csv
from tkinter import StringVar
from tkinter import filedialog
from tkinter import messagebox
from game import QuizGame


class QuizGameMenu(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window properties
        self.title("Quiz Game")
        self.game_title = "Example Quiz Game"
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        # Window size and placement
        width, height = 500, 350
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        win_x, win_y = ((screen_width / 2) - width / 2
                        ), ((screen_height / 2) - height / 2)
        self.geometry("%dx%d+%d+%d" % (width, height, win_x, win_y))
        self.resizable(0, 0)

        # Set location of csv file
        self.csv_path = StringVar()
        self.csv_path.set(pathlib.Path("questions.csv"))

        # Set up and display window
        self.place_widgets()
        self.mainloop()

    def browse_files(self):
        self.filename = filedialog.askopenfilename(
            initialdir=__file__, title="Select questions file", filetypes=(("Comma-separated values", "*.csv*"), ("All files", "*.*")))
        self.csv_path.set(self.filename)

    def verify_input(self):
        valid_input = False

        if self.csv_path.get().endswith(".csv"):
            try:
                with open(self.csv_path.get(), "r") as file:
                    c = csv.reader(file)
                    for row in c:
                        try:
                            if row == [] or row[1] == "":
                                messagebox.showerror("Error!",
                                                     "Your CSV file has empty lines.\n\nPlease try again.")
                                break
                            else:
                                valid_input = True
                        except IndexError:
                            messagebox.showerror("Error!",
                                                 "Your .csv file is not formatted properly.\n\nPlease try again.")
                            break

            except UnicodeDecodeError:
                messagebox.showerror(
                    "Error!", "Invalid file type. Please try again.")
        else:
            messagebox.showerror(
                "Error!", "You must select a file with a .csv extension")

        if valid_input:
            self.destroy()
            QuizGame(self.csv_path.get())

    def place_widgets(self):
        # configure Ttk styling
        style = ttk.Style()
        style.configure("TButton", font=(
            "calibri", 10, "bold"), foreground="black", background="white")

        # LOGO
        logo = tk.Label(self, text=self.game_title,
                        font=("Arial, 18"))
        logo.pack(pady=10, anchor="n", fill="both", expand=1)

        # --- TOP FRAME --- 
        frame_top = tk.Frame(self)
        frame_top.pack(expand=True, anchor="n")

        # select csv file
        label_csv = tk.Label(frame_top, text="CSV file: ",
                             font=("Arial, 10"))
        label_csv.grid(row=0, column=0)

        entry_csv = tk.Entry(frame_top, width=30, textvariable=self.csv_path)
        entry_csv.grid(row=0, column=1)

        btn_browse = ttk.Button(
            frame_top, text="browse", style="W.TButton", command=self.browse_files)
        btn_browse.grid(row=0, column=2)

        # --- BOTTOM FRAME --- 
        frame_bottom = tk.Frame(self)
        frame_bottom.pack(expand=True, anchor="n")

        # start button
        btn_start = ttk.Button(
            frame_bottom, text="Start Quiz", width=25, command=lambda: self.verify_input())
        btn_start.grid(row=1, columnspan=3)

        # about program button
        btn_about = ttk.Button(
            frame_bottom, text="About program", width=25, command=lambda: print("about quiz"))
        btn_about.grid(row=2, columnspan=3)

        # exit button
        btn_exit = ttk.Button(frame_bottom, text="Exit", width=25,
                              command=self.destroy)
        btn_exit.grid(row=3, columnspan=3)


if __name__ == "__main__":
    qg = QuizGameMenu()
