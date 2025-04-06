import os
import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate
import bokeh.models as bm
import bokeh.plotting as pl
from bokeh.io import output_file
import webbrowser


class Visualizer:
    """Collection of visualization methods"""
    OUTPUT_FILE = 'output/output00.html' # vars for drawing vectors
    MAX_FILES = 5

    @staticmethod
    def plot_series(series: list[pd.Series], titles: list[str],
                        main_title: str = None, x_label: str = None, y_label: str = None,
                        bins: int = 100, plot_type: str = "hist") -> None:
        """Plot histograms of the text column lengths in the train and test dataframes

        :@param series: list of pd.Series to plot histograms for
        :@param titles: list of titles for the histograms
        :@param main_title: title of the plot (default: None)
        :@param x_label: x-axis label (default: None)
        :@param y_label: y-axis label (default: None)
        :@param bins: number of bins for the histogram (default: 100)
        :@param plot_type: type of plot to use (default: "hist", options: "hist", "bar")
        """
        n_series = len(series)
        fig, ax = plt.subplots(1, n_series, figsize=(12, 6))
        if n_series == 1:
            ax = [ax]

        for i, (s, title) in enumerate(zip(series, titles)):
            if plot_type == "hist":
                ax[i].hist(s, bins=bins)
            elif plot_type == "bar":
                s.plot(kind='bar', ax=ax[i])
            ax[i].set_title(title)
        
        if main_title is not None:
            fig.suptitle(main_title, fontsize=16)
        
        if x_label is not None:
            ax[0].set_xlabel(x_label)
        
        if y_label is not None:
            ax[0].set_ylabel(y_label)
        
        plt.show()
    
    @staticmethod
    def pretty_sample(df: pd.DataFrame, n_sample: int = 3, max_length: int = 100) -> None:
        """Print a pretty sample of the DataFrame

        :@param df: DataFrame to print
        :@param n_sample: number of samples to print (default: 3)
        :@param max_length: maximum length of the text to print (default: 100
        """
        df_trunc = df.applymap(lambda x: x[:max_length] if isinstance(x, str) else x)
        print(tabulate(df.sample(n_sample), headers='keys', tablefmt='pretty'))
    
    @staticmethod
    def update_output_file_if_needed() -> None:
        """Updates the output file if it already exists and create the output directory if needed."""
        out_file = Visualizer.OUTPUT_FILE
        out_folder = os.path.dirname(out_file)
        if os.path.exists(out_file):
            number = int(out_file.split('.')[0][-2:])
            number += 1
            if number == Visualizer.MAX_FILES:
                number = 0
            Visualizer.OUTPUT_FILE = os.path.join(out_folder, f'output{number:02d}.html')
        
        os.makedirs(out_folder, exist_ok=True)
    
    @staticmethod
    def draw_vectors(x, y, radius=10, alpha=0.25, color='blue', width=1400, height=800, show=True, **kwargs):
        """
        Draws an interactive plot for data points with auxiliary info on hover.
        x: x-coordinates of points
        y: y-coordinates of points
        """
        Visualizer.update_output_file_if_needed()
        output_file(Visualizer.OUTPUT_FILE)  # Save the plot to an HTML file
        if isinstance(color, str):
            color = [color] * len(x)

        data_source = bm.ColumnDataSource({'x': x, 'y': y, 'color': color, **kwargs})

        fig = pl.figure(active_scroll='wheel_zoom', width=width, height=height)
        fig.scatter('x', 'y', size=radius, color='color', alpha=alpha, source=data_source)

        fig.add_tools(bm.HoverTool(tooltips=[(key, "@" + key) for key in kwargs.keys()]))
        if show:
            pl.show(fig)

        return fig
    
    @staticmethod
    def open_in_browser():
        """Opens the saved HTML file in the default web browser."""
        full_path = os.path.abspath(Visualizer.OUTPUT_FILE)
        webbrowser.open(f'file://{full_path}')

