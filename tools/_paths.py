# -*- coding: utf-8 -*-
"""Where the tools find the repository and keep their working files.

ROOT is the repository; WORK is a folder for drafts, transcriptions, second-pass replies, reports
and pickles — none of it committed (it is in .gitignore). Set EI_WORK to keep it elsewhere."""
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1].as_posix()
TOOLS = ROOT + "/tools"
DECISIONS = TOOLS + "/decisions"
WORK = os.environ.get("EI_WORK", TOOLS + "/work").replace("\\", "/")
os.makedirs(WORK, exist_ok=True)


def rahlfs_dir():
    """The local CCAT Rahlfs module, for cross-checking only (sources/README.md)."""
    path = os.environ.get("LXX_RAHLFS_DIR")
    if not path:
        raise SystemExit("set LXX_RAHLFS_DIR to the CCAT Rahlfs module (sources/README.md)")
    return path
