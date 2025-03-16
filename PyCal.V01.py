import tkinter as tk

def button_click(event):
    text = event.widget.cget("text")
    if text == "=":
        try:
            result = str(eval(entry.get()))
            entry.delete(0, tk.END)
            entry.insert(tk.END, result)
        except Exception as e:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
    elif text == "C":
        entry.delete(0, tk.END)
    else:
        entry.insert(tk.END, text)

# Create the main window
root = tk.Tk()
root.title("Simple Calculator")
root.geometry("300x400")

# Create an entry widget to display the input and results
entry = tk.Entry(root, font=("Arial", 20), justify="right")
entry.pack(fill=tk.BOTH, ipadx=8, pady=10, padx=10)

# Create a frame for the buttons
button_frame = tk.Frame(root)
button_frame.pack()

# Define the buttons
buttons = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "C", "0", "=", "+"
]

# Add buttons to the frame
for i, button_text in enumerate(buttons):
    button = tk.Button(button_frame, text=button_text, font=("Arial", 18), padx=20, pady=20)
    button.grid(row=i//4, column=i%4, sticky="nsew")
    button.bind("<Button-1>", button_click)

# Configure the grid to expand buttons evenly
for i in range(4):
    button_frame.grid_columnconfigure(i, weight=1)
    button_frame.grid_rowconfigure(i, weight=1)

# Run the main loop
root.mainloop()