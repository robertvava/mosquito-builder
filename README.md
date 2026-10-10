# Drone Club

Custom quadrotor project for hover stability, autonomous 3D movement and an
indoor FPV obstacle course.  The complete system must cost less than £400 and
the same hardware configuration will be used for all three tasks.

## Current component list

- [Revised 4.9-inch build component list](docs/COMPONENT_LIST_4P9_INCH.md)

The root-level `list` file is the working shopping list. The v0.4 CAD below is
a 4.9-inch fit prototype with a mounted Pi and a separately supported battery
tray. Structural and remaining component integration work still remain.

## Current mechanical concept

- [4.9-inch frame with supported Pi and battery v0.4](docs/FRAME_DESIGN_V0_4_PAYLOAD.md)
- [Earlier 4-inch/carbon concept v0.1](docs/FRAME_DESIGN_V0_1.md)
- [Full design and OCP CAD guide](docs/DRONE_DESIGN_AND_OCP_CAD_GUIDE.md)
- [Top review image](cad/exports/frame_top.png)
- [Isometric review image](cad/exports/frame_isometric.png)

Run the interactive build in VS Code with OCP CAD Viewer open:

```bash
uv sync
uv run python -m cad.assembly --show
```

Run checks and regenerate the review/export files:

```bash
uv run python -m unittest discover -s tests -v
uv run python -m cad.assembly --coupons-only
uv run python -m cad.assembly --export
uv run python -m cad.render_svg
uv run python -m cad.render_png
```

The Python files under `cad/` are the design master. Generated STEP/STL and
review images live under `cad/exports/`. Current STEP/STL fit samples and parts
are in `cad/exports/v0_4/`; individual STLs are centred and placed on Z=0.
