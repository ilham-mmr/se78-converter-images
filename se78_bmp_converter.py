#!/usr/bin/env python3
"""SAP SE78-friendly BMP converter.

Default presets:
- Header: 2475 x 300 px
- Footer: 2475 x 150 px

Output:
- BMP
- 8-bit / 256-color indexed palette
- Pure white background RGB(255, 255, 255)
- Aspect ratio preserved
- Centered on a fixed-size canvas
- Mild sharpening after upscaling
- No dithering during palette conversion
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageFilter

HEADER_SIZE = (2475, 300)
FOOTER_SIZE = (2475, 150)
SUPPORTED_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp"
}
OUTPUT_SUFFIX = "_SE78_256COLOR"


def flatten_on_white(img: Image.Image) -> Image.Image:
    """Composite transparency onto pure white and return RGB."""
    if img.mode in ("RGBA", "LA") or "transparency" in img.info:
        rgba = img.convert("RGBA")
        background = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        background.alpha_composite(rgba)
        return background.convert("RGB")
    return img.convert("RGB")


def detect_asset_type(path: Path) -> str:
    """Detect header/footer from the filename."""
    name = path.stem.lower()
    if "header" in name:
        return "header"
    if "footer" in name:
        return "footer"
    raise ValueError(
        f"Cannot determine header/footer from filename: {path.name}. "
        'Rename it to include HEADER/FOOTER, use "--type", or provide '
        'both "--width" and "--height".'
    )


def get_target_size(
    asset_type: str,
    width: int | None,
    height: int | None,
) -> tuple[int, int]:
    """Resolve preset or custom output dimensions."""
    if (width is None) != (height is None):
        raise ValueError("Use --width and --height together.")

    if width is not None and height is not None:
        if width <= 0 or height <= 0:
            raise ValueError("--width and --height must be greater than zero.")
        return width, height

    if asset_type == "header":
        return HEADER_SIZE
    if asset_type == "footer":
        return FOOTER_SIZE
    raise ValueError(f"Unsupported asset type: {asset_type}")


def ensure_pure_white_palette(
    paletted: Image.Image,
    original_rgb: Image.Image,
) -> Image.Image:
    """Guarantee exact RGB(255,255,255) in the indexed palette."""
    palette = paletted.getpalette()
    white_index = None

    for index in range(256):
        start = index * 3
        r, g, b = palette[start:start + 3]
        if (r, g, b) == (255, 255, 255):
            white_index = index
            break

    if white_index is None:
        usage = Counter(paletted.getdata())
        white_index = min(range(256), key=lambda i: usage.get(i, 0))
        start = white_index * 3
        palette[start:start + 3] = [255, 255, 255]
        paletted.putpalette(palette)

    rgb_pixels = original_rgb.load()
    indexed_pixels = paletted.load()
    width, height = original_rgb.size

    for y in range(height):
        for x in range(width):
            if rgb_pixels[x, y] == (255, 255, 255):
                indexed_pixels[x, y] = white_index

    return paletted


def convert_image(
    src: Path,
    dst: Path,
    target_size: tuple[int, int],
    sharpen: bool = True,
) -> None:
    """Convert one image to an SAP SE78-friendly 256-color BMP."""
    target_width, target_height = target_size

    with Image.open(src) as opened:
        image = flatten_on_white(opened)

    scale = min(target_width / image.width, target_height / image.height)
    resized_width = max(1, round(image.width * scale))
    resized_height = max(1, round(image.height * scale))

    resized = image.resize(
        (resized_width, resized_height),
        Image.Resampling.LANCZOS,
    )

    if sharpen and scale > 1:
        resized = resized.filter(
            ImageFilter.UnsharpMask(radius=1.0, percent=110, threshold=2)
        )

    canvas = Image.new(
        "RGB",
        (target_width, target_height),
        (255, 255, 255),
    )

    x = (target_width - resized_width) // 2
    y = (target_height - resized_height) // 2
    canvas.paste(resized, (x, y))

    indexed = canvas.quantize(
        colors=256,
        method=Image.Quantize.MAXCOVERAGE,
        dither=Image.Dither.NONE,
    )
    indexed = ensure_pure_white_palette(indexed, canvas)

    dst.parent.mkdir(parents=True, exist_ok=True)
    indexed.save(dst, format="BMP")

    print(
        f"[OK] {src.name} -> {dst.name} "
        f"({target_width}x{target_height}, 8-bit/256-color)"
    )


def collect_files(inputs: Iterable[str]) -> list[Path]:
    """Expand input files/directories into supported image files."""
    files: list[Path] = []

    for raw in inputs:
        path = Path(raw)

        if not path.exists():
            print(f"[SKIP] Not found: {path}", file=sys.stderr)
            continue

        if path.is_file():
            if path.suffix.lower() in SUPPORTED_EXTENSIONS:
                files.append(path)
            else:
                print(f"[SKIP] Unsupported file type: {path}", file=sys.stderr)
            continue

        if path.is_dir():
            for child in sorted(path.iterdir()):
                if not child.is_file():
                    continue
                if child.suffix.lower() not in SUPPORTED_EXTENSIONS:
                    continue
                if child.stem.upper().endswith(OUTPUT_SUFFIX):
                    continue
                files.append(child)

    return files


def build_output_name(src: Path) -> str:
    """Build NAME_SE78_256COLOR.BMP output filename."""
    stem = src.stem
    if stem.upper().endswith(OUTPUT_SUFFIX):
        stem = stem[:-len(OUTPUT_SUFFIX)]
    return f"{stem}{OUTPUT_SUFFIX}.BMP"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert images into SAP SE78-friendly 256-color BMPs."
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="Image file(s) or folder(s) to convert.",
    )
    parser.add_argument(
        "--type",
        choices=("auto", "header", "footer"),
        default="auto",
        help="Preset type. Default: auto-detect HEADER/FOOTER from filename.",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=None,
        help="Custom output width in pixels. Use together with --height.",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=None,
        help="Custom output height in pixels. Use together with --width.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory. Default: same folder as each source file.",
    )
    parser.add_argument(
        "--no-sharpen",
        action="store_true",
        help="Disable mild sharpening after upscaling.",
    )

    args = parser.parse_args()
    files = collect_files(args.inputs)

    if not files:
        print("No supported image files found.", file=sys.stderr)
        return 1

    converted = 0
    failed = 0

    for src in files:
        try:
            if args.width is not None or args.height is not None:
                asset_type = args.type
            else:
                asset_type = detect_asset_type(src) if args.type == "auto" else args.type

            target_size = get_target_size(asset_type, args.width, args.height)
            output_dir = args.output_dir if args.output_dir is not None else src.parent
            dst = output_dir / build_output_name(src)

            convert_image(
                src=src,
                dst=dst,
                target_size=target_size,
                sharpen=not args.no_sharpen,
            )
            converted += 1
        except Exception as exc:
            failed += 1
            print(f"[ERROR] {src}: {exc}", file=sys.stderr)

    print()
    print(f"Converted: {converted}")
    print(f"Failed:    {failed}")
    return 0 if failed == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
