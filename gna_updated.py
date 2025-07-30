import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import time
import threading
import tkinter.font as tkFont



# Tkinter app starting

root = tk.Tk()
root.title("GUI")
root.geometry("1420x800")
root.configure(bg="white")



blank = tk.PhotoImage()
tk.Label(
    root,
    image=blank,
    text="Raman Spectroscopic Tool for Detection of Explosives",
    compound="c",              # Center text over image
    font=("Arial",30, "bold"),
    bg="#545454",
    fg="white",
    width=1420,                # Full window width in pixels
    height=60,                 # Banner height in pixels
    bd=0,
    padx=0
).pack(fill="x")
# left panel
left_frame = tk.Frame(root, bg="white", width=355)
left_frame.pack(side="left", fill="y")
left_frame.pack_propagate(False)

# Top frame in left panel
top_frame = tk.Frame(left_frame, bg="#69c0eb", height=80, width=355)
top_frame.pack(pady=(0, 0), padx=0)
top_frame.pack_propagate(False)

# Middle Frame
middle_frame = tk.Frame(left_frame, bg="#b7b9b6", height=300, width=355)
middle_frame.pack(pady=0, padx=0)
middle_frame.pack_propagate(False)

# Bottom: Light Pink Frame (Taller)
bottom_frame = tk.Frame(left_frame, bg="#F5D9C8", height=360, width=355)
bottom_frame.pack(pady=(0, 0), padx=0, fill="both", expand=True)
bottom_frame.pack_propagate(False)

#rght panel
right_frame = tk.Frame(root, bg="white", width=1065)
right_frame.pack(side="right", fill="y")
right_frame.pack_propagate(False)

def create_plot_box(parent, title):
    # Define color by title
    title_lower = title.lower()
    if "normalised" in title_lower:
        box_color = "white"
        text_color = "orange"
    elif "corrected" in title_lower:
        box_color = "white"
        text_color = "green"
    else:  # Live spectrum or others
        box_color = "white"
        text_color = "black"

    # Outer container (holds label and box)
    container = tk.Frame(parent, bg="white")
    container.pack(pady=(15, 5), anchor="w")

    # Label (above box, outside)
    title_label = tk.Label(container, text=title, font=("Arial", 16, "bold"),
                           fg=text_color, bg="white", anchor="w", justify="left")
    title_label.pack(anchor="w", padx=10)

    # Colored frame (box)
    frame = tk.Frame(container, bg=box_color, height=230, width=1020,
                     highlightbackground="black", highlightthickness=2)
    frame.pack_propagate(False)
    frame.pack(padx=10, pady=(2, 0))

   
create_plot_box(right_frame, "Live Spectrum")
create_plot_box(right_frame, "Background Corrected Spectrum")
create_plot_box(right_frame, "Normalised Spectrum")





# Top frame in right panel
top_frame_r = tk.Frame(right_frame, bg="white", height=246.5, width=1060)
top_frame_r.pack(pady=(0, 0), padx=0)
top_frame_r.pack_propagate(False)

# Middle Frame in right panel
middle_frame_r = tk.Frame(right_frame, bg="white", height=247, width=1060)
middle_frame_r.pack(pady=0, padx=0)
middle_frame_r.pack_propagate(False)

# Bottom from in right panel
bottom_frame_r = tk.Frame(right_frame, bg="white", height=246.5, width=1060)
bottom_frame_r.pack(pady=(0, 0), padx=0, fill="both", expand=True)
bottom_frame_r.pack_propagate(False)

top_button_frame = tk.Frame(top_frame_r, bg="white")
top_button_frame.pack(side="top", fill="x", padx=10, pady=(10, 5))

#Train button
# Define the custom font
custom_font = tkFont.Font(family="Arial", size=16, weight="bold")

# Set style BEFORE creating the buttons
style = ttk.Style()
style.theme_use("clam")  # Needed to apply background color on macOS/Linux


# Flat style for Train button
style.configure("Flat.TButton",
                foreground="white",
                background="#0082b2",
                font=custom_font,
                padding=(8, 6),
                borderwidth=0,
                focusthickness=0)





# Menubutton styling 

style.configure("Black.TMenubutton",
                background="#0082b2",
                foreground="white",
                arrowcolor="white",
                font=('Arial', 16),
                relief="flat",
                padding=(10, 8),
                width=17)

style.map("Black.TMenubutton",
          background=[("active", "#333333")],
          foreground=[("active", "white")],
          arrowcolor=[("active", "white")])

# Menu options
options = ["Linear Regression", "Poly Regression", "Logistic Regression", "Decision Tree", "CNN"]
vars = [tk.BooleanVar() for _ in options]

# Callback to update text
def update_selection():
    selected = [opt for opt, var in zip(options, vars) if var.get()]
    btn_var.set(", ".join(selected) if selected else "Select options")

# Variable and Menubutton
btn_var = tk.StringVar(value="Select ML model(s)")
menu_btn = ttk.Menubutton(left_frame, textvariable=btn_var, direction="below", style="Black.TMenubutton")

# Attach menu to Menubutton
menu = tk.Menu(menu_btn, tearoff=False)
for i, opt in enumerate(options):
    menu.add_checkbutton(label=opt, variable=vars[i], command=update_selection)

menu_btn["menu"] = menu

menu_btn.grid(row=0, column=0, padx=10, pady=20, sticky="ew")



# Train button
btn2 = ttk.Button(left_frame, text="Train", style="Flat.TButton")
btn2.grid(row=0, column=1, padx=10, pady=20, sticky="ew")

spectrometer_var = tk.StringVar(value="Select spectrometer")

# Style for spectrometer Menubutton
style.configure("BlackSingle.TMenubutton",
                background="black",
                foreground="white",
                arrowcolor="white",
                font=('Arial', 16),
                relief="flat", padding=(10, 8),
                width=31)

style.map("BlackSingle.TMenubutton",
          background=[("active", "#333333")],
          foreground=[("active", "white")],
          arrowcolor=[("active", "white")])



# Inside MIDDLE_FRAME — create a row container
label_row = tk.Frame(middle_frame, bg="#b7b9b6")
label_row.pack(padx=10, pady=(10, 0), anchor="w")

# Inside middle_frame — Spectrometer Menubutton first

spectrometer_var = tk.StringVar(value="Select spectrometer")

spectrometer_menu_btn = ttk.Menubutton(
    middle_frame,
    textvariable=spectrometer_var,
    direction="below",
    style="BlackSingle.TMenubutton"
)
spectrometer_menu_btn.pack(padx=10, pady=(10, 10), anchor="w")

# Spectrometer menu setup
spectrometer_menu = tk.Menu(spectrometer_menu_btn, tearoff=False)

def set_spectrometer(val):
    spectrometer_var.set(val)

spectrometer_menu.add_radiobutton(label="laser1", command=lambda: set_spectrometer("laser1"))
spectrometer_menu.add_radiobutton(label="laser2", command=lambda: set_spectrometer("laser2"))

spectrometer_menu_btn["menu"] = spectrometer_menu


# Now the Wavelength + Integration Time labels below
label_row = tk.Frame(middle_frame, bg="#b7b9b6")
label_row.pack(padx=10, pady=(5, 0), anchor="w")

tk.Label(
    label_row,
    text="Wavelength (nm)",
    bg="#b7b9b6",
    fg="black",
    font=("Arial", 16, "bold")
).pack(side="left", padx=(5, 25))

tk.Label(
    label_row,
    text="Integration Time",
    bg="#b7b9b6",
    fg="black",
    font=("Arial", 16, "bold")
).pack(side="left", padx=(0, 10))

# Entry + Combobox row
entry_row = tk.Frame(middle_frame, bg="#b7b9b6")
entry_row.pack(padx=10, pady=(10, 15), anchor="w")

# Wavelength Entry
wavelength_entry = tk.Entry(
    entry_row,
    width=10,
    font=("Arial", 16),
    justify="center",
    relief="flat",
    bg="white",
    bd=0,
    highlightthickness=1,
highlightbackground="black",
    highlightcolor="black"
)
wavelength_entry.insert(0, "785")
wavelength_entry.pack(side=tk.LEFT, padx=(20, 5), ipady=4)

# Add a spacer Label to shift right without resizing widgets
spacer = tk.Label(entry_row, width=7, bg="#b7b9b6")  # Adjust width to control right shift
spacer.pack(side=tk.LEFT)

# Frame for Integration Time + Unit
integration_frame = tk.Frame(entry_row, bg="#b7b9b6")
integration_frame.pack(side=tk.LEFT)

# Integration Time Entry
int_time_entry = tk.Entry(
    integration_frame,
    width=5,
    font=("Arial", 16),
    justify="center",
    relief="flat",
    bg="white",
    bd=0,
    highlightthickness=1,
highlightbackground="black",
    highlightcolor="black"
)
int_time_entry.insert(0, "5")
int_time_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=4)

# Flat Combobox Style
style = ttk.Style()
style.theme_use("clam")
style.configure("Flat.TCombobox",
                fieldbackground="white",
                background="white",
                selectbackground="white",
                selectforeground="black",
                relief="flat",
                borderwidth=1,
                bordercolor="black",
                padding=2)
style.map("Flat.TCombobox",
          fieldbackground=[('readonly', 'white')],
          background=[('readonly', 'white')])

# Unit Combobox
unit_combo = ttk.Combobox(
    integration_frame,
    values=["s", "ms", "ns", "µs"],
    width=5,
    font=("Arial", 14),
    state="readonly",
    style="Flat.TCombobox"
)
unit_combo.set("s")
unit_combo.pack(side=tk.LEFT, ipady=2)
tk.Label(middle_frame, text="", bg="#b7b9b6", height=1).pack()


# Row below Integration time + Combobox
baseline_row = tk.Frame(middle_frame, bg="#b7b9b6")
baseline_row.pack(padx=10, pady=(10, 5), anchor="w")

# "Baseline order:" Label
tk.Label(
    baseline_row,
    text="Baseline order:",
    bg="#b7b9b6",
    fg="black",
    font=("Arial", 16, "bold")
).pack(side="left", padx=(0, 10))

# Entry field (default: 1)
baseline_entry = tk.Entry(
    baseline_row,
    width=5,
    font=("Arial", 16),
    justify="center",
    relief="flat",
    bg="white",
    highlightthickness=1,
    highlightbackground="black",
    highlightcolor="black"
)
baseline_entry.insert(0, "1")
baseline_entry.pack(side="left", padx=(0, 20), ipady=4)
# Flat style for Correct button
style.configure("Black.TButton",
                foreground="white",
                background="black",
                font=custom_font,
                padding=(6, 4),
                borderwidth=0,
                focusthickness=0)

# "Correct" Button
btn3 = ttk.Button(baseline_row, text="Correct", style="Black.TButton")
btn3.pack(side="left", ipadx=10, ipady=4)

tk.Label(middle_frame, text="", bg="#b7b9b6", height=1).pack()


# Row for Normalisation button (full width)
normalise_row = tk.Frame(middle_frame, bg="#b7b9b6")
normalise_row.pack(padx=15, pady=(0, 10), fill="x")

# "Normalisation" button occupying full width
normalise_btn = ttk.Button(
    normalise_row,
    text="Normalisation",
    style="Black.TButton"
)
normalise_btn.pack(fill="x", ipady=6)

# ---- Detect Button Section in bottom_frame ----

def detect_action():
    # Show banner
    banner_label.pack(fill="x", pady=(10, 5))

    # Clear previous results
    for widget in bottom_frame.winfo_children():
        if getattr(widget, "is_result", False):
            widget.destroy()

    # Get selected models
    selected_models = [opt for opt, var in zip(options, vars) if var.get()]

    # Adjust height based on number of selected models
    canvas_height = 70 if not selected_models else 30 + 35 * len(selected_models)
    canvas_width = 335  # Fit inside left_frame safely

    # Create result canvas
    result_canvas = tk.Canvas(
        bottom_frame,
        width=canvas_width,
        height=canvas_height,
        bg=bottom_frame.cget("bg"),
        highlightthickness=0
    )
    result_canvas.pack(pady=(0, 10), padx=10, anchor="w")
    result_canvas.is_result = True

    # Draw rectangles
    result_canvas.create_rectangle(10, 10, canvas_width - 10, canvas_height - 10, fill="black", outline="black", width=2)
    result_canvas.create_rectangle(12, 12, canvas_width - 12, canvas_height - 12, fill="white", outline="white")

    if not selected_models:
        # Clear message
        result_canvas.create_text(canvas_width // 2, canvas_height // 2, text="No ML model(s) selected", font=("Arial", 14, "italic"), fill="gray")
        return

    # Show full model names and predictions with reduced spacing
    y_base = 35
    for model in selected_models:
        is_poly = "poly" in model.lower()
        result_text = "Non-Explosive" if is_poly else "Explosive"
        color = "green" if is_poly else "red"

        # Reduced gap between model and result
        result_canvas.create_text(20, y_base, text=f"{model}:", anchor="w", font=("Arial", 16, "bold"), fill="black")
        result_canvas.create_text(200, y_base, text=result_text, anchor="w", font=("Arial", 16, "bold"), fill=color)
        y_base += 35



# Canvas for the oval-shaped Detect button
canvas = tk.Canvas(bottom_frame, width=200, height=120, highlightthickness=0, bg="#F5D9C8", bd=0)
canvas.pack(pady=(10, 0))

# Oval color
matched_color = "#bc3fde"

# Create oval and text
oval = canvas.create_oval(20, 20, 180, 100, fill=matched_color, outline=matched_color)
text = canvas.create_text(100, 60, text="Detect", font=("Arial", 16, "bold"), fill="white")


# Placeholder image
blank = tk.PhotoImage()

# Label to show after clicking Detect
banner_label = tk.Label(
    bottom_frame,
    image=blank,
    text=" Explosive ",
    compound="c",
    font=("Arial", 20, "bold"),
    bg="#f8f549",
    fg="#ff6d4d",
    height=40,
    bd=0
)


# Bind click events
canvas.tag_bind(oval, "<Button-1>", lambda e: detect_action())
canvas.tag_bind(text, "<Button-1>", lambda e: detect_action())

# -- Play/Pause tracking variables --
paused = False
start_time = time.time()
last_pause_time = 0
accumulated_pause = 0

# -- Pause/Play functions --
def toggle_pause():
    global paused, last_pause_time
    paused = True
    last_pause_time = time.time()

def toggle_play():
    global paused, accumulated_pause
    if paused:
        paused = False
        accumulated_pause += time.time() - last_pause_time

# -- Function to create a modern icon-like label that acts like a button : still working--
def create_icon_button(parent, symbol, command=None):
    lbl = tk.Label(
        parent,
        text=symbol,
        font=("Arial", 26),
        bg="white",
        fg="black",
        padx=12,
        pady=2,
        cursor="hand2"
    )
    if command:
        lbl.bind("<Button-1>", lambda e: command())

    # Hover effect
    lbl.bind("<Enter>", lambda e: lbl.config(bg="#f0f0f0"))
    lbl.bind("<Leave>", lambda e: lbl.config(bg="white"))

    lbl.pack(side=tk.LEFT, padx=8)
    return lbl



root.mainloop()
