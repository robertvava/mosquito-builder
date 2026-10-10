"""Build, display and export frame concept v0.4.

Examples:
    uv run python -m cad.assembly
    uv run python -m cad.assembly --show
    uv run python -m cad.assembly --export
    uv run python -m cad.assembly --coupons-only
"""

from __future__ import annotations

import argparse
from pathlib import Path

from build123d import Part, Pos, export_step, export_stl

from cad.checks import format_report
from cad.coupons import make_motor_coupon, make_pi_coupon, make_stack_coupon
from cad.frame import build_frame_model, make_arm


def place_on_print_bed(part: Part) -> Part:
    """Centre a single part in XY and put its lowest face on Z=0."""

    bounds = part.bounding_box()
    return Pos(
        -(bounds.min.X + bounds.max.X) / 2.0,
        -(bounds.min.Y + bounds.max.Y) / 2.0,
        -bounds.min.Z,
    ) * part


def export_model(output_directory: Path, coupons_only: bool = False) -> list[Path]:
    model = build_frame_model()
    output_directory.mkdir(parents=True, exist_ok=True)

    parts = [
        ("motor_mount_coupon_8mm.stl", make_motor_coupon(model.parameters)),
        ("stack_mount_coupon_4mm.stl", make_stack_coupon(
            model.parameters, model.electronics_parameters
        )),
        ("pi_mount_coupon_3mm.stl", make_pi_coupon(
            model.parameters, model.electronics_parameters
        )),
    ]
    paths = []
    if not coupons_only:
        assembly_path = output_directory / "frame_assembly.step"
        export_step(model.complete_compound, assembly_path)
        paths.append(assembly_path)
        parts.extend([
            ("arm_8mm_provisional.stl", make_arm(model.parameters)),
            ("lower_plate_4mm_provisional.stl", model.lower_plate),
            ("top_plate_3mm_provisional.stl", model.top_plate),
            ("standoff_36mm_provisional.stl", model.standoffs[0]),
            ("pi_spacer_6mm_provisional.stl", model.pi_spacers[0]),
            ("battery_tray_support_22mm_provisional.stl", model.battery_tray_supports[0]),
            ("battery_tray_3mm_provisional.stl", model.battery_tray),
        ])
    for filename, part in parts:
        path = output_directory / filename
        export_stl(place_on_print_bed(part), path)
        paths.append(path)
    return paths


def show_model() -> None:
    from ocp_vscode import Camera, show
    from ocp_vscode.comms import get_port

    try:
        port = get_port()
    except (OSError, RuntimeError) as error:
        print(f"Could not query OCP CAD Viewer: {error}")
        port = None
    if port is None:
        print(
            "OCP CAD Viewer is not running. In VS Code, open the OCP CAD "
            "Viewer sidebar, start the ocp_vscode viewer from Viewer Manager, "
            "then rerun this command."
        )
        return

    model = build_frame_model()
    objects = [
        *model.arms,
        model.lower_plate,
        model.top_plate,
        *model.standoffs,
        *model.motor_envelopes,
        *model.propeller_disks,
        model.esc_keepout,
        model.flight_controller_keepout,
        model.raspberry_pi_keepout,
        model.battery_keepout,
    ]
    names = [
        "arm-front-right",
        "arm-rear-right",
        "arm-rear-left",
        "arm-front-left",
        "lower-centre-plate",
        "upper-electronics-deck-with-Pi-mounts",
        "standoff-front",
        "standoff-rear",
        "standoff-right",
        "standoff-left",
        "motor-front-right",
        "motor-rear-right",
        "motor-rear-left",
        "motor-front-left",
        "prop-disk-front-right",
        "prop-disk-rear-right",
        "prop-disk-rear-left",
        "prop-disk-front-left",
        "NewBeeDrone-ESC-keepout-provisional-height",
        "Matek-F405-HDTE-keepout",
        "Raspberry-Pi-Zero-2-W-payload-keepout",
        "battery-envelope-provisional",
    ]
    colors = [
        "#222222",
        "#222222",
        "#222222",
        "#222222",
        "#333333",
        "#333333",
        "#a8a8a8",
        "#a8a8a8",
        "#a8a8a8",
        "#a8a8a8",
        "#3366cc",
        "#3366cc",
        "#3366cc",
        "#3366cc",
        "#88bbff",
        "#88bbff",
        "#88bbff",
        "#88bbff",
        "#2f9e44",
        "#7048e8",
        "#e03131",
        "#f08c00",
    ]
    alphas = [
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        0.8,
        0.8,
        0.8,
        0.8,
        0.18,
        0.18,
        0.18,
        0.18,
        0.65,
        0.35,
        0.35,
        0.35,
    ]
    extras = [
        *[(part, f"Pi-M2p5-spacer-{i + 1}", "#a8a8a8", 1.0)
          for i, part in enumerate(model.pi_spacers)],
        *[(part, f"battery-tray-side-support-{i + 1}", "#a8a8a8", 1.0)
          for i, part in enumerate(model.battery_tray_supports)],
        (model.battery_tray, "supported-removable-battery-tray", "#555555", 1.0),
        (model.battery_pad_keepout, "nonslip-battery-pad-2mm-provisional", "#ad7b43", 0.6),
        *[(part, f"prop-clearance-127mm-{i + 1}", "#00bcd4", 0.12)
          for i, part in enumerate(model.propeller_clearance_disks)],
    ]
    for part, name, color, alpha in extras:
        objects.append(part)
        names.append(name)
        colors.append(color)
        alphas.append(alpha)
    show(
        *objects,
        names=names,
        colors=colors,
        alphas=alphas,
        axes=True,
        axes0=True,
        grid=(True, True, True),
        ortho=True,
        reset_camera=Camera.RESET,
        port=port,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--show", action="store_true", help="send the model to OCP CAD Viewer")
    exports = parser.add_mutually_exclusive_group()
    exports.add_argument("--export", action="store_true", help="write STEP/STL files to cad/exports/v0_4")
    exports.add_argument("--coupons-only", action="store_true", help="export the motor, stack and Pi mounting fit samples")
    args = parser.parse_args()

    model = build_frame_model()
    print(format_report(model))

    if args.export or args.coupons_only:
        for path in export_model(
            Path(__file__).parent / "exports" / "v0_4", args.coupons_only
        ):
            print(f"Exported {path}")
    if args.show:
        show_model()


if __name__ == "__main__":
    main()

