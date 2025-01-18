import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure


def sinepark(
    x_ramps=9,
    y_ramps=9,
    ramp_width=4 * np.pi,
    ramp_height=10.0,
    x_spacing=2.5,
    y_spacing=5.0,
    ramp_resolution=50,
) -> Figure:
    """Simple example map. Full of trigonometric ramps."""
    fig, ax = plt.subplots(figsize=(8, 4), dpi=300)
    rng = np.random.default_rng(seed=43)

    ax.plot([-1, 1], [0, 0])

    width = x_ramps * ramp_width + (x_ramps - 1) * x_spacing
    height = y_ramps * ramp_height + (y_ramps - 1) * y_spacing

    functions = [np.sin, np.sin, np.sinh, np.cosh, np.tanh]

    for y_start in np.linspace(-y_spacing, -height - y_spacing, num=y_ramps):
        for x_start in np.linspace(-width/2, width/2, num=x_ramps):
            x = np.linspace(x_start, x_start + ramp_width, num=ramp_resolution)
            x += rng.uniform(x_spacing * -0.5, x_spacing * 0.5)

            x_function = np.linspace(-np.pi, np.pi, num=ramp_resolution) * rng.choice(
                [-1, 1]
            ) + rng.uniform(-np.pi / 2, np.pi / 2)
            function = functions[rng.integers(0, high=len(functions))]
            y = function(x_function) * rng.choice([-1, 1]) + rng.uniform(-1, 1) * x_function
            y -= y.min()
            y = (y / y.max()) * ramp_height * rng.uniform(0.2, 1.0)
            y += y_start - ramp_height
            ax.plot(x, y, color=plt.get_cmap("viridis")(rng.uniform()), lw=2.0)

    return fig
