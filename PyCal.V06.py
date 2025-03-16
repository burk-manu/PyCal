import tkinter as tk
from math import sqrt

class NeonCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("NeonCalc 9000")
        self.root.geometry("600x900")
        self.root.configure(bg="#0a0a14")  # Deep space background
        self.root.resizable(False, False)

        # Variables
        self.current_input = ""
        self.memory = 0
        self.history = []

        # Custom colors
        self.bg_color = "#0a0a14"
        self.display_bg = "#1a1a2f"
        self.neon_blue = "#00f3ff"
        self.neon_purple = "#ff00ff"
        self.neon_green = "#00ff00"
        self.neon_red = "#ff0000"
        self.button_colors = {
            "digit": {"bg": "#2d2d4d", "fg": self.neon_blue, "glow": self.neon_blue},
            "operator": {"bg": "#4a004a", "fg": self.neon_purple, "glow": self.neon_purple},
            "special": {"bg": "#004d4d", "fg": self.neon_green, "glow": self.neon_green},
            "equals": {"bg": "#4a004a", "fg": self.neon_purple, "glow": self.neon_purple},
            "clear": {"bg": "#4d0000", "fg": self.neon_red, "glow": self.neon_red}
        }

        # Create display
        self.create_display()

        # Create buttons
        self.create_buttons()

        # Bind keyboard
        self.root.bind("<Key>", self.on_key_press)

    def create_display(self):
        # Display frame
        self.display_frame = tk.Canvas(self.root, bg=self.bg_color, highlightthickness=0)
        self.display_frame.pack(pady=20, padx=20, fill=tk.X)

        # Display background with neon glow
        self.display_bg = self.display_frame.create_rectangle(
            10, 10, 390, 90, 
            fill=self.display_bg, 
            outline=self.neon_blue, 
            width=2
        )

        # Display text
        self.display_text = self.display_frame.create_text(
            380, 50, 
            text="0", 
            anchor=tk.E, 
            fill=self.neon_blue, 
            font=("Courier New", 24, "bold")
        )

    def create_buttons(self):
        button_frame = tk.Canvas(self.root, bg=self.bg_color, highlightthickness=0)
        button_frame.pack(padx=20, pady=10)

        buttons = [
            ("C", "⌫", "%", "/"),
            ("7", "8", "9", "*"),
            ("4", "5", "6", "-"),
            ("1", "2", "3", "+"),
            ("±", "0", ".", "=")
        ]

        for row_idx, row in enumerate(buttons):
            for col_idx, text in enumerate(row):
                x = col_idx * 90 + 10
                y = row_idx * 90 + 10
                self.create_neon_button(
                    button_frame, 
                    x, y, 80, 80, 
                    text=text,
                    command=lambda t=text: self.on_button_click(t)
                )

    def create_neon_button(self, parent, x, y, w, h, text, command):
        # Determine button style
        if text.isdigit() or text == ".":
            style = "digit"
        elif text in ["+", "-", "*", "/", "%"]:
            style = "operator"
        elif text == "=":
            style = "equals"
        elif text in ["C", "⌫", "±"]:
            style = "clear"
        else:
            style = "special"

        colors = self.button_colors[style]

        # Create button base
        btn = tk.Canvas(parent, width=w, height=h, bg=self.bg_color, highlightthickness=0)
        btn.place(x=x, y=y)

        # Rounded rectangle with neon glow
        btn.create_arc(0, 0, 20, 20, start=90, extent=90, fill=colors["bg"], outline="")
        btn.create_arc(w-20, 0, w, 20, start=0, extent=90, fill=colors["bg"], outline="")
        btn.create_arc(0, h-20, 20, h, start=180, extent=90, fill=colors["bg"], outline="")
        btn.create_arc(w-20, h-20, w, h, start=270, extent=90, fill=colors["bg"], outline="")
        btn.create_rectangle(10, 0, w-10, h, fill=colors["bg"], outline="")
        btn.create_rectangle(0, 10, w, h-10, fill=colors["bg"], outline="")

        # Button text
        btn.create_text(
            w/2, h/2, 
            text=text, 
            fill=colors["fg"], 
            font=("Impact", 18)
        )

        # Glow effect
        glow = btn.create_oval(
            w/2-30, h/2-30, w/2+30, h/2+30, 
            fill=colors["glow"], 
            state=tk.HIDDEN
        )

        # Bind events
        btn.bind("<Enter>", lambda e, b=btn, g=glow: (
            b.itemconfig(g, state=tk.NORMAL),
            self.display_frame.itemconfig(self.display_bg, outline=colors["glow"])
        ))
        btn.bind("<Leave>", lambda e, b=btn, g=glow: (
            b.itemconfig(g, state=tk.HIDDEN),
            self.display_frame.itemconfig(self.display_bg, outline=self.neon_blue)
        ))
        btn.bind("<Button-1>", lambda e: command())

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
        self.display_frame.itemconfig(self.display_text, text=self.current_input[-20:])

    def clear_entry(self):
        self.current_input = ""
        self.display_frame.itemconfig(self.display_text, text="0")

    def backspace(self):
        self.current_input = self.current_input[:-1]
        self.display_frame.itemconfig(self.display_text, text=self.current_input or "0")

    def toggle_sign(self):
        if self.current_input and self.current_input[0] == "-":
            self.current_input = self.current_input[1:]
        else:
            self.current_input = "-" + self.current_input
        self.display_frame.itemconfig(self.display_text, text=self.current_input)

    def modulus(self):
        try:
            result = float(self.current_input) / 100
            self.current_input = str(result)
            self.display_frame.itemconfig(self.display_text, text=self.current_input)
        except Exception:
            self.show_error()

    def calculate_result(self):
        try:
            result = eval(self.current_input)
            self.current_input = str(result)
            self.display_frame.itemconfig(self.display_text, text=self.current_input)
        except Exception:
            self.show_error()

    def show_error(self):
        self.display_frame.itemconfig(self.display_text, text="ERROR", fill=self.neon_red)
        self.current_input = ""
        self.root.after(1000, lambda: (
            self.display_frame.itemconfig(self.display_text, fill=self.neon_blue),
            self.display_frame.itemconfig(self.display_text, text="0")
        ))


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = NeonCalculator(root)
    root.mainloop()