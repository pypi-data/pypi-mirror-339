import ctypes
from ctypes import cdll, c_int, c_longlong


def szconvert(value):
    if value.endswith("K"):
        size_in_bytes = int(value[:-1]) * 1024

    elif value.endswith("M"):
        size_in_bytes = int(value[:-1]) * 1024 * 1024  # Convert MB to bytes

    elif value.endswith("G"):
        size_in_bytes = int(value[:-1]) * 1024 * 1024 * 1024  # Convert GB to bytes

    else:
        raise int(value)

    return size_in_bytes


def mkfile(fname: str, size: int) -> None:
    # Load the C standard library
    libc = cdll.LoadLibrary("libc.so.6")

    # Define the argument types for fallocate (optional but safer)
    libc.fallocate.argtypes = [c_int, c_int, c_longlong, c_longlong]
    libc.fallocate.restype = c_int

    with open(fname, "wb") as f:
        fd = f.fileno()  # Get file descriptor
        ret = libc.fallocate(fd, 0, 0, size)

    if ret != 0:
        errno = ctypes.get_errno()
        raise OSError(errno, f"fallocate failed with errno {errno}")
