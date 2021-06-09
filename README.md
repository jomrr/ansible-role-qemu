# ansible-role-qemu

![GitHub](https://img.shields.io/github/license/jam82/ansible-role-qemu) ![GitHub last commit](https://img.shields.io/github/last-commit/jam82/ansible-role-qemu) ![GitHub issues](https://img.shields.io/github/issues-raw/jam82/ansible-role-qemu) ![Travis (.com) branch](https://img.shields.io/travis/com/jam82/ansible-role-qemu/main?label=ansible-lint%20latest)

**Ansible role for setting up qemu on headless systems.**

This role just installs basic qemu-kvm and qemu-img.
Additional packages can be added via `qemu_add_packages` variable.

## Supported Platforms

- Alpine
- Archlinux
- CentOS
- Debian
- Fedora
- OpenSuse Leap, Tumbleweed
- OracleLinux
- Ubuntu

## Requirements

Ansible 2.9 or higher.

## Variables

Variables and defaults for this role.

### defaults/main.yml

```yaml
# The role is disabled by default, so you do not get in trouble.
# Checked in tasks/main.yml which inlcudes tasks/main.yml if enabled.
qemu_role_enabled: false

# Install additional packages like qemu-block-rbd, etc...
qemu_add_packages: []
```

## Dependencies

None.

## Example Playbook

```yaml
---
# role: ansible-role-qemu
# play: qemu
# file: qemu.yml

- hosts: all
  become: true
  gather_facts: true
  vars:
    qemu_role_enabled: true
  roles:
    - role: ansible-role-qemu
```

## License and Author

- Author:: [jam82](https://github.com/jam82/)
- Copyright:: 2021, [jam82](https://github.com/jam82/)

Licensed under [MIT License](https://opensource.org/licenses/MIT).
See [LICENSE](https://github.com/jam82/ansible-role-qemu/blob/master/LICENSE) file in repository.

## References

- [ArchWiki](https://wiki.archlinux.org/)
