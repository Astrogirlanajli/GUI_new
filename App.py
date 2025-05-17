import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from shiny import App, reactive
from shiny.express import input, render, ui
from shinywidgets import render_plotly
import pandas as pd
import plotly.express as px
import numpy as np
from faicons import icon_svg as icon
import time

# Page setup
ui.input_dark_mode()
ui.page_opts(title="Raman spectroscopy", fillable=True)
# ui.h2("Spectrum", style="color:Blue; font-weight:bold")


# Sidebar inputs
with ui.sidebar():

    with ui.panel_well():
        # ui.h1("Select trained model")
        ui.input_selectize(
            "select",
            "Select AI model",
            {
                "Linear Regression": "Linear Regression",
                "Polynomial Regression": "Polynomial Regression",
                "Logistic Regression": "Logistic Regression",
                "Decision Tree": "Decision Tree",
                "Convolutional Neural Network": "CNN",
            },
            multiple=True,
        )



    with ui.panel_well():
        # ui.h1("Acqustition")
        ui.input_numeric("wavelength", "Excitation wavelength (nm)", 785)
        ui.h6("Integration time")
        with ui.layout_columns():
            ui.input_numeric("aq", " ", 10)
            ui.input_selectize("var", " ", ["s", "ms", "ns", "µs"])
 
    

    with ui.panel_well():
        ui.h6("Baseline order")
        with ui.layout_columns():
            ui.input_numeric("base", " ", 5)
            ui.input_action_button("cor", "  Correct ",  style="width: 70px; height: 50px; font-size: 9px;", class_="btn-success")
          
        ui.input_action_button("nor", "Normalise")

    with ui.panel_well():
        ui.input_action_button("res", "Test the model")



# outputs
with ui.div(style="display: flex; gap: 1.5px; margin-left: 10px;"):
    with ui.tooltip(id="btn_tooltip", placement="top"):
        ui.input_action_button("pause", "⏸️", style="width:40px; height:40px; font-size:28px; padding:0; line-height:40px; text-align:center; background-color:#444444; color:white; border:none;")
        "Pause"

    with ui.tooltip(placement="top"):
        ui.input_action_button("play", "▶️", style="width:40px; height:40px; font-size:28px; padding:0; line-height:40px; text-align:center; background-color:#2e7d32; color:white; border:none;")
        "Resume"

    with ui.tooltip(placement="top"):
        ui.input_action_button("tubelight", "💡", style="width:40px; height:40px; font-size:28px; padding:0; line-height:40px; text-align:center; background-color:#ff9800; color:black; border:none;")
        "Dark spectrum"

    with ui.tooltip(placement="top"):
        ui.input_action_button("record", "🔴", style="width:40px; height:40px; font-size:28px; padding:0; line-height:40px; text-align:center; background-color:#d32f2f; color:white; border:none;")
        "Start recording"


start_time = time.time()
paused = reactive.value(False)
last_pause_time = [0]
accumulated_pause = [0]

@reactive.effect
@reactive.event(input.pause)
def do_pause():
    paused.set(True)
    last_pause_time[0] = time.time()

@reactive.effect
@reactive.event(input.play)
def do_play():
    if paused():
        paused.set(False)
        accumulated_pause[0] += time.time() - last_pause_time[0]

@render.plot
def live_plot():
    reactive.invalidate_later(0.5)

    if paused():
        t = last_pause_time[0] - start_time - accumulated_pause[0]
    else:
        t = time.time() - start_time - accumulated_pause[0]

    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x + t)

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_ylim(-1.2, 1.2)
    ax.set_title("Graph-1")
    return fig

# From https://icons.getbootstrap.com/icons/explosion/
explosion_icon = ui.HTML(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" class="bi bi-explosion" style="fill:currentColor;height:100%;" aria-hidden="true" role="img">'
    '<path d="M7.646.146a.5.5 0 0 1 .708 0l.468.468a.5.5 0 0 0 .61.075l.567-.331a.5.5 0 0 1 .685.685l-.331.567a.5.5 0 0 0 .075.61l.468.468a.5.5 0 0 1 0 .708l-.468.468a.5.5 0 0 0-.075.61l.331.567a.5.5 0 0 1-.685.685l-.567-.331a.5.5 0 0 0-.61.075l-.468.468a.5.5 0 0 1-.708 0l-.468-.468a.5.5 0 0 0-.61-.075l-.567.331a.5.5 0 0 1-.685-.685l.331-.567a.5.5 0 0 0-.075-.61L5.146 3.56a.5.5 0 0 1 0-.708l.468-.468a.5.5 0 0 0 .075-.61l-.331-.567a.5.5 0 0 1 .685-.685l.567.331a.5.5 0 0 0 .61-.075L7.646.146Z"/>'
    '<path d="M7.09 5.365 8 8l2.635.91L8 9.818 7.09 12.45 6.182 9.818 3.547 8.91 6.182 8 7.09 5.365ZM8 13.5c0-.098.008-.195.023-.29l.318-1.59 1.54-.533c.062-.021.12-.05.175-.084l1.345-.82-1.345-.82a1.04 1.04 0 0 1-.175-.084l-1.54-.533-.318-1.59A1.5 1.5 0 0 0 8 2.5a1.5 1.5 0 0 0-1.023 2.68l-.318 1.59-1.54.533a1.04 1.04 0 0 1-.175.084l-1.345.82 1.345.82c.055.033.113.063.175.084l1.54.533.318 1.59c.015.095.023.192.023.29a1.5 1.5 0 0 0 3 0Z"/>'
    "</svg>"
)

with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=explosion_icon, theme="bg-gradient-orange-red"):
        "This sample is"
        "🔥 Explosive"
        " With accuracy of 70 %"
    with ui.value_box():
        
        @render.ui
        def selected_models_box():
            selected = input.select()
            if not selected:
                return ui.markdown("💥 No model selected")
            lines = [f"{model}: explosive" for model in selected]
            return ui.markdown("\n \n".join(lines))
        "Explosive"
