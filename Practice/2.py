import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw

# Initialize the main window
root = tk.Tk()
root.geometry("400x400")
root.title("Advanced Button Styles")

# Create a custom theme
style = ttk.Style(root)
style.theme_create("my_theme", parent="alt", settings={
    "TButton": {
        "configure": {
            "padding": 10,
            "relief": "flat",
            "background": "#ffffff",
            "foreground": "#000000",
            "font": ("Helvetica", 12),
            "anchor": "center"
        },
        "map": {
            "background": [("active", "#e0e0e0"), ("pressed", "#d0d0d0")],
            "foreground": [("active", "#000000"), ("pressed", "#333333")],
            "relief": [("pressed", "sunken")]
        }
    }
})

# Apply the custom theme
style.theme_use("my_theme")

# Function to create gradient background for a button
def create_gradient(width, height, color1, color2):
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        mask_data.extend([int(255 * (y / height))] * width)
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

# Gradient button background
gradient_image = create_gradient(150, 50, "#ff6f61", "#de4d86")
gradient_photo = ImageTk.PhotoImage(gradient_image)

# Create buttons with different styles
glass_button = ttk.Button(root, text="Glassmorphism", style="TButton")
glass_button.grid(row=0, column=0, padx=20, pady=10)

neumorphic_button = ttk.Button(root, text="Neumorphism", style="TButton")
neumorphic_button.grid(row=1, column=0, padx=20, pady=10)

flat_button = ttk.Button(root, text="Flat Design", style="TButton")
flat_button.grid(row=2, column=0, padx=20, pady=10)

gradient_button = tk.Label(root, image=gradient_photo, compound='center', text="Gradient", font=('Helvetica', 12, 'bold'), fg="black")
gradient_button.grid(row=3, column=0, padx=20, pady=10)

outline_button = ttk.Button(root, text="Outline", style="TButton")
outline_button.grid(row=4, column=0, padx=20, pady=10)

# Run the main loop
root.mainloop()
