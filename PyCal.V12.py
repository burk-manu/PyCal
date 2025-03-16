import tkinter as tk
from math import sqrt

def get_button_colors(label):
    """
    Returns a tuple (frame_color, _) based on the button label.
    The first element will be used for the neon-coloured frame.
    Adjust these hex codes to suit your neon palette.
    """
    if label in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "±"}:
        # Numbers: neon green frame
        return ("#00C853", "#B9F6CA")
    elif label == "=":
        # Equal sign: neon yellow frame
        return ("#FFD600", "#FFFF8D")
    elif label in {"+", "-", "*", "/", "%", "^", "√", "(", ")"}:
        # Operation buttons: neon magenta/purple frame
        return ("#D500F9", "#EA80FC")
    elif label in {"MC", "MR", "M+", "M-", "C"}:
        # Memory and clear functions: neon blue frame
        return ("#2979FF", "#82B1FF")
    elif label in {"⌫", "Hist", "AC"}:
        # Other functions: neon red frame
        return ("#FF3D00", "#FF8A65")
    else:
        # Default fallback colour
        return ("#0D47A1", "#42A5F5")

class NeonButton(tk.Canvas):
    """
    A custom canvas-based button that shows a rounded rectangle with a dark grey fill 
    and a neon-coloured frame (outline). The frame colour depends on the button label.
    Now the button uses a darker grey fill and lights up (changes fill color)
    slightly when hovered over.
    """
    def __init__(self, master, text, command,
                 width=80, height=80, corner_radius=20,
                 frame_color="#0D47A1",
                 font=("Helvetica Neue", 16, "bold"), **kwargs):
        # Initialize the canvas with the master's background colour.
        super().__init__(master, width=width, height=height,
                         bg=master['bg'], highlightthickness=0, bd=0, **kwargs)
        self.text = text
        self.command = command
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        # The neon frame (outline) colour for this button.
        self.frame_color = frame_color
        self.font = font

        # Define the fill colours for normal and hover states.
        self.normal_fill = "#222222"  # darker grey fill
        self.hover_fill = "#444444"   # lighter grey when hovered
        self.current_fill = self.normal_fill

        self.draw_button()
        # Bind click events.
        self.bind("<Button-1>", lambda e: self.command())
        # Bind hover events.
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def draw_button(self):
        self.delete("all")
        # Draw a rounded rectangle with the current fill color and a neon-coloured outline.
        self.create_round_rect(
            2, 2,
            self.width - 2, self.height - 2,
            r=self.corner_radius,
            fill=self.current_fill,         # use the current fill color
            outline=self.frame_color,         # neon-coloured frame
            width=3
        )
        # Draw the button's text centered.
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
        """Change the fill to a lighter grey when the mouse hovers over the button."""
        self.current_fill = self.hover_fill
        self.draw_button()

    def on_leave(self, event):
        """Return the fill to the normal dark grey when the mouse leaves the button."""
        self.current_fill = self.normal_fill
        self.draw_button()

class NeonCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Gamer Neon Calculator")
        self.root.geometry("480x700")
        self.root.configure(bg="#121212")  # Very dark background for a futuristic look

        # Internal state variables.
        self.current_input = ""
        self.memory = 0
        self.history = []

        # Define fonts.
        self.display_font = ("Helvetica Neue", 32, "bold")
        self.button_font = ("Helvetica Neue", 16, "bold")
        self.history_font = ("Helvetica Neue", 12)

        # --- Display Area ---
        self.display_frame = tk.Frame(root, bg="#121212")
        self.display_frame.pack(fill=tk.BOTH, padx=20, pady=(20, 10))
        self.entry = tk.Entry(self.display_frame,
                              font=self.display_font,
                              justify="right",
                              bd=0,
                              relief=tk.FLAT,
                              bg="#1E1E1E",
                              fg="#00E5FF",         # neon blue text
                              insertbackground="#00E5FF")
        self.entry.pack(fill=tk.BOTH, ipadx=10, ipady=20)

        self.history_label = tk.Label(root,
                                      text="",
                                      font=self.history_font,
                                      bg="#121212",
                                      fg="#80DEEA",
                                      anchor="e",
                                      justify="right")
        self.history_label.pack(fill=tk.BOTH, padx=20, pady=(0, 10))

        # --- Buttons Area ---
        self.button_frame = tk.Frame(root, bg="#121212")
        self.button_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

        # Define the layout for the buttons (each row is a tuple of labels).
        buttons = [
            ("MC", "MR", "M+", "M-", "C"),
            ("√", "^", "%", "/", "*"),
            ("7", "8", "9", "-", "("),
            ("4", "5", "6", "+", ")"),
            ("1", "2", "3", "=", "⌫"),
            ("0", ".", "±", "AC", "Hist")
        ]

        # Create a NeonButton for each label using our colour mapping.
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                frame_color, _ = get_button_colors(text)
                btn = NeonButton(
                    self.button_frame,
                    text=text,
                    command=lambda t=text: self.on_button_click(t),
                    width=70, height=70, corner_radius=15,
                    frame_color=frame_color,
                    font=self.button_font
                )
                btn.grid(row=i, column=j, padx=8, pady=8, sticky="nsew")

        # Configure the grid so that buttons expand evenly.
        rows = len(buttons)
        cols = len(buttons[0])
        for i in range(rows):
            self.button_frame.grid_rowconfigure(i, weight=1)
        for j in range(cols):
            self.button_frame.grid_columnconfigure(j, weight=1)

        # Bind key events for keyboard input.
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
        # Display the last five calculations.
        history_text = "\n".join(self.history[-5:])
        self.history_label.config(text=history_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = NeonCalculator(root)
    root.mainloop()
