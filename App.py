from shiny import App, reactive
from shiny.express import input, render, ui
from shinywidgets import render_plotly
import pandas as pd
import plotly.express as px

# Page setup
ui.input_dark_mode() 
ui.page_opts(title="Raman spectroscopy", fillable=True)
ui.h2("Spectrum", style="color:Blue; font-weight:bold")


# Sidebar inputs
with ui.sidebar():
    ui.input_numeric("wavelength", "Wavelength of Laser (nm)", 876.0)
    ui.input_selectize(
        "var", "Select AI model",
        ["Linear Regression", "Polynomial Regression", "Logistic Regression",
         "Decision Tree", "Random Forest", "Convolutional Neural Network"]
    )
    ui.input_file("train", "Upload the training data")
    ui.input_action_button("btn", "Train the model")
    ui.input_slider("slider", "Aquasation time(sec)", 0, 100, 50)
    ui.input_file("test", "Upload the test data")
    ui.input_action_button("bt", "Test the model")
# outputs
