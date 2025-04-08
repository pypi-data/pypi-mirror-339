# Installation Guide

## Installing from PyPI

The simplest way to install `mojo_arrow_sys` is via pip:

```bash
pip install mojo_arrow_sys
```

Pre-built wheels are available for:
- macOS (x86_64 and arm64)
- Linux (x86_64)
- Python versions 3.10 through 3.12

## Installing from Source

If you need to install from source:

```bash
pip install git+https://github.com/winding-lines/mojo_arrow_sys.git
```

This requires:
- A C compiler (gcc, clang, etc.)
- Python development headers

## Verify Installation

You can verify your installation by running:

```python
import mojo_arrow_sys
print(mojo_arrow_sys)
```

## Platform-Specific Considerations

### macOS

On macOS, both Intel (x86_64) and Apple Silicon (arm64) are supported. The package should work with universal2 wheels.

### Linux

On Linux, make sure you have the appropriate development tools installed:

```bash
# Ubuntu/Debian
sudo apt-get install gcc python3-dev

# CentOS/RHEL
sudo yum install gcc python3-devel
```
