# Compiler and flags
CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -fPIC
PYTHON ?= python3
UV ?= uv
PYTHON_INCLUDES = $(shell $(UV) run $(PYTHON) -c "import sysconfig; print(sysconfig.get_path('include'))")
SYSTEM_INCLUDES = $(shell $(UV) run $(PYTHON) -c "import sysconfig; print(sysconfig.get_config_var('INCLUDEPY'))")

# Platform detection
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
	SHARED_EXT = so
else ifeq ($(UNAME_S),Darwin)
	SHARED_EXT = dylib
else
	$(error Unsupported platform: $(UNAME_S))
endif

# Targets
.PHONY: all clean build install test dist wheels

all: build

build:
	$(UV) pip install -e .

install:
	$(UV) pip install .

test: build
	$(UV) run $(PYTHON) -m pytest tests/

dist: clean
	$(UV) run $(PYTHON) -m pip install build
	$(UV) run $(PYTHON) -m build

wheels:
	$(UV) run $(PYTHON) -m pip install cibuildwheel
	$(UV) run $(PYTHON) -m cibuildwheel --output-dir wheelhouse

clean:
	rm -rf build/ dist/ wheelhouse/
	rm -f src/*.so src/*.dylib
	rm -rf *.egg-info
