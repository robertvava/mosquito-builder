# 4.9-inch frame — v0.4 with supported Pi and battery

This revision incorporates the reviewer feedback: conservative propeller
clearance, real Pi mounting geometry, a separate battery load path and an
independent propeller seating-height parameter. It remains an unpowered fit
prototype pending material, structural, component and wiring checks.

## Dimensions and clearance

| Item | v0.4 |
|---|---:|
| Opposite-motor wheelbase | 224 mm |
| Actual nominal prop diameter | 124.46 mm |
| Prop diameter used for clearance calculations | 127 mm |
| Gap between adjacent clearance envelopes | 31.39 mm |
| Battery allowance / plan clearance | 85 x 45 x 30 mm / 4.04 mm |
| Upper electronics deck / plan clearance | 74 x 66 x 3 mm, R12 corners / 4.02 mm |
| Battery tray / plan clearance | 89 x 54 x 3 mm, R10 corners, two mounting tabs / 3.09 mm |
| Pi mounting holes | 58 x 23 mm pattern; 2.8 mm printed M2.5 clearance |
| Pi spacers | Four, 6 mm tall x 6 mm diameter |
| Battery tray columns | Two, 22 mm tall x 8 mm diameter, M3 clearance bores |
| Chassis spacers | Four, 36 mm tall x 7 mm diameter |
| Arms / motor pad | 18 x 8 mm / 34 mm diameter |
| Arm root / attachment bolt radii | 27 mm / 33 and 42 mm |
| Stack mounting / screw access | 30.5 x 30.5 mm / 8 mm access cylinders below |
| Provisional prop seating height above motor mounting face | 31.8 mm, unverified |

The nominal diameter is used for blue propeller disks in the viewer. The cyan
disks show the 127 mm clearance envelope. All battery, upper-deck and tray
clearances use the larger diameter. The envelope adds 1.27 mm radially to the
nominal diameter; the stated plan gaps are additional to that allowance.

`propeller_seating_height` is independent of `motor_envelope_height`.
Its current value preserves the earlier display position only. Measure from
the motor mounting face to the installed propeller seating surface and set
`propeller_seating_height_verified` only after checking it. This does not verify
the entire blade thickness or flex envelope. Neither 39.8 mm nor the reviewer's
55 mm absolute plane was established by a measurement.

The 85 x 45 x 30 mm battery box remains an allowance. A larger measured pack
needs another clearance calculation and potentially a tray/layout change.
The pack and Pi are both centred at X=Y=0; their positions are now supported
by physical mounting parts rather than being floating boxes.

## Payload arrangement

The upper electronics deck has four M2.5 holes at X=+/-29 mm, Y=+/-11.5 mm.
The Pi rests on four 6 mm spacers. Use suitable M2.5 bolts and nuts, with
insulating spacers. The printed holes are clearance holes, not threads.

The battery tray is held above the Pi by two columns at X=0, Y=+/-28 mm.
They align with the two side chassis spacers. Battery force passes through the
tray, side columns and chassis; it does not pass through the Pi or its mounts.
The tray is removable for access to the Pi, CSI ribbon, microSD and connectors.

Two transverse straps use four 22 x 3 mm slots, at X=+/-18 mm and Y=+/-24 mm.
Use straps no wider than about 20 mm and no thicker than the 1 mm allowance
for the portion passing underneath. A 2 mm nonslip pad is modelled between
the tray and the battery; it is a purchased/cut consumable, not a print part.
Do not clamp the battery down so hard that it deforms.

| Part | Bottom Z | Top Z |
|---|---:|---:|
| Upper electronics deck | 48 mm | 51 mm |
| Pi spacers | 51 mm | 57 mm |
| Pi and connector allowance | 57 mm | 69 mm |
| Tray support columns | 51 mm | 73 mm |
| Battery tray | 73 mm | 76 mm |
| Nonslip pad allowance | 76 mm | 78 mm |
| Battery allowance | 78 mm | 108 mm |

There is 4 mm between the Pi allowance and the tray underside. The validation
reserves 1 mm of that for the strap and 3 mm for remaining clearance. Actual
ribbon bend radius, connectors, regulator and wiring still need checking; this
revision does not model those cable paths.

## Export and first prints

```bash
uv run python -m cad.assembly --show
uv run python -m cad.assembly --coupons-only
uv run python -m cad.assembly --export
```

Current STEP/STL files are in `cad/exports/v0_4/`. Each individual STL is centred
in XY and rests at Z=0. Keep older versions for reference and use the new
directory for this revision. The assembled STEP includes component/reference
envelopes and must not be printed as one object.

Start with one each of the motor, stack and Pi mounting coupons. The Pi sample
is 65 x 30 x 3 mm with the four M2.5 holes. Check all bores and the mounting
patterns against the actual hardware. An 8 mm motor pad needs screw engagement
to be checked against the motor; supplied screw length may be insufficient.

For the chassis and payload fit prototype:

| STL | Print quantity |
|---|---:|
| `arm_8mm_provisional.stl` | 4 |
| `lower_plate_4mm_provisional.stl` | 1 |
| `top_plate_3mm_provisional.stl` | 1 |
| `standoff_36mm_provisional.stl` | 4 |
| `pi_spacer_6mm_provisional.stl` | 4 |
| `battery_tray_support_22mm_provisional.stl` | 2 |
| `battery_tray_3mm_provisional.stl` | 1 |

## Assembly order

1. Attach the arms beneath the lower plate using their two M3 bolts each.
   Keep screw heads, washers and nuts within the reserved 7 mm diameter and
   3.5 mm height; any protruding arm screw tip allowance is 1 mm.
2. Install the FC/ESC stack through its unobstructed holes. Use insulating
   spacers and the correct board grommets. Check the real stack against the
   6 mm floor gap, 10 mm ESC allowance and 5 mm inter-board gap.
3. Fit the four chassis spacers and upper deck. Attach the Pi with its four
   M2.5 spacers and verify access before installing the battery tray.
4. At the two side-axis mounts, use continuous M3 through-bolts through lower
   plate, 36 mm spacer, upper deck, 22 mm tray column and tray. This material
   stack is 68 mm long. Select bolt length for actual washers, head and nut
   engagement; 68 mm is not the required bolt length. The printed bores are
   not threaded.
5. The other two chassis mounts use the shorter lower-plate/spacer/deck stack
   of 43 mm. Limit fastener height above the deck to 4.5 mm, leaving clearance
   below the Pi, which starts 6 mm above the deck.
6. Thread the two straps through the tray slots and add the nonslip pad. Verify
   wiring and ribbon paths before fitting the actual battery. Fit all parts
   unpowered and confirm that straps cannot enter a propeller disk.

## Checks and remaining work

The tests check nominal/clearance separation, the prior screw-access fixes,
Pi mounting bores, tray support contact, full battery footprint support,
strap slots, clearances against 127 mm disks and individual print placement.
They reject the old 220 mm wheelbase with the conservative envelope and reject
tray columns too short to clear the Pi and strap.

The solid-polymer mass estimate includes the tray, four Pi spacers and two tray
columns as well as the original chassis. Slicer mass and printed strength still
depend on material, walls, infill, orientation and the actual printer. The
two-column tray needs bending/twist and fastener tests as part of the prototype.

Camera mounts, receiver, regulator, capacitor and antenna placement, guard
requirements, cable routes and flight firmware remain outside this mechanical
revision. No material or flight approval follows from passing geometry tests.
