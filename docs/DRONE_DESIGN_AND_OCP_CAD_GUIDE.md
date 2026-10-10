# Sub-£400 multi-challenge drone: design and OCP CAD guide

Status: concept brief v0.1  
Date: 15 August 2026  
Budget ceiling: **less than £400**

## 1. Executive recommendation

Do not choose or buy components until the competition rules in section 2 have been confirmed. Several missing details could change the correct aircraft substantially, especially what “50 cm³ cube” means, what is included in the £400, and how the visual reference points are provided.

Subject to those answers, the best starting concept is:

- a **4-inch X quadcopter**, approximately 170–200 mm motor-to-motor;
- a target all-up mass of **about 350–400 g**, including the competition battery and all autonomy hardware;
- a 4S electrical system, with battery capacity selected from measured hover current rather than guesswork;
- a flight controller with enough processing, flash, serial ports and supported firmware for non-GPS navigation—provisionally an H7-class board running ArduPilot;
- a separate, low-latency analogue FPV camera/video transmitter path;
- a downward optical-flow sensor plus rangefinder for short-term horizontal velocity and height;
- a calibrated navigation camera and lightweight companion computer for detecting the competition’s visual references and producing an absolute/local pose correction;
- one fixed competition configuration; any guards, sensors, propellers and battery selected for competition must remain fitted for every task.

This is a **provisional architecture, not yet a bill of materials**. A 4-inch platform is a compromise: more efficient than a very small racing quad, less intimidating indoors than a 5-inch quad, large enough to carry navigation hardware, and still agile enough for an FPV course.

The scoring rule rewards balance. Because the score is the sum of finishing positions, reliability in all three events is likely more valuable than a narrow Task 1 or Task 3 optimum that risks a did-not-finish in Task 2. We should design the fixed aircraft for completion first, then use software flight modes and control settings—not component swaps—to adapt its behaviour.

Confirmed after the first brief: the 50 × 50 × 50 cm volume is a practical stability test rather than a strict packaging exercise; no components may change between tasks; the £400 covers the complete system; any FPV brand is permitted; and detailed Task 2 perception choices are deferred while the main frame is designed.

## 2. Questions to settle with the organiser first

Record the answers in the repository before freezing the design.

| Question | Why it can change the design |
|---|---|
| What measurable drift or boundary excursion fails the 50 × 50 × 50 cm stability test? | The cube meaning is confirmed, but the allowed excursion and timing still set the position-control target. |
| In Task 1, must the whole aircraft stay inside the cube, or only its centre? | This sets the maximum propeller diameter and the required position accuracy. |
| Is Task 1 manual or autonomous, and what ends the timed run? | Manual hover, altitude hold and full position hold need different sensors and tuning. |
| What are the Task 1 boundary, contact and landing penalties? | Prop guards and conservative control margins may be essential. |
| Can software flight modes/settings change even though components cannot? | Hardware is fixed; confirming permitted software changes determines how hover and race behaviour may be tuned. |
| Must all tasks use one physical airframe and one firmware image? | This determines how modular the design and software must be. |
| How is existing workshop equipment costed within the all-inclusive £400 rule? | The complete system is included, but owned/borrowed workshop equipment may materially change the available aircraft budget. |
| Are second-hand, borrowed, sponsored or team-manufactured parts costed, and if so how? | This affects the real accounting limit. |
| For Task 2, what visual references are supplied: AprilTags, ArUco markers, coloured points, or natural features? | This determines the vision algorithm, lens and processor. |
| Are marker dimensions and world positions known in advance? | A known fiducial map allows direct pose estimation; unknown features may require SLAM. |
| What is the coordinate frame, axis direction, unit, tolerance, order and required dwell time? | “Hit a coordinate” is not implementable until these are defined. |
| Is offboard processing or an external tracking camera allowed? | An allowed laptop or motion-capture feed can remove considerable mass and complexity. |
| What happens when a marker is not visible? | The vehicle needs a permitted and testable lost-localisation behaviour. |
| For Task 3, what are the smallest gate, course length and expected top speed? | These set aircraft span, camera angle, battery and motor/propeller requirements. |
| Which FPV bands, channels and output powers are allowed? | Any brand is allowed, but frequency compatibility, event power and interference rules still matter. |
| Are propeller guards mandatory? | Guards materially affect mass, drag, tuning and frame geometry. |
| What safety features, pilot override, arming method and failsafes are mandatory? | These must be part of the architecture, not added at the end. |
| How are a DNF, tie or penalty scored? | This determines how strongly the design should favour robustness over peak performance. |

The cube interpretation, fixed hardware configuration and all-inclusive budget are now confirmed. Remaining rule questions include the exact stability metric, software changes between tasks, Task 2 reference system, guard requirements and how workshop-owned equipment is costed.

## 3. What parameters matter when designing the drone?

The parameters form a coupled system. Changing propeller size, for example, changes the frame, motors, current, battery, endurance, guards and control tuning. We should maintain a single calculation sheet and a parametric CAD model rather than selecting each part independently.

### 3.1 Competition and mission parameters

- Maximum aircraft envelope and mass.
- Hover volume, required duration and boundary tolerance.
- Coordinate course extent, waypoint tolerance, dwell time and maximum time.
- Marker type, size, positions, lighting, viewing distance and allowed computing location.
- Race gate size, course length, collision likelihood and video rules.
- Fixed hardware configuration and any permitted software-mode changes between tasks.
- Cost-accounting rules and replacement/spare policy.

These are the top-level requirements. Every component should trace back to at least one of them.

### 3.2 Geometry, mass and balance

Track the following explicitly:

- motor-to-motor wheelbase;
- overall span including propellers and guards;
- propeller diameter, pitch, blade count and clearance;
- all-up mass (AUW) in the exact configuration for each task;
- centre of gravity in X, Y and Z;
- distance of heavy items from the centre, because this affects rotational inertia;
- camera fields of view and anything that obscures them;
- rangefinder clear cone, propeller wash and ground clearance;
- access to USB, SD card, battery strap, connectors and fasteners;
- antenna separation from carbon fibre, high-current wiring and the video transmitter.

Keep the battery and companion computer close to the centre. The centre of gravity should be close to the geometric centre of the four motors and on the flight controller’s vertical axis. A low moment of inertia improves racing response; a symmetric, rigid layout makes position control easier to tune.

### 3.3 Propulsion

For every candidate motor/propeller/battery combination, obtain manufacturer or independent thrust-stand data at the intended voltage. Record:

- maximum thrust per motor;
- thrust and electrical power near the expected hover point;
- current at full throttle;
- motor and ESC temperature;
- propeller efficiency and noise;
- voltage sag with the chosen battery.

Use the following first-pass checks:

\[
\text{thrust-to-weight ratio} = \frac{4T_{\max}}{m g}
\]

When thrust is given in grams-force and mass in grams, the ratio is simply `4 × motor thrust / AUW`. Target at least **2.5:1 in the heaviest configuration** as an initial compromise, then validate. More margin helps the race and recovery from disturbances, but oversized motors add mass and can operate inefficiently in hover.

\[
\text{disk loading} = \frac{m g}{4\pi(D/2)^2}
\]

Lower disk loading generally helps hover efficiency, which favours larger, slower propellers. Racing response favours lower inertia and more power. The preliminary 4-inch choice is the compromise to test.

The ESC must support the battery voltage, firmware/protocol and motor peak current. As a screening rule, give each ESC channel at least **20% current margin** over the measured or published peak for the exact motor/propeller combination. This is not a substitute for temperature and current testing.

### 3.4 Battery and hover duration

Track battery nominal voltage, capacity, mass, continuous current capability, connector, internal resistance and safe usable fraction. Estimate duration from measured hover current:

\[
t_{\text{hover, min}} \approx 60\frac{C_{\text{Ah}}\,f_{\text{usable}}}{I_{\text{hover, A}}}
\]

Use `f_usable = 0.8` for early planning, then replace it with a safe value justified by battery logs and the competition end condition. Example: a 0.85 Ah pack at 6 A average hover current gives about `60 × 0.85 × 0.8 / 6 = 6.8 minutes` before reserve. This example is not a prediction for the final vehicle.

Energy in watt-hours is:

\[
E_{\text{Wh}} = V_{\text{nominal}} C_{\text{Ah}}
\]

Compare battery candidates during development by **measured safe hover time per gram**, not capacity alone. A larger battery initially adds duration, but eventually its extra weight costs too much hover power. The selected competition battery then remains fixed for all tasks.

### 3.5 Structure and materials

- Use a bought carbon-fibre plate frame or equivalent proven stiff frame for the load path; do not begin with 3D-printed structural arms.
- Use printed parts for sensor brackets, camera mounts, antenna supports, guards and wire management.
- Design sacrificial, replaceable guards and mounts so a race impact does not destroy navigation hardware.
- Check arm bending, motor screw engagement, propeller clearance, fastener locking and landing impact paths.
- Isolate vibration-sensitive cameras where necessary, but mount the flight controller according to its manufacturer’s guidance and avoid a flexible stack that can resonate.
- Keep hot devices—especially the video transmitter and voltage regulators—ventilated.

### 3.6 Flight controller, firmware and control

The flight controller must have:

- a supported processor and enough flash for the selected firmware and non-GPS features;
- enough UART/I²C/CAN connections for receiver, FPV/OSD, optical flow, rangefinder and companion computer;
- a barometer, IMU and logging storage;
- current and voltage sensing;
- spare processing margin and accessible debugging/programming ports.

For a single aircraft covering all tasks, the provisional baseline is **ArduPilot on an H7-class controller**. ArduPilot supports autonomous modes and an Acro mode intended for smooth, fast FPV control; it also documents non-GPS navigation and companion-computer commands. Its official non-GPS guide warns that low-cost autopilot IMUs alone drift too quickly for position estimation, so an external velocity or position source is required ([ArduPilot non-GPS navigation](https://ardupilot.org/copter/docs/common-non-gps-navigation-landing-page.html), [ArduPilot Acro mode](https://ardupilot.org/copter/docs/acro-mode.html), [Guided-mode local coordinates](https://ardupilot.org/dev/docs/copter-commands-in-guided-mode.html)).

PX4 is a reasonable alternative if the team already knows ROS 2. Its documented Offboard mode accepts external position/velocity/attitude setpoints but requires a valid estimate and a continuous proof-of-life stream; loss behaviour must be configured and tested ([PX4 Offboard mode](https://docs.px4.io/main/en/flight_modes/offboard)). Betaflight is attractive for pure racing, but it should not be the default for this combined aircraft because Task 2 is an autonomy and state-estimation problem.

Whichever firmware is selected, tune and validate the inner attitude/rate controller before tuning trajectory speed or waypoint behaviour. Do not try to hide vibration or poor tracking by changing high-level trajectory limits.

### 3.7 Indoor localisation and autonomy

The autonomous system must know at least `(x, y, z, yaw)` in the competition’s coordinate frame. The flight-controller IMU provides fast attitude and angular-rate information, but cannot provide a stable indoor position by itself.

A practical sensor fusion stack is:

- flight-controller IMU: attitude and fast motion;
- downward optical flow: horizontal velocity relative to the floor;
- downward rangefinder: height and the scale needed by optical flow;
- visual markers: absolute or drift-correcting pose in the course frame;
- optional magnetometer only after testing the venue for indoor magnetic interference.

PX4’s official optical-flow guide likewise specifies a downward-looking camera and a downward distance sensor, preferably LiDAR ([PX4 optical flow](https://docs.px4.io/main/en/sensor/optical_flow)). Barometric height alone is weak indoors: doors and ventilation can alter room pressure, so ArduPilot recommends a downward sonar or LiDAR for indoor altitude assistance ([ArduPilot indoor flying](https://ardupilot.org/copter/docs/indoor-flying.html)).

If the reference points are fiducials, AprilTag is a strong first candidate. Its official implementation supports tag identification and pose estimation from the known tag size and calibrated camera intrinsics ([AprilTag 3](https://github.com/AprilRobotics/apriltag)). This is only a recommendation until the organiser confirms the marker system.

The proposed data path is:

```text
navigation camera -> companion computer -> filtered pose/odometry -> flight controller
                                                 ^                       |
downward optical flow + rangefinder -------------+                       v
                                                                  ESCs -> motors

FPV camera -> video transmitter -> pilot goggles       (independent video path)
RC receiver ---------------------> flight controller    (override/mode/kill path)
```

The companion computer should **not** command motor outputs directly. It should estimate pose and request bounded position/velocity targets; the flight controller remains responsible for estimation fusion, stabilization, motor mixing and failsafes.

The vision implementation must include:

- camera intrinsic calibration;
- a measured rigid transform between camera and vehicle body;
- an unambiguous transformation between marker, camera, body and competition frames;
- timestamping and measured end-to-end latency;
- pose-quality checks and rejection of implausible jumps;
- a defined response to marker loss, stale data, companion-computer reset and serial-link loss;
- logs of raw detections, fused position, target, tracking error, battery and control output.

Coordinate conventions need special attention. CAD will normally use millimetres and Z-up. ArduPilot local targets commonly use metres in NED (X north, Y east, Z down), while many robotics libraries use ENU/Z-up and camera libraries commonly use X-right, Y-down, Z-forward. Convert at one named boundary, unit-test it, and never scatter sign changes through the control code.

### 3.8 FPV and radio links

- Keep the FPV video chain independent of autonomy so vision software failure does not remove the pilot’s view.
- A low-cost analogue system is the provisional choice because it is light, low latency and leaves budget for localisation. Confirm event compatibility before purchase.
- Choose the FPV camera angle as a compromise or make it repeatably adjustable; level or shallow angles help slow indoor flight, while a steeper angle helps racing.
- Ensure the control receiver has a tested failsafe and a dedicated, reachable arm/kill function.
- Verify video range and interference with all teams operating, not just on an empty bench.
- Record radio, VTX and telemetry frequencies and legal/event power limits.

### 3.9 Reliability, safety and maintainability

Design for:

- pre-arm validation of the position estimate in autonomous modes;
- low-battery and radio-loss actions appropriate to the indoor venue;
- companion-link loss detection and a bounded fallback such as hover briefly then land, subject to the rules and available position estimate;
- physical access to disconnect the battery quickly;
- correctly insulated power wiring, strain relief and a smoke-stopper for first power-up;
- charging, transporting and storing LiPo batteries exactly as the battery/charger manufacturers require, in a suitable fire-safe area and never unattended while charging;
- props-off setup, firmware, receiver, sensor and motor-direction tests;
- guarded flight testing in a controlled area with a spotter and no uninvolved people nearby;
- easy replacement of arms, motors, props, guards and antennas;
- configuration backups and a repeatable pre-flight checklist.

ArduPilot explicitly warns against relying on indoor GPS because reflections can produce a plausible but badly wrong location. It also recommends configuring battery/radio failsafes and using a downward range sensor where available ([indoor flying guidance](https://ardupilot.org/copter/docs/indoor-flying.html)). Treat any autonomous propeller test as hazardous; software confidence does not make spinning props safe.

## 4. How the three tasks pull the design in different directions

| Task | Favours | Conflicts created | Proposed response |
|---|---|---|---|
| 1. Hover duration in a 50 cm cube | low mass, large efficient propellers, high specific-energy battery, excellent position hold | large battery reduces agility; large props reduce clearance; turbulent recirculation may disturb a small volume | select one balanced battery/propeller set during development, optical flow + range, conservative position limits |
| 2. Autonomous 3D coordinates | reliable absolute/local pose, low latency, stable hover, computing and sensor redundancy | compute and cameras add mass/power; aggressive motion blurs images | flight controller handles stabilization, companion handles markers, quality-gated pose fusion, jerk/acceleration limits |
| 3. FPV race | high thrust-to-weight, low inertia, durable frame, low-latency video, pilot-friendly rates | high-pitch props and large motors hurt hover endurance; steep camera angle hurts precision | fixed hardware with a race flight mode, conservative fixed camera angle and extensive pilot practice |

Build the aircraft to survive and finish all three. Optimise software modes only after the fixed hardware configuration is stable.

## 5. Preliminary target values and calculations

These are starting hypotheses to test, not final specifications.

| Parameter | Preliminary target |
|---|---:|
| Layout | 4-inch X quad |
| Wheelbase | 170–200 mm |
| Maximum overall span | derive from confirmed cube boundary with at least 50 mm control margin per side |
| AUW with autonomy and Task 1 battery | 350–400 g |
| Loaded maximum thrust-to-weight | ≥ 2.5:1 initially |
| Nominal battery | 4S; capacity selected after hover-current tests |
| Hover position error | target well below half the allowed boundary margin; final value from rules |
| Waypoint error and dwell | derive from Task 2 tolerance and scoring |
| Budget target | £390 internal hard stop for the complete system |

An initial mass budget is:

| Subsystem | Target mass |
|---|---:|
| Frame, guards and hardware | 55 g |
| Four motors and propellers | 65 g |
| Flight controller, ESC and power wiring | 30 g |
| Competition battery | 90–110 g |
| FPV, receiver and antennas | 25 g |
| Optical flow and rangefinder | 15–25 g |
| Companion computer, navigation camera and regulator | 40–55 g |
| Mounts, wiring and contingency | 30 g |
| **Indicative total** | **350–395 g** |

The mass sheet must contain actual measured masses before CAD packaging is frozen. Vendor figures are useful for screening but the assembled wiring, solder and fasteners are often forgotten.

## 6. Budget framework

Prices and availability change, so this is an allocation rather than a shopping list. The budget now includes the aircraft and required ground equipment. Record delivered price including VAT and mandatory accessories; inventory workshop-owned equipment before relying on any zero-cost assumption.

| Category | Working allocation |
|---|---:|
| Frame, guards, printed parts and hardware | £30 |
| Motors, propellers and racing spares | £45 |
| Flight controller, 4-in-1 ESC and power sensing | £55 |
| RC receiver/required telemetry | £15 |
| FPV camera, VTX and antenna | £25 |
| Deferred navigation sensors/compute allowance | £40 |
| Batteries, connectors and straps | £35 |
| Radio transmitter | £55 |
| FPV goggles/receiver | £45 |
| Charger and battery-safety accessories | £30 |
| Wire, fasteners and miscellaneous fabrication | £10 |
| Project contingency | £5 |
| **Internal complete-system maximum** | **£390** |

The £390 internal stop leaves £10 below the strict “less than £400” rule for rounding, price movement or an item initially missed from the organiser's cost definition. This allocation is tight, especially the deferred navigation allowance, and must be rebuilt from current delivered prices after the workshop inventory is known. Existing compatible transmitter, goggles or charger equipment would release budget for the aircraft, but only if the competition costing rules permit it.

Maintain a BOM with: part, purpose, quantity, unit mass, total mass, unit delivered price, total price, supplier, date quoted, voltage/current compatibility, firmware support, CAD envelope source and purchase status.

## 7. Verification plan

Progress through gates. Do not combine unproven propulsion, controls and vision in the first flight.

1. **Rules gate:** competition assumptions are answered and measurable requirements are written down.
2. **Calculation gate:** mass, thrust, full-current, ESC, connector and predicted hover-duration margins pass on paper.
3. **CAD gate:** propeller envelopes, camera/rangefinder views, centre of gravity, connectors, fasteners and guards are checked.
4. **Bench gate—props removed:** power rails, sensor directions, receiver, kill switch, motor order, logging, companion timeout and all coordinate transforms pass.
5. **Propulsion gate:** restrained thrust-stand or other safe test provides current, thrust and temperature data for the exact propeller and battery.
6. **Manual flight gate:** simulator practice comes first; then guarded line-of-sight hover, attitude tuning and failsafes pass before FPV or autonomy.
7. **Task 1 gate:** repeated timed hover tests provide mean duration, variance, boundary excursions, remaining capacity and temperatures.
8. **Vision gate:** recorded and live video tests establish detection range, frame rate, latency, pose noise and behaviour under blur, glare, partial occlusion and marker loss.
9. **Autonomy gate:** position hold precedes one slow waypoint; only then increase to the full sequence and competition speeds.
10. **Race gate:** pilot training begins slowly with the final FPV installation, then increases rates and course speed while monitoring current and motor temperature.
11. **Full rehearsal:** run the tasks in competition order, with the real turnaround time, battery procedure and interference from other radios/video links.

For every flight, save firmware version, parameter file, software commit, configuration, battery ID, propeller, AUW, weather/venue conditions and logs. Change one important variable at a time.

## 8. How OCP CAD Viewer fits into the project

OCP CAD Viewer is the **viewer and VS Code integration**, not the modelling language. We write the parametric model in Python using build123d or CadQuery; `ocp_vscode` sends the resulting solids and assemblies to the viewer. The Python source is the design master.

It is useful for geometry, packaging, clearances, assemblies, sections and measurements. It does not predict motor thrust, propeller efficiency, flight time, control stability or structural strength by itself; those need calculations, test data and, where justified, separate analysis tools.

The recommended starting library is **build123d** because its explicit Python objects and assembly-oriented workflow fit this project well. CadQuery is also fully supported, and changing this choice does not require changing the viewer. The official OCP CAD Viewer README shows both libraries and documents VS Code execution, visual debugging, measurements, object selection, clipping and standalone mode ([OCP CAD Viewer README](https://github.com/bernhard-42/vscode-ocp-cad-viewer/blob/main/README.md)). The build123d documentation also supports displaying objects with `show(...)` and exporting printable STL or exchange STEP files ([build123d introductory examples](https://build123d.readthedocs.io/en/stable/introductory_examples.html)).

### 8.1 Installation model

As of this brief, the official OCP CAD Viewer instructions require VS Code 1.85 or newer, the Microsoft Python extension, and a Python environment with `python` plus `pip` or `uv`. The extension’s **Quickstart build123d** action can install the required Python packages, or we can manage a repository-local virtual environment ourselves.

For this workspace, which is under WSL (`/mnt/d/droneclub`), keep all three pieces in the same context:

1. open the folder using VS Code’s WSL/remote environment;
2. install/enable OCP CAD Viewer and the Python extension in that remote context;
3. create a project virtual environment inside the repository;
4. select that exact interpreter in VS Code;
5. install `build123d` and `ocp-vscode` into that interpreter.

A planned terminal setup is:

```bash
cd /mnt/d/droneclub
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install build123d ocp-vscode
```

We should execute this together in the next phase because it downloads packages and because the correct Python interpreter depends on how VS Code is connected.

Alternatively, install the **OCP CAD Viewer** extension from the VS Code Marketplace, open its sidebar and select **Quickstart build123d**. Do not mix Quickstart and a different interpreter without checking which environment received the packages.

### 8.2 The smallest interface test

Create a Python file containing:

```python
from build123d import Box
from ocp_vscode import show

test_block = Box(10, 20, 30)
show(test_block)
```

Open the OCP CAD Viewer sidebar and start the viewer if it is not already running. Then use **Run > Run Without Debugging** (`Ctrl+F5`) or start the Python debugger with `F5`. Importing `ocp_vscode` matches the extension’s default autostart trigger. Each `show(...)` call sends the object to the running viewer.

The normal loop is:

```text
edit Python parameters/geometry -> run file -> inspect/measure in viewer
        -> adjust design -> run again -> export STEP/STL when reviewed
```

The viewer lets us rotate, isolate, hide, clip and measure objects. Those are inspection operations; dimension changes belong in the Python parameters.

### 8.3 Troubleshooting the interface

- `ModuleNotFoundError` almost always means VS Code is running a different Python interpreter from the one containing `ocp-vscode`/`build123d`.
- If the viewer does not start, ensure the file imports `ocp_vscode`, open the OCP sidebar and start the viewer from Viewer Manager.
- If more than one viewer is running, `show()` may ask for a port; close extras or select/set the desired port.
- Under WSL/Remote VS Code, do not install the Python packages in Windows and run the script in Linux, or vice versa.
- Test settings with a small model like the block above. The official README warns that its logo/demo can override settings for consistent presentation.
- Prefer `python -m pip ...` over a bare `pip ...` so the installer is visibly tied to the selected Python.

### 8.4 How we will work with it together

I will edit the parametric Python files in this shared repository, add checks and generate intentional exports. You will open the same folder in VS Code, run the current assembly file and inspect it in OCP CAD Viewer. We can then iterate from measurements, screenshots and design decisions. The viewer is a display endpoint; changes remain reviewable in the Python source instead of being hidden in a binary CAD file.

## 9. How we should model the drone

Model **interfaces and keep-out envelopes first**, not decorative detail.

Use millimetres in CAD and define one vehicle coordinate system:

- origin: centre of the motor square at the nominal thrust plane;
- +X: forward;
- +Y: right;
- +Z: up.

Create named parameters for:

- wheelbase and motor coordinates;
- propeller diameter, thickness envelope and safety clearance;
- frame-plate dimensions and thicknesses;
- stack-hole pattern and keep-out height;
- motor mounting pattern and screw depth;
- battery envelope and centre of mass;
- camera position, pitch and field-of-view cone;
- optical-flow and rangefinder view cones;
- companion-computer, receiver, VTX and antenna envelopes;
- guard thickness, clearance and mounting points;
- fastener sizes and print tolerances.

Represent bought electronics initially as simple labelled boxes/cylinders with accurate mounting holes and connector keep-outs. Detailed STEP files can be imported later when trustworthy manufacturer geometry is available. Model propellers as translucent swept-disk keep-outs; no solid part may enter these disks under tolerances or arm flex.

A suitable repository layout for the next phase is:

```text
cad/
  parameters.py        # all dimensions and design variants
  components.py        # simplified bought-part envelopes
  frame.py             # frame plates/arms
  mounts.py            # printable sensor/camera/antenna parts
  assembly.py          # complete vehicle and task configurations
  exports/             # generated STEP/STL files, when intentionally exported
docs/
  DRONE_DESIGN_AND_OCP_CAD_GUIDE.md
  decisions/            # short design-decision records
data/
  bom.csv
  mass_budget.csv
  test_log.csv
```

The first CAD review should answer six questions:

1. Does the complete aircraft, including guards, fit the confirmed competition envelope with control margin?
2. Are the propeller disks clear in every configuration?
3. Can every camera and range sensor see its required scene without frame/propeller obstruction?
4. Is the predicted centre of gravity close to the motor-square centre?
5. Can we assemble, wire, cool, inspect and repair it without dismantling the whole vehicle?
6. Can every printed item be produced in a strong orientation with realistic tolerance and fasteners?

## 10. Recommended next working session

1. Obtain or paste the complete competition rules and answer section 2.
2. Inventory workshop equipment and confirm how owned items are costed inside the £400.
3. Set up the VS Code/WSL Python environment and run the OCP smoke-test block.
4. Create the parametric 4-inch envelope model: motor locations, propeller disks, cube, frame plates and provisional component boxes.
5. Create the BOM and mass-budget files with candidate—not purchased—parts.
6. Use published thrust tables to compare two or three motor/propeller/battery combinations.
7. Freeze the flight-controller/firmware choice only after its ports, sensor support and autonomy interface are checked.

The first design milestone is not a photorealistic aircraft. It is a measurable envelope model and a mass/power/budget calculation that proves the concept can plausibly complete all three tasks.

## 11. Short glossary

- **4S:** four lithium-polymer cells in series; nominally about 14.8 V and 16.8 V when fully charged.
- **AUW:** all-up weight/mass—the complete ready-to-fly aircraft, including battery.
- **Companion computer:** a small onboard computer that runs vision or high-level navigation alongside the flight controller.
- **ESC:** electronic speed controller; converts flight-controller commands into three-phase power for a brushless motor. A 4-in-1 ESC contains four channels.
- **EKF:** extended Kalman filter; the estimator that combines IMU and other sensor data into position, velocity and attitude estimates.
- **FC:** flight controller; the real-time autopilot board responsible for stabilisation and motor commands.
- **FPV:** first-person view; the pilot flies using a live onboard-camera image.
- **LiPo:** lithium-polymer flight battery; capable of very high current and requiring correct charging, handling and storage.
- **Optical flow:** image motion from a downward camera, used with height information to estimate horizontal velocity.
- **Rangefinder:** a downward distance sensor, commonly LiDAR or sonar, used to measure height above the floor.
- **UART / I²C / CAN:** common electrical/data interfaces used to connect receivers, sensors and companion computers.
- **VIO:** visual-inertial odometry; camera motion estimation combined with inertial measurements to estimate 3D pose and velocity.
- **VTX:** video transmitter that sends the FPV camera image to the pilot’s receiver/goggles.

## 12. Primary references

- [OCP CAD Viewer for VS Code—official repository and usage](https://github.com/bernhard-42/vscode-ocp-cad-viewer/blob/main/README.md)
- [build123d documentation—introductory examples, viewing and export](https://build123d.readthedocs.io/en/stable/introductory_examples.html)
- [ArduPilot—indoor flying guidance](https://ardupilot.org/copter/docs/indoor-flying.html)
- [ArduPilot—non-GPS navigation](https://ardupilot.org/copter/docs/common-non-gps-navigation-landing-page.html)
- [ArduPilot—Copter commands in Guided mode](https://ardupilot.org/dev/docs/copter-commands-in-guided-mode.html)
- [ArduPilot—Acro mode](https://ardupilot.org/copter/docs/acro-mode.html)
- [PX4—optical flow](https://docs.px4.io/main/en/sensor/optical_flow)
- [PX4—visual-inertial odometry](https://docs.px4.io/main/en/computer_vision/visual_inertial_odometry)
- [PX4—Offboard mode](https://docs.px4.io/main/en/flight_modes/offboard)
- [AprilTag 3—official implementation and pose-estimation notes](https://github.com/AprilRobotics/apriltag)
