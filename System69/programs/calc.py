import tkinter as tk
import math

def create_calculator_window():
    window = tk.Tk()
    window.title("ShellOS Calculator")

    # Create a display area
    display = tk.Entry(window, font=("Arial", 20))
    display.grid(row=0, column=0, columnspan=6, sticky="nsew")  # Adjust for scientific layout

    # Toggle state for calculator type
    is_scientific = tk.BooleanVar(value=False)

    def toggle_mode():
        nonlocal is_scientific
        is_scientific.set(not is_scientific.get())
        update_buttons()

    def handle_button_click(button_text):
        if button_text == "=":
            try:
                result = eval(display.get())
                display.delete(0, tk.END)
                display.insert(0, str(result))
            except Exception:
                display.delete(0, tk.END)
                display.insert(0, "Error")
        elif button_text == "C":
            display.delete(0, tk.END)
        elif button_text == "sin":
            try:
                result = math.sin(math.radians(float(display.get())))
                display.delete(0, tk.END)
                display.insert(0, str(result))
            except Exception:
                display.delete(0, tk.END)
                display.insert(0, "Error")
        elif button_text == "cos":
            try:
                result = math.cos(math.radians(float(display.get())))
                display.delete(0, tk.END)
                display.insert(0, str(result))
            except Exception:
                display.delete(0, tk.END)
                display.insert(0, "Error")
        elif button_text == "tan":
            try:
                result = math.tan(math.radians(float(display.get())))
                display.delete(0, tk.END)
                display.insert(0, str(result))
            except Exception:
                display.delete(0, tk.END)
                display.insert(0, "Error")
        elif button_text == "log":
            try:
                result = math.log10(float(display.get()))
                display.delete(0, tk.END)
                display.insert(0, str(result))
            except Exception:
                display.delete(0, tk.END)
                display.insert(0, "Error")
        elif button_text == "^":
            display.insert(tk.END, "**")
        else:
            display.insert(tk.END, button_text)

    def update_buttons():
        # Clear existing buttons
        for widget in window.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

        # Basic calculator buttons
        basic_buttons = [
            "7", "8", "9", "/", "C",
            "4", "5", "6", "*", "^",
            "1", "2", "3", "-", "=",
            "0", ".", "+", "Mode"
        ]

        # Scientific calculator buttons
        scientific_buttons = basic_buttons + [
            "sin", "cos", "tan", "log"
        ]

        buttons = scientific_buttons if is_scientific.get() else basic_buttons

        row, col = 1, 0
        for btn_text in buttons:
            command = toggle_mode if btn_text == "Mode" else lambda t=btn_text: handle_button_click(t)
            btn = tk.Button(window, text=btn_text, font=("Arial", 16), command=command)
            btn.grid(row=row, column=col, sticky="nsew")
            col = (col + 1) % 5 if is_scientific.get() else (col + 1) % 4
            if col == 0:
                row += 1

        # Update resizing behavior
        for i in range(row + 1):
            window.grid_rowconfigure(i, weight=1)
        for i in range(5 if is_scientific.get() else 4):
            window.grid_columnconfigure(i, weight=1)

    update_buttons()

    window.mainloop()

create_calculator_window()
