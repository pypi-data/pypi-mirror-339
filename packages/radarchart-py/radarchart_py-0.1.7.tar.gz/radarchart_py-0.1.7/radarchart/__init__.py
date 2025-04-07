import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Tuple, Union


def plot(
    df: pd.DataFrame,
    norm_max: bool = False,
    streamlit: bool = False
) -> Union[plt.Axes, Tuple[plt.Figure, plt.Axes]]:
    """
    Plot a radar chart for the rows of a DataFrame.

    Parameters:
        df (pd.DataFrame): Input data where rows are entities and columns are variables.
        norm_max (bool): Normalize each column by its maximum value if True.
        streamlit (bool): If True, return (fig, ax) for use in Streamlit. Otherwise, return ax.

    Returns:
        plt.Axes or Tuple[plt.Figure, plt.Axes]: The axis or (figure, axis) depending on `streamlit`.
    """
    df = df.copy()
    if norm_max:
        df /= df.max()

    # Compute angles for each axis and complete the circle
    angles = np.linspace(0, 2 * np.pi, len(df.columns), endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))  # close the plot

    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)

    for i in df.index:
        stats = df.loc[i, :].values
        stats = np.concatenate((stats, [stats[0]]))  # close the plot
        ax.plot(angles, stats, 'o-', linewidth=2, label=i)
        ax.fill(angles, stats, alpha=0.25)

    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

    columns = list(df.columns) + list(df.columns[:1])
    # print((angles * 180 / np.pi).shape, len(columns))
    ax.set_thetagrids(angles * 180 / np.pi, columns)
    ax.grid(True)

    return (fig, ax) if streamlit else ax


def example_dataframe():
    df = pd.DataFrame([
        [0.2, 0.1, 0.1, 0.1, 0.1, 0.1],
        [0.8, 0.7, 0.7, 0.7, 0.7, 0.7],
        [0.9, 0.8, 0.8, 0.8, 0.8, 0.8],
    ])
    df.columns = ['P1', 'P5', 'P10', 'P20', 'P50', 'P100']
    df.index = ['Model-A', 'Model-B', 'Model-C']
    df.index.name = 'Model'
    return df
