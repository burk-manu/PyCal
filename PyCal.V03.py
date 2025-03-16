import tkinter as tk
from math import sqrt, pow

class AdvancedCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("400x600")
        self.root.configure(bg="#2E3440")  # Dark background

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
            bg="#3B4252", fg="#ECEFF4", insertbackground="#ECEFF4"
        )
        self.entry.pack(fill=tk.BOTH, ipadx=10, ipady=20, padx=10, pady=10)

        # History display
        self.history_label = tk.Label(
            root, text="", font=("Helvetica", 12), bg="#2E3440", fg="#88C0D0"
        )
        self.history_label.pack(fill=tk.BOTH, padx=10, pady=5)

        # Button frame
        button_frame = tk.Frame(root, bg="#2E3440")
        button_frame.pack()

        # Button layout
        buttons = [
            ("MC", "MR", "M+", "M-", "C"),
            ("√", "^", "%", "/", "*"),
            ("7", "8", "9", "-", "("),
            ("4", "5", "6", "+", ")"),
            ("1", "2", "3", "=", "⌫"),
            ("0", ".", "±", "AC", "History")
        ]

        # Add buttons to the frame
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                button = tk.Button(
                    button_frame, text=text, font=self.font_bold, padx=20, pady=20,
                    bg="#4C566A", fg="#ECEFF4", bd=0, relief=tk.FLAT,
                    activebackground="#5E81AC", activeforeground="#ECEFF4",
                    command=lambda t=text: self.on_button_click(t)
                )
                button.grid(row=i, column=j, sticky="nsew", padx=5, pady=5)
                button.bind("<Enter>", lambda e, b=button: b.config(bg="#5E81AC"))
                button.bind("<Leave>", lambda e, b=button: b.config(bg="#4C566A"))

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
        self.entry.insert(0, self.current_input)

    def clear_entry(self):
        self.current_input = ""
        self.entry.delete(0, tk.END)

    def clear_all(self):
        self.clear_entry()
        self.history_label.config(text="")

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

    def square_root(self):
        try:
            result = sqrt(float(self.current_input))
            self.current_input = str(result)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.current_input)
        except Exception:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Error")

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
            self.entry.insert(0, self.current_input)
        except Exception:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Error")

    def memory_clear(self):
        self.memory = 0

    def memory_recall(self):
        self.update_entry(str(self.memory))

    def memory_add(self):
        try:
            self.memory += float(self.current_input)
        except Exception:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Error")

    def memory_subtract(self):
        try:
            self.memory -= float(self.current_input)
        except Exception:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Error")

    def show_history(self):
        history_text = "\n".join(self.history[-5:])  # Show last 5 calculations
        self.history_label.config(text=history_text)


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedCalculator(root)
    root.mainloop()