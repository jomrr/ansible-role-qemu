#!/usr/bin/env python3
"""Exercise the installed QEMU capabilities without creating virtual machines."""

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from typing import cast


def run(*arguments: str) -> str:
    """Run an installed tool and surface its output on failure."""
    result = subprocess.run(
        arguments, check=False, capture_output=True, text=True, timeout=30
    )
    if result.returncode:
        raise AssertionError(
            f"{arguments!r} failed ({result.returncode}): {result.stdout}{result.stderr}"
        )
    return result.stdout + result.stderr


def selected(name: str) -> list[str]:
    """Read the scenario's requested capabilities."""
    return cast(list[str], json.loads(os.environ[name]))


def emulator(architecture: str) -> str:
    """Locate the distribution's emulator and check its machine support."""
    executable = shutil.which(f"qemu-system-{architecture}")
    if executable is None:
        executable = "/usr/libexec/qemu-kvm"
    machines = run(executable, "-machine", "help")
    machine = {"x86_64": r"^(?:pc|q35)[ -]", "aarch64": r"^virt[ -]"}
    if re.search(machine[architecture], machines, re.MULTILINE) is None:
        raise AssertionError(f"{executable} provides no machines for {architecture}")
    return executable


def verify_firmware(architectures: list[str]) -> None:
    """Check that UEFI descriptors resolve to usable installed firmware files."""
    available: set[str] = set()
    for descriptor in Path("/usr/share/qemu/firmware").glob("*.json"):
        data = json.loads(descriptor.read_text(encoding="utf-8"))
        if "uefi" not in data["interface-types"]:
            continue
        mapping = data["mapping"]
        filename = (
            mapping["executable"]["filename"]
            if mapping["device"] == "flash"
            else mapping["filename"]
        )
        firmware = Path(filename)
        if not firmware.is_file() or firmware.stat().st_size == 0:
            continue
        if "nvram-template" in mapping:
            nvram = Path(mapping["nvram-template"]["filename"])
            if not nvram.is_file() or nvram.stat().st_size == 0:
                continue
        available.update(target["architecture"] for target in data["targets"])
    missing = set(architectures) - available
    if missing:
        raise AssertionError(f"No installed UEFI firmware for {sorted(missing)}")


def verify_image_tools() -> None:
    """Create and inspect an image using QEMU and the requested extra package."""
    with tempfile.TemporaryDirectory(prefix="qemu-molecule-") as directory:
        image = str(Path(directory) / "disk.qcow2")
        run("qemu-img", "create", "-f", "qcow2", image, "1M")
        run("qemu-img", "check", image)
        description = run("file", "--brief", image)
        if "qcow" not in description.lower():
            raise AssertionError(f"The additional file package cannot identify {image}")


def main() -> None:
    """Verify the capabilities selected by the current Molecule run."""
    architectures = selected("QEMU_TEST_ARCHITECTURES")
    display_modules = selected("QEMU_TEST_DISPLAY_MODULES")
    for architecture in architectures:
        executable = emulator(architecture)
        displays = run(executable, "-display", "help")
        for module in display_modules:
            backend = "spice-app" if module == "spice" else module
            if re.search(rf"\b{re.escape(backend)}\b", displays) is None:
                raise AssertionError(f"{executable} cannot load the {module} display")
    formats = run("qemu-img", "--help")
    for module in selected("QEMU_TEST_STORAGE_MODULES"):
        protocol = "https" if module == "curl" else module
        if re.search(rf"\b{re.escape(protocol)}\b", formats) is None:
            raise AssertionError(f"qemu-img cannot load the {module} storage backend")
    if os.environ["QEMU_TEST_UEFI"] == "true":
        verify_firmware(architectures)
    verify_image_tools()
    print("Verified QEMU emulators, selected modules, firmware, and image tools.")


if __name__ == "__main__":
    main()
