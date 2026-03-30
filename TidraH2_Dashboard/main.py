# main.py

import tkinter as tk
from frontend.page1_inputs import Page1Inputs
from frontend.page2_validation import Page2Validation
from frontend.page3_simulation import Page3Simulation
from frontend.page4_results import Page4Results

class TidraH2App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TidraH2: Territorial Interface for Dakhla’s Renewable Advancement")
        self.geometry("800x600")

        self.shared_data = {}  # Dictionary to pass data between pages

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (Page1Inputs, Page2Validation, Page3Simulation, Page4Results):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Page1Inputs")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = TidraH2App()
    app.mainloop()

