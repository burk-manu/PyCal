import tkinter as tk
from math import sqrt, log, log10, sin, cos, tan, pi, e

def get_button_colors(label):
    """
    Returns a tuple (frame_color, _) based on the button label.
    """
    if label in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "±"}:
        return ("#00C853", "#B9F6CA")
    elif label == "=":
        return ("#FFD600", "#FFFF8D")
    elif label in {"+", "-", "*", "/", "%", "^", "√", "(", ")", "log", "ln", "|x|", "sin", "cos", "tan", "π", "e"}:
        return ("#D500F9", "#EA80FC")
    elif label in {"MC", "MR", "M+", "M-", "C"}:
        return ("#2979FF", "#82B1FF")
    elif label in {"⌫", "History", "AC"}:
        return ("#FF3D00", "#FF8A65")
    else:
        return ("#0D47A1", "#42A5F5")

class NeonCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Gamer Neon Calculator")
        self.root.geometry("500x750")
        self.root.configure(bg="#121212")
        self.current_input = ""
        self.memory = 0
        self.history = []

        self.entry = tk.Entry(root, font=("Helvetica Neue", 32, "bold"), justify="right", bd=0,
                              relief=tk.FLAT, bg="#1E1E1E", fg="#00E5FF", insertbackground="#00E5FF")
        self.entry.pack(fill=tk.BOTH, ipadx=10, ipady=20, padx=20, pady=(20, 10))
        
        self.history_label = tk.Label(root, text="", font=("Helvetica Neue", 12), bg="#121212", fg="#80DEEA", 
                                      anchor="e", justify="right")
        self.history_label.pack(fill=tk.BOTH, padx=20, pady=(0, 10))
        
        self.button_frame = tk.Frame(root, bg="#121212")
        self.button_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

        buttons = [
            ("MC", "MR", "M+", "M-", "C"),
            ("log", "ln", "|x|", "√", "^"),
            ("7", "8", "9", "/", "("),
            ("4", "5", "6", "*", ")"),
            ("1", "2", "3", "-", "π"),
            ("0", ".", "±", "+", "e"),
            ("sin", "cos", "tan", "=", "⌫"),
        ]

        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                frame_color, _ = get_button_colors(text)
                btn = tk.Button(
                    self.button_frame, text=text, font=("Helvetica Neue", 16, "bold"),
                    bg="#222222", fg="#FFFFFF", width=5, height=2, bd=0,
                    activebackground="#444444", command=lambda t=text: self.on_button_click(t)
                )
                btn.grid(row=i, column=j, padx=8, pady=8, sticky="nsew")

        for i in range(len(buttons)):
            self.button_frame.grid_rowconfigure(i, weight=1)
        for j in range(len(buttons[0])):
            self.button_frame.grid_columnconfigure(j, weight=1)

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
            self.update_entry("**")
        elif text == "|x|":
            self.absolute_value()
        elif text == "log":
            self.log_base_10()
        elif text == "ln":
            self.natural_log()
        elif text in {"sin", "cos", "tan"}:
            self.trigonometric_function(text)
        elif text == "π":
            self.update_entry(str(pi))
        elif text == "e":
            self.update_entry(str(e))
        else:
            self.update_entry(text)

    def on_key_press(self, event):
        key = event.char
        if key.isdigit() or key in "+-*/%().":
            self.update_entry(key)
        elif key == "\r":
            self.calculate_result()
        elif key == "\x08":
            self.backspace()

    def update_entry(self, text):
        self.current_input += text
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.current_input)

    def clear_entry(self):
        self.current_input = ""
        self.entry.delete(0, tk.END)

    def backspace(self):
        self.current_input = self.current_input[:-1]
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.current_input)

    def toggle_sign(self):
        if self.current_input:
            self.current_input = str(-float(self.current_input))
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, self.current_input)

    def square_root(self):
        self.calculate_operation(sqrt)

    def absolute_value(self):
        self.calculate_operation(abs)

    def log_base_10(self):
        self.calculate_operation(log10)

    def natural_log(self):
        self.calculate_operation(log)

    def trigonometric_function(self, func):
        self.calculate_operation({"sin": sin, "cos": cos, "tan": tan}[func])

    def calculate_operation(self, operation):
        try:
            result = operation(float(self.current_input))
            self.current_input = str(result)
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, self.current_input)
        except Exception:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Error")

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

if __name__ == "__main__":
    root = tk.Tk()
    app = NeonCalculator(root)
    root.mainloop()