import tkinter as tk
from math import sqrt, pow
import re

class GamingCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("CyberCalc 3000")
        self.root.geometry("500x700")
        self.root.configure(bg="#0a0a14")
        self.root.resizable(False, False)
        
        # Custom colors
        self.bg_color = "#0a0a14"
        self.display_bg = "#1a1a2f"
        self.button_bg = "#1a1a2f"
        self.glow_color = "#00f3ff"
        self.special_ops = ["=", "AC", "C", "⌫", "±", "√", "^", "%", "History"]
        
        # Variables
        self.current_input = ""
        self.memory = 0
        self.history = []
        self.button_styles = {
            "digit": {"colors": ("#2d2d4d", "#3d3d7d"), "text": "#ffffff"},
            "operator": {"colors": ("#4a004a", "#7a007a"), "text": "#ff66ff"},
            "special": {"colors": ("#004d4d", "#007d7d"), "text": "#00ffff"}
        }

        # Create display
        self.create_display()
        
        # Create buttons
        self.create_buttons()
        
        # Bind keyboard
        self.root.bind("<Key>", self.on_key_press)

    def create_display(self):
        # Main display
        self.display_frame = tk.Canvas(self.root, bg=self.bg_color, highlightthickness=0)
        self.display_frame.pack(pady=20, padx=20, fill=tk.X)
        
        # Display background with glow effect
        self.display_bg = self.display_frame.create_rectangle(
            10, 10, 490, 90, 
            fill=self.display_bg, 
            outline="#00f3ff", 
            width=2
        )
        self.display_glow = self.display_frame.create_oval(
            0, 0, 20, 20, 
            fill=self.glow_color, 
            state=tk.HIDDEN
        )
        
        # Display text
        self.display_text = self.display_frame.create_text(
            460, 50, 
            text="0", 
            anchor=tk.E, 
            fill="#00f3ff", 
            font=("Courier New", 24, "bold")
        )

        # History display
        self.history_text = self.display_frame.create_text(
            20, 20, 
            text="", 
            anchor=tk.NW, 
            fill="#00f3ff", 
            font=("Courier New", 12)
        )

    def create_buttons(self):
        button_frame = tk.Canvas(self.root, bg=self.bg_color, highlightthickness=0)
        button_frame.pack(padx=20, pady=10)
        
        buttons = [
            ("MC", "MR", "M+", "M-", "C"),
            ("√", "^", "%", "/", "*"),
            ("7", "8", "9", "-", "("),
            ("4", "5", "6", "+", ")"),
            ("1", "2", "3", "=", "⌫"),
            ("0", ".", "±", "AC", "History")
        ]

        for row_idx, row in enumerate(buttons):
            for col_idx, text in enumerate(row):
                x = col_idx * 90 + 10
                y = row_idx * 90 + 10
                self.create_rounded_button(
                    button_frame, 
                    x, y, 80, 80, 
                    text=text,
                    command=lambda t=text: self.on_button_click(t)
                )

    def create_rounded_button(self, parent, x, y, w, h, text, command):
        # Determine button style
        if text in self.special_ops:
            style = "special"
        elif text in ["+", "-", "*", "/", "%", "^", "√"]:
            style = "operator"
        else:
            style = "digit"
        
        colors = self.button_styles[style]["colors"]
        text_color = self.button_styles[style]["text"]
        
        # Create button base
        btn = tk.Canvas(parent, width=w, height=h, bg=self.bg_color, highlightthickness=0)
        btn.place(x=x, y=y)
        
        # Button background with gradient
        for i in range(h):
            ratio = i / h
            r = int((int(colors[0][1:3], 16) * (1 - ratio) + int(colors[1][1:3], 16) * ratio))
            g = int((int(colors[0][3:5], 16) * (1 - ratio) + int(colors[1][3:5], 16) * ratio))
            b = int((int(colors[0][5:7], 16) * (1 - ratio) + int(colors[1][5:7], 16) * ratio))
            color = f"#{r:02x}{g:02x}{b:02x}"
            btn.create_line(0, i, w, i, fill=color)
        
        # Rounded corners
        btn.create_oval(0, 0, 20, 20, fill=colors[1], outline="")
        btn.create_oval(w-20, 0, w, 20, fill=colors[1], outline="")
        btn.create_oval(0, h-20, 20, h, fill=colors[1], outline="")
        btn.create_oval(w-20, h-20, w, h, fill=colors[1], outline="")
        
        # Button text
        btn.create_text(
            w/2, h/2, 
            text=text, 
            fill=text_color, 
            font=("Impact", 16)
        )
        
        # Glow effect
        glow = btn.create_oval(
            w/2-30, h/2-30, w/2+30, h/2+30, 
            fill=self.glow_color, 
            state=tk.HIDDEN
        )
        
        # Bind events
        btn.bind("<Enter>", lambda e, b=btn, g=glow: (
            b.itemconfig(g, state=tk.NORMAL),
            self.display_frame.itemconfig(self.display_glow, state=tk.NORMAL)
        ))
        btn.bind("<Leave>", lambda e, b=btn, g=glow: (
            b.itemconfig(g, state=tk.HIDDEN),
            self.display_frame.itemconfig(self.display_glow, state=tk.HIDDEN)
        ))
        btn.bind("<Button-1>", lambda e: command())

    def update_display(self):
        self.display_frame.itemconfig(self.display_text, text=self.current_input[-20:])
        
    # (Keep all the previous functional methods from the AdvancedCalculator class here)
    # ... [Previous functional methods (on_button_click, calculate_result, etc.) remain unchanged] ...

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
        self.update_display()

    def clear_entry(self):
        self.current_input = ""
        self.update_display()

    def clear_all(self):
        self.clear_entry()
        self.display_frame.itemconfig(self.history_text, text="")

    def backspace(self):
        self.current_input = self.current_input[:-1]
        self.update_display()

    def toggle_sign(self):
        if self.current_input and self.current_input[0] == "-":
            self.current_input = self.current_input[1:]
        else:
            self.current_input = "-" + self.current_input
        self.update_display()

    def square_root(self):
        try:
            result = sqrt(float(self.current_input))
            self.current_input = str(result)
            self.update_display()
        except Exception:
            self.show_error()

    def exponentiation(self):
        self.update_entry("**")

    def modulus(self):
        self.update_entry("%")

    def calculate_result(self):
        try:
            result = eval(self.current_input)
            self.history.append(f"{self.current_input} = {result}")
            self.current_input = str(result)
            self.update_display()
        except Exception:
            self.show_error()

    def memory_clear(self):
        self.memory = 0

    def memory_recall(self):
        self.update_entry(str(self.memory))

    def memory_add(self):
        try:
            self.memory += float(self.current_input)
        except Exception:
            self.show_error()

    def memory_subtract(self):
        try:
            self.memory -= float(self.current_input)
        except Exception:
            self.show_error()

    def show_history(self):
        history = "\n".join(self.history[-3:])
        self.display_frame.itemconfig(self.history_text, text=history)

    def show_error(self):
        self.display_frame.itemconfig(self.display_text, text="ERROR", fill="#ff0000")
        self.current_input = ""
        self.root.after(1000, lambda: (
            self.display_frame.itemconfig(self.display_text, fill="#00f3ff"),
            self.update_display()
        ))

if __name__ == "__main__":
    root = tk.Tk()
    app = GamingCalculator(root)
    root.mainloop()