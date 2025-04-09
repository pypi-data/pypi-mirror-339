import fcntl

# FICLONE is 0x40049409 on Linux
FICLONE = 0x40049409


def reflink(src, dest):
    """Create a reflink (copy-on-write) from src to dest."""
    try:
        # Open source file in read-only mode
        with open(src, "rb") as src_fd:
            # Open destination file in read-write mode, creating it if necessary
            with open(dest, "wb") as dest_fd:
                # Perform the reflink operation
                fcntl.ioctl(dest_fd.fileno(), FICLONE, src_fd.fileno())
        print(f"Reflink: {src} -> {dest}")
    except OSError as e:
        print(f"Reflink error: {e}")
