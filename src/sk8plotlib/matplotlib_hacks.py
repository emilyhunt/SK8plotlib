def fetch_matplotlib_data(fig):
    ax = get_ax(fig)
    lines, line_data = get_lines(ax)
    return ax, lines, line_data


def get_ax(fig):
    """Fetches the first ax associated to fig."""
    return fig.axes[0]


def get_lines(ax):
    """Fetches all line data on an axis."""
    lines = ax.get_lines()
    line_data = []
    for line in lines:
        x_data = line.get_xdata()
        y_data = line.get_ydata()
        tuples = []
        for x, y in zip(x_data, y_data):
            tuples.append((x, y))
        line_data.append(tuples)
    # line_data = [[line.get_xdata(), line.get_ydata()] for i, line in enumerate(lines)]
    return lines, line_data
