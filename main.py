#!/usr/bin/env python3
"""Entry program for make.fun bounty news-image-20261120.

Copies the finished front-page image (entry.png, drawn by draw.py) into
the grader's output directory as entry.png. Standard library only, no
network; writes identical bytes on every run.
"""
import os
import shutil
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
