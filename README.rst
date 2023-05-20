EXPLORE: clang-tidy
===============================================================================

:Category: static code analysis for C++/C

`clang-tidy`_ is a static code analysis tool (as: checker, linter) for C++.
`clang-tidy`_ is part of the `clang-tools-extra`_ collection of C++ tools.

This area is used to explore `clang-tidy`_ and how it can be used.

SUMMARY:

* Use `clang-tidy`_ for only one file or directory
* Use `run-clang-tidy`_ in parallel for a complete project
  (or use OTHER `clang-tidy`_ runners)

* The Rust-based `cargo-run-clang-tidy`_ tool
  looks really interesting (usability is better than the original `run-clang-tidy`_)

* Use codechecker to detect more errors and better explanations.

  **HINT:** codechecker runs `clang-tidy`_ , `cppcheck`_ and ...

SEE ALSO:

* https://clang.llvm.org/extra/clang-tidy/
* https://clang.llvm.org/extra/index.html

SOURCE CODE REPOS:

* https://github.com/llvm/llvm-project
* https://github.com/llvm/llvm-project/tree/main/clang-tools-extra

RELATED: Examples as project to explore clang-tidy

* https://github.com/polystat/clang-tidy-mistakes
  EXAMPLES: that clang-tidy can find

RELATED: Articles on clang-tidy

* https://www.kdab.com/clang-tidy-part-1-modernize-source-code-using-c11c14/

.. _clang-tidy: https://clang.llvm.org/extra/clang-tidy/
.. _clang-tools-extra: https://clang.llvm.org/extra/index.html
.. _cppcheck: http://cppcheck.net
.. _run-clang-tidy: https://clang.llvm.org/extra/doxygen/run-clang-tidy_8py_source.html
.. _cargo-run-clang-tidy: https://github.com/lmapii/run-clang-tidy


USE: clang-tidy, run-clang-tidy
-------------------------------------------------------------------------------

CONFIG-FILE EXAMPLE: $HERE/.clang-tidy

* ``Checks``: Leading MINUS sign disables a rule / rule-set
* ``Checks``: List of rules / rule-sets separated with comma
* ``WarningsAsErrors``: Same syntax as ``Checks``.
* ``WarningsAsErrors = "*"`` enables all check-warnings as errors
* ``WarningsAsErrors = ""`` (EMPTY-STRING) disables check-warnings as errors

.. code::

    ---
    Checks: "-*,
        bugprone-*,
        cert-*,
        modernize-*,
        clang-diagnostic-*,
        -clang-analyzer-*,
        cppcoreguidelines-*,
        -readability-*,
        -llvmlibc-*
        "
    WarningsAsErrors: ""
    HeaderFilterRegex: ""
    FormatStyle:     none
    ...

The usage of `clang-tidy`_ can be simplified if your build-system generates a
compile-time database:

.. code:: cmake

    # -- FILE: CMakeLists.txt
    cmake_minimum_required(VERSION 3.20..3.26)

    # SAME AS: cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON ...
    # ASSET:  ${CMAKE_BUILD_DIR}/compile_commands.json
    if(NOT DEFINED CMAKE_EXPORT_COMPILE_COMMANDS)
        set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
    endif()


Use `clang-tidy`_ to work on one file (or some files only):

.. code:: bash

    # -- USE: clang-tidy on one source-file
    # REQUIRES: ${BUILD_DIR}/compile_commands.json
    # SIMILAR to cmake-build: cmake --workflow --preset=debug
    $ cmake-build
    $ clang-tidy -p ${BUILD_DIR} src/some_file.cpp

    # -- USE: clang-tidy on a source-directory
    $ clang-tidy -p ${BUILD_DIR} src/some_dir/*.cpp


.. code:: bash

    # -- HINT: run-clang-tidy can run multiple jobs in parallel.
    # REQUIRES: ${BUILD_DIR}/compile_commands.json
    export BUILD_DIR="build"
    $ cmake-build
    $ run-clang-tidy -p ${BUILD_DIR}



.. code:: bash

    # -- GENERATE HTML-REPORT: From clang-tidy output
    # REQUIRES: pip install clang-html
    # SEE: https://github.com/austinbhale/clang-tidy-html
    $ clang-tidy -p ${BUILD_DIR} src/some_dir/*.cpp > __clang_tidy_output.log
    $ clang-tidy-html -o __clang_tidy_output.html __clang_tidy_output.log




USE: clang-tidy WarningsAsErrors
-------------------------------------------------------------------------------

Config-file schema::

    WarningsAsErrors : string = "rule-names"
    # -- SAME SYNTAX AS: Checks : string = "rule-names"

Enable all warnings as errors (use: ``"*" = match-any-checker``):

.. code::

    ...
    WarningsAsErrors: "*"
    ...

Disable all warnings as errors (use: ``"" = EMPTY_STRING``):

.. code::

    ...
    WarningsAsErrors: ""
    ...



USE: run-clang-tidy (Rust based; aka: cargo-run-clang-tidy)
-------------------------------------------------------------------------------

Install the `Rust`_ based tool by using the `cargo`_ build system (and package manager):

.. code:: bash

    # -- PRECONDITION: Rust is installed (with: rustup)
    # HINT: Normally installed under "$HOME/.cargo/bin"
    $ cargo install run-clang-tidy

Use it:

.. code:: bash

    # -- ASSUMPTION: Rust is installed in the $HOME directory of the user.
    # SAME NAME: This tool and "run-clang-tidy" (from: clang-extra-tools)
    $ cmake-build
    $ $HOME/.cargo/bin/run-clang-tidy .clang_tidy.json

    # -- RUN PARALLEL: With 4 jobs
    $ $HOME/.cargo/bin/run-clang-tidy .clang_tidy.json --jobs=4


CONFIG-FILE EXAMPLE: ``.clang_tidy.json``

.. code:: json

    {
        "paths": [
            "clang-tidy-mistakes/**/*.cpp"
        ],
        "buildRoot": "build"
    }

A more complex config-file example:

.. code:: json

    {
        "paths": [
            "clang-tidy-mistakes/**/*.cpp"
        ],
        "buildRoot": "build",
        "tidyFile": ".clang-tidy",
        "tidyRoot": ".",
        "command": "/usr/local/opt/llvm/bin/clang-tidy"
    }

HINT:

* You may need to set ``WarningsAsErrors = "bugprone-*"`` (or similar)
  in the `.clang_tidy` config-file to see warnings.

ADVANTAGES:

* Makes it easy to select source-files from one or multiple sub-directory(s)
* Runs in parallel by using the ``-jobs`` command-line option
* Readable output


SEE ALSO:

* https://github.com/lmapii/run-clang-tidy
* https://crates.io/crates/run-clang-tidy

RELATED: Rust

* https://www.rust-lang.org
* https://doc.rust-lang.org/cargo/index.html

.. _cargo: https://doc.rust-lang.org/cargo/index.html
.. _Rust: https://www.rust-lang.org


USE: Ericsson CodeChecker
-------------------------------------------------------------------------------

.. code:: bash

    CodeChecker check --logfile $BUILD_DIR/compile_commands.json -o codechecker.reports/
    CodeChecker parse -e html codechecker.reports -o codechecker.reports_html

    # -- ALTERNATIVE:
    # CodeChecker analyze $BUILD_DIR/compile_commands.json --enable sensitive --output codechecker.reports
    CodeChecker analyze $BUILD_DIR/compile_commands.json --output codechecker.reports --skip=.codechecker.skip_file
    CodeChecker parse -e html codechecker.reports -o codechecker.reports_html

EXMAPLE: .codechecker.skip_file (see: https://codechecker.readthedocs.io/en/latest/analyzer/user_guide/#skip-file )

.. code::

    -/Applications/*
    +*/*.cpp

NICE POINTS:

* HTML reports of code-analyzer warnings are excellent.
  REASON: Explains what the problem is (and which checker found it).

* Runs "clang-tidy", "cppcheck" and ...
  NOTE: Detects more bugs than "clang-tidy" alone.

* Shows summary of problem classes with severiry and counts (after checks run)

SAD POINTS:

* Rather complicated command-line options

RESOLVED:

* Shows problems from system-headers (XCode)
  SOLVED-BY: Use SKIP_FILE with exclude-patterns

SEE ALSO:

* https://github.com/Ericsson/codechecker
* https://codechecker.readthedocs.io/en/latest/
* https://github.com/Ericsson/codechecker/blob/master/docs/config_file.md
* https://codechecker.readthedocs.io/en/latest/analyzer/user_guide/#skip-file
* https://codechecker.readthedocs.io/en/latest/tools/tu_collector/#create-skip-file-from-source-files-that-need-to-be-reanalyzed



USE: cppcheck as C++ static code analysis tool
-------------------------------------------------------------------------------

.. code:: bash

    # -- EXPECT: cppchecks finds "Division by zero"
    # NOTE: Not found by clang-tidy
    $ cppcheck --cppcheck-build-dir=$BUILD_DIR false-negative/long-loop.cpp
    Checking false-negative/long-loop.cpp ...
    false-negative/long-loop.cpp:8:13: error: Division by zero. [zerodiv]
    sum += 42 / i;
                ^
    false-negative/long-loop.cpp:7:20: note: Assuming that condition 'i>=0' is not redundant
    for (int i = 4; i >= 0; i--) {
                    ^
    false-negative/long-loop.cpp:8:13: note: Division by zero
    sum += 42 / i;
                ^

USE: cpp-linter
-------------------------------------------------------------------------------

:Hint: clang-tidy runner

.. code:: bash

    # -- SHELL=bash
    # PRECONDITION: pip install cpp-linter
    # REQUIRES: $BUILD_DIR/compile_commands.json
    $ cpp-linter -p $BUILD_DIR > __cpp_linter_output.log 2>&1
    $ clang-tidy-html -o __cpp_linter_output.html __cpp_linter_output.log


SEE ALSO:

* https://github.com/cpp-linter/cpp-linter


USE: processcdb
-------------------------------------------------------------------------------

:Hint: clang-tidy wrapper

.. code:: bash

    # PRECONDITIONS:
    #   * $BUILD_DIR/compile_commands.json exists
    #   * REQUIRES: pip install processcdb
    $ processcdb --tool clang-tidy --cdb $BUILD_DIR/compile_commands.json --output=__processcdb_scan.log
    $ clang-tidy-html -o __processcdb_scan.html __processcdb_scan.log

SEE ALSO:

* https://github.com/rasjani/processcdb


SCRATCHPAD
-------------------------------------------------------------------------------

RELATED TO: clang-tidy

* https://github.com/sasq64/autotidy
* https://github.com/mloskot/clang-tidy-test (uses: autotidy)


