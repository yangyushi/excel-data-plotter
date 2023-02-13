# Data Plotter

This is a GUI application for plotting data from an Excel spreadsheet. The application is implemented using Python and PyQt.

## ChatGPT

The code and the organisation of the project was generated by chatGPT.
It takes some effort to get the chatGPT producing usable code.
The important text prompt is included in the commit message.

(This repo is to memorise my first AI aided project. Hopefully more will come very soon!)

## Features

- Load data from an Excel file
- Select two columns to plot interactively
- Update the plot each time different columns are selected or the plot button is clicked
- Plot data as either a line plot or scatter plot
- Apply a custom Y-Transformation to the plotted data
- Interactive plot with the toolbar from matplotlib, allowing the user to zoom in and out

## Usage

1. Clone or download the repository
2. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Run the code:
    ```
    python main.py
    ```
3. Build a package:
    ```
    make package
    ```
