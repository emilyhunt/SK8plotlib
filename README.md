# SK8plotlib

<p align="center">
<img src="https://github.com/user-attachments/assets/5d922753-74e5-4119-8ff5-de70ff55d4c8" width="500" />
</p>

Turn any matplotlib line chart into a line skateboarding game.

> [!CAUTION]
> SK8plotlib is in pre-alpha. Expect bugs. Software provided without warranty, yada yada.

## Installation

Install from PyPI with:

```bash
pip install sk8plotlib
```

## Use

Turn any matplotlib line chart into a skatepark with:

```python
import sk8plotlib.sk8plot as sk8

# ... create a matplotlib figure

sk8(fig)
```

Alternatively, you can load example maps by running SK8plotlib on the command line, such as by doing:

```bash
python -m sk8plotlib
```

## Roadmap

Planned features before v0.1:

- ~~Automatic detection of lines in plot~~
- ~~Basic physics simulation (single accelerating point)~~
- ~~Basic collision detection (skateboard only)~~
- ~~Skateboard rotation on surfaces~~
- ~~User control input~~
- Smooth camera
- Automatic map scaling
- Auto-initialize in correct location

Planned future features:

- Improved player character
- ~~Improved collisions~~ (had to be done sooner than planned...)
- Improved graphics
- Music
- Support for log plots
- Scoring system?
