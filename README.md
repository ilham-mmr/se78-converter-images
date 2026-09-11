# SAP SE78 Image Converter

A small Python utility for converting common image files into **SAP SE78-friendly 8-bit / 256-color BMPs** with an exact white background.

It was built to avoid the common issue where a true-color BMP is converted by SE78 and a white background ends up looking gray or cream.

## Default presets

| Type | Output size |
|---|---:|
| Header | 2475 × 300 px |
| Footer | 2475 × 150 px |

The converter preserves the source aspect ratio, centers the artwork on a pure-white canvas (`RGB 255,255,255`), applies mild sharpening when upscaling, and writes an indexed 256-color BMP without dithering.

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

The image is still fitted proportionally, centered on white, and saved as an 8-bit / 256-color BMP.

## Output characteristics

- BMP format
- 8-bit / 256-color indexed palette
- Exact white canvas: `RGB(255,255,255)`
- Aspect ratio preserved
- No stretching
- No dithering during palette conversion
- Existing `_SE78_256COLOR.BMP` outputs are skipped during folder conversion

## Troubleshooting

If Windows says `python` is not recognized, reinstall Python and make sure **Add Python to PATH** is enabled.

If you see `No module named PIL`, run:

```bat
python -m pip install pillow
```

If automatic detection fails, either rename the file to include `HEADER`/`FOOTER`, pass `--type header` or `--type footer`, or use a custom `--width` and `--height`.

## Downloading as a ZIP

On GitHub, choose **Code → Download ZIP** to download the complete toolkit without using Git.
