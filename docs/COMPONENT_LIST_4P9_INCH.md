# 4.9-inch competition drone — revised component list

Last reviewed: 12 September 2026  
Design basis: 4.9-inch (124.46 mm) tri-blade props, 4S power, indoor FPV and autonomous flight

## Decision summary

This is a coherent **5-inch-class, 4S build**, subject to the verification tests near the end of this document. The original 1404 motors and anonymous 4-in-1 ESC must not be used with the 4.9-inch props. The Raspberry Pi Zero 2 W, 4S 1300 mAh battery and Gemfan 4935 props can remain.

The two cameras have different jobs and both are required:

- The RunCam and analogue VTX provide the pilot's low-latency FPV view.
- The Raspberry Pi Camera Module 3 Wide provides images to the autonomy software.

Prices below are snapshots or planning allowances, include VAT where the linked seller states that, and exclude delivery. Re-check price, stock and the competition rules before ordering.

## A. Airborne bill of materials

| # | Component | Qty | Selected part / required specification | Approx. line cost | Decision and compatibility notes |
|---:|---|---:|---|---:|---|
| 1 | Flight controller | 1 | [Holybro Kakute H7 Mini v1.5](https://www.3dxr.co.uk/products/holybro-kakute-h7-mini-v1-5) | £58.99 | H743, barometer, analogue OSD, 6 UARTs, 2–6S input and ArduPilot support. 20 × 20 mm M2 mounting. Use the current ArduPilot Kakute H7 target after confirming the v1.5 board revision. |
| 2 | 4-in-1 ESC | 1 | [ZEEZ 55A 4-in-1 BLHeli32 ESC V3](https://www.flyingtech.co.uk/product/zeez-55a-4-in-1-blheli32-3030-esc-v3/) | £59.90 | 3–6S, 55 A continuous per motor, DShot and current sensing. 30.5 × 30.5 mm mounting. It includes an XT60/12 AWG lead and two 470 µF 35 V capacitors. **Verify every FC/ESC harness pin before applying power; do not assume the plugs share a pinout.** |
| 3 | Motors | 4 | [T-Motor Velox V2207 V3 2550KV](https://www.hobbyrc.co.uk/t-motor-v2207-v3-2550kv-motor) | £51.60 | A 2207 motor intended for 5-inch 4S builds, with a 5 mm prop shaft and 16 × 16 mm M3 mounting. This replaces all four 1404/3750KV motors. A fifth motor is a useful competition spare but is not required to assemble one aircraft. |
| 4 | Propellers | 3 packs | [Gemfan SBANG 4935-3](https://yourfpv.co.uk/product/gemfan-sbang-4935-3-4-9-3-blade-freestyle-propellers/) | £7.17 | Keep the selected props. Each pack has 2 CW and 2 CCW props; one pack flies and two are spares. Diameter 124.46 mm, 3.5-inch pitch and 5 mm centre hole. Never fit props during electronics setup. |
| 5 | Flight battery | 2 | [DOGCOM 1300 mAh 4S 14.8 V XT60](https://yourfpv.co.uk/product/dogcom-1300mah-4s-14-8v-150c-lipo-battery-xt60/) | £37.80 | Keep this selection. One battery is fitted and the second is an identical spare/training pack. Listed size is about 77 × 39 × 23 mm and 152 g. Treat the advertised C rating as marketing, not as proof of safe sustained current. |
| 6 | ESC input capacitor | 1 fitted | One of the supplied 470 µF, 35 V low-ESR capacitors | included | Solder it directly across the ESC battery pads with the shortest practical leads and correct polarity. Keep the second as a spare. |
| 7 | Companion computer | 1 | [Raspberry Pi Zero 2 W, no headers](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) | ~£14.38 | Keep. Use only for high-level perception/navigation. The flight controller retains attitude control, arming and failsafes. Solder only the required power and UART wires. Disable Wi-Fi/Bluetooth during flight if they are not required, reducing 2.4 GHz interference and load. |
| 8 | Pi storage | 1 | Reputable 32 GB A1/A2 microSD, e.g. [Raspberry Pi 32 GB card](https://www.aliexpress.com/item/1005012337269274.html?isdl=y&aff_fsk=_ol8w4bv&src=SalesoarUKgeneral&aff_platform=aff_feeds&aff_short_key=_ol8w4bv&pdp_npi=4%40dis!GBP!3.84!3.84!!!!!%40!12000058137552304!afff!!!&dp=Cj0KCQjw8JPVBhD-ARIsAO691sFEc0nrgRRdFVv3mknD2GVfi9Tx_5PNz0saC_ux6ZNSOaC4rVJiC8waAoUDEALw_wcB|0AAAAA_4-1Lk3Y6lYy0i3mrVv-XECXRZAh|Cj8KCQjwzY7VBhDpARIuACVAqzrtz_VZoMLvKOxRtbnk9whQOb0zJgbYbZv4WfSBcWOa0pm_Fuj0KVOBhRoCuHc|v1&cn=gb_a&gad_source=1) or SanDisk High Endurance | ~£8 | Replaces the unverified marketplace 256/512 GB card. Capacity beyond 32–64 GB is unnecessary; reliability matters more. |
| 9 | Navigation camera | 1 | [Raspberry Pi Camera Module 3 Wide](https://www.raspberrypi.com/products/camera-module-3/) | ~£35 | 120° diagonal field of view, CSI-2 connection. Use the visible-light Wide model unless the competition environment specifically calls for NoIR. Lock focus/exposure in software where practical and calibrate the installed camera intrinsics. |
| 10 | Pi Zero camera cable | 1 | 15-pin camera to 22-pin Pi Zero CSI cable | ~£3 | Required: the normal Camera Module 3 cable does not fit the Pi Zero connector. Select a short cable that reaches without folding sharply. |
| 11 | Dedicated Pi regulator | 1 | [Pololu D24V50F5 5 V, 5 A step-down regulator](https://www.pololu.com/product/2851) | ~£30 | Replaces the unknown BEC. Accepts the 4S battery voltage and gives ample regulated 5 V capacity. Follow the manufacturer's capacitor/layout guidance, fuse the branch if practical, load-test it, and verify 5.0 V before connecting the Pi. Do not power the Pi from the FC's 5 V rail. |
| 12 | Indoor velocity/height sensor | 1 | [Matek 3901-L0X optical-flow/LiDAR module](https://www.3dxr.co.uk/products/matek-systems-optical-flow-lidar-sensor-3901-l0x) | £29.90 | Adds downward optical flow and short-range height sensing for non-GPS hover. Connect to an FC UART using the documented ArduPilot protocol. Needs an unobstructed downward view, a textured floor, adequate light and suitable ground clearance. |
| 13 | RC receiver | 1 | [RadioMaster RP1 V2 ExpressLRS 2.4 GHz receiver](https://www.hobbyrc.co.uk/radiomaster-rp1-elrs-receiver) | £18.99 | Use CRSF on a full FC UART (both RX and TX) for control and telemetry. Receiver and transmitter must use compatible ExpressLRS firmware and the same regulatory domain. Mount its antenna away from the Pi and carbon/conductive parts. |
| 14 | Pilot FPV camera | 1 | [RunCam Phoenix 2](https://www.hobbyrc.co.uk/runcam-phoenix-2-fpv-camera) | £26.35 | Independent, low-latency analogue camera. 19 × 19 mm mounting. Wire video through the FC's analogue OSD: camera video → FC CAM, FC VOUT → VTX video. |
| 15 | Video transmitter | 1 | [GEPRC RAD Tiny 5.8 GHz VTX](https://www.hobbyrc.co.uk/geprc-rad-tiny-58ghz-vtx) | £22.00 | 5 V input, U.FL antenna connector and IRC Tramp control. Start at the competition-approved channel and lowest permitted power; never power the VTX without an antenna. |
| 17 | Lost-model/independent buzzer | 1 | [VIFLY Finder 2](https://www.hobbyrc.co.uk/vifly) | £8.70 | Battery-backed audible locator and useful arming/status indication. Mount where its own battery cannot be punctured in a crash. |
| 18 | Printed frame and four prop guards | 1 set | Club-designed 4.9-inch frame, mounts and guards | ~£30 allowance | Design/fabrication item, not an off-the-shelf purchase. See the mechanical interface section. Include replaceable arms or sacrificial guard sections if the rules allow. |
| 19 | Installation hardware and consumables | 1 lot | M2/M3 stack hardware and soft mounts; correctly sized M3 motor screws; two battery straps and nonslip pad; silicone wire; heat-shrink; cable ties; solder; thread-lock for metal-to-metal fasteners | ~£25 allowance | Check motor screws cannot touch the windings. Do not use thread-lock on plastic. No loose wiring may reach a propeller. |

**Estimated airborne subtotal with two batteries and three prop packs: about £479.**  
With only one battery and one prop pack, it is still about **£456** before delivery. The frame and small-parts figures are estimates.

## B. Ground equipment and safety equipment

| # | Component | Qty | Selected part / required specification | Approx. line cost | Notes |
|---:|---|---:|---|---:|---|
| 20 | RC transmitter | 1 | [RadioMaster Pocket **ELRS** 2.4 GHz](https://www.hobbyrc.co.uk/radiomaster-pocket-transmitter-elrs-clear) | £71.49 | Buy the ELRS version, not the visually similar CC2500 version. Configure a latching arm switch, flight-mode switch, throttle cut and telemetry warnings. |
| 21 | Transmitter cells | 1 pair | [RadioMaster 3200 mAh 18650 cells](https://www.hobbyrc.co.uk/radiomaster-3200mah-18650-cells-2pcs) | £11.99 | The Pocket requires two cells; it can charge them through its charging USB-C port. |
| 22 | Analogue FPV goggles | 1 | [EV800D 5.8 GHz diversity goggles with DVR](https://yourfpv.co.uk/product/ev800d-5-8ghz-diversity-fpv/) | £104.99 | Compatible with the analogue 5.8 GHz VTX. Confirm that the received unit really has two receiver paths/diversity, and use RHCP receive antennas to match the aircraft. A shared club analogue monitor/goggle set can replace this purchase. |
| 23 | Balance charger | 1 | [SkyRC B6 Neo](https://shop.bristolbotbuilders.com/product/charger/) | £36.50 | Supports 4S LiPo balance charging. It requires a suitable USB-C PD supply or DC source; it is not a mains charger by itself. Charge this 1300 mAh pack at 1.3 A (1C) unless the actual battery label/manual specifies a lower rate. |
| 24 | Charger power supply | 1 | Reputable 65 W or greater USB-C PD mains supply and rated cable | ~£25 allowance | Omit if the club already owns a compatible supply. Alternatively buy a genuine mains-powered balance charger such as the [SkyRC iMAX B6AC V2](https://www.skyrc.com/Compact/iMAX_B6AC_V2_Charger?order=DESC&sort=pd.name) instead of rows 23–24. |
| 25 | Smoke stopper | 1 | [VIFLY ShortSaver 2](https://www.unmannedtechshop.co.uk/collections/battery-accessories) or equivalent XT60 resettable current limiter | ~£8.69 | Mandatory for initial power-up after soldering. It does not make prop-on testing safe. |
| 26 | LiPo safety bag | 1 | Fire-resistant LiPo charging/storage bag | ~£3.39 | Charge on a non-combustible surface, attended throughout. The bag is containment assistance, not a substitute for supervision. |
| 27 | Battery checker | 1 | 1–8S cell checker with per-cell voltage display | ~£7 allowance | Check cell balance before and after use. Store packs near 3.8 V per cell; retire swollen, punctured or badly imbalanced packs. |
| 28 | Workshop data cables | 1 lot | Data-capable USB-C cable for FC; USB OTG/power cable and microSD reader for Pi | ~£10 allowance | The original USB-to-UART adapter is not required for normal operation. Keep one only as an optional 3.3 V TTL bench tool. Never connect a 5 V UART signal to FC/Pi UART pins. |

**Estimated ground/safety subtotal: about £279.**  
**Estimated complete system total: about £758**, including the recommended spares and estimated printed parts/consumables, but excluding delivery and workshop tools.

## C. Parts from the original list: keep, replace or remove

| Original item | Decision | Reason |
|---|---|---|
| Matek F405-HDTE | Replace with Kakute H7 Mini | The Matek listing is a flight controller, not an FC+ESC stack. It could fly a quad, but its F405/1 MB target has much less margin for the planned ArduPilot non-GPS feature set. An H7 is the safer project choice. |
| Flywoo NIN 1404 V2 3750KV motors | Replace with four 2207 2550KV motors | 1404 motors are for much smaller props and cannot sensibly drive these 124.46 mm tri-blades or the expected payload. |
| DOGCOM 1300 mAh 4S XT60 battery | Keep | Correct voltage, connector and a normal capacity for a 4S 5-inch-class build. Validate flight time after the final all-up mass is known. |
| Gemfan SBANG 4935-3 props | Keep | Correct 4.9-inch size and 5 mm hub for the replacement motors. Buy spares. |
| Charger missing | Add B6 Neo + PD supply, or one genuine mains balance charger | A LiPo balance charger is essential. |
| Anonymous eBay 4-in-1 ESC | Replace with a documented 55 A ESC | Current capacity, firmware, current sensing, connector pinout and authenticity must be known. |
| Raspberry Pi Zero 2 W | Keep | Suitable as a modest companion computer, not as the safety-critical flight controller. |
| Anonymous Pi camera | Replace with Camera Module 3 Wide and the Pi Zero cable | Known interface, optics and software support; the special Pi Zero cable was missing. |
| Anonymous large-capacity microSD | Replace with a reputable 32 GB card | Reduces counterfeit/corruption risk; very large capacity is unnecessary. |
| USB-to-UART adapter | Move to optional workshop tools | Normal FC USB and the direct 3.3 V UART link are sufficient. |
| Unspecified RC transmitter/receiver | Replace with Pocket ELRS + RP1 V2 | Establishes a known matched control link with telemetry and failsafe support. |
| Unspecified 5 V BEC | Replace with documented Pololu regulator | The Pi needs a clean, load-tested 5 V rail independent of the FC peripherals. |

## D. Required system connections

```text
4S XT60 battery
 ├─> ZEEZ ESC ─> four motors
 │    ├─ motor signals/current sense ─> Kakute H7 Mini
 │    └─ supplied low-ESR capacitor across battery pads
 ├─> Kakute H7 Mini VBAT
 └─> Pololu 5 V regulator ─> Raspberry Pi Zero 2 W

RP1 ELRS receiver ─CRSF UART─> flight controller
Matek optical-flow/LiDAR ─UART─> flight controller
Pi Zero 2 W ─MAVLink UART─> flight controller
Camera Module 3 Wide ─CSI─> Pi Zero 2 W
RunCam Phoenix 2 ─video─> FC analogue OSD ─video─> RAD Tiny VTX ─> RHCP antenna
```

Grounds must be common where signals cross between power domains. Connect only 3.3 V UART signals between the Pi and FC; cross TX to RX and RX to TX. The companion computer may request position/velocity targets over MAVLink, but it must never drive ESC/motor signals directly.

Planned UART use is approximately four ports: ELRS/CRSF, optical flow, Pi/MAVLink and VTX control. That fits the selected FC, while leaving some margin. Confirm the final ArduPilot serial-port map before soldering.

## E. Interfaces the new 4.9-inch printed frame must support

The repository's current CAD is still documented around 101.6 mm props and 12 × 12 mm M2 motor holes. It is **not a validated frame for this BOM** and needs a separate revision before printing.

The replacement frame must provide:

- Clear 124.46 mm swept prop discs at every attitude and under guard/arm flex.
- Four 16 × 16 mm M3 motor patterns, with screw length matched to the printed arm thickness and motor base.
- A 20 × 20 mm M2 FC pattern and a 30.5 × 30.5 mm M3 ESC pattern. These can be on different vertical levels; leave connector and cooling access.
- Space for a 77 × 39 × 23 mm battery, two independent straps and a nonslip pad.
- A rigid, level, vibration-isolated FC position close to the centre of gravity.
- A downward, unobstructed optical-flow/LiDAR window with useful ground clearance.
- A rigid forward navigation-camera mount and a protected 19 × 19 mm FPV-camera mount.
- Protected mounts for the Pi, BEC, receiver/buzzer, VTX and antennas, with cooling and RF separation.
- Four guards designed from the actual 124.46 mm prop envelope. Choose radial clearance from measured print tolerance and deflection; a guard that can flex into a prop is unsafe.
- Access to USB, microSD, bind/boot controls, battery connector and status LEDs without removing the propellers.

Record the mass of every printed revision. A guarded printed frame may put the all-up mass roughly in the 550–700 g region; that is a planning estimate, not a validated result. Do not approve the frame on CAD geometry alone—perform material coupons, arm bending, motor pull-out, guard-deflection and drop/impact tests.

## F. Compatibility and purchase gates

Do not place the full order until all of these are answered:

1. **Budget definition:** the repository states a £400 complete-system limit. This BOM is about £758, and even the minimum one-battery/one-prop-pack aircraft is about £456. Ask whether shared transmitter, goggles, charger, safety equipment, batteries, consumables and printed material count. If everything counts, requirements or architecture must change before purchasing.
2. **Navigation reference:** optical flow plus short-range LiDAR improves indoor hover but does not by itself provide absolute X/Y/Z position around a course. Confirm whether the course permits visual markers (for example AprilTag/ArUco localisation through the Pi camera), external tracking, or another reference system. Do not buy a different positioning sensor until that rule is known.
3. **Competition rules:** confirm maximum dimensions, prop-guard construction, all-up mass, permitted radio/video bands and VTX power, autonomy boundaries, required pilot override and emergency-stop method.
4. **FC/ESC wiring:** obtain both pinout diagrams and write a pin-by-pin harness table for VBAT, ground, motor 1–4, current and telemetry. Continuity-test it before connection.
5. **Motor/prop/current test:** no exact manufacturer bench table was located for this precise motor/4935 combination. Test one motor with the real prop and 4S supply on a guarded thrust stand. Measure thrust, current, motor temperature and vibration; begin flight testing with a conservative throttle limit.
6. **Mass/thrust/power calculation:** weigh the finished aircraft, verify at least 2:1 measured total thrust-to-weight margin, and confirm the battery, XT60, wiring and ESC remain within measured current and temperature limits. Do not derive this only from advertised C ratings.
7. **Power-rail test:** load the Pi regulator with the Pi, camera and software running; verify 5 V stability and no Pi undervoltage events from a full 16.8 V pack down to the chosen landing voltage.
8. **Failsafes:** bench-test RC loss, Pi crash/disconnect, optical-flow loss, low battery, flight-controller reboot and manual takeover with props removed. The aircraft must disarm safely without the Pi.

## G. Bring-up order

1. Inspect and continuity-test all soldering.
2. First power-up through the smoke stopper, with no props and no Pi connected.
3. Verify FC orientation, receiver link, modes, arming logic, motor protocol/order/direction and current/voltage calibration.
4. Verify regulated 5 V under load, then connect the Pi and test MAVLink without granting it automatic control.
5. Configure and calibrate optical flow/rangefinder; test loss/fallback behaviour.
6. Verify analogue video, OSD, VTX channel/power and matched antenna polarisation.
7. Complete the single-motor thrust/current test, then a restrained four-motor test.
8. Fit balanced, undamaged props only at the flight site. Conduct a low hover under a conservative throttle cap, tune, then progressively add FPV and autonomy functions.

## H. Useful technical references

- [ArduPilot: Holybro Kakute H7 hardware](https://ardupilot.ardupilot.org/plane/docs/common-holybro-kakuteh7.html)
- [ArduPilot: non-GPS navigation overview](https://ardupilot.org/copter/docs/common-non-gps-navigation-landing-page.html)
- [Raspberry Pi Zero 2 W specifications](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/)
- [Raspberry Pi Camera Module 3 specifications](https://www.raspberrypi.com/products/camera-module-3/)
- [Pololu D24V50F5 regulator specifications](https://www.pololu.com/product/2851/specs)

