# Main drone frame — concept v0.1

Date: 15 August 2026  
Status: **parametric concept for review; do not manufacture yet**

## Confirmed design constraints

- Exactly four motors.
- One unchanged hardware configuration for hover, autonomy and FPV racing.
- The 50 × 50 × 50 cm volume expresses hover stability; it is not currently a hard airframe envelope.
- The complete system, including required ground equipment, must cost less than £400.
- Any FPV brand is allowed.
- The aircraft must be the team's own integrated design and safe to operate indoors under supervision.
- Task 2 perception details are deliberately deferred, but the frame must reserve an electronics bay for them.

## Selected starting geometry

The first model is a custom 4-inch true-X frame with four identical replaceable arms. The arms bolt beneath a lower electronics plate. Four standoffs support a top/battery plate, leaving a protected central bay for the existing PCB and later flight/autonomy electronics.

| Parameter | v0.1 value |
|---|---:|
| Opposite-motor wheelbase | 190.0 mm |
| Arm angles | 45°, 135°, 225°, 315° |
| Propeller envelope | 4 inch / 101.6 mm |
| Overall span including propeller disks | 236.0 × 236.0 mm |
| Adjacent propeller tip clearance | 32.8 mm |
| Provisional battery-to-propeller plan clearance | 4.7 mm |
| Replaceable arm | 14 mm wide × 4 mm thick |
| Motor pad | 28 mm diameter |
| Provisional motor holes | four M2 holes on a 12 × 12 mm square plus 8 mm centre hole |
| Lower/top plates | 76 × 68 × 1.5 mm, 8 mm corner radii |
| Electronics bay height | 20 mm |
| Frame hardware | M3 arm/standoff clearance holes |
| Provisional battery keep-out | 85 × 35 × 30 mm |
| Estimated carbon-only mass | 61.7 g |

The mass estimate uses 1.6 g/cm³ laminate density and excludes motors, fasteners, standoffs, wiring, printed mounts and guards. It must be replaced with supplier density and measured part masses before manufacture.

## Why the wheelbase became 190 mm

The first calculation used 180 mm. Rendering the conservative 85 × 35 mm battery envelope showed that its corners almost entered the 4-inch swept propeller disks in plan view. Increasing the wheelbase to 190 mm provides 4.7 mm nominal plan clearance, rather than relying on the battery being above the propeller plane. This adds little carbon mass and keeps the overall prop span at approximately 236 mm.

## PCB mechanical audit

The current [KiCad PCB](../designs/session4.kicad_pcb) contains:

- a 31 × 33 mm rectangular board outline;
- 1.6 mm board thickness;
- no mounting holes;
- four placed footprints: LED, capacitor, resistor and two-pin header;
- no placed ESP32 footprint.

The separate [ESP32 footprint](../designs/ESP32_30pin.kicad_mod) describes an approximately 28.3 × 51.5 mm module outline with four 3 mm holes on an approximately 23 × 46 mm pattern. It is physically longer than the current 31 × 33 mm PCB. The CAD therefore displays:

- the saved PCB outline in green; and
- the larger, unresolved ESP32/module keep-out in red.

These objects are packaging warnings, not a finished mount. The frame deliberately has no invented PCB mounting holes. The electrical and mechanical teams need to decide whether the ESP32 overhangs a carrier PCB, whether the board outline is unfinished, and where proper mounting holes/connectors belong.

## Frame construction represented by the model

1. Four identical 4 mm carbon-sheet arms sit at Z = 0–4 mm.
2. The 1.5 mm lower plate sits on the arms and retains each arm with two M3 bolts.
3. Four 20 mm standoffs create the electronics bay.
4. The 1.5 mm top plate includes two rounded 4 × 24 mm battery-strap slots.
5. The battery is mounted on top so the underside remains available for an optical-flow/range sensor.
6. Motor, propeller, PCB, ESP32 and battery shapes are keep-out envelopes, not purchased-component geometry.

This architecture makes a damaged arm individually replaceable and keeps all four arms identical, reducing spare-part cost and workshop setup.

## OCP CAD Viewer workflow

Open this repository in the same VS Code/WSL context that contains the `.venv`, then open the OCP CAD Viewer sidebar. Run:

```bash
uv sync
uv run python -m cad.assembly --show
```

The viewer object tree separates:

- four carbon arms;
- lower and top plates;
- four standoffs;
- four motor envelopes;
- four translucent propeller disks;
- current PCB outline;
- unresolved ESP32 keep-out;
- provisional battery envelope.

All primary dimensions are in [parameters.py](../cad/parameters.py). Geometry is built in [frame.py](../cad/frame.py); [assembly.py](../cad/assembly.py) handles the viewer and exports. Do not edit the generated STEP/STL files to change the design.

## Generated review files

- [Top review](../cad/exports/frame_top.png)
- [Isometric review](../cad/exports/frame_isometric.png)
- [STEP assembly](../cad/exports/frame_assembly.step)

The STL files are convenient geometry checks only. Flat carbon parts should eventually be produced from reviewed 2D profiles matched to the workshop's actual cutting process.

## Propeller guards

The note in the repository asks whether to buy or print the blade cage. Do not decide this independently of the frame and competition safety review:

- permanent full rings improve contact protection but add mass, drag and a large impact lever arm;
- printed rings can be repaired and customised but need stiffness and impact tests;
- motor-bolt-mounted guards require no extra arm holes, but their fasteners must not be too long for the motors;
- because the hardware cannot change between tasks, any guard must remain fitted for the race and hover test as well.

For v0.1 the propeller disks are modelled and the motor pads can accept a later motor-bolt-mounted guard. No guard is approved yet. We should first confirm whether guards are mandatory, choose the motors/propellers and measure the acceptable mass penalty.

## Checks currently passing

The automated geometry tests verify:

- exactly four arms, motors and propeller disks;
- adjacent propeller clearance;
- no plan overlap between the conservative battery box and propeller disks;
- ESP32 keep-out height fits inside the electronics bay;
- estimated carbon mass remains below the initial 65 g allocation;
- invalid overlapping-propeller parameter sets are rejected.

Run them with:

```bash
uv run python -m unittest discover -s tests -v
```

## Decisions required before v0.2

1. Exact motor model, body diameter, shaft/clip clearance and mounting-hole pattern.
2. Exact propeller model and whether guards are compulsory.
3. Exact fixed competition battery dimensions, mass, connector and strap width.
4. Workshop inventory: transmitter, goggles, charger, soldering equipment, carbon/G10 sheet, router/CNC/waterjet capability and fasteners.
5. Whether the workshop equipment is free to use under the competition's costing rules.
6. Final PCB/module outline, mounting holes, component height and connector/USB access.
7. Flight-controller/ESC packaging; the current ESP32 test PCB is not yet a complete multirotor flight-control/power system.
8. FPV camera size, tilt range and front impact protection.
9. Optical-flow/rangefinder underside position and unobstructed field of view.
10. Arm-joint strength, bolt head/nut clearance and whether the selected carbon thicknesses are available.

Only after these are known should we add detailed mounts, weight-reduction pockets, guard geometry and manufacturing drawings.
