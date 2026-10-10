"""Single source of truth for the 4.9-inch ballpark frame concept.

All CAD dimensions are millimetres.  The vehicle frame is X-forward,
Y-right and Z-up, with the origin at the centre of the motor square in the
arm lower surface.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, hypot, radians, sin, sqrt


@dataclass(frozen=True)
class FrameParameters:
    """Mechanical parameters for frame concept v0.4.

    Values that depend on a printer or final fit are deliberately conservative.
    They must be replaced after coupon prints and checks against the real parts.
    """

    # Propulsion envelope.  The wheelbase is the distance between opposite
    # motors; the four arm axes are at 45, 135, 225 and 315 degrees.
    wheelbase: float = 224.0
    propeller_diameter: float = 124.46  # Gemfan 4935, nominal 4.9 inches
    propeller_clearance_diameter: float = 127.0
    propeller_disk_thickness: float = 0.6
    # Explicit placeholder above the motor mounting face. This is NOT derived
    # from overall motor height and must be measured before flight validation.
    propeller_seating_height: float = 31.8
    propeller_seating_height_verified: bool = False

    # Four identical, replaceable printed arms.  These are starting dimensions,
    # not validated structural values.
    arm_inner_radius: float = 27.0
    arm_width: float = 18.0
    arm_thickness: float = 8.0
    motor_pad_diameter: float = 34.0
    motor_centre_hole_diameter: float = 10.0
    motor_mount_spacing: float = 16.0
    motor_mount_hole_diameter: float = 3.4  # provisional printed M3 clearance

    # Two M3 bolts attach each arm to the lower centre plate.
    arm_bolt_radii: tuple[float, float] = (33.0, 42.0)
    arm_bolt_hole_diameter: float = 3.4  # provisional printed M3 clearance
    fastener_envelope_diameter: float = 7.0  # screw head / washer / nut allowance
    fastener_envelope_height: float = 3.5
    fastener_tip_allowance: float = 1.0
    fastener_clearance: float = 1.0

    # Printed central plates.  X is length and Y is width.
    plate_length: float = 78.0
    plate_width: float = 70.0
    plate_corner_radius: float = 8.0
    lower_plate_thickness: float = 4.0
    top_plate_thickness: float = 3.0
    top_plate_length: float = 74.0
    top_plate_width: float = 66.0
    top_plate_corner_radius: float = 12.0

    # Four vertical standoffs leave an electronics bay between the plates.
    standoff_height: float = 36.0
    standoff_outer_diameter: float = 7.0
    standoff_hole_diameter: float = 3.4
    standoff_locations: tuple[tuple[float, float], ...] = (
        (32.0, 0.0),
        (-32.0, 0.0),
        (0.0, 28.0),
        (0.0, -28.0),
    )

    # Two transverse straps attach the battery to a separate supported tray.
    battery_slot_x: float = 18.0
    battery_slot_y: float = 24.0
    battery_slot_length: float = 22.0
    battery_slot_width: float = 3.0
    battery_strap_thickness: float = 1.0  # allowance for the run below the tray
    battery_tray_thickness: float = 3.0
    battery_tray_corner_radius: float = 10.0
    battery_tray_tab_diameter: float = 10.0
    battery_tray_support_height: float = 22.0
    battery_tray_support_diameter: float = 8.0
    battery_pad_thickness: float = 2.0  # nonprinted, compressible nonslip pad

    # Display-only envelopes.  They are deliberately conservative until
    # actual components have been chosen.
    motor_envelope_diameter: float = 27.5
    motor_envelope_height: float = 31.8
    battery_envelope_length: float = 85.0
    battery_envelope_width: float = 45.0
    battery_envelope_height: float = 30.0

    # Approximate printed-polymer density.  This is a solid-geometry comparison,
    # not a slicer mass prediction; walls and infill will change it materially.
    frame_material_density_g_per_mm3: float = 0.00115

    @property
    def motor_radius(self) -> float:
        return self.wheelbase / 2.0

    @property
    def arm_angles_deg(self) -> tuple[float, ...]:
        return (45.0, 135.0, 225.0, 315.0)

    @property
    def adjacent_motor_distance(self) -> float:
        return self.wheelbase / sqrt(2.0)

    @property
    def propeller_tip_clearance(self) -> float:
        return self.adjacent_motor_distance - self.propeller_clearance_diameter

    @property
    def nominal_propeller_tip_clearance(self) -> float:
        return self.adjacent_motor_distance - self.propeller_diameter

    @property
    def overall_propeller_span_x_y(self) -> float:
        motor_axis_offset = self.motor_radius / sqrt(2.0)
        return 2.0 * motor_axis_offset + self.propeller_diameter

    @property
    def overall_clearance_span_x_y(self) -> float:
        return self.adjacent_motor_distance + self.propeller_clearance_diameter

    @property
    def battery_to_propeller_plan_clearance(self) -> float:
        """Nearest plan-view distance from the battery box to a prop disk."""

        motor_axis_offset = self.motor_radius / sqrt(2.0)
        nearest_dx = max(motor_axis_offset - self.battery_envelope_length / 2.0, 0.0)
        nearest_dy = max(motor_axis_offset - self.battery_envelope_width / 2.0, 0.0)
        distance_to_motor = sqrt(nearest_dx**2 + nearest_dy**2)
        return distance_to_motor - self.propeller_clearance_diameter / 2.0

    def rounded_plate_propeller_clearance(self, length: float, width: float, radius: float) -> float:
        offset = self.motor_radius / sqrt(2.0)
        dx = max(offset - (length / 2.0 - radius), 0.0)
        dy = max(offset - (width / 2.0 - radius), 0.0)
        return hypot(dx, dy) - radius - self.propeller_clearance_diameter / 2.0

    @property
    def top_plate_to_propeller_plan_clearance(self) -> float:
        """Distance from a motor centre to the rounded plate, minus prop radius."""

        return self.rounded_plate_propeller_clearance(
            self.top_plate_length, self.top_plate_width, self.top_plate_corner_radius
        )

    @property
    def battery_tray_length(self) -> float:
        return self.battery_envelope_length + 4.0

    @property
    def battery_tray_width(self) -> float:
        return self.battery_envelope_width + 9.0

    @property
    def battery_tray_support_locations(self) -> tuple[tuple[float, float], ...]:
        return tuple((x, y) for x, y in self.standoff_locations if x == 0)

    @property
    def battery_tray_z(self) -> float:
        return self.top_plate_z + self.top_plate_thickness + self.battery_tray_support_height

    @property
    def battery_tray_to_propeller_plan_clearance(self) -> float:
        body_gap = self.rounded_plate_propeller_clearance(
            self.battery_tray_length, self.battery_tray_width, self.battery_tray_corner_radius
        )
        offset = self.motor_radius / sqrt(2.0)
        tab_gap = min(
            hypot(offset - abs(x), offset - abs(y))
            - self.battery_tray_tab_diameter / 2.0
            - self.propeller_clearance_diameter / 2.0
            for x, y in self.battery_tray_support_locations
        )
        return min(body_gap, tab_gap)

    @property
    def lower_plate_z(self) -> float:
        return self.arm_thickness

    @property
    def top_plate_z(self) -> float:
        return (
            self.lower_plate_z
            + self.lower_plate_thickness
            + self.standoff_height
        )

    @property
    def propeller_plane_z(self) -> float:
        return self.arm_thickness + self.propeller_seating_height

    def validate(self) -> None:
        """Reject internally inconsistent geometry before building solids."""

        positive_values = {
            "wheelbase": self.wheelbase,
            "propeller_diameter": self.propeller_diameter,
            "propeller_clearance_diameter": self.propeller_clearance_diameter,
            "propeller_seating_height": self.propeller_seating_height,
            "arm_width": self.arm_width,
            "arm_thickness": self.arm_thickness,
            "motor_pad_diameter": self.motor_pad_diameter,
            "plate_length": self.plate_length,
            "plate_width": self.plate_width,
            "standoff_height": self.standoff_height,
            "top_plate_length": self.top_plate_length,
            "top_plate_width": self.top_plate_width,
            "top_plate_corner_radius": self.top_plate_corner_radius,
            "battery_envelope_length": self.battery_envelope_length,
            "battery_envelope_width": self.battery_envelope_width,
            "battery_envelope_height": self.battery_envelope_height,
            "battery_tray_thickness": self.battery_tray_thickness,
            "battery_tray_support_height": self.battery_tray_support_height,
            "battery_tray_support_diameter": self.battery_tray_support_diameter,
            "battery_slot_length": self.battery_slot_length,
            "battery_slot_width": self.battery_slot_width,
        }
        for name, value in positive_values.items():
            if value <= 0:
                raise ValueError(f"{name} must be positive, got {value}")

        if self.propeller_clearance_diameter < self.propeller_diameter:
            raise ValueError("Propeller clearance envelope cannot be smaller than nominal diameter")
        if len(self.battery_tray_support_locations) != 2:
            raise ValueError("Battery tray requires two side-axis chassis supports")
        if not 0 < self.battery_tray_corner_radius < min(
            self.battery_tray_length, self.battery_tray_width
        ) / 2:
            raise ValueError("Battery tray corner radius does not fit")
        if self.battery_tray_to_propeller_plan_clearance < 3.0:
            raise ValueError("Battery tray needs at least 3 mm propeller plan clearance")
        corner_dx = max(self.battery_envelope_length / 2 - (
            self.battery_tray_length / 2 - self.battery_tray_corner_radius
        ), 0)
        corner_dy = max(self.battery_envelope_width / 2 - (
            self.battery_tray_width / 2 - self.battery_tray_corner_radius
        ), 0)
        if hypot(corner_dx, corner_dy) > self.battery_tray_corner_radius:
            raise ValueError("Battery allowance corners overhang the rounded tray")
        if self.battery_slot_width >= self.battery_slot_length:
            raise ValueError("Battery strap slot must be longer than its width")
        if self.battery_slot_y - self.battery_slot_width / 2 < self.battery_envelope_width / 2:
            raise ValueError("Battery strap slots are beneath the battery allowance")
        if self.battery_slot_y + self.battery_slot_width / 2 > self.battery_tray_width / 2 - 1:
            raise ValueError("Battery strap slots leave insufficient tray edge material")
        if self.battery_slot_x + self.battery_slot_length / 2 > (
            self.battery_tray_length / 2 - self.battery_tray_corner_radius
        ):
            raise ValueError("Battery strap slots enter the rounded tray corners")
        if self.battery_tray_support_diameter > self.battery_tray_tab_diameter:
            raise ValueError("Battery tray tabs cannot support the column footprint")

        if self.propeller_tip_clearance < 5.0:
            raise ValueError(
                "Adjacent propellers need at least 5 mm nominal clearance; "
                f"current value is {self.propeller_tip_clearance:.2f} mm"
            )

        if self.battery_to_propeller_plan_clearance < 3.0:
            raise ValueError(
                "The provisional battery envelope needs at least 3 mm plan-view "
                "clearance from every propeller disk; current value is "
                f"{self.battery_to_propeller_plan_clearance:.2f} mm"
            )

        if not 0 < self.top_plate_corner_radius < min(
            self.top_plate_length, self.top_plate_width
        ) / 2.0:
            raise ValueError("Upper-plate corner radius does not fit the plate")
        if self.top_plate_to_propeller_plan_clearance < 3.0:
            raise ValueError("Upper plate needs at least 3 mm propeller plan clearance")

        for x, y in self.standoff_locations:
            if (
                abs(x) + self.standoff_outer_diameter / 2.0 > self.top_plate_length / 2.0
                or abs(y) + self.standoff_outer_diameter / 2.0 > self.top_plate_width / 2.0
            ):
                raise ValueError("Standoff envelope extends beyond the upper plate")

        if self.arm_inner_radius >= min(self.arm_bolt_radii):
            raise ValueError("The inner arm end must lie inside the first arm bolt")
        if min(self.arm_bolt_radii) - self.arm_inner_radius < (
            self.fastener_envelope_diameter / 2.0 + self.fastener_clearance
        ):
            raise ValueError("Inner arm fastener is too close to the arm root")
        if abs(self.arm_bolt_radii[1] - self.arm_bolt_radii[0]) < (
            self.fastener_envelope_diameter + self.fastener_clearance
        ):
            raise ValueError("Arm fastener envelopes need separation")

        motor_hole_extent = (
            self.motor_mount_spacing / sqrt(2.0)
            + self.motor_mount_hole_diameter / 2.0
        )
        if motor_hole_extent >= self.motor_pad_diameter / 2.0:
            raise ValueError("Motor mounting holes do not fit inside the motor pad")

        outer_bolt_coordinate = max(self.arm_bolt_radii) / sqrt(2.0)
        plate_edge_margin = min(
            self.plate_length / 2.0 - outer_bolt_coordinate,
            self.plate_width / 2.0 - outer_bolt_coordinate,
        )
        if plate_edge_margin < self.arm_bolt_hole_diameter:
            raise ValueError(
                "Outer arm bolts are too close to the centre-plate edge; "
                f"available margin is {plate_edge_margin:.2f} mm"
            )


@dataclass(frozen=True)
class ElectronicsParameters:
    """Published envelopes plus conservative allowances for the chosen stack."""

    esc_x: float = 43.0
    esc_y: float = 43.0
    esc_height: float = 10.0  # provisional; published plan size omits height
    flight_controller_x: float = 36.0
    flight_controller_y: float = 36.0
    flight_controller_height: float = 9.0
    stack_mount_spacing: float = 30.5
    stack_hole_diameter: float = 3.4
    stack_screw_access_diameter: float = 8.0
    electronics_floor_clearance: float = 6.0
    esc_to_flight_controller_gap: float = 5.0

    raspberry_pi_x: float = 65.0
    raspberry_pi_y: float = 30.0
    raspberry_pi_height: float = 12.0  # includes provisional connector clearance
    raspberry_pi_mount_spacing_x: float = 58.0
    raspberry_pi_mount_spacing_y: float = 23.0
    raspberry_pi_hole_diameter: float = 2.8  # provisional printed M2.5 clearance
    raspberry_pi_spacer_diameter: float = 6.0
    payload_floor_clearance: float = 6.0  # length of the four Pi spacers
    payload_to_battery_clearance: float = 3.0  # minimum under the tray

    @property
    def raspberry_pi_mount_locations(self) -> tuple[tuple[float, float], ...]:
        return tuple(
            (x, y)
            for x in (-self.raspberry_pi_mount_spacing_x / 2, self.raspberry_pi_mount_spacing_x / 2)
            for y in (-self.raspberry_pi_mount_spacing_y / 2, self.raspberry_pi_mount_spacing_y / 2)
        )

    @property
    def core_stack_height(self) -> float:
        return (
            self.electronics_floor_clearance
            + self.esc_height
            + self.esc_to_flight_controller_gap
            + self.flight_controller_height
        )

    def validate(self, frame: FrameParameters) -> None:
        """Check the stack against the arm fasteners and their access path."""

        if self.raspberry_pi_hole_diameter >= self.raspberry_pi_spacer_diameter:
            raise ValueError("Pi spacer bore must be smaller than its outer diameter")
        half = self.stack_mount_spacing / 2.0
        stack_points = tuple((x, y) for x in (-half, half) for y in (-half, half))
        required_gap = frame.fastener_envelope_diameter + frame.fastener_clearance
        for angle in frame.arm_angles_deg:
            for radius in frame.arm_bolt_radii:
                x = radius * cos(radians(angle))
                y = radius * sin(radians(angle))
                if any(hypot(x - sx, y - sy) < required_gap for sx, sy in stack_points):
                    raise ValueError("Arm and stack fastener envelopes are too close")
        required_root_radius = (
            self.stack_mount_spacing / sqrt(2.0)
            + self.stack_screw_access_diameter / 2.0
            + frame.fastener_clearance
        )
        if frame.arm_inner_radius < required_root_radius:
            raise ValueError("Arm roots obstruct stack screw access from below")
        required_floor = (
            frame.fastener_envelope_height
            + frame.fastener_tip_allowance
            + frame.fastener_clearance
        )
        if self.electronics_floor_clearance < required_floor:
            raise ValueError("ESC floor clearance is insufficient for arm fasteners")
        if self.core_stack_height + frame.fastener_clearance > frame.standoff_height:
            raise ValueError("Electronics stack does not fit below the upper plate")
        if frame.battery_tray_support_height < (
            self.payload_floor_clearance + self.raspberry_pi_height
            + self.payload_to_battery_clearance + frame.battery_strap_thickness
        ):
            raise ValueError("Battery tray is too low to clear the Pi envelope")
        for x, y in frame.battery_tray_support_locations:
            distance = hypot(max(abs(x) - self.raspberry_pi_x / 2, 0),
                             max(abs(y) - self.raspberry_pi_y / 2, 0))
            if distance < frame.battery_tray_support_diameter / 2 + frame.fastener_clearance:
                raise ValueError("Battery tray columns obstruct the Pi envelope")
        for x, y in self.raspberry_pi_mount_locations:
            if abs(x) + self.raspberry_pi_spacer_diameter / 2 > frame.top_plate_length / 2 or (
                abs(y) + self.raspberry_pi_spacer_diameter / 2 > frame.top_plate_width / 2
            ):
                raise ValueError("Pi spacer extends beyond the upper plate")
            for sx, sy in frame.standoff_locations:
                if hypot(x - sx, y - sy) < (
                    self.raspberry_pi_spacer_diameter + frame.fastener_envelope_diameter
                ) / 2 + frame.fastener_clearance:
                    raise ValueError("Pi mounts conflict with chassis fasteners")
