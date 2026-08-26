#!/usr/bin/env python3
"""Generate gallery thumbnails for _includes/gallery.html.

For every .jpg / .jpeg / .png in the given folder(s) a centre-cropped 600x400 thumbnail named
<file>_t.<ext> is written next to it (JPEG: quality 82, progressive; PNG: optimised). Existing
thumbnails are skipped unless --force is given. Originals are never modified.

Usage:  python3 scripts/make_thumbnails.py assets/images/driver/e46 [more folders] [--force]
Needs:  Pillow >= 9.1  (pip install "pillow>=9.1")
"""
import argparse
import pathlib
import sys

from PIL import Image, ImageOps

# Keep in sync with width/height in _includes/gallery.html and `aspect-ratio: 3 / 2` in _sass/_driver.scss.
SIZE = (600, 400)
SUFFIX = "_t"
# Same set as the extension filter in _includes/gallery.html.
EXTENSIONS = {".jpg", ".jpeg", ".png"}


def make_thumbnail(src, dst):
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        if dst.suffix.lower() == ".png":
            thumb = ImageOps.fit(im.convert("RGBA"), SIZE, Image.Resampling.LANCZOS)
            thumb.save(dst, "PNG", optimize=True)
        else:
            thumb = ImageOps.fit(im.convert("RGB"), SIZE, Image.Resampling.LANCZOS)
            thumb.save(dst, "JPEG", quality=82, optimize=True, progressive=True)


def main(argv):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("folders", nargs="+", type=pathlib.Path, help="gallery folder(s) with the original photos")
    parser.add_argument("--force", action="store_true", help="overwrite existing thumbnails")
    args = parser.parse_args(argv)

    failed = 0
    for folder in args.folders:
        if not folder.is_dir():
            print(f"error  {folder} is not a directory", file=sys.stderr)
            failed += 1
            continue
        for src in sorted(p for p in folder.iterdir() if p.suffix.lower() in EXTENSIONS):
            if src.stem.endswith(SUFFIX):
                continue
            dst = src.with_name(f"{src.stem}{SUFFIX}{src.suffix}")
            if dst.exists() and not args.force:
                print(f"skip   {dst} (exists)")
                continue
            try:
                make_thumbnail(src, dst)
            except (OSError, ValueError, Image.DecompressionBombError) as e:  # unreadable, truncated, not an image
                print(f"error  {src}: {e}", file=sys.stderr)
                failed += 1
                continue
            print(f"wrote  {dst} {dst.stat().st_size // 1024} KB")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
