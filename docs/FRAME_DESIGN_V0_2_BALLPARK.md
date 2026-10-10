# 4.9-inch printed frame — ballpark concept v0.2

Superseded by [v0.3 mounting and fit prototype](FRAME_DESIGN_V0_3_FIT.md).
The v0.2 central arm and stack holes conflict; use v0.3 for fit prints.

Status: packaging and fit prototype only. Do not treat this revision as a
flight-ready structure.

## What is known

The first pass uses published dimensions instead of photographs or caliper
measurements:

| Item | Modelled interface or envelope |
|---|---:|
| Propeller | Gemfan SBANG 4935, 124.46 mm swept diameter |
| Motor | T-Motor Velox V2207 V3, 27.5 mm diameter, 31.8 mm height, 16 x 16 mm M3 pattern |
| Flight controller | Matek F405-HDTE, 36 x 36 x 9 mm, 30.5 x 30.5 mm mounting |
| ESC | NewBeeDrone Hummingbird 305, 43 x 43 mm, 30.5 x 30.5 mm M3 mounting |
| Companion computer | Raspberry Pi Zero 2 W, 65 x 30 mm board envelope |
| Battery | Provisional 85 x 45 x 30 mm keep-out until the actual pack is available |

The ESC's plan dimensions and mounting pattern are published, but its maximum
assembled height is not. The model reserves 10 mm for the ESC plus separate
clearance between it and the flight controller. Solder joints, the XT60 lead,
motor wires, capacitor and connector bends still need a physical check.

## Starting geometry

| Parameter | v0.2 value |
|---|---:|
| True-X opposite-motor wheelbase | 220 mm |
| Adjacent propeller tip clearance | 31.1 mm nominal |
| Replaceable arm section | 18 x 8 mm, provisional |
| Motor pad | 34 mm diameter |
| Motor holes | 16 x 16 mm, 3.4 mm provisional printed holes |
| Centre plates | 78 x 70 mm |
| Lower / upper plate thickness | 4 / 3 mm, provisional |
| Electronics bay height | 32 mm |
| FC/ESC mounting | 30.5 x 30.5 mm, 3.4 mm provisional printed holes |

The 220 mm wheelbase is intentionally conservative. For a true-X layout its
adjacent motor spacing is about 155.6 mm, leaving about 31.1 mm between ideal
4.9-inch swept disks. The extra space helps accommodate printing tolerances,
propeller flex and the unusually large payload. It does not account for full
propeller guards; mandatory guards would require another layout revision.

The Pi and battery are currently shown as stacked keep-outs so their packaging
problem is visible. The supporting payload/battery tray is deliberately not
designed yet. It should be added only after the battery, regulator, camera
locations and competition guard rules are known.

## Software workflow

The repository uses code-based CAD, so the VS Code extension is **OCP CAD
Viewer**, accompanied by Microsoft's Python extension. `build123d` creates the
parts and `uv` manages the Python environment.

1. Open the repository in VS Code.
2. Install the Python and OCP CAD Viewer extensions.
3. Open the OCP CAD Viewer panel.
4. In the VS Code terminal run:

   ```bash
   uv sync
   uv run python -m cad.assembly --show
   ```

5. Change dimensions in `cad/parameters.py`; save and rerun the show command.
6. Run the geometry checks before exporting:

   ```bash
   uv run python -m unittest discover -s tests -v
   uv run python -m cad.assembly --export
   ```

The exported STL files are not ready for flight. When a printer is selected,
open them in that printer's supported slicer (for example OrcaSlicer,
PrusaSlicer or Cura) and create a printer/material profile there.

## Build order without all final information

1. **Packaging model now.** Model propeller disks, motors, the FC/ESC stack and
   conservative component keep-outs from published specifications.
2. **Mounting coupons after a printer is available.** Print only a 16 x 16 mm
   motor-hole coupon and a 30.5 x 30.5 mm stack-hole coupon. Adjust hole
   compensation and press/clearance fits in the slicer and CAD.
3. **One motor pad and one arm.** Fit a real motor with the correct screw
   length. Check that screws cannot touch the motor windings. Perform bending,
   twist and motor-pull-out tests away from people.
4. **Centre-chassis mock-up.** Print the plates cheaply and install the real
   grommets, FC and ESC with no battery and no propellers. Check USB access,
   solder-pad access, capacitor placement, cooling and every cable bend.
5. **Payload module.** After the battery, Pi regulator and camera arrangement
   are known, design a separate removable Pi/camera/battery tray instead of
   changing the motor and arm geometry.
6. **Full fit prototype.** Assemble the complete unpowered aircraft, verify its
   centre of gravity, weigh it and turn each propeller by hand to check the
   entire swept volume.
7. **Structural revision.** Choose the final material and printer, then revise
   arm section, fillets, layer orientation, perimeters and fastener interfaces.
   Repeat destructive tests on spare arms.
8. **Electrical and restrained tests.** Bring up the FC, receiver, ESC and
   motors with propellers removed. Only after failsafes, motor order/direction,
   power integrity and structure pass should controlled low-energy flight tests
   be considered.

## Information that can wait

- Printer model, nozzle and material are not needed for the packaging model.
- Exact ESC height and wire exits can wait until the centre-chassis mock-up.
- Battery, regulator and camera measurements can wait until the removable
  payload tray.
- Cosmetic shaping, ducts and guards should wait until the competition rules
  and mass budget are fixed.

## Gates before any flight print

- Measure every actual component and update its keep-out.
- Confirm the Matek-to-NewBeeDrone ESC signal pinout wire by wire; matching
  connector size and mounting pattern do not prove electrical compatibility.
- Confirm propeller-guard requirements.
- Set a take-off-mass target and thrust margin.
- Select and dry/test the final filament, calibrate the printer and record the
  slicer profile.
- Document arm load, impact and fastener-retention tests.

