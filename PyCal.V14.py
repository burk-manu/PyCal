import tkinter as tk
from math import sqrt, log, log10, sin, cos, tan, pi, e

def get_button_colors(label):
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

class NeonButton(tk.Canvas):
    def __init__(self, master, text, command, width=80, height=80, corner_radius=20, frame_color="#0D47A1", font=("Helvetica Neue", 16, "bold"), **kwargs):
        super().__init__(master, width=width, height=height, bg=master['bg'], highlightthickness=0, bd=0, **kwargs)
        self.text = text
        self.command = command
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.frame_color = frame_color
        self.font = font
        self.normal_fill = "#222222"
        self.hover_fill = "#444444"
        self.current_fill = self.normal_fill
        self.draw_button()
        self.bind("<Button-1>", lambda e: self.command())
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def draw_button(self):
        self.delete("all")
        self.create_round_rect(2, 2, self.width - 2, self.height - 2, r=self.corner_radius, fill=self.current_fill, outline=self.frame_color, width=3)
        self.create_text(self.width / 2, self.height / 2, text=self.text, font=self.font, fill="#FFFFFF")

    def create_round_rect(self, x1, y1, x2, y2, r=25, **kwargs):
        points = [x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_enter(self, event):
        self.current_fill = self.hover_fill
        self.draw_button()

    def on_leave(self, event):
        self.current_fill = self.normal_fill
        self.draw_button()

class NeonCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Gamer Neon Calculator")
        self.root.geometry("500x750")
        self.root.configure(bg="#121212")
        self.current_input = ""
        self.memory = 0
        self.history = []
        self.entry = tk.Entry(root, font=("Helvetica Neue", 32, "bold"), justify="right", bd=0, relief=tk.FLAT, bg="#1E1E1E", fg="#00E5FF", insertbackground="#00E5FF")
        self.entry.pack(fill=tk.BOTH, ipadx=10, ipady=20, padx=20, pady=(20, 10))
        self.history_label = tk.Label(root, text="", font=("Helvetica Neue", 12), bg="#121212", fg="#80DEEA", anchor="e", justify="right")
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
                btn = NeonButton(self.button_frame, text=text, command=lambda t=text: self.on_button_click(t), width=70, height=70, corner_radius=15, frame_color=frame_color, font=("Helvetica Neue", 16, "bold"))
                btn.grid(row=i, column=j, padx=8, pady=8, sticky="nsew")
        self.root.bind("<Key>", self.on_key_press)

if __name__ == "__main__":
    root = tk.Tk()
    app = NeonCalculator(root)
    root.mainloop()
