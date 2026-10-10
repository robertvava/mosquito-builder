# 4.9-inch frame — v0.3 mounting and fit prototype

Superseded by [v0.4 with supported Pi and battery](FRAME_DESIGN_V0_4_PAYLOAD.md).
Use v0.4 for the 127 mm clearance envelope and payload mounting parts.

The central mounting conflicts identified in v0.2 are corrected. This revision
is ready for small, unpowered mounting trials. Structural qualification and the
Pi/battery/camera mounting assembly still remain.

## Geometry changes

| Feature | v0.3 |
|---|---:|
| Opposite-motor wheelbase | 220 mm |
| Prop diameter | 124.46 mm |
| Adjacent prop gap | 31.1 mm nominal |
| Arm section | 18 x 8 mm, provisional |
| Arm root radius | 27 mm |
| Arm bolt radii | 33 and 42 mm |
| Motor mounting | 16 x 16 mm; 3.4 mm printed holes |
| FC/ESC mounting | 30.5 x 30.5 mm; 3.4 mm printed holes |
| Stack screw/tool access | 8 mm diameter clear below each stack hole |
| Fastener head/washer/nut allowance | 7 mm diameter, 3.5 mm height |
| Additional screw tip allowance | 1 mm |
| ESC floor clearance above lower plate | 6 mm |
| Electronics bay height | 36 mm |
| Lower plate | 78 x 70 x 4 mm, 8 mm corner radius |
| Upper plate | 74 x 66 x 3 mm, 12 mm corner radius |

The roots end outside the stack screws' access cylinders. The two bolts on each
arm are further out, so their holes and reserved head/nut envelopes no longer
overlap the stack fasteners. The ESC sits above the arm bolt heads and any
permitted short screw protrusion. Select actual screws, washers and nuts to fit
these envelopes; they are not included in the CAD assembly.

The upper plate has over 3 mm of clearance from each propeller disk in top view,
so its clearance does not depend on the provisional propeller height. The
display still uses the motor's total 31.8 mm height to position the prop disk;
the blade mounting height must be corrected when available.

## View and export

Start OCP CAD Viewer in VS Code, then run:

```bash
uv run python -m cad.assembly --show
```

For just the first two test prints:

```bash
uv run python -m cad.assembly --coupons-only
```

For the complete fit-prototype export:

```bash
uv run python -m cad.assembly --export
```

All new STEP/STL files are under `cad/exports/v0_3/`. Older root-level exports
are retained for reference. Use the new directory for this revision.

Each individual STL is centred in XY with its bottom at Z=0. The STEP assembly
retains assembly positions. Do not print the assembly with its component boxes.

## First prints

Print one of each coupon flat, using the intended printer and the same hole
compensation settings planned for the frame:

| File | Quantity | Purpose |
|---|---:|---|
| `motor_mount_coupon_8mm.stl` | 1 | Same 34 mm pad, 8 mm thickness, shaft opening and four motor holes as the arms |
| `stack_mount_coupon_4mm.stl` | 1 | Same plate thickness and four mounting holes as the central stack interface |

Use the motor sample to check that the motor sits flat, its shaft/base clears
the opening, and all four screws align. Check screw engagement separately:
the 8 mm printed pad may require longer screws than those supplied with the
motor. Screw tips must clear the windings; do not choose a length by guessing.

Use the stack sample to check that M3 hardware passes through the printed holes
and that the actual FC/ESC grommets fit correctly over that hardware. The FC's
grommets fit the board holes; do not press those grommets into the printed
coupon. Fit the stack without power or propellers.

If fit is too tight or loose, adjust the printed hole diameter or slicer hole
compensation and reprint both samples. Avoid changing both at once: record one
adjustment so the successful setting is reproducible.

## Chassis trial after coupons fit

Print four arms, one lower plate, one upper plate and four copies of
`standoff_36mm_provisional.stl`. The spacers are plain through-bored tubes for
M3 hardware, not threaded pillars. Retain them with through-bolts and nuts or
another verified mounting arrangement; do not assume screws will thread into
the 3.4 mm bores. Purchased non-conductive 36 mm spacers are an alternative if
their geometry and screw access match.

1. Bolt the four arms under the lower plate, with each arm using two bolts.
2. Confirm stack screw heads fit between the arm roots and can be reached from
   underneath. Assemble the stack using insulating spacers and the supplied
   vibration grommets. Actual hardware determines the stack bolt lengths.
3. Install the ESC with at least the modelled 6 mm floor gap and the FC with
   the provisional 5 mm inter-board gap. Check actual component and connector
   heights rather than using PCB thickness alone.
4. Attach the four perimeter spacers and upper plate. Check USB access, solder
   joints, wiring bends, cooling and capacitor placement before closing it.
5. Fit the motors and repeat alignment checks. Keep the assembly unpowered.

The Pi and battery boxes reserve space above the upper plate. Their mounting
tray is still absent; the existing slots alone do not provide that support.
Receiver, regulator, cameras, antenna, guards and wiring retention must be
incorporated before a complete aircraft can be assembled.

## Verification scope

The 14 geometry tests include solid checks for open mounting bores, unobstructed
stack tool paths, fastener-envelope separation, head clearance under the ESC,
upper-plate propeller projection clearance and bed-aligned print parts. They
also reject the earlier overlapping bolt positions and obstructing arm roots.

The mass report now includes all four spacers. It uses solid CAD volume and an
assumed polymer density; use the slicer's material/profile estimate for printing.
No geometry test establishes the strength of a printed arm or validates the
finished propulsion, firmware or power system.
