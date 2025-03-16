import tkinter as tk
from math import sqrt

class NeonButton(tk.Canvas):
    """
    A custom canvas-based button with rounded corners and a neon glow effect.
    """
    def __init__(self, master, text, command,
                 width=80, height=80, corner_radius=20,
                 button_color="#0D47A1", glow_color="#42A5F5",
                 font=("Helvetica Neue", 16, "bold"), **kwargs):
        # Set the canvas background to match its container (master)
        super().__init__(master, width=width, height=height,
                         bg=master['bg'], highlightthickness=0, bd=0, **kwargs)
        self.text = text
        self.command = command
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.button_color = button_color
        self.glow_color = glow_color
        self.font = font
        self.normal = True  # state flag: normal or hovered
        self.draw_button()
        # Bind click and hover events
        self.bind("<Button-1>", lambda e: self.command())
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def draw_button(self):
        """Redraw the button with (or without) the neon glow effect."""
        self.delete("all")
        if not self.normal:
            # Draw several rounds of outlines to simulate a neon glow
            for i in range(4, 0, -1):
                self.create_round_rect(i, i, self.width - i, self.height - i,
                                       r=self.corner_radius, outline=self.glow_color, width=i)
        # Draw the main rounded rectangle
        self.create_round_rect(4, 4, self.width - 4, self.height - 4,
                               r=self.corner_radius, fill=self.button_color, outline="")
        # Draw the button text centered
        self.create_text(self.width / 2, self.height / 2,
                         text=self.text, font=self.font, fill="#FFFFFF")

    def create_round_rect(self, x1, y1, x2, y2, r=25, **kwargs):
        """Draw a rounded rectangle (using a smooth polygon)."""
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
        """When the mouse enters the button, show the glow."""
        self.normal = False
        self.draw_button()

    def on_leave(self, event):
        """When the mouse leaves, remove the glow effect."""
        self.normal = True
        self.draw_button()


class NeonCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Gamer Neon Calculator")
        self.root.geometry("400x700")
        self.root.configure(bg="#121212")  # Dark background for a futuristic look

        # Internal state variables
        self.current_input = ""
        self.memory = 0
        self.history = []

        # Define fonts
        self.display_font = ("Helvetica Neue", 32, "bold")
        self.button_font = ("Helvetica Neue", 16, "bold")
        self.history_font = ("Helvetica Neue", 12)

        # --- Display Area ---
        # Frame for the calculator display
        self.display_frame = tk.Frame(root, bg="#121212")
        self.display_frame.pack(fill=tk.BOTH, padx=20, pady=(20, 10))

        # Entry widget for showing current input/result
        self.entry = tk.Entry(self.display_frame,
                              font=self.display_font,
                              justify="right",
                              bd=0,
                              relief=tk.FLAT,
                              bg="#1E1E1E",
                              fg="#00E5FF",        # bright neon blue text
                              insertbackground="#00E5FF")
        self.entry.pack(fill=tk.BOTH, ipadx=10, ipady=20)

        # History display (shows recent calculations)
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

        # Define the button labels by rows
        buttons = [
            ("MC", "MR", "M+", "M-", "C"),
            ("√", "^", "%", "/", "*"),
            ("7", "8", "9", "-", "("),
            ("4", "5", "6", "+", ")"),
            ("1", "2", "3", "=", "⌫"),
            ("0", ".", "±", "AC", "Hist")
        ]

        # Create a NeonButton for each label, arranged in a grid.
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                # Use a lambda with a default argument to capture the button text
                btn = NeonButton(self.button_frame, text=text,
                                 command=lambda t=text: self.on_button_click(t),
                                 width=70, height=70, corner_radius=15,
                                 button_color="#0D47A1",  # dark blue button
                                 glow_color="#42A5F5",    # neon blue glow
                                 font=self.button_font)
                btn.grid(row=i, column=j, padx=8, pady=8, sticky="nsew")

        # Make sure the grid expands evenly
        rows = len(buttons)
        cols = len(buttons[0])
        for i in range(rows):
            self.button_frame.grid_rowconfigure(i, weight=1)
        for j in range(cols):
            self.button_frame.grid_columnconfigure(j, weight=1)

        # Bind key events for keyboard input
        self.root.bind("<Key>", self.on_key_press)

    def on_button_click(self, text):
        """Handle button clicks based on their label."""
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
        # Display the last five calculations
        history_text = "\n".join(self.history[-5:])
        self.history_label.config(text=history_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = NeonCalculator(root)
    root.mainloop()
