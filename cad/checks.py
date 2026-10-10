"""Numerical checks and a concise report for the frame model."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from cad.frame import FrameModel, build_frame_model


def design_metrics(model: FrameModel) -> dict[str, Any]:
    parameters = model.parameters
    frame_volume_mm3 = sum(part.volume for part in model.frame_parts)
    solid_frame_mass_g = (
        frame_volume_mm3 * parameters.frame_material_density_g_per_mm3
    )

    return {
        "wheelbase_mm": parameters.wheelbase,
        "propeller_diameter_mm": parameters.propeller_diameter,
        "propeller_clearance_diameter_mm": parameters.propeller_clearance_diameter,
        "adjacent_motor_distance_mm": parameters.adjacent_motor_distance,
        "propeller_tip_clearance_mm": parameters.propeller_tip_clearance,
        "overall_propeller_span_x_y_mm": parameters.overall_propeller_span_x_y,
        "overall_clearance_span_x_y_mm": parameters.overall_clearance_span_x_y,
        "battery_to_propeller_plan_clearance_mm": (
            parameters.battery_to_propeller_plan_clearance
        ),
        "electronics_bay_height_mm": parameters.standoff_height,
        "top_plate_to_propeller_plan_clearance_mm": (
            parameters.top_plate_to_propeller_plan_clearance
        ),
        "battery_tray_to_propeller_plan_clearance_mm": (
            parameters.battery_tray_to_propeller_plan_clearance
        ),
        "propeller_seating_height_verified": parameters.propeller_seating_height_verified,
        "propeller_plane_z_mm": parameters.propeller_plane_z,
        "frame_solid_volume_mm3": frame_volume_mm3,
        "estimated_solid_print_mass_g": solid_frame_mass_g,
        "esc_keepout_mm": (
            model.electronics_parameters.esc_x,
            model.electronics_parameters.esc_y,
            model.electronics_parameters.esc_height,
        ),
        "flight_controller_keepout_mm": (
            model.electronics_parameters.flight_controller_x,
            model.electronics_parameters.flight_controller_y,
            model.electronics_parameters.flight_controller_height,
        ),
        "parameters": asdict(parameters),
    }


def format_report(model: FrameModel) -> str:
    metrics = design_metrics(model)
    return "\n".join(
        (
            "Drone frame concept v0.4 (supported payload fit prototype)",
            f"Wheelbase: {metrics['wheelbase_mm']:.1f} mm",
            f"Propellers: {metrics['propeller_diameter_mm']:.2f} mm (4.9 inch)",
            "Conservative propeller clearance envelope: "
            f"{metrics['propeller_clearance_diameter_mm']:.1f} mm",
            "Adjacent clearance-envelope gap: "
            f"{metrics['propeller_tip_clearance_mm']:.1f} mm",
            "Overall span including propeller disks: "
            f"{metrics['overall_propeller_span_x_y_mm']:.1f} mm square",
            "Overall span including clearance envelopes: "
            f"{metrics['overall_clearance_span_x_y_mm']:.1f} mm square",
            "Battery-to-propeller plan clearance: "
            f"{metrics['battery_to_propeller_plan_clearance_mm']:.1f} mm",
            f"Electronics bay height: {metrics['electronics_bay_height_mm']:.1f} mm",
            "Upper-plate-to-propeller plan clearance: "
            f"{metrics['top_plate_to_propeller_plan_clearance_mm']:.1f} mm",
            "Battery-tray-to-propeller plan clearance: "
            f"{metrics['battery_tray_to_propeller_plan_clearance_mm']:.2f} mm",
            "Solid-geometry polymer mass estimate: "
            f"{metrics['estimated_solid_print_mass_g']:.1f} g "
            "(includes tray and all spacers; not a slicer prediction)",
            "Core stack: 43 mm ESC + 36 mm FC, 30.5 mm M3 pattern",
            "Pi: 58 x 23 mm M2.5 mounts; battery tray supported by side columns",
            "Battery allowance: 85 x 45 x 30 mm, centred above the Pi",
            f"Propeller seating height above motor mounting face: {model.parameters.propeller_seating_height:.1f} mm "
            f"({'verified' if metrics['propeller_seating_height_verified'] else 'UNVERIFIED placeholder'})",
        )
    )


if __name__ == "__main__":
    print(format_report(build_frame_model()))
