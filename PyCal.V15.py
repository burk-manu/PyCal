import tkinter as tk
from math import sqrt, log, log10, sin, cos, tan, pi, e

def get_button_colors(label):
    """
    Returns a tuple (frame_color, _) based on the button label.
    """
    if label in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "±"}:
        return ("#00C853", "#B9F6CA")  # Neon green frame for numbers
    elif label == "=":
        return ("#FFD600", "#FFFF8D")  # Neon yellow frame for the equal sign
    elif label in {"+", "-", "*", "/", "%", "^", "√", "(", ")", "log", "ln", "|x|", "sin", "cos", "tan", "π", "e"}:
        return ("#D500F9", "#EA80FC")  # Neon magenta/purple for operations
    elif label in {"MC", "MR", "M+", "M-", "C"}:
        return ("#2979FF", "#82B1FF")  # Neon blue for memory/clear functions
    elif label in {"⌫", "History", "AC"}:
        return ("#FF3D00", "#FF8A65")  # Neon red for backspace, history, etc.
    else:
        return ("#0D47A1", "#42A5F5")  # Fallback colours

class NeonButton(tk.Canvas):
    """
    A custom canvas-based button that displays a rounded rectangle with a dark grey fill 
    and a neon-coloured frame (outline). The button lightens slightly when hovered.
    """
    def __init__(self, master, text, command,
                 width=80, height=80, corner_radius=20,
                 frame_color="#0D47A1",
                 font=("Helvetica Neue", 16, "bold"), **kwargs):
        # Initialize the canvas using the master widget's background.
        super().__init__(master, width=width, height=height,
                         bg=master['bg'], highlightthickness=0, bd=0, **kwargs)
        self.text = text
        self.command = command
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.frame_color = frame_color
        self.font = font

        # Set fill colours for normal and hover states.
        self.normal_fill = "#222222"  # Darker grey fill
        self.hover_fill = "#333333"   # Lighter grey on hover
        self.current_fill = self.normal_fill

        self.draw_button()
        # Bind mouse events for click and hover.
        self.bind("<Button-1>", lambda e: self.command())
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def draw_button(self):
        """Draws the button with the current fill and neon frame."""
        self.delete("all")
        self.create_round_rect(
            2, 2, self.width - 2, self.height - 2,
            r=self.corner_radius,
            fill=self.current_fill,
            outline=self.frame_color,
            width=3
        )
        self.create_text(self.width / 2, self.height / 2,
                         text=self.text, font=self.font, fill="#FFFFFF")

    def create_round_rect(self, x1, y1, x2, y2, r=25, **kwargs):
        """
        Draw a rounded rectangle using a smooth polygon.
        """
        points = [
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_enter(self, event):
        """Lighten the button fill when the cursor enters."""
        self.current_fill = self.hover_fill
        self.draw_button()

    def on_leave(self, event):
        """Restore the original fill when the cursor leaves."""
        self.current_fill = self.normal_fill
        self.draw_button()

class NeonCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Gamer Neon Calculator")
        self.root.geometry("550x850")
        self.root.configure(bg="#121212")
        self.current_input = ""
        self.memory = 0
        self.history = []

        # Display area for the current input/result.
        self.entry = tk.Entry(root, font=("Helvetica Neue", 32, "bold"), justify="right", bd=0,
                              relief=tk.FLAT, bg="#1E1E1E", fg="#00E5FF", insertbackground="#00E5FF")
        self.entry.pack(fill=tk.BOTH, ipadx=10, ipady=20, padx=20, pady=(20, 10))
        
        # History label.
        self.history_label = tk.Label(root, text="", font=("Helvetica Neue", 12), bg="#121212", fg="#80DEEA", 
                                      anchor="e", justify="right")
        self.history_label.pack(fill=tk.BOTH, padx=20, pady=(0, 10))
        
        # Button grid frame.
        self.button_frame = tk.Frame(root, bg="#121212")
        self.button_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

        # Define the layout for all buttons.
        buttons = [
            ("MC", "MR", "M+", "M-", "C"),
            ("log", "ln", "|x|", "√", "^"),
            ("sin", "cos", "tan", "(", ")"),
            ("7", "8", "9", "/", "π"),
            ("4", "5", "6", "*", "e"),
            ("1", "2", "3", "-", "="),
            ("0", ".", "±", "+", "⌫"),
        ]

        # Create a NeonButton for each label.
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                frame_color, _ = get_button_colors(text)
                btn = NeonButton(
                    self.button_frame,
                    text=text,
                    command=lambda t=text: self.on_button_click(t),
                    width=80, height=80, corner_radius=15,
                    frame_color=frame_color,
                    font=("Helvetica Neue", 16, "bold")
                )
                btn.grid(row=i, column=j, padx=8, pady=8, sticky="nsew")

        # Ensure the grid expands evenly.
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

    def clear_all(self):
        self.clear_entry()
        self.history_label.config(text="")

    def backspace(self):
        self.current_input = self.current_input[:-1]
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.current_input)

    def toggle_sign(self):
        if self.current_input:
            try:
                self.current_input = str(-float(self.current_input))
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, self.current_input)
            except Exception:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Error")

    def square_root(self):
        self.calculate_operation(sqrt)

    def absolute_value(self):
        self.calculate_operation(abs)

    def log_base_10(self):
        self.calculate_operation(log10)

    def natural_log(self):
        self.calculate_operation(log)

    def trigonometric_function(self, func):
        operations = {"sin": sin, "cos": cos, "tan": tan}
        self.calculate_operation(operations[func])

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
