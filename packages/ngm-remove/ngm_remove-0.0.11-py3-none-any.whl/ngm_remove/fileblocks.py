import ctypes
import ctypes.util
import os
import sys

# Constants
MAX_EXTENTS = 256
FS_IOC_FIEMAP = 0xC020660B  # ioctl number for FS_IOC_FIEMAP

# FIEMAP extent flags (from linux/fs.h)
FIEMAP_EXTENT_LAST = 0x00000001
FIEMAP_EXTENT_UNKNOWN = 0x00000002
FIEMAP_EXTENT_DELALLOC = 0x00000004
FIEMAP_EXTENT_ENCODED = 0x00000008
FIEMAP_EXTENT_DATA_ENCRYPTED = 0x00000080
FIEMAP_EXTENT_NOT_ALIGNED = 0x00000100
FIEMAP_EXTENT_DATA_INLINE = 0x00000200
FIEMAP_EXTENT_SHARED = 0x00000400
FIEMAP_EXTENT_MERGED = 0x00000800


# Define struct fiemap_extent (see linux/fiemap.h)
class FiemapExtent(ctypes.Structure):
    _fields_ = [
        ("fe_logical", ctypes.c_uint64),
        ("fe_physical", ctypes.c_uint64),
        ("fe_length", ctypes.c_uint64),
        ("fe_reserved64", ctypes.c_uint64 * 2),
        ("fe_flags", ctypes.c_uint32),
        ("fe_reserved", ctypes.c_uint32 * 3),
    ]


# Define struct fiemap (see linux/fiemap.h)
class Fiemap(ctypes.Structure):
    _fields_ = [
        ("fm_start", ctypes.c_uint64),
        ("fm_length", ctypes.c_uint64),
        ("fm_flags", ctypes.c_uint32),
        ("fm_mapped_extents", ctypes.c_uint32),
        ("fm_extent_count", ctypes.c_uint32),
        ("fm_reserved", ctypes.c_uint32),
        ("fm_extents", FiemapExtent * MAX_EXTENTS),
    ]


def get_block_size(fd):
    statvfs = os.statvfs(fd)
    return statvfs.f_bsize


def fileblocks(path):
    try:
        fd = os.open(path, os.O_RDONLY)
    except OSError as e:
        print(f"Error opening file: {e}", file=sys.stderr)
        return 1

    block_size = get_block_size(path)
    print(f"Block size: {block_size}\n")

    fiemap = Fiemap()
    fiemap.fm_start = 0
    fiemap.fm_length = ctypes.c_uint64(-1).value
    fiemap.fm_flags = 0
    fiemap.fm_extent_count = MAX_EXTENTS

    try:
        libc = ctypes.CDLL(ctypes.util.find_library("c"))
        if libc.ioctl(fd, FS_IOC_FIEMAP, ctypes.byref(fiemap)) < 0:
            raise OSError(ctypes.get_errno(), "ioctl failed")
    except Exception as e:
        print(f"Error using ioctl: {e}", file=sys.stderr)
        os.close(fd)
        return 1

    for i in range(fiemap.fm_mapped_extents):
        extent = fiemap.fm_extents[i]
        block_count = extent.fe_length // block_size

        print(f"Extent {i}:")
        print(f"  Logical offset: {extent.fe_logical}")
        print(f"  Physical offset: {extent.fe_physical}")
        print(f"  Length: {extent.fe_length}")
        print(f"  Blocks: {block_count}")
        print(f"  Flags: 0x{extent.fe_flags:x}")

        if extent.fe_flags & FIEMAP_EXTENT_LAST:
            print("  Last extent")
        if extent.fe_flags & FIEMAP_EXTENT_DELALLOC:
            print("  Delayed allocation")
        if extent.fe_flags & FIEMAP_EXTENT_UNKNOWN:
            print("  Unknown")
        if extent.fe_flags & FIEMAP_EXTENT_ENCODED:
            print("  Encoded")
        if extent.fe_flags & FIEMAP_EXTENT_DATA_ENCRYPTED:
            print("  Data encrypted")
        if extent.fe_flags & FIEMAP_EXTENT_NOT_ALIGNED:
            print("  Not aligned")
        if extent.fe_flags & FIEMAP_EXTENT_DATA_INLINE:
            print("  Data inline")
        if extent.fe_flags & FIEMAP_EXTENT_SHARED:
            print("  Shared")
        if extent.fe_flags & FIEMAP_EXTENT_MERGED:
            print("  Merged")
        print()

    os.close(fd)
    return 0
