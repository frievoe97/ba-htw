import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick

from viz_utils import read_csv, aggregate_data, remove_constant_columns, \
    aggregate_correct_percent_by_parameters, determine_group_columns, measurements_per_room

# Set uniform font size
plt.rcParams.update({'font.size': 12})

def configure_axes(axes):
    """
    Configures the axes with grid, limits, and format.

    Parameters:
        axes (array): An array of matplotlib Axes.
    """

    axes.grid(True, which='both', linestyle='--', linewidth=0.5)
    axes.set_ylim(0, 100)
    axes.yaxis.set_major_formatter(mtick.PercentFormatter())

def plot_avg_correct_percent(data, title, ax, palette, ylabel='Average Correct Percent'):
    """
    Plots the average correct percentage by algorithm value with a bar plot.

    Parameters:
        data (DataFrame): The data to plot.
        title (str): The title of the plot.
        ax (Axes): The matplotlib Axes to plot on.
        palette (list): The color palette to use.
        ylabel (str): The label for the y-axis.
    """
    sns.barplot(data=data, x='algorithm_value', y='correct_percent', hue='algorithm_value', ax=ax, palette=palette, dodge=False)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_ylim(0, data['correct_percent'].max() + 10)
    ax.set_xlabel('Algorithm Value')

def plot_algorithm(data, ax, title):
    """
    Plots the average and weighted average correct percent for a given algorithm.

    Parameters:
        data (DataFrame): The data to plot.
        algorithm (str): The algorithm to filter the data.
        ax (Axes): The matplotlib Axes to plot on.
        title (str): The title of the plot.
    """
    palette = sns.color_palette("viridis", len(data['algorithm_value'].unique()))
    data_to_plot = data

    bar_width = 0.4  # Width of the bars

    x = range(len(data_to_plot))

    # Plot for average
    ax.bar(x, data_to_plot['correct_percent'], width=bar_width, label='Average', color=palette)
    print(data_to_plot)
    # Plot for weighted average
    ax.bar([p + bar_width for p in x], data_to_plot['weighted_correct_percent'],
           width=bar_width, label='Weighted Average', color=palette, alpha=0.6)

    ax.set_title(title)
    ax.set_ylabel('Average Correct Percent')
    ax.set_xlabel('Algorithm Value')
    ax.set_xticks([p + bar_width / 2 for p in x])
    ax.set_xticklabels(data_to_plot['algorithm_value'])

    add_bar_labels(ax)

def plot_correct_percent(data, title, ax, palette, ylabel='Correct Percent', xlabel='Number of measurements per room'):
    """
    Plots the correct percentage by room count with a line plot.

    Parameters:
        data (DataFrame): The data to plot.
        title (str): The title of the plot.
        ax (Axes): The matplotlib Axes to plot on.
        palette (list): The color palette to use.
        ylabel (str): The label for the y-axis.
    """
    sns.lineplot(data=data, x='room_count', y='correct_percent', hue='algorithm_value', ax=ax, palette=palette, errorbar=None)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.legend(title='Algorithm Value')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.xaxis.set_major_locator(mtick.MultipleLocator(1))

def add_bar_labels(ax):
    """
    Adds labels on top of the bars in a bar plot.

    Parameters:
        ax (Axes): The matplotlib Axes to plot on.
    """
    for p in ax.patches:
        value = format(p.get_height(), '.1f')
        if value != "0.0":  # Remove 0.0 values
            ax.annotate(value,
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center',
                        xytext=(0, 9),
                        textcoords='offset points')

def main():
    """
    Main function to read the CSV file, process the data, and generate multiple plots
    showing the correct percent by algorithm and room count.
    """
    file_path = "04_random_forest_n_estimators.csv"
    df = read_csv(file_path)

    if df is not None:
        group_columns = determine_group_columns(df)

        df["algorithm_value"] = df["algorithm_value"].fillna('None')

        aggregated_data = aggregate_data(df, group_columns)
        group_columns.extend(['room_name', 'room_count'])
        grouped_by_parameters = aggregate_correct_percent_by_parameters(aggregated_data, group_columns)
        cleaned_data = remove_constant_columns(grouped_by_parameters)

        # Weighted average
        cleaned_data['weighted_correct_percent'] = cleaned_data['correct_percent'] * cleaned_data['room_count']
        weighted_avg_correct_percent = cleaned_data.groupby(['algorithm_value']).apply(
            lambda x: pd.Series({'weighted_correct_percent': x['weighted_correct_percent'].sum() / x[
                'room_count'].sum()})).reset_index()

        # Create the figure and axes for a 2x1 matrix (2 subplots)
        fig, axes = plt.subplots(1, 1, figsize=(14, 6))

        # Define the color palette
        palette = sns.color_palette("viridis", 19)

        # Plot for knn_euclidean_data
        plot_correct_percent(cleaned_data, 'SVM (RBF)', axes, palette)


        plt.tight_layout(rect=(0, 0, 1, 1))

        # Save the plot as an image
        plt.savefig('04_random_forest_n_estimators_01.png', dpi=300)
        plt.show()

        # Calculate the average correct percent for each algorithm and algorithm value
        avg_correct_percent = cleaned_data.groupby(['algorithm_value'])['correct_percent'].mean().reset_index()

        # Create the figure and axes for a 2x1 matrix (2 subplots)
        fig, axes = plt.subplots(1, 1, figsize=(18, 12))
        fig.suptitle('Average Correct Percent by Algorithm and Algorithm Value', fontsize=16)

        # Plot for knn_euclidean_data
        knn_euclidean_palette = sns.color_palette("viridis", len(
            avg_correct_percent['algorithm_value'].unique()))
        plot_avg_correct_percent(avg_correct_percent,
                                 'KNN (euclidean)', axes, knn_euclidean_palette)

        # Merge the two DataFrames
        avg_correct_percent = avg_correct_percent.merge(weighted_avg_correct_percent,
                                                        on=['algorithm_value'])



        plt.tight_layout(rect=(0, 0, 1, 0.95))
        # Save the plot as an image
        plt.savefig('04_random_forest_n_estimators_02.png', dpi=300)
        plt.show()

        # Create the figure and axes for a 5x1 matrix (5 subplots)
        fig, axes = plt.subplots(1, 1, figsize=(18, 8))

        # Configure common settings for all subplots
        configure_axes(axes)

        # Plots for each algorithm
        plot_algorithm(avg_correct_percent, axes, 'KNN (euclidean)')

        # Dummy patches for the legend
        legend_patches = [
            plt.Line2D([0], [0], color='grey', lw=4, label='Average'),
            plt.Line2D([0], [0], color='lightgrey', lw=4, label='Weighted Average')
        ]

        fig.legend(handles=legend_patches, loc='lower center', ncol=2, bbox_to_anchor=(0.2, -0.01))

        plt.tight_layout(rect=(0, 0, 1, 0.99))
        # Save the plot as an image
        plt.savefig('04_random_forest_n_estimators_03.png', dpi=300, bbox_inches='tight')
        plt.show()

if __name__ == "__main__":
    main()
