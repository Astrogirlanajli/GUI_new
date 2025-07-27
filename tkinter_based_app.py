import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import time
import threading

# Logics
paused = False
start_time = time.time()
last_pause_time = 0
accumulated_pause = 0

# Tkinter App
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
).pack(padx=0, pady=0)

# LEFT PANEL
frame_left = tk.Frame(root, background="white", width=320)
frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
frame_left.pack_propagate(False)

# AI Model Selection
tk.Label(frame_left, text="Select AI model", bg="white").pack(anchor="w", pady=(0, 5))
model_var = tk.StringVar(value=["Polynomial Regression", "Logistic Regression"])
model_listbox = tk.Listbox(frame_left, listvariable=model_var, selectmode='multiple', height=5, exportselection=False)
models = ["Linear Regression", "Polynomial Regression", "Logistic Regression", "Decision Tree", "CNN"]
for model in models:
    model_listbox.insert(tk.END, model)
model_listbox.pack(fill=tk.X, pady=(0, 10))

# Train button

style = ttk.Style()
style.theme_use("clam")  # Works across OSes
style.configure("My.TButton", foreground="white", background="blue")
myButton = ttk.Button(frame_left, text="Train", style="My.TButton")
myButton.grid()


# Excitation Wavelength
tk.Label(frame_left, text="Excitation wavelength (nm)", bg="white").pack(anchor="w", pady=(0, 5))
wavelength_entry = tk.Entry(frame_left)
wavelength_entry.insert(0, "785")
wavelength_entry.pack(fill=tk.X, pady=(0, 10))

# Integration Time
tk.Label(frame_left, text="Integration time", bg="white").pack(anchor="w", pady=(0, 5))
integration_frame = tk.Frame(frame_left, bg="white")
integration_frame.pack(fill=tk.X, pady=(0, 10))
int_time_entry = tk.Entry(integration_frame, width=5)
int_time_entry.insert(0, "10")
int_time_entry.pack(side=tk.LEFT, padx=(0, 5))
unit_combo = ttk.Combobox(integration_frame, values=["s", "ms", "ns", "µs"], width=5)
unit_combo.set("s")
unit_combo.pack(side=tk.LEFT)

# Baseline Order
tk.Label(frame_left, text="Baseline order", bg="white").pack(anchor="w", pady=(0, 5))
baseline_frame = tk.Frame(frame_left, bg="white")
baseline_frame.pack(fill=tk.X, pady=(0, 10))
baseline_entry = tk.Entry(baseline_frame, width=5)
baseline_entry.insert(0, "5")
baseline_entry.pack(side=tk.LEFT)
tk.Button(baseline_frame, text="Correct", bg="green", fg="black", width=10).pack(side=tk.LEFT, padx=(10, 0))

# Normalise Button
tk.Button(frame_left, text="Normalise", bg="lightgray").pack(fill=tk.X, pady=5)

# Test Model Button
def test_model():
    result_var.set("This sample is\nExplosive\nWith accuracy of 70%")
    selected = [model_listbox.get(i) for i in model_listbox.curselection()]
    if selected:
        lines = [f"{model}: explosive" for model in selected]
        final_text = "\n".join(lines) + "\n\n🔥 Explosive"
    else:
        final_text = "💥 No model selected"
    model_result_var.set(final_text)

tk.Button(frame_left, text="Test the model", bg="#444", fg="black", command=test_model).pack(fill=tk.X, pady=10)

#  TOP BUTTONS
top_button_frame = tk.Frame(root, bg="white", pady=10)
top_button_frame.pack(fill=tk.X, padx=20)

def toggle_pause():
    global paused, last_pause_time
    paused = True
    last_pause_time = time.time()

def toggle_play():
    global paused, accumulated_pause
    if paused:
        paused = False
        accumulated_pause += time.time() - last_pause_time

tk.Button(top_button_frame, text="⏸️", command=toggle_pause, width=3, bg="#444", fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(top_button_frame, text="▶️", command=toggle_play, width=3, bg="#2e7d32", fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(top_button_frame, text="💡", width=3, bg="#ff9800", fg="black").pack(side=tk.LEFT, padx=5)
tk.Button(top_button_frame, text="🔴", width=3, bg="#d32f2f", fg="white").pack(side=tk.LEFT, padx=5)

# Dummy plot
plot_frame = tk.Frame(root, bg="white")
plot_frame.pack()

fig, ax = plt.subplots(figsize=(7, 4))
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

def update_plot():
    global start_time
    while True:
        if paused:
            t = last_pause_time - start_time - accumulated_pause
        else:
            t = time.time() - start_time - accumulated_pause

        x = np.linspace(0, 2 * np.pi, 100)
        y = np.sin(x + t)
        ax.clear()
        ax.plot(x, y)
        ax.set_ylim(-1.2, 1.2)
        ax.set_title("Graph-1")
        canvas.draw()
        time.sleep(0.5)

plot_thread = threading.Thread(target=update_plot, daemon=True)
plot_thread.start()

# RESULTS
results_frame = tk.Frame(root, bg="white")
results_frame.pack(pady=10)

# Left result box
result_var = tk.StringVar(value="This sample is\nExplosive\nWith accuracy of 70%")
result_label = tk.Label(
    results_frame,
    textvariable=result_var,
    bg="orange",
    fg="white",
    font=("Helvetica", 14),
    width=30,
    height=5,
    wraplength=250,
    justify="left"
)
result_label.pack(side=tk.LEFT, padx=10)

# Right model result box
model_result_var = tk.StringVar()
model_result_label = tk.Label(
    results_frame,
    textvariable=model_result_var,
    bg="#dd2476",
    fg="white",
    font=("Helvetica", 12),
    width=40,
    height=5,
    wraplength=300,
    justify="left"
)
model_result_label.pack(side=tk.LEFT, padx=10)

# Start GUI loop

root.mainloop()
