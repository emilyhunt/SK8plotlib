import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure


def thebigsine(
    x_scale=60,
    y_scale=100,
    periods=5,
    ramp_resolution=1500,
) -> Figure:
    """Simple example map. Designed purely for speed."""
    fig, ax = plt.subplots(figsize=(8, 4), dpi=300)

    x = np.linspace(
        -np.pi * x_scale, (periods - 0.5) * 2 * np.pi * x_scale, num=ramp_resolution
    )
    y = np.sin(x / x_scale) * y_scale
    ax.plot(x, y)

    return fig
