import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick

from viz_utils import read_csv, aggregate_data, remove_constant_columns, \
    aggregate_correct_percent_by_parameters, determine_group_columns

# Set uniform font size
plt.rcParams.update({'font.size': 12})

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
    sns.lineplot(data=data, x='room_count', y='correct_percent', hue='weights', ax=ax, palette=palette, errorbar=None)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.legend(title='Algorithm Value')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.xaxis.set_major_locator(mtick.MultipleLocator(1))


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
    sns.barplot(data=data, x='weights', y='correct_percent', hue='weights', ax=ax, palette=palette, dodge=False)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_ylim(0, data['correct_percent'].max() + 10)
    ax.set_xlabel('Algorithm Value')


def main():
    """
    Main function to read the CSV file, process the data, and generate multiple plots
    showing the correct percent by algorithm and room count.
    """
    file_path = "01_knn_weights.csv"
    df = read_csv(file_path)

    if df is not None:
        group_columns = determine_group_columns(df)
        aggregated_data = aggregate_data(df, group_columns)
        group_columns.extend(['room_name', 'room_count'])
        grouped_by_parameters = aggregate_correct_percent_by_parameters(aggregated_data, group_columns)
        cleaned_data = remove_constant_columns(grouped_by_parameters)

        # Filter data for each algorithm
        knn_euclidean_data = cleaned_data[cleaned_data['algorithm'] == 'knn_euclidean']
        knn_sorensen_data = cleaned_data[cleaned_data['algorithm'] == 'knn_sorensen']

        # Create the figure and axes for a 2x1 matrix (2 subplots)
        fig, axes = plt.subplots(2, 1, figsize=(14, 6))

        # Define the color palette
        palette = sns.color_palette("viridis", 2)

        # Plot for knn_euclidean_data
        plot_correct_percent(knn_euclidean_data, 'KNN (euclidean)', axes[0], palette)

        # Plot for knn_sorensen_data
        plot_correct_percent(knn_sorensen_data, 'KNN (sorensen)', axes[1], palette)

        plt.tight_layout(rect=(0, 0, 1, 1))

        # Save the plot as an image
        plt.savefig('01_knn_weights_01.png', dpi=300)
        plt.show()

if __name__ == "__main__":
    main()
