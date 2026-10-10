"""Create lightweight top and isometric drawings for design review."""

from __future__ import annotations

from pathlib import Path

from build123d import Color, ExportSVG, LineType

from cad.frame import build_frame_model


def render_projection(
    output_path: Path,
    viewport_origin: tuple[float, float, float],
    viewport_up: tuple[float, float, float],
    look_at: tuple[float, float, float],
) -> None:
    model = build_frame_model()
    visible, hidden = model.complete_compound.project_to_viewport(
        viewport_origin=viewport_origin,
        viewport_up=viewport_up,
        look_at=look_at,
    )

    exporter = ExportSVG(scale=2.5, margin=8.0, fill_color=None)
    exporter.add_layer(
        "visible",
        line_color=Color("#202124"),
        line_weight=0.35,
    )
    exporter.add_layer(
        "hidden",
        line_color=Color("#9aa0a6"),
        line_weight=0.18,
        line_type=LineType.DASHED,
    )
    exporter.add_shape(hidden, layer="hidden")
    exporter.add_shape(visible, layer="visible")
    exporter.write(output_path)


def main() -> None:
    output_directory = Path(__file__).parent / "exports"
    output_directory.mkdir(parents=True, exist_ok=True)

    render_projection(
        output_directory / "frame_top.svg",
        viewport_origin=(0.0, 0.0, 500.0),
        viewport_up=(0.0, 1.0, 0.0),
        look_at=(0.0, 0.0, 10.0),
    )
    render_projection(
        output_directory / "frame_isometric.svg",
        viewport_origin=(320.0, -320.0, 260.0),
        viewport_up=(0.0, 0.0, 1.0),
        look_at=(0.0, 0.0, 8.0),
    )


if __name__ == "__main__":
    main()
