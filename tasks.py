#!/usr/bin/env python3
# =============================================================================
# INVOKE TASKS
# =============================================================================
# SEE: https://pyinvoke.org/

from __future__ import absolute_import, print_function
from contextlib import contextmanager
from io import StringIO
from pathlib import Path
import sys
from invoke import task, Collection

# -- MORE TASKS:
import invoke_cleanup as cleanup


# -----------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------
BUILD_DIR = Path("build.debug")
COMPILE_COMMANDS_FILE = BUILD_DIR/"compile_commands.json"


# -----------------------------------------------------------------------------
# UTILITY FUNCTIONS
# -----------------------------------------------------------------------------
def _require_existing_source_file_or_directory(source_path, file_extension="cpp"):
    if not source_path:
        print("REQUIRES source_path (as: file or directory")
        sys.exit(1)

    source_path = Path(source_path)
    if source_path.is_dir():
        source_path = source_path/f"*.{file_extension}"
    elif not source_path.exists():
        print("FileNotFoundError: {}".format(source_path))
        # MAYBE: raise FileNotFoundError(str(source_path))
        sys.exit(2)
    return source_path


@contextmanager
def capture_output():
    """Provide a context-manager to capture-output to a stream."""
    # -- try .. finally:
    # ENSURE ON_EXIT: is used if with-block raises an exception.
    try:
        # -- ON_ENTER:
        output_stream = StringIO()
        yield output_stream
    finally:
        # -- ON_EXIT:
        print("CAPTURED_OUTPUT:")
        print(output_stream.getvalue())
        output_stream.close()


# -----------------------------------------------------------------------------
# TASKS
# -----------------------------------------------------------------------------
@task
def build(ctx):
    """Build the project (and: compile_commands.json)"""
    ctx.run("cmake-build")


@task
def _ensure_compile_database_exists(ctx):
    if not COMPILE_COMMANDS_FILE.exists():
        print("NEEDS: build")
        build(ctx)


@task(pre=[_ensure_compile_database_exists])
def clang_tidy(ctx, source_path=None):
    """Run clang-tidy on a source-file or source-directory"""
    build_dir = BUILD_DIR
    if source_path:
        source_path = _require_existing_source_file_or_directory(source_path)
    else:
        source_path = "false-negative/*.cpp"
    ctx.run(f"clang-tidy -p {build_dir} {source_path}",
            echo=True, pty=True)


@task(pre=[_ensure_compile_database_exists])
def run_clang_tidy(ctx, jobs=1):
    """Use run-clang-tidy to run clang-tidy on sources"""
    try:
        build_dir = BUILD_DIR
        ctx.run(f"run-clang-tidy -p {build_dir} -j {jobs}",
                echo=True, pty=True, hide="stderr")
        print("PASSED")
    except Exception as e:
        print("FAILED: %s:%s" % (e.__class__.__name__, e))


# -- ALTERNATIVE SOLUTION:
# @task(pre=[_ensure_compile_database_exists])
# def __run_clang_tidy_captured(ctx, jobs=1):
#     """Use run-clang-tidy to run clang-tidy on sources"""
#     try:
#         with capture_output() as output:
#             build_dir = BUILD_DIR
#             ctx.run(f"run-clang-tidy -p {build_dir} -j {jobs}",
#                     echo=True, pty=True, out_stream=output, hide="stderr")
#                     # warning=True)
#         print("PASSED")
#     except Exception as e:
#         print("EXCEPTION: %s:%s" % (e.__class__.__name__, e))
#         print("FAILED")


@task(pre=[_ensure_compile_database_exists])
def cargo_run_clang_tidy(ctx, jobs=1):
    """Use run-clang-tidy <https://github.com/lmapii/run-clang-tidy>"""
    ctx.run(f"$HOME/.cargo/bin/run-clang-tidy .clang-tidy.json -j {jobs}",
            echo=True, pty=True)


@task(pre=[_ensure_compile_database_exists])
def codechecker(ctx):
    """Run codechecker"""
    compile_commands_file = COMPILE_COMMANDS_FILE
    reports_dir = "codechecker.reports"
    reports_html_dir = "codechecker.reports_html"
    skip_file = ".codechecker.skip_file"

    # try:
    #     ctx.run(f"CodeChecker check --logfile={compile_commands_file} -o {reports_dir}")
    # except Exception as e:
    #     print("EXCEPTION: %s:%s" % (e.__class__.__name__, e))

    try:
        print(f"STEP: codechecker: Analyzing ... to {reports_dir}")
        ctx.run(f"CodeChecker analyze {compile_commands_file} --output={reports_dir}  --skip={skip_file}",
                echo=True, pty=True, warn=True)
    except Exception as e:
        print("EXCEPTION: %s:%s" % (e.__class__.__name__, e))
    print("_" * 60)
    print(f"STEP: codechecker: Generate HTML to: {reports_html_dir}")
    ctx.run(f"CodeChecker parse -e html {reports_dir} -o {reports_html_dir}",
            echo=True, pty=True)



namespace = Collection()
namespace.add_collection(Collection.from_module(cleanup), name="cleanup")
namespace.add_task(build)
namespace.add_task(clang_tidy)
namespace.add_task(run_clang_tidy)
namespace.add_task(cargo_run_clang_tidy)
namespace.add_task(codechecker)
