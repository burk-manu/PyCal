import tkinter as tk
from math import sqrt

class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Calculator")
        self.root.geometry("400x600")
        self.root.configure(bg="#1e1e1e")  # Dark background
        self.root.resizable(False, False)

        # Variables
        self.current_input = ""
        self.memory = 0
        self.history = []

        # Custom font
        self.font = ("Helvetica", 18)
        self.font_bold = ("Helvetica", 18, "bold")

        # Entry widget for display
        self.entry = tk.Entry(
            root, font=("Helvetica", 24), justify="right", bd=0, relief=tk.FLAT,
            bg="#2d2d2d", fg="#ffffff", insertbackground="#ffffff"
        )
        self.entry.pack(fill=tk.BOTH, ipadx=10, ipady=20, padx=20, pady=20)

        # Button frame
        button_frame = tk.Frame(root, bg="#1e1e1e")
        button_frame.pack(padx=10, pady=10)

        # Button layout
        buttons = [
            ("C", "⌫", "%", "/"),
            ("7", "8", "9", "*"),
            ("4", "5", "6", "-"),
            ("1", "2", "3", "+"),
            ("±", "0", ".", "=")
        ]

        # Add buttons to the frame
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                button = tk.Button(
                    button_frame, text=text, font=self.font_bold, padx=20, pady=20,
                    bg="#3d3d3d", fg="#ffffff", bd=0, relief=tk.FLAT,
                    activebackground="#4d4d4d", activeforeground="#ffffff",
                    command=lambda t=text: self.on_button_click(t)
                )
                button.grid(row=i, column=j, sticky="nsew", padx=5, pady=5)
                button.bind("<Enter>", lambda e, b=button: b.config(bg="#4d4d4d"))
                button.bind("<Leave>", lambda e, b=button: b.config(bg="#3d3d3d"))

        # Configure grid to expand buttons evenly
        for i in range(len(buttons)):
            button_frame.grid_rowconfigure(i, weight=1)
        for j in range(len(buttons[0])):
            button_frame.grid_columnconfigure(j, weight=1)

        # Bind keyboard events
        self.root.bind("<Key>", self.on_key_press)

    def on_button_click(self, text):
        if text == "=":
            self.calculate_result()
        elif text == "C":
            self.clear_entry()
        elif text == "⌫":
            self.backspace()
        elif text == "±":
            self.toggle_sign()
        elif text == "%":
            self.modulus()
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
        self.entry.insert(0, self.current_input)

    def clear_entry(self):
        self.current_input = ""
        self.entry.delete(0, tk.END)

    def backspace(self):
        self.current_input = self.current_input[:-1]
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.current_input)

    def toggle_sign(self):
        if self.current_input and self.current_input[0] == "-":
            self.current_input = self.current_input[1:]
        else:
            self.current_input = "-" + self.current_input
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.current_input)

    def modulus(self):
        try:
            result = float(self.current_input) / 100
            self.current_input = str(result)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.current_input)
        except Exception:
            self.show_error()

    def calculate_result(self):
        try:
            result = eval(self.current_input)
            self.current_input = str(result)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.current_input)
        except Exception:
            self.show_error()

    def show_error(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, "Error")
        self.root.after(1000, self.clear_entry)


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ModernCalculator(root)
    root.mainloop()