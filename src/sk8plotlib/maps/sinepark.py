import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure


def sinepark() -> Figure:
    """Simple example map. Full o' sines."""

    x = np.linspace(-np.pi, 50 * np.pi, num=1000)
    y = np.cos(x) - x * 0.2 * np.cos(x) - 0.5*x

    x = x * 2 - 1
    y = y - 2
    y = y * 3

    fig, ax = plt.subplots(figsize=(8, 4), dpi=300)
    ax.plot(x, y)
    return fig
