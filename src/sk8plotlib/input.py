class UserInput:
    def __init__(self, fig):
        self.fig = fig
        self._held_keys = set()
        fig.canvas.mpl_connect("key_press_event", self.key_press_handler)
        fig.canvas.mpl_connect("key_release_event", self.key_release_handler)

    def key_press_handler(self, event):
        self._held_keys.add(event.key)

    def key_release_handler(self, event):
        self._held_keys.remove(event.key)

    def left_right_input(self):
        """Calculates the difference in left/right input."""
        output = 0
        if "right" in self._held_keys:
            output += 1
        if "left" in self._held_keys:
            output -= 1
        return output

    def up_down_input(self):
        """Calculates the difference in left/right input."""
        output = 0
        if "up" in self._held_keys:
            output += 1
        if "down" in self._held_keys:
            output -= 1
        return output
