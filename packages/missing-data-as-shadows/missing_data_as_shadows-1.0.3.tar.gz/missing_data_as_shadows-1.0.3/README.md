# **Visualization of Incomplete Datasets** #
This project focuses on visualizing incomplete datasets, where missing data is represented using shadows or other graphical elements. The goal is to facilitate the interpretation of missing values and help analysts gain a deeper understanding of the data.
# **Usage** #
import pandas as pd

from missing_data_as_shadows import make_full_analysis, scatter_with_shadows_rect_binned

## Load data with missing values
df = pd.read_csv('data.csv')

## Generate full visualization
make_full_analysis(df, output_name="output_name", method="spearman")

**Method parameter is correlation method**

If you don't provide method parameter default is pearson.

The method parameter allows you to select any correlation method supported by pandas, such as:

- pearson

- kendall

- spearman

## Generate Subplots with Shadows for Two Attributes

 create_subplot_with_shadows(data, atr1, atr2, name="test", save=True)

### Parameters 

data (DataFrame) – The dataset containing the attributes to visualize.

atr1 (str) – The first attribute (column name) for visualization.

atr2 (str) – The second attribute (column name) for visualization.

name (str, optional, default=None) – The filename to save the plot. If None, the plot will not be saved.


## Generate visualization for two chosen attributes

# Usage

scatter_with_shadows_rect_binned(

    diabetesData,
    diabetes_data_attribute_one, 
    diabetes_data_attribute_two,
    bins_count=10,
    marker_size_scatter=3,
    marker_size_rect=0.001
    name="Name"
)
### Parameters
df (DataFrame) – The dataset containing the attributes to visualize.

col_a (str) – The first attribute (column name) to be plotted on the x-axis.

col_b (str) – The second attribute (column name) to be plotted on the y-axis.

marker_size_scatter (float, default=3) – The size of scatter plot markers.

marker_size_rect (float, default=0.5) – The size of markers for binned data representation.

bins_count (int, default=10) – The number of bins used for shadow visualization.

fraction_of_range (float, default=0.5) – Determines the proportion of the attribute range considered for binning.

color_missing_a (str, default='grey') – Color used to highlight missing values in col_a.

color_missing_b (str, default='grey') – Color used to highlight missing values in col_b.

alpha_main (float, default=0.3) – Transparency level of the scatter points.

outline_color (str, default='black') – Color of the outline around data points.

outline_width (float, default=0.5) – Thickness of the outline around data points.

name - (str) - save with specified name

