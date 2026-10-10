"""Regression tests for the parametric frame geometry."""

from __future__ import annotations

import unittest
from math import cos, radians, sin
from dataclasses import replace

from build123d import Align, Box, Cylinder, Pos
from cad.assembly import place_on_print_bed
from cad.checks import design_metrics
from cad.coupons import make_motor_coupon, make_pi_coupon, make_stack_coupon
from cad.frame import build_frame_model
from cad.parameters import ElectronicsParameters, FrameParameters


class FrameGeometryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = build_frame_model()
        cls.metrics = design_metrics(cls.model)

    def test_frame_has_exactly_four_arms_and_motor_envelopes(self) -> None:
        self.assertEqual(len(self.model.arms), 4)
        self.assertEqual(len(self.model.motor_envelopes), 4)
        self.assertEqual(len(self.model.propeller_disks), 4)

    def test_propellers_have_generous_nominal_clearance(self) -> None:
        self.assertGreaterEqual(self.metrics["propeller_tip_clearance_mm"], 5.0)

    def test_battery_envelope_does_not_overhang_propeller_disks(self) -> None:
        self.assertGreaterEqual(
            self.metrics["battery_to_propeller_plan_clearance_mm"],
            3.0,
        )

    def test_electronics_keepout_fits_between_centre_plates(self) -> None:
        available = self.model.parameters.standoff_height
        required = self.model.electronics_parameters.core_stack_height
        self.assertLess(required, available)

    def test_selected_motor_and_stack_interfaces_are_modelled(self) -> None:
        self.assertEqual(self.model.parameters.motor_mount_spacing, 16.0)
        self.assertEqual(
            self.model.electronics_parameters.stack_mount_spacing,
            30.5,
        )

    def test_ballpark_frame_mass_remains_reviewable(self) -> None:
        self.assertLess(self.metrics["estimated_solid_print_mass_g"], 160.0)

    def test_invalid_propeller_overlap_is_rejected(self) -> None:
        parameters = FrameParameters(propeller_diameter=160.0)
        with self.assertRaises(ValueError):
            parameters.validate()

    def test_old_overlapping_arm_fasteners_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "fastener envelopes"):
            ElectronicsParameters().validate(FrameParameters(arm_bolt_radii=(24, 40)))

    def test_old_arm_roots_block_stack_access(self) -> None:
        with self.assertRaisesRegex(ValueError, "obstruct stack screw access"):
            ElectronicsParameters().validate(FrameParameters(arm_inner_radius=14))

    def test_stack_screw_and_tool_paths_are_clear_through_arm_plane(self) -> None:
        p, e = self.model.parameters, self.model.electronics_parameters
        half = e.stack_mount_spacing / 2.0
        for x in (-half, half):
            for y in (-half, half):
                probe = Pos(x, y, 0) * Cylinder(
                    e.stack_screw_access_diameter / 2.0,
                    p.arm_thickness,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                )
                for arm in self.model.arms:
                    self.assertLess((probe & arm).volume, 1e-6)
                bore = Pos(x, y, p.lower_plate_z) * Cylinder(
                    e.stack_hole_diameter / 2.0,
                    p.lower_plate_thickness,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                )
                self.assertLess((bore & self.model.lower_plate).volume, 1e-6)

    def test_arm_fastener_envelopes_clear_stack_and_standoffs(self) -> None:
        p, e = self.model.parameters, self.model.electronics_parameters
        half = e.stack_mount_spacing / 2.0
        for angle in p.arm_angles_deg:
            for radius in p.arm_bolt_radii:
                x = radius * cos(radians(angle))
                y = radius * sin(radians(angle))
                envelope = Pos(x, y, p.lower_plate_z + p.lower_plate_thickness) * Cylinder(
                    p.fastener_envelope_diameter / 2.0,
                    p.fastener_envelope_height + p.fastener_tip_allowance,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                )
                for part in (self.model.esc_keepout, *self.model.standoffs):
                    self.assertLess((envelope & part).volume, 1e-6)
                for sx in (-half, half):
                    for sy in (-half, half):
                        stack_head = Pos(sx, sy, p.lower_plate_z) * Cylinder(
                            p.fastener_envelope_diameter / 2.0,
                            1,
                            align=(Align.CENTER, Align.CENTER, Align.MIN),
                        )
                        arm_head = Pos(x, y, p.lower_plate_z) * Cylinder(
                            p.fastener_envelope_diameter / 2.0,
                            1,
                            align=(Align.CENTER, Align.CENTER, Align.MIN),
                        )
                        self.assertLess((stack_head & arm_head).volume, 1e-6)

    def test_upper_plate_clears_entire_prop_projection(self) -> None:
        p = self.model.parameters
        self.assertGreaterEqual(p.top_plate_to_propeller_plan_clearance, 3.0)
        for motor in self.model.motor_envelopes:
            centre = motor.bounding_box().center()
            sweep = Pos(centre.X, centre.Y, 0) * Cylinder(
                p.propeller_clearance_diameter / 2.0, 150,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )
            self.assertLess((sweep & self.model.top_plate).volume, 1e-6)

    def test_fit_coupons_have_open_mounting_bores(self) -> None:
        p, e = self.model.parameters, self.model.electronics_parameters
        for coupon, spacing, diameter, height in (
            (make_motor_coupon(p), p.motor_mount_spacing, p.motor_mount_hole_diameter, p.arm_thickness),
            (make_stack_coupon(p, e), e.stack_mount_spacing, e.stack_hole_diameter, p.lower_plate_thickness),
        ):
            self.assertTrue(coupon.is_valid)
            self.assertEqual(len(coupon.solids()), 1)
            half = spacing / 2.0
            for x in (-half, half):
                for y in (-half, half):
                    probe = Pos(x, y, 0) * Cylinder(
                        diameter / 2.0, height,
                        align=(Align.CENTER, Align.CENTER, Align.MIN),
                    )
                    self.assertLess((probe & coupon).volume, 1e-6)

    def test_print_parts_are_bed_aligned_and_mass_includes_spacers(self) -> None:
        self.assertEqual(len(self.model.frame_parts), 17)
        for part in self.model.frame_parts:
            bounds = place_on_print_bed(part).bounding_box()
            self.assertAlmostEqual(bounds.min.Z, 0, places=6)
            self.assertAlmostEqual(bounds.min.X + bounds.max.X, 0, places=6)
            self.assertAlmostEqual(bounds.min.Y + bounds.max.Y, 0, places=6)
        self.assertAlmostEqual(
            self.metrics["estimated_solid_print_mass_g"],
            sum(part.volume for part in self.model.frame_parts)
            * self.model.parameters.frame_material_density_g_per_mm3,
        )

    def test_nominal_propeller_and_clearance_envelope_are_separate(self) -> None:
        p = self.model.parameters
        self.assertAlmostEqual(p.propeller_diameter, 124.46)
        self.assertAlmostEqual(p.propeller_clearance_diameter, 127)
        nominal = self.model.propeller_disks[0].volume
        envelope = self.model.propeller_clearance_disks[0].volume
        self.assertGreater(envelope, nominal)
        with self.assertRaisesRegex(ValueError, "smaller than nominal"):
            replace(p, propeller_clearance_diameter=120).validate()

    def test_old_wheelbase_fails_conservative_clearance(self) -> None:
        with self.assertRaises(ValueError):
            replace(self.model.parameters, wheelbase=220).validate()

    def test_propeller_seating_height_is_independent_of_motor_envelope(self) -> None:
        p = self.model.parameters
        self.assertFalse(p.propeller_seating_height_verified)
        self.assertEqual(replace(p, motor_envelope_height=50).propeller_plane_z,
                         p.propeller_plane_z)
        self.assertEqual(replace(p, propeller_seating_height=25).propeller_plane_z,
                         p.arm_thickness + 25)

    def test_pi_mounting_bores_and_spacers_match_board_pattern(self) -> None:
        p, e = self.model.parameters, self.model.electronics_parameters
        self.assertEqual(e.raspberry_pi_mount_spacing_x, 58)
        self.assertEqual(e.raspberry_pi_mount_spacing_y, 23)
        coupon = make_pi_coupon(p, e)
        for (x, y), spacer in zip(e.raspberry_pi_mount_locations, self.model.pi_spacers):
            for part, z, height in ((self.model.top_plate, p.top_plate_z, p.top_plate_thickness),
                                    (spacer, p.top_plate_z + p.top_plate_thickness,
                                     e.payload_floor_clearance),
                                    (coupon, 0, p.top_plate_thickness)):
                bore = Pos(x, y, z) * Cylinder(e.raspberry_pi_hole_diameter / 2, height,
                          align=(Align.CENTER, Align.CENTER, Align.MIN))
                self.assertLess((bore & part).volume, 1e-6)
            self.assertAlmostEqual(spacer.bounding_box().max.Z,
                                   self.model.raspberry_pi_keepout.bounding_box().min.Z)

    def test_battery_tray_load_path_is_separate_from_pi(self) -> None:
        p, e = self.model.parameters, self.model.electronics_parameters
        self.assertEqual(len(self.model.battery_tray_supports), 2)
        self.assertGreaterEqual(self.model.battery_tray.bounding_box().min.Z
                               - self.model.raspberry_pi_keepout.bounding_box().max.Z,
                               e.payload_to_battery_clearance)
        for support in self.model.battery_tray_supports:
            self.assertLess((support & self.model.raspberry_pi_keepout).volume, 1e-6)
            self.assertAlmostEqual(support.bounding_box().min.Z,
                                   self.model.top_plate.bounding_box().max.Z)
            self.assertAlmostEqual(support.bounding_box().max.Z,
                                   self.model.battery_tray.bounding_box().min.Z)
        with self.assertRaisesRegex(ValueError, "too low"):
            e.validate(replace(p, battery_tray_support_height=18))

    def test_battery_tray_clears_envelopes_and_supports_whole_pack(self) -> None:
        p = self.model.parameters
        self.assertGreaterEqual(p.battery_tray_to_propeller_plan_clearance, 3)
        for motor in self.model.motor_envelopes:
            c = motor.bounding_box().center()
            sweep = Pos(c.X, c.Y, 0) * Cylinder(p.propeller_clearance_diameter / 2, 150,
                     align=(Align.CENTER, Align.CENTER, Align.MIN))
            for part in (self.model.battery_tray, *self.model.battery_tray_supports,
                         self.model.battery_keepout):
                self.assertLess((sweep & part).volume, 1e-6)
        pack_projection = Pos(0, 0, p.battery_tray_z) * Box(
            p.battery_envelope_length, p.battery_envelope_width, p.battery_tray_thickness,
            align=(Align.CENTER, Align.CENTER, Align.MIN))
        self.assertLess((pack_projection - self.model.battery_tray).volume, 1e-6)

    def test_tray_strap_slots_and_support_bores_are_open(self) -> None:
        p = self.model.parameters
        for x in (-p.battery_slot_x, p.battery_slot_x):
            for y in (-p.battery_slot_y, p.battery_slot_y):
                slot = Pos(x, y, p.battery_tray_z) * Box(
                    p.battery_slot_length - p.battery_slot_width, p.battery_slot_width,
                    p.battery_tray_thickness, align=(Align.CENTER, Align.CENTER, Align.MIN))
                self.assertLess((slot & self.model.battery_tray).volume, 1e-6)
        for (x, y), support in zip(p.battery_tray_support_locations,
                                   self.model.battery_tray_supports):
            bore = Pos(x, y, p.top_plate_z) * Cylinder(p.standoff_hole_diameter / 2,
                     p.battery_tray_support_height + p.top_plate_thickness + p.battery_tray_thickness,
                     align=(Align.CENTER, Align.CENTER, Align.MIN))
            for part in (self.model.top_plate, support, self.model.battery_tray):
                self.assertLess((bore & part).volume, 1e-6)


if __name__ == "__main__":
    unittest.main()
