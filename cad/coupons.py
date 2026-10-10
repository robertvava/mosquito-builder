"""Small fit samples; print flat before committing to a complete chassis.

Both use the same through-hole helper as the frame. They are intended for
unpowered fit checks, not motor running or structural qualification.
"""

from build123d import Align, Cylinder, Part, extrude, RectangleRounded

from cad.frame import _through_cylinder
from cad.parameters import ElectronicsParameters, FrameParameters


def make_motor_coupon(frame: FrameParameters | None = None) -> Part:
    """An 8 mm thick motor pad with the actual 16 x 16 mm mounting holes."""

    frame = frame or FrameParameters()
    frame.validate()
    coupon = Cylinder(
        frame.motor_pad_diameter / 2.0,
        frame.arm_thickness,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    coupon -= _through_cylinder(
        0, 0, 0, frame.motor_centre_hole_diameter, frame.arm_thickness
    )
    half = frame.motor_mount_spacing / 2.0
    for x in (-half, half):
        for y in (-half, half):
            coupon -= _through_cylinder(
                x, y, 0, frame.motor_mount_hole_diameter, frame.arm_thickness
            )
    return coupon


def make_stack_coupon(
    frame: FrameParameters | None = None,
    electronics: ElectronicsParameters | None = None,
) -> Part:
    """A 43 mm square, 4 mm thick sample for stack screw and grommet fit."""

    frame = frame or FrameParameters()
    electronics = electronics or ElectronicsParameters()
    frame.validate()
    electronics.validate(frame)
    coupon = extrude(RectangleRounded(electronics.esc_x, electronics.esc_y, 3.0),
                     amount=frame.lower_plate_thickness)
    half = electronics.stack_mount_spacing / 2.0
    for x in (-half, half):
        for y in (-half, half):
            coupon -= _through_cylinder(
                x, y, 0, electronics.stack_hole_diameter, frame.lower_plate_thickness
            )
    return coupon


def make_pi_coupon(
    frame: FrameParameters | None = None,
    electronics: ElectronicsParameters | None = None,
) -> Part:
    """Small M2.5 sample matching the Pi's 58 x 23 mm mounting pattern."""

    frame = frame or FrameParameters()
    electronics = electronics or ElectronicsParameters()
    frame.validate()
    electronics.validate(frame)
    coupon = extrude(RectangleRounded(electronics.raspberry_pi_x,
                                     electronics.raspberry_pi_y, 2),
                     amount=frame.top_plate_thickness)
    for x, y in electronics.raspberry_pi_mount_locations:
        coupon -= _through_cylinder(x, y, 0, electronics.raspberry_pi_hole_diameter,
                                    frame.top_plate_thickness)
    return coupon
