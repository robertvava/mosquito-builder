# Generated CAD exports

Run the following from the repository root to regenerate these files from the
Python design master:

```bash
uv run python -m cad.assembly --export
uv run python -m cad.render_svg
uv run python -m cad.render_png
```

Current STEP/STL files are in `v0_4/`. The STEP assembly is for review/interchange;
each individual STL is centred in XY and placed on Z=0 for slicing.

Print one each of `motor_mount_coupon_8mm.stl`, `stack_mount_coupon_4mm.stl`
and `pi_mount_coupon_3mm.stl` first. Export only these with
`uv run python -m cad.assembly --coupons-only`.

The chassis needs four arms, one lower plate, one upper plate and four copies of
the single exported `standoff_36mm_provisional.stl`. Standoffs have plain M3
clearance bores; use suitable through-bolts/nuts, not self-tapped threads.
The payload also needs four `pi_spacer_6mm_provisional.stl`, two
`battery_tray_support_22mm_provisional.stl` and one
`battery_tray_3mm_provisional.stl`.

See [v0.4 fit instructions](../../docs/FRAME_DESIGN_V0_4_PAYLOAD.md). Printer
calibration, material selection, component fit and structural work remain.

The `v0_3/` directory is retained as the earlier mounting revision. It lacks the
127 mm conservative envelope and the Pi and battery tray mounting parts.

Root-level STEP/STL files belong to superseded revisions. The v0.2
`*_provisional.stl` parts have conflicting central mounting holes; do not use
them for the updated chassis.

The older `arm_4mm.stl`, `lower_plate_1p5mm.stl` and
`top_plate_1p5mm.stl` belong to the superseded v0.1 carbon-sheet concept and
must not be used for the 4.9-inch build.
