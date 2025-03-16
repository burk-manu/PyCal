import tkinter as tk
from math import sqrt

class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Calculator")
        self.root.geometry("400x650")
        self.root.configure(bg="#1E1E1E")  # Modern dark background

        # Variables
        self.current_input = ""
        self.memory = 0
        self.history = []

        # Fonts
        self.display_font = ("Helvetica Neue", 28, "bold")
        self.button_font = ("Helvetica Neue", 16, "bold")
        self.history_font = ("Helvetica Neue", 12)

        # Create a frame for the display area with extra padding
        self.display_frame = tk.Frame(root, bg="#1E1E1E")
        self.display_frame.pack(fill=tk.BOTH, padx=20, pady=(20, 10))

        # Entry widget for calculator display
        self.entry = tk.Entry(
            self.display_frame,
            font=self.display_font,
            justify="right",
            bd=0,
            relief=tk.FLAT,
            bg="#2D2D2D",
            fg="#FFFFFF",
            insertbackground="#FFFFFF"
        )
        self.entry.pack(fill=tk.BOTH, ipadx=10, ipady=20)

        # Label for displaying history (last few calculations)
        self.history_label = tk.Label(
            root,
            text="",
            font=self.history_font,
            bg="#1E1E1E",
            fg="#80CBC4",
            anchor="e",
            justify="right"
        )
        self.history_label.pack(fill=tk.BOTH, padx=20, pady=(0,10))

        # Frame for the buttons with padding
        self.button_frame = tk.Frame(root, bg="#1E1E1E")
        self.button_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

        # Define button layout (each row is a tuple of button labels)
        buttons = [
            ("MC", "MR", "M+", "M-", "C"),
            ("√", "^", "%", "/", "*"),
            ("7", "8", "9", "-", "("),
            ("4", "5", "6", "+", ")"),
            ("1", "2", "3", "=", "⌫"),
            ("0", ".", "±", "AC", "History")
        ]

        # Colors for the buttons
        self.button_bg = "#3C3F41"
        self.button_fg = "#A9B7C6"
        self.button_active_bg = "#4E5254"

        # Create and place buttons in a grid layout
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                button = tk.Button(
                    self.button_frame,
                    text=text,
                    font=self.button_font,
                    bg=self.button_bg,
                    fg=self.button_fg,
                    bd=0,
                    relief=tk.FLAT,
                    activebackground=self.button_active_bg,
                    activeforeground="#FFFFFF",
                    command=lambda t=text: self.on_button_click(t)
                )
                button.grid(row=i, column=j, sticky="nsew", padx=5, pady=5)
                # Add hover effects
                button.bind("<Enter>", lambda e, b=button: b.config(bg=self.button_active_bg))
                button.bind("<Leave>", lambda e, b=button: b.config(bg=self.button_bg))

        # Configure grid so buttons expand evenly
        rows = len(buttons)
        cols = len(buttons[0])
        for i in range(rows):
            self.button_frame.grid_rowconfigure(i, weight=1)
        for j in range(cols):
            self.button_frame.grid_columnconfigure(j, weight=1)

        # Bind keyboard events to allow typing from the keyboard
        self.root.bind("<Key>", self.on_key_press)

    def on_button_click(self, text):
        if text == "=":
            self.calculate_result()
        elif text == "C":
            self.clear_entry()
        elif text == "AC":
            self.clear_all()
        elif text == "⌫":
            self.backspace()
        elif text == "±":
            self.toggle_sign()
        elif text == "√":
            self.square_root()
        elif text == "^":
            self.exponentiation()
        elif text == "%":
            self.modulus()
        elif text == "MC":
            self.memory_clear()
        elif text == "MR":
            self.memory_recall()
        elif text == "M+":
            self.memory_add()
        elif text == "M-":
            self.memory_subtract()
        elif text == "History":
            self.show_history()
        else:
            self.update_entry(text)

    def on_key_press(self, event):
        key = event.char
        if key.isdigit() or key in "+-*/%().":
            self.update_entry(key)
        elif key == "\r":  # Enter key
            self.calculate_result()
        elif key == "\x08":  # Backspace key
            self.backspace()

    def update_entry(self, text):
        self.current_input += text
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.current_input)

    def clear_entry(self):
        self.current_input = ""
        self.entry.delete(0, tk.END)

    def clear_all(self):
        self.clear_entry()
        self.history_label.config(text="")

    def backspace(self):
        self.current_input = self.current_input[:-1]
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.current_input)

    def toggle_sign(self):
        if self.current_input:
            if self.current_input[0] == "-":
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, self.current_input)

    def square_root(self):
        try:
            result = sqrt(float(self.current_input))
            self.current_input = str(result)
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, self.current_input)
        except Exception:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Error")

    def exponentiation(self):
        self.update_entry("**")

    def modulus(self):
        self.update_entry("%")

    def calculate_result(self):
        try:
            result = eval(self.current_input)
            self.history.append(f"{self.current_input} = {result}")
            self.current_input = str(result)
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, self.current_input)
        except Exception:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Error")

    def memory_clear(self):
        self.memory = 0

    def memory_recall(self):
        self.update_entry(str(self.memory))

    def memory_add(self):
        try:
            self.memory += float(self.current_input)
        except Exception:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Error")

    def memory_subtract(self):
        try:
            self.memory -= float(self.current_input)
        except Exception:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Error")

    def show_history(self):
        history_text = "\n".join(self.history[-5:])  # Show last 5 calculations
        self.history_label.config(text=history_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernCalculator(root)
    root.mainloop()
