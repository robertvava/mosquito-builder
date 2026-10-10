"""Render simple coloured CAD-review images without a GUI.

OCP CAD Viewer remains the interactive viewer.  These PNGs are only convenient
snapshots for automated review and repository documentation.
"""

from __future__ import annotations

from math import ceil, hypot
from pathlib import Path
from typing import Iterable

from build123d import Compound, Edge, Part
from PIL import Image, ImageDraw, ImageFont

from cad.frame import build_frame_model


VIEW_SIZE = (1400, 1100)
MARGIN = 70


def _sample_edge(edge: Edge) -> list[tuple[float, float]]:
    sample_count = max(2, min(100, ceil(edge.length / 2.0) + 1))
    points = [edge.position_at(i / (sample_count - 1)) for i in range(sample_count)]
    return [(point.X, point.Y) for point in points]


def _project(
    shapes: Iterable[Part],
    viewport_origin: tuple[float, float, float],
    viewport_up: tuple[float, float, float],
    look_at: tuple[float, float, float],
) -> list[list[tuple[float, float]]]:
    compound = Compound(children=list(shapes))
    visible, _hidden = compound.project_to_viewport(
        viewport_origin=viewport_origin,
        viewport_up=viewport_up,
        look_at=look_at,
    )
    return [_sample_edge(edge) for edge in visible]


def _draw_dashed_line(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    fill: str,
    width: int,
    dash: float = 10.0,
) -> None:
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = hypot(dx, dy)
    if length == 0:
        return
    ux, uy = dx / length, dy / length
    distance = 0.0
    while distance < length:
        dash_end = min(distance + dash, length)
        draw.line(
            (
                start[0] + ux * distance,
                start[1] + uy * distance,
                start[0] + ux * dash_end,
                start[1] + uy * dash_end,
            ),
            fill=fill,
            width=width,
        )
        distance += 2.0 * dash


def render_review(
    output_path: Path,
    title: str,
    viewport_origin: tuple[float, float, float],
    viewport_up: tuple[float, float, float],
    look_at: tuple[float, float, float],
) -> None:
    model = build_frame_model()
    categories = [
        (model.propeller_clearance_disks, "#00bcd4", 2, True),
        (model.propeller_disks, "#8ecae6", 3, True),
        (model.frame_parts, "#202124", 5, False),
        (model.motor_envelopes, "#4361ee", 3, False),
        ((model.esc_keepout,), "#2b9348", 4, True),
        ((model.flight_controller_keepout,), "#7048e8", 4, True),
        ((model.raspberry_pi_keepout,), "#d00000", 4, True),
        ((model.battery_pad_keepout,), "#ad7b43", 2, True),
        ((model.battery_keepout,), "#f48c06", 4, True),
    ]

    projected = [
        (
            _project(shapes, viewport_origin, viewport_up, look_at),
            colour,
            width,
            dashed,
        )
        for shapes, colour, width, dashed in categories
    ]
    all_points = [point for paths, *_ in projected for path in paths for point in path]
    min_x = min(point[0] for point in all_points)
    max_x = max(point[0] for point in all_points)
    min_y = min(point[1] for point in all_points)
    max_y = max(point[1] for point in all_points)
    width, height = VIEW_SIZE
    scale = min(
        (width - 2 * MARGIN) / (max_x - min_x),
        (height - 2 * MARGIN) / (max_y - min_y),
    )

    def pixel(point: tuple[float, float]) -> tuple[float, float]:
        drawing_width = (max_x - min_x) * scale
        drawing_height = (max_y - min_y) * scale
        x_offset = (width - drawing_width) / 2.0
        y_offset = (height - drawing_height) / 2.0
        return (
            x_offset + (point[0] - min_x) * scale,
            height - (y_offset + (point[1] - min_y) * scale),
        )

    image = Image.new("RGB", VIEW_SIZE, "#ffffff")
    draw = ImageDraw.Draw(image)
    for paths, colour, line_width, dashed in projected:
        for path in paths:
            pixels = [pixel(point) for point in path]
            if dashed:
                for start, end in zip(pixels, pixels[1:]):
                    _draw_dashed_line(draw, start, end, colour, line_width)
            else:
                draw.line(pixels, fill=colour, width=line_width, joint="curve")

    font = ImageFont.load_default(size=22)
    draw.text((24, 20), title, fill="#202124", font=font)
    legend = (
        "black: printed frame   blue: motors/props   cyan: 127 mm envelope\n"
        "green: ESC   purple: FC   red: Pi keep-out   brown: pad   orange: battery"
    )
    draw.multiline_text((24, height - 62), legend, fill="#495057", font=font, spacing=5)
    image.save(output_path)


def main() -> None:
    output_directory = Path(__file__).parent / "exports"
    output_directory.mkdir(parents=True, exist_ok=True)
    render_review(
        output_directory / "frame_top.png",
        "Drone frame v0.4 supported payload - top review",
        viewport_origin=(0.0, 0.0, 500.0),
        viewport_up=(0.0, 1.0, 0.0),
        look_at=(0.0, 0.0, 10.0),
    )
    render_review(
        output_directory / "frame_isometric.png",
        "Drone frame v0.4 supported payload - isometric review",
        viewport_origin=(320.0, -320.0, 260.0),
        viewport_up=(0.0, 0.0, 1.0),
        look_at=(0.0, 0.0, 8.0),
    )


if __name__ == "__main__":
    main()
