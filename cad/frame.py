"""build123d geometry for the provisional 4.9-inch printed frame."""

from __future__ import annotations

from dataclasses import dataclass

from build123d import (
    Align,
    Box,
    Compound,
    Cylinder,
    Part,
    Pos,
    RectangleRounded,
    Rot,
    extrude,
)

from cad.parameters import ElectronicsParameters, FrameParameters


def _through_cylinder(
    x: float,
    y: float,
    z: float,
    diameter: float,
    depth: float,
) -> Part:
    return Pos(x, y, z - 0.5) * Cylinder(
        diameter / 2.0,
        depth + 1.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )


def make_arm(parameters: FrameParameters, angle_deg: float = 0.0) -> Part:
    """Create one arm, with its local motor centre on +X."""

    parameters.validate()
    rail_length = parameters.motor_radius - parameters.arm_inner_radius
    rail_centre_x = parameters.arm_inner_radius + rail_length / 2.0

    rail = Pos(rail_centre_x, 0.0, 0.0) * Box(
        rail_length,
        parameters.arm_width,
        parameters.arm_thickness,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    motor_pad = Pos(parameters.motor_radius, 0.0, 0.0) * Cylinder(
        parameters.motor_pad_diameter / 2.0,
        parameters.arm_thickness,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    arm = rail + motor_pad

    cutters: list[Part] = [
        _through_cylinder(
            parameters.motor_radius,
            0.0,
            0.0,
            parameters.motor_centre_hole_diameter,
            parameters.arm_thickness,
        )
    ]

    half_spacing = parameters.motor_mount_spacing / 2.0
    for x_offset in (-half_spacing, half_spacing):
        for y_offset in (-half_spacing, half_spacing):
            cutters.append(
                _through_cylinder(
                    parameters.motor_radius + x_offset,
                    y_offset,
                    0.0,
                    parameters.motor_mount_hole_diameter,
                    parameters.arm_thickness,
                )
            )

    for bolt_radius in parameters.arm_bolt_radii:
        cutters.append(
            _through_cylinder(
                bolt_radius,
                0.0,
                0.0,
                parameters.arm_bolt_hole_diameter,
                parameters.arm_thickness,
            )
        )

    for cutter in cutters:
        arm = arm - cutter

    return Rot(0.0, 0.0, angle_deg) * arm


def _rounded_plate(
    length: float,
    width: float,
    corner_radius: float,
    thickness: float,
    z: float,
) -> Part:
    profile = RectangleRounded(length, width, corner_radius)
    return Pos(0.0, 0.0, z) * extrude(profile, amount=thickness)


def _cut_arm_bolt_holes(plate: Part, parameters: FrameParameters, z: float) -> Part:
    for angle_deg in parameters.arm_angles_deg:
        for bolt_radius in parameters.arm_bolt_radii:
            cutter = Rot(0.0, 0.0, angle_deg) * _through_cylinder(
                bolt_radius,
                0.0,
                z,
                parameters.arm_bolt_hole_diameter,
                parameters.lower_plate_thickness,
            )
            plate = plate - cutter
    return plate


def _cut_standoff_holes(
    plate: Part,
    parameters: FrameParameters,
    z: float,
    thickness: float,
) -> Part:
    for x, y in parameters.standoff_locations:
        plate = plate - _through_cylinder(
            x,
            y,
            z,
            parameters.standoff_hole_diameter,
            thickness,
        )
    return plate


def _cut_stack_holes(
    plate: Part,
    parameters: FrameParameters,
    electronics: ElectronicsParameters,
) -> Part:
    half_spacing = electronics.stack_mount_spacing / 2.0
    for x in (-half_spacing, half_spacing):
        for y in (-half_spacing, half_spacing):
            plate = plate - _through_cylinder(
                x,
                y,
                parameters.lower_plate_z,
                electronics.stack_hole_diameter,
                parameters.lower_plate_thickness,
            )
    return plate


def make_lower_plate(
    parameters: FrameParameters,
    electronics: ElectronicsParameters,
) -> Part:
    """Create the lower electronics plate that also retains the arms."""

    parameters.validate()
    plate = _rounded_plate(
        parameters.plate_length,
        parameters.plate_width,
        parameters.plate_corner_radius,
        parameters.lower_plate_thickness,
        parameters.lower_plate_z,
    )
    plate = _cut_arm_bolt_holes(plate, parameters, parameters.lower_plate_z)
    plate = _cut_standoff_holes(
        plate,
        parameters,
        parameters.lower_plate_z,
        parameters.lower_plate_thickness,
    )
    return _cut_stack_holes(plate, parameters, electronics)


def make_top_plate(parameters: FrameParameters, electronics: ElectronicsParameters) -> Part:
    """Create the upper electronics deck with chassis and M2.5 Pi holes."""

    parameters.validate()
    plate = _rounded_plate(
        parameters.top_plate_length,
        parameters.top_plate_width,
        parameters.top_plate_corner_radius,
        parameters.top_plate_thickness,
        parameters.top_plate_z,
    )
    plate = _cut_standoff_holes(
        plate,
        parameters,
        parameters.top_plate_z,
        parameters.top_plate_thickness,
    )

    for x, y in electronics.raspberry_pi_mount_locations:
        plate -= _through_cylinder(x, y, parameters.top_plate_z,
                                   electronics.raspberry_pi_hole_diameter,
                                   parameters.top_plate_thickness)
    return plate


def _make_spacer(x: float, y: float, z: float, outer: float, bore: float, height: float) -> Part:
    return Pos(x, y, z) * Cylinder(
        outer / 2, height, align=(Align.CENTER, Align.CENTER, Align.MIN)
    ) - _through_cylinder(x, y, z, bore, height)


def make_pi_spacers(parameters: FrameParameters, electronics: ElectronicsParameters) -> tuple[Part, ...]:
    return tuple(
        _make_spacer(x, y, parameters.top_plate_z + parameters.top_plate_thickness,
                     electronics.raspberry_pi_spacer_diameter,
                     electronics.raspberry_pi_hole_diameter,
                     electronics.payload_floor_clearance)
        for x, y in electronics.raspberry_pi_mount_locations
    )


def make_battery_tray_supports(parameters: FrameParameters) -> tuple[Part, ...]:
    return tuple(
        _make_spacer(x, y, parameters.top_plate_z + parameters.top_plate_thickness,
                     parameters.battery_tray_support_diameter,
                     parameters.standoff_hole_diameter,
                     parameters.battery_tray_support_height)
        for x, y in parameters.battery_tray_support_locations
    )


def make_battery_tray(parameters: FrameParameters) -> Part:
    """Removable tray supported at the side chassis mounts, with two straps."""

    z = parameters.battery_tray_z
    tray = _rounded_plate(parameters.battery_tray_length, parameters.battery_tray_width,
                          parameters.battery_tray_corner_radius, parameters.battery_tray_thickness, z)
    for x, y in parameters.battery_tray_support_locations:
        tray += Pos(x, y, z) * Cylinder(
            parameters.battery_tray_tab_diameter / 2, parameters.battery_tray_thickness,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        tray -= _through_cylinder(x, y, z, parameters.standoff_hole_diameter,
                                  parameters.battery_tray_thickness)

    straight = parameters.battery_slot_length - parameters.battery_slot_width
    depth = parameters.battery_tray_thickness + 1
    for x in (-parameters.battery_slot_x, parameters.battery_slot_x):
        for y in (-parameters.battery_slot_y, parameters.battery_slot_y):
            slot = Pos(x, y, z - 0.5) * Box(
                straight, parameters.battery_slot_width, depth,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )
            for end in (-straight / 2, straight / 2):
                slot += Pos(x + end, y, z - 0.5) * Cylinder(
                    parameters.battery_slot_width / 2, depth,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                )
            tray -= slot
    return tray


def make_standoffs(parameters: FrameParameters) -> tuple[Part, ...]:
    start_z = parameters.lower_plate_z + parameters.lower_plate_thickness
    standoffs: list[Part] = []
    for x, y in parameters.standoff_locations:
        outer = Pos(x, y, start_z) * Cylinder(
            parameters.standoff_outer_diameter / 2.0,
            parameters.standoff_height,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        inner = _through_cylinder(
            x,
            y,
            start_z,
            parameters.standoff_hole_diameter,
            parameters.standoff_height,
        )
        standoffs.append(outer - inner)
    return tuple(standoffs)


@dataclass(frozen=True)
class FrameModel:
    parameters: FrameParameters
    electronics_parameters: ElectronicsParameters
    arms: tuple[Part, ...]
    lower_plate: Part
    top_plate: Part
    standoffs: tuple[Part, ...]
    pi_spacers: tuple[Part, ...]
    battery_tray_supports: tuple[Part, ...]
    battery_tray: Part
    motor_envelopes: tuple[Part, ...]
    propeller_disks: tuple[Part, ...]
    propeller_clearance_disks: tuple[Part, ...]
    esc_keepout: Part
    flight_controller_keepout: Part
    raspberry_pi_keepout: Part
    battery_pad_keepout: Part
    battery_keepout: Part

    @property
    def frame_parts(self) -> tuple[Part, ...]:
        return (*self.arms, self.lower_plate, self.top_plate, *self.standoffs,
                *self.pi_spacers, *self.battery_tray_supports, self.battery_tray)

    @property
    def printable_compound(self) -> Compound:
        return Compound(children=list(self.frame_parts))

    @property
    def complete_compound(self) -> Compound:
        return Compound(
            children=[
                *self.frame_parts,
                *self.motor_envelopes,
                *self.propeller_disks,
                *self.propeller_clearance_disks,
                self.esc_keepout,
                self.flight_controller_keepout,
                self.raspberry_pi_keepout,
                self.battery_pad_keepout,
                self.battery_keepout,
            ]
        )


def build_frame_model(
    parameters: FrameParameters | None = None,
    electronics_parameters: ElectronicsParameters | None = None,
) -> FrameModel:
    parameters = parameters or FrameParameters()
    electronics_parameters = electronics_parameters or ElectronicsParameters()
    parameters.validate()
    electronics_parameters.validate(parameters)

    arms = tuple(make_arm(parameters, angle) for angle in parameters.arm_angles_deg)
    lower_plate = make_lower_plate(parameters, electronics_parameters)
    top_plate = make_top_plate(parameters, electronics_parameters)
    standoffs = make_standoffs(parameters)
    pi_spacers = make_pi_spacers(parameters, electronics_parameters)
    battery_tray_supports = make_battery_tray_supports(parameters)
    battery_tray = make_battery_tray(parameters)

    motor_envelopes: list[Part] = []
    propeller_disks: list[Part] = []
    propeller_clearance_disks: list[Part] = []
    for angle in parameters.arm_angles_deg:
        motor = Pos(parameters.motor_radius, 0.0, parameters.arm_thickness) * Cylinder(
            parameters.motor_envelope_diameter / 2.0,
            parameters.motor_envelope_height,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        propeller = Pos(
            parameters.motor_radius,
            0.0,
            parameters.propeller_plane_z,
        ) * Cylinder(
            parameters.propeller_diameter / 2.0,
            parameters.propeller_disk_thickness,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        motor_envelopes.append(Rot(0.0, 0.0, angle) * motor)
        propeller_disks.append(Rot(0.0, 0.0, angle) * propeller)
        clearance = Pos(parameters.motor_radius, 0, parameters.propeller_plane_z) * Cylinder(
            parameters.propeller_clearance_diameter / 2, parameters.propeller_disk_thickness,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        propeller_clearance_disks.append(Rot(0, 0, angle) * clearance)

    esc_z = (
        parameters.lower_plate_z
        + parameters.lower_plate_thickness
        + electronics_parameters.electronics_floor_clearance
    )
    esc_keepout = Pos(0.0, 0.0, esc_z) * Box(
        electronics_parameters.esc_x,
        electronics_parameters.esc_y,
        electronics_parameters.esc_height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    flight_controller_z = (
        esc_z
        + electronics_parameters.esc_height
        + electronics_parameters.esc_to_flight_controller_gap
    )
    flight_controller_keepout = Pos(0.0, 0.0, flight_controller_z) * Box(
        electronics_parameters.flight_controller_x,
        electronics_parameters.flight_controller_y,
        electronics_parameters.flight_controller_height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    raspberry_pi_z = (
        parameters.top_plate_z
        + parameters.top_plate_thickness
        + electronics_parameters.payload_floor_clearance
    )
    raspberry_pi_keepout = Pos(0.0, 0.0, raspberry_pi_z) * Box(
        electronics_parameters.raspberry_pi_x,
        electronics_parameters.raspberry_pi_y,
        electronics_parameters.raspberry_pi_height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    battery_pad_keepout = Pos(0, 0, parameters.battery_tray_z + parameters.battery_tray_thickness) * Box(
        parameters.battery_envelope_length, parameters.battery_envelope_width,
        parameters.battery_pad_thickness, align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    battery_z = parameters.battery_tray_z + parameters.battery_tray_thickness + parameters.battery_pad_thickness
    battery_keepout = Pos(
        0.0,
        0.0,
        battery_z,
    ) * Box(
        parameters.battery_envelope_length,
        parameters.battery_envelope_width,
        parameters.battery_envelope_height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )

    return FrameModel(
        parameters=parameters,
        electronics_parameters=electronics_parameters,
        arms=arms,
        lower_plate=lower_plate,
        top_plate=top_plate,
        standoffs=standoffs,
        pi_spacers=pi_spacers,
        battery_tray_supports=battery_tray_supports,
        battery_tray=battery_tray,
        motor_envelopes=tuple(motor_envelopes),
        propeller_disks=tuple(propeller_disks),
        propeller_clearance_disks=tuple(propeller_clearance_disks),
        esc_keepout=esc_keepout,
        flight_controller_keepout=flight_controller_keepout,
        raspberry_pi_keepout=raspberry_pi_keepout,
        battery_pad_keepout=battery_pad_keepout,
        battery_keepout=battery_keepout,
    )
