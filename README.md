# Ansible Role: qemu

![GitHub](https://img.shields.io/github/license/jomrr/ansible-role-qemu)
![GitHub last commit](https://img.shields.io/github/last-commit/jomrr/ansible-role-qemu)
![GitHub issues](https://img.shields.io/github/issues-raw/jomrr/ansible-role-qemu)
[![dev](https://img.shields.io/github/actions/workflow/status/jomrr/ansible-role-qemu/dev.yml?branch=dev&label=dev)](https://github.com/jomrr/ansible-role-qemu/actions/workflows/dev.yml?query=branch%3Adev)
[![main](https://img.shields.io/github/actions/workflow/status/jomrr/ansible-role-qemu/main.yml?branch=main&label=main)](https://github.com/jomrr/ansible-role-qemu/actions/workflows/main.yml?query=branch%3Amain)

Install selected QEMU system emulators, UEFI firmware, and optional storage and
display modules.

## Purpose

Install the selected QEMU system emulators, disk image tools, UEFI firmware, and
optional storage and display modules from distribution packages. By default, the
role installs the x86_64 emulator and UEFI firmware without requesting optional
modules.

## Scope

### Managed

- System emulators for the selected x86_64 and/or aarch64 target architectures.
- QEMU disk image tools and optional UEFI firmware for the selected
  architectures.
- Requested storage and display modules, plus packages listed in
  qemu_add_packages.

### Not Managed

- Virtual machine CPU, RAM, networking, definitions, execution, and lifecycle.
- Libvirt services, KVM device permissions, kernel modules, disk images, and
  per-VM firmware state.

## Dependencies

```yaml
collections:
  - name: community.general
    version: '>=12.0.0'
```

## Role Variables

### `qemu_architectures`

Type: `list`. Required: `false`.

System emulator target architectures to install; at least one is required.
AlmaLinux supports only the host architecture.

Default:

```yaml
qemu_architectures:
  - x86_64
```

### `qemu_uefi`

Type: `bool`. Required: `false`.

Install UEFI firmware for each selected emulator architecture.
Disabling this option does not remove firmware installed previously or pulled in
as a package dependency.

Default:

```yaml
qemu_uefi: true
```

### `qemu_storage_modules`

Type: `list`. Required: `false`.

Optional storage backends to install where supported by the distribution.
Available names are curl, iscsi, nfs, rbd, and ssh.
Distribution packages may provide several backends together; omitted modules are
not removed.

Default:

```yaml
qemu_storage_modules: []
```

### `qemu_display_modules`

Type: `list`. Required: `false`.

Optional display backends to install where supported by the distribution.
Available names are gtk, sdl, spice, and egl-headless.
This installs modules without configuring or starting a graphical display or
remote endpoint.

Default:

```yaml
qemu_display_modules: []
```

### `qemu_add_packages`

Type: `list`. Required: `false`.

Additional distribution packages to install alongside the platform's QEMU
packages.

Default:

```yaml
qemu_add_packages: []
```

## Check Mode

Check mode reports pending package installation without changing the host.
Repeated normal runs are idempotent when the requested packages are already
installed.

## Service Behavior

The role does not start virtual machines or manage a QEMU service. Package
installation follows the distribution's packaging behavior.

## Operational Notes

- Selection is additive: the role installs requested capabilities and does not
  remove previously installed packages. Package dependencies and bundled modules
  can provide additional capabilities.
- Debian and Ubuntu bundle storage backends in qemu-block-extra and some display
  backends in shared packages. Fedora and openSUSE provide more granular module
  packages.
- Fedora, Debian, Ubuntu, and openSUSE support x86_64 and aarch64 selection.
  AlmaLinux provides only the host architecture through qemu-kvm-core.
- AlmaLinux supports curl and rbd storage modules and egl-headless display
  support on x86_64. SDL is supported on openSUSE Tumbleweed, but not by the
  shared Leap mapping.
- UEFI selection installs firmware files only. It does not select Secure Boot
  policy or create writable NVRAM for virtual machines.

## Supported Platforms

| OS Family | Distribution | Version | Container Image |
| --------- | ------------ | ------- | --------------- |
| RedHat | AlmaLinux | latest | [jomrr/molecule-almalinux:latest](https://hub.docker.com/r/jomrr/molecule-almalinux) |
| Debian | Debian | latest | [jomrr/molecule-debian:latest](https://hub.docker.com/r/jomrr/molecule-debian) |
| RedHat | Fedora | latest | [jomrr/molecule-fedora:latest](https://hub.docker.com/r/jomrr/molecule-fedora) |
| Suse | OpenSuse Leap | latest | [jomrr/molecule-opensuse-leap:latest](https://hub.docker.com/r/jomrr/molecule-opensuse-leap) |
| Suse | OpenSuse Tumbleweed | latest | [jomrr/molecule-opensuse-tumbleweed:latest](https://hub.docker.com/r/jomrr/molecule-opensuse-tumbleweed) |
| Debian | Ubuntu | latest | [jomrr/molecule-ubuntu:latest](https://hub.docker.com/r/jomrr/molecule-ubuntu) |

## Example Playbook

### Install QEMU

Install the default x86_64 emulator and UEFI firmware.

```yaml
---
- name: QEMU | Install QEMU
  hosts: "qemu"
  gather_facts: true
  roles:
    - role: "jomrr.qemu"
```

### Install multiple emulators and optional modules on Fedora

Install both emulators with UEFI, RBD storage, and GTK display support.

```yaml
---
- name: QEMU | Install selected QEMU capabilities
  hosts: fedora
  gather_facts: true
  roles:
    - role: jomrr.qemu
      qemu_architectures:
        - x86_64
        - aarch64
      qemu_uefi: true
      qemu_storage_modules:
        - rbd
      qemu_display_modules:
        - gtk

```

## References

- [QEMU system emulation](https://www.qemu.org/docs/master/system/index.html)
- [QEMU disk image tools](https://www.qemu.org/docs/master/tools/qemu-img.html)

## Author

[Jonas Mauer](https://github.com/jomrr)

## License

This project is licensed under the MIT License.
See [LICENSE](LICENSE) for the full license text.

Copyright (c) 2021 Jonas Mauer.
