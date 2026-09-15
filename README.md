# SAP SE78 Image Converter

A small Python utility for converting common image files into **SAP SE78-friendly 8-bit / 256-color BMPs** with an exact white background.

It was built to avoid the common issue where a true-color BMP is converted by SE78 and a white background ends up looking gray or cream.

## Default presets

| Type | Output size |
|---|---:|
| Header | 2475 × 300 px |
| Footer | 2475 × 150 px |

By default, the converter preserves the source aspect ratio and centers the artwork on a pure-white canvas (`RGB 255,255,255`). It also supports a **full-width** layout for footer/header designs whose left/right positioning must be preserved, such as a decorative line or logo that needs to reach the right edge.

## Beginner-friendly Windows usage

### 1. Install Python

Install Python 3 from <https://www.python.org/downloads/>. During installation, enable **Add Python to PATH**.

Check it from Command Prompt:

```bat
python --version
```

### 2. Install Pillow once

Double-click:

```text
1_INSTALL_PILLOW.bat
```

Or run manually:

```bat
python -m pip install -r requirements.txt
```

### 3. Put your images in the repository folder

For automatic header/footer detection, include `HEADER` or `FOOTER` in the filename:

```text
ZKPJ_H001_HEADER.png
ZKPJ_H001_FOOTER.png
ZKPJ_S050_HEADER.png
ZKPJ_S050_FOOTER.png
```

### 4. Convert all images

Double-click:

```text
2_CONVERT_IMAGES.bat
```

A file such as:

```text
ZKPJ_S050_HEADER.png
```

becomes:

```text
ZKPJ_S050_HEADER_SE78_256COLOR.BMP
```

Upload the generated BMP into **SE78 → GRAPHICS → BMAP → Color**.

## Supported input formats

- PNG
- JPG / JPEG
- BMP
- TIFF
- WEBP

## Layout modes

### Center layout — default

Use this for normal logos/headers/footers where preserving proportions is more important than touching the page edges.

```bat
python se78_bmp_converter.py ZKPJ_S050_FOOTER.png
```

Equivalent explicit command:

```bat
python se78_bmp_converter.py ZKPJ_S050_FOOTER.png --layout center
```

The image is resized proportionally and centered on the white output canvas.

### Full-width layout

Use this when the original image has meaningful left/right positioning and must span the entire footer/header width. This is useful for designs where a decorative line must touch the right edge or a logo must remain far to the right.

```bat
python se78_bmp_converter.py ZKPJ_H001_FOOTER.jpeg --type footer --layout full-width
```

In `full-width` mode the converter:

- preserves the source's horizontal composition
- removes only outer top/bottom whitespace
- scales the artwork to the exact target width
- keeps all footer content inside the target height rather than cropping text/logos
- still outputs a white-background 8-bit / 256-color SE78 BMP

## Command-line examples

Convert one header:

```bat
python se78_bmp_converter.py ZKPJ_S050_HEADER.png
```

Convert one footer:

```bat
python se78_bmp_converter.py ZKPJ_S050_FOOTER.png
```

Convert all supported images in the current folder:

```bat
python se78_bmp_converter.py .
```

Convert a full-width footer:

```bat
python se78_bmp_converter.py ZKPJ_H001_FOOTER.jpeg --layout full-width
```

Convert a file whose name does not contain `HEADER` or `FOOTER`:

```bat
python se78_bmp_converter.py logo.png --type header
```

Save results into another folder:

```bat
python se78_bmp_converter.py . --output-dir converted
```

Disable sharpening:

```bat
python se78_bmp_converter.py . --no-sharpen
```

## Custom output size

You can also use the converter for arbitrary canvas sizes. When both `--width` and `--height` are supplied, the filename does not need to contain `HEADER` or `FOOTER`.

```bat
python se78_bmp_converter.py logo.png --width 2475 --height 500
```

You can combine custom dimensions with either layout mode:

```bat
python se78_bmp_converter.py logo.png --width 2475 --height 500 --layout full-width
```

## Output characteristics

- BMP format
- 8-bit / 256-color indexed palette
- Exact white canvas: `RGB(255,255,255)`
- No dithering during palette conversion
- Mild sharpening after upscaling
- Existing `_SE78_256COLOR.BMP` outputs are skipped during folder conversion

`center` preserves the source aspect ratio. `full-width` prioritizes the source's horizontal layout and edge placement, so it may vertically compress very wide artwork to keep all content inside the target height.

## Troubleshooting

If Windows says `python` is not recognized, reinstall Python and make sure **Add Python to PATH** is enabled.

If you see `No module named PIL`, run:

```bat
python -m pip install pillow
```

If automatic detection fails, either rename the file to include `HEADER`/`FOOTER`, pass `--type header` or `--type footer`, or use a custom `--width` and `--height`.

If a footer is centered but the original artwork is supposed to span from left to right, use:

```bat
--layout full-width
```

## Downloading as a ZIP

On GitHub, choose **Code → Download ZIP** to download the complete toolkit without using Git.
