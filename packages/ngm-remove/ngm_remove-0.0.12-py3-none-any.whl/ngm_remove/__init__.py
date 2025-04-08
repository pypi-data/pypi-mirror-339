import os
import sys
import json
import argparse
import platform
import uuid
import subprocess

from importlib.metadata import version
from pathlib import Path

from ngm_remove import lib
from ngm_remove import db
from ngm_remove import utils
from ngm_remove import reflink
from ngm_remove import mkfile
from ngm_remove import fileblocks


def run_remove():
    parser = argparse.ArgumentParser(description="Remove files/folders")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    parser.add_argument(
        "--input", help="file with list of items to remove", type=str, default=""
    )
    parser.add_argument(
        "--cmd", help="command to get list of items to remove", type=str, default=""
    )
    parser.add_argument(
        "--url",
        help="http/https url to get list of items to remove",
        type=str,
        default="",
    )
    # parser.add_argument("--option", help="some option", type=str, default="default_value")
    parser.add_argument("paths", nargs="*", help="Files/Folders to Remove")

    args = parser.parse_args()

    if args.version:
        print(version("ngm-remove"))
        exit(0)

    sessionid = uuid.uuid4()
    dbi = db.DB(sessionid)

    if args.cmd:
        try:
            process = subprocess.run(
                args.cmd,
                shell=True,
                capture_output=True,
                text=True,  # Capture output as text (strings)
                check=True,  # Raise CalledProcessError for non-zero exit codes
            )
            lines = process.stdout.strip().splitlines()
            print(lines)
            for item in lines:
                lib.remove(item.strip(), dbi)

        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            print(f"Stderr: {e.stderr}")  # print the standard error
            exit(1)

        except FileNotFoundError:
            print("Command not found.")
            exit(1)

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            exit(1)

        finally:
            print("exiting")
            exit(0)

    if args.input:
        # check for file exitence
        inputpath = Path(args.input)
        if not inputpath.is_file():
            print("Input file not found:", args.input)
            exit(1)

        # use try/except
        try:
            with open(args.input, "r", encoding="utf-8") as file:
                lines = file.readlines()

                if platform.system() == "Windows":
                    for item in lines:
                        lib.remove(item.strip(), dbi)

                else:
                    for item in lines:
                        elem = utils.get_first_part(item)
                        lib.remove(elem, dbi)
        except Exception as e:
            print("Failed to read input file:", args.input)
            print(e)
            exit(1)

        finally:
            exit(0)

    argscount = len(args.paths)

    if argscount == 0:
        print("Usage: remove <path>")
        sys.exit(1)

    for item in args.paths:
        lib.remove(item, dbi)


def run_copy():
    print("Copy!")


def run_reflink():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <source> <destination>")
        sys.exit(1)

    src_file = sys.argv[1]
    dest_file = sys.argv[2]

    reflink.reflink(src_file, dest_file)


def run_mkfile():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <file> <size>")
        sys.exit(1)

    fpath = sys.argv[1]
    strsize = sys.argv[2]

    try:
        size = mkfile.szconvert(strsize)
    except Exception as e:
        print("Convert error:", e)
        sys.exit(2)

    try:
        mkfile.mkfile(fpath, size)
    except Exception as e:
        print("Fallocate error:", e)


def run_fileblocks():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>")
        sys.exit(1)

    fpath = sys.argv[1]
    fileblocks.fileblocks(fpath)


def run_filestat():
    if len(sys.argv) != 2:
        print("Usage: filestat <file>")
        sys.exit(1)

    fpath = sys.argv[1]
    info = os.stat(fpath)

    data = {
        "name": fpath,
        "st_mode": info.st_mode,  # protection bits
        "st_ino": info.st_ino,  # inode number
        "st_dev": info.st_dev,  # ID of device containing file
        "st_nlink": info.st_nlink,  # number of hard links
        "st_uid": info.st_uid,  # user ID of owner
        "st_gid": info.st_gid,  # group ID of owner
        "st_rdev": info.st_rdev,  # device ID (if special file)
        "st_size": info.st_size,  # total size, in bytes
        "st_blksize": info.st_blksize,  # blocksize for filesystem I/O
        "st_blocks": info.st_blocks,  # number of blocks allocated
        "st_atime": info.st_atime,  # time of last access
        "st_mtime": info.st_mtime,  # time of last modification
        "st_ctime": info.st_ctime,  # time of last status change
        # "st_birthtime": info.st_birthtime, # not always available
    }

    jinfo = json.dumps(data)
    print(jinfo)


def run_filesize():
    if len(sys.argv) != 2:
        print("Usage: filestat <file>")
        sys.exit(1)

    fpath = sys.argv[1]
    info = os.stat(fpath)

    # number of blocks are counted as count of 512B blocks - not as count of real blocks
    psize = info.st_blocks * 512
    size = info.st_size
    bsize = info.st_blksize

    print("logical size:", size)
    print("physical size:", psize)
    print("block size:", bsize)
