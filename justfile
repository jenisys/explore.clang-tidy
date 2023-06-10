# =============================================================================
# justfile: A makefile like build script -- Command Runner (Rust-based)
# =============================================================================
# REQUIRES: cargo install just
# PLATFORMS: macOS, Linux, Windows, ...
# USAGE:
#   just --list
#   just <TARGET>
#   just <TARGET> <PARAM_VALUE1> ...
#
# SEE ALSO:
#   * https://github.com/casey/just
# =============================================================================
# WORKS BEST FOR: macOS, Linux
# PLATFORM HINTS:
#  * Windows: Python 3.x has only "python.exe", but no "python3.exe"
#             HINT: Requires "bash.exe", provided by WSL or git-bash.
#  * Linux: Python 3.x has only "python3", but no "python" (for newer versions)
#           HINT: "python" seems to be used for "python2".
# =============================================================================

set export
set positional-arguments
set shell := ["/bin/sh", "-c"]

# -----------------------------------------------------------------------------
# CONFIGURATION:
# -----------------------------------------------------------------------------
HERE   := justfile_directory()
HOME_DIR := env_var("HOME")
PYTHON_DEFAULT := if os() == "windows" { "python" } else { "python3" }
PYTHON := env_var_or_default("PYTHON", PYTHON_DEFAULT)
PIP_INSTALL_OPTIONS := env_var_or_default("PIP_INSTALL_OPTIONS", "--quiet")
CARGO := HOME_DIR/".cargo/bin/cargo"
CARGO_RUN_CLANG_TIDY_OPTIONS := ""
# MAYBE: CARGO_RUN_CLANG_TIDY_OPTIONS := "--suppress-warnings"

BUILD_DIR := "build"
COMPILE_COMMANDS_FILE := HERE/BUILD_DIR/"compile_commands.json"
CMAKE_PRESET := "debug"
JOBS := "4"


# -----------------------------------------------------------------------------
# BUILD RECIPES / TARGETS:
# -----------------------------------------------------------------------------
# DEFAULT-TARGET
default:
    just --list

_ensure_packages_are_installed PART:
    #!/usr/bin/env python3
    from subprocess import run
    from os import path
    if not path.exists(".done.install-{{PART}}-packages"):
        print("NEEDS: install-{{PART}}-packages")
        run("just install-{{PART}}-packages", shell=True)

install-python-packages:
    {{PYTHON}} -m pip install {{PIP_INSTALL_OPTIONS}} -r py.requirements.txt
    @touch ".done.install-python-packages"


install-rust-packages:
    {{CARGO}} install run-clang-tidy
    @touch ".done.install-rust-packages"


install-packages: install-python-packages install-rust-packages


# Install all required packages.
bootstrap: (_ensure_packages_are_installed "python") (_ensure_packages_are_installed "rust")
    @echo "BOOTSTRAP.done"


# ----------------------------------------------------------
# CLANG-TIDY RELATED:
# ----------------------------------------------------------
# SIMILAR AS BELOW: Using a ninja build-script
# _ensure_compile_database_exists:
#     #!/usr/bin/env ninja -f
#     rule cmake_build
#         command = just build
#
#     build {{COMPILE_COMMANDS_FILE}}: cmake_build

_ensure_compile_database_exists:
    #!/usr/bin/env {{PYTHON}}
    #!/usr/bin/env python3
    from subprocess import run
    from os import path
    if not path.exists(r"{{COMPILE_COMMANDS_FILE}}"):
        print("NEEDS: build")
        run("just build", shell=True)

# -- HINT ON: cmake-build
#    SAME AS: cmake --workflow --preset={{CMAKE_PRESET}}
# Build C++ sources (and generate: $BUILD_DIR/compile_commands.json)
build: (_ensure_packages_are_installed "python")
    @echo "build: Using cmake.preset={{CMAKE_PRESET}} ..."
    @echo "build: Generating {{BUILD_DIR}}/compile_commands.json"
    cmake-build


CPP_SOURCES_PATTERN := "clang-tidy-mistakes/**/*.cpp"
CPP_SOURCES := `python3 .justlib.glob.py "clang-tidy-mistakes/**/*.cpp" `

# Run clang-tidy (from: clang-extra-tools)
clang-tidy *SOURCES=CPP_SOURCES: _ensure_compile_database_exists
    @echo "clang-tidy: SOURCES={{SOURCES}}"
    clang-tidy -p {{BUILD_DIR}} {{SOURCES}}


# Use run-clang-tidy (from: clang-extra-tools)
run-clang-tidy: _ensure_compile_database_exists
    run-clang-tidy -p {{BUILD_DIR}} -j {{JOBS}}


# Use run-clang-tidy (aka: cargo-run-clang-tidy)
cargo-run-clang-tidy: _ensure_compile_database_exists (_ensure_packages_are_installed "rust")
    {{HOME_DIR}}/.cargo/bin/run-clang-tidy {{CARGO_RUN_CLANG_TIDY_OPTIONS}} .clang-tidy.json -j {{JOBS}}


CODECHECKER_REPORTS_DIR := "codechecker.reports"
CODECHECKER_REPORTS_HTML_DIR := "codechecker.reports_html"
CODECHECKER_SKIP_FILE := ".codechecker.skip_file"

# Run codechecker
codechecker: _ensure_compile_database_exists (_ensure_packages_are_installed "python")
    -CodeChecker analyze {{COMPILE_COMMANDS_FILE}} --output={{CODECHECKER_REPORTS_DIR}}  --skip={{CODECHECKER_SKIP_FILE}}
    @CodeChecker parse -e html "{{CODECHECKER_REPORTS_DIR}}" -o "{{CODECHECKER_REPORTS_HTML_DIR}}"

# MAYBE: CodeChecker check --logfile={{COMPILE_COMMANDS_FILE}} -o {{CODECHECKER_REPORTS_DIR}}

# ----------------------------------------------------------
# CLEANUP: Cleanup most parts (but leave PRECIOUS parts).
# ----------------------------------------------------------
# Clean-up temporary artifacts and directories.
cleanup:
    invoke cleanup

# Clean-up everything.
cleanup-all:
    invoke cleanup.all
