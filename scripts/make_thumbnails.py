#!/usr/bin/env python3
"""Generate gallery thumbnails for _includes/gallery.html.

For every *.jpg / *.jpeg in the given folder(s) a centre-cropped 600x400 thumbnail named
<file>_t.<ext> is written next to it (quality 82, progressive). Existing thumbnails are
skipped unless --force is given. Originals are never modified.

Usage:  python3 scripts/make_thumbnails.py assets/images/driver/e46 [more folders] [--force]
Needs:  Pillow  (pip install pillow)
"""
import pathlib
import sys

from PIL import Image, ImageOps

SIZE = (600, 400)
SUFFIX = "_t"


def main(argv):
    folders = [a for a in argv if not a.startswith("--")]
    force = "--force" in argv
    if not folders:
        print(__doc__)
        return 1
    for folder in folders:
        for src in sorted(pathlib.Path(folder).glob("*.jp*g")):
            if src.stem.endswith(SUFFIX):
                continue
            dst = src.with_name(f"{src.stem}{SUFFIX}{src.suffix}")
            if dst.exists() and not force:
                print(f"skip   {dst} (exists)")
                continue
            with Image.open(src) as im:
                im = ImageOps.exif_transpose(im).convert("RGB")
                thumb = ImageOps.fit(im, SIZE, Image.Resampling.LANCZOS)
                thumb.save(dst, "JPEG", quality=82, optimize=True, progressive=True)
            print(f"wrote  {dst} {thumb.size[0]}x{thumb.size[1]} {dst.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
