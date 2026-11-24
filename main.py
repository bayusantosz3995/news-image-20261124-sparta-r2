#!/usr/bin/env python3
"""Copy the pre-rendered entry.png to the make.fun output directory.

Standard library only. No rendering happens here, so repeated runs
produce byte-identical output.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    with open(dst, "rb") as f:
        if f.read(8) != b"\x89PNG\r\n\x1a\n":
            print("error: copied file is not a PNG", file=sys.stderr)
            return 1
    if sha256(SRC) != sha256(dst):
        print("error: copied entry.png differs from source", file=sys.stderr)
        return 1
    print("wrote", dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
