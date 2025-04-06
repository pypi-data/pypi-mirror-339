import ctypes
import logging
import subprocess
from dataclasses import dataclass
from pathlib import Path

import numpy as np

logger = logging.getLogger("ldipc")


@dataclass
class EmuInfo:
    index: int
    name: str
    pid: int
    width: int
    height: int


def _run_ldconsole_list2(path):
    try:
        result = subprocess.run(
            [path, "list2"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW,
            text=True,
        )
        return result.stdout
    except Exception as e:
        logger.error(f"Failed to run ldconsole: {e}")
        return ""


def _parse_ldlist2(data):
    emulators = []
    for line in data.strip().splitlines():
        parts = line.strip().split(",")
        try:
            index = int(parts[0])
            name = parts[1]
            pid = int(parts[5])
            width = int(parts[7])
            height = int(parts[8])
            emulators.append(EmuInfo(index, name, pid, width, height))
        except ValueError:
            logger.debug(f"Skipping invalid line: {line}")
            continue
    return emulators


def _find_player_info(path, playeridx):
    raw = _run_ldconsole_list2(path)
    players = _parse_ldlist2(raw)
    for p in players:
        if p.index == playeridx:
            return p
    logger.debug(f"No player found with index: {playeridx}")
    return None


class _IScreenShotVTable(ctypes.Structure):
    _fields_ = [
        ("destructor", ctypes.c_void_p),
        ("cap", ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)),
        ("release", ctypes.CFUNCTYPE(None, ctypes.c_void_p)),
    ]


class _IScreenShotClass(ctypes.Structure):
    _fields_ = [("vtable", ctypes.POINTER(_IScreenShotVTable))]


class LDPlayer:
    def __init__(self, path: Path, index):
        if not path.exists():
            logger.error(f"Path does not exist: {path}")
            raise ValueError(f"Invalid path: {path}")

        self._path = path
        self._dll_path = path / "ldopengl64.dll"
        self._console_path = path / "ldconsole.exe"

        self._info: EmuInfo = _find_player_info(str(self._console_path), index)
        if not self._info:
            logger.error(f"Failed to find player info for index: {index}")
            raise ValueError(f"Invalid player index: {index}")

        self.index = index
        self.pid = self._info.pid
        self.width = self._info.width
        self.height = self._info.height

        try:
            self.dll = ctypes.CDLL(str(self._dll_path.absolute()))
            self.dll.CreateScreenShotInstance.argtypes = [ctypes.c_uint, ctypes.c_uint]
            self.dll.CreateScreenShotInstance.restype = ctypes.c_void_p
        except Exception as e:
            logger.error(f"Failed to load DLL: {e}")
            raise

        self.screenshot_instance_ptr = self.dll.CreateScreenShotInstance(
            self.index, self.pid
        )
        if not self.screenshot_instance_ptr:
            logger.error("Failed to create IScreenShotClass instance.")
            raise RuntimeError("Failed to create IScreenShotClass instance.")

        self._screenshot_instance = ctypes.cast(
            self.screenshot_instance_ptr, ctypes.POINTER(_IScreenShotClass)
        ).contents

    @property
    def resolution(self):
        return (self.width, self.height)

    def capture(self) -> np.ndarray:
        """
        Capture a screenshot of the current LDPlayer instance.

        This method takes screen pixel data and converts it into a NumPy array.
        The returned array is an image in RGB format with the shape (height, width, 3).
        """
        width, height = self.width, self.height
        channels = 3
        img_ptr = self._screenshot_instance.vtable.contents.cap(
            self.screenshot_instance_ptr
        )
        if not img_ptr:
            logger.error("cap() returned NULL")
            raise RuntimeError("cap() returned NULL")

        size = width * height * channels
        buf = ctypes.string_at(img_ptr, size)

        arr = np.frombuffer(buf, dtype=np.uint8).reshape((height, width, channels))
        arr = arr.reshape((height, width, 3))
        arr = arr[::-1]
        arr = arr[:, :, ::-1]

        return arr

    def __del__(self):
        if hasattr(self, "_screenshot_instance"):
            self._screenshot_instance.vtable.contents.release(
                self.screenshot_instance_ptr
            )
