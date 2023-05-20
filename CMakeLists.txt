# ===========================================================================
# CMAKE: clang-tidy-mistakes
# ===========================================================================
# DESCRIPTION:
#   Example repository with C++ mistakes that can be found with clang-tidy.
#   Allows to explore "clang-tidy" and its features.
#
# EXAMPLE:
#   # -- STEP: Use CMake to build compile-database: $BUILD_DIR/compile_commands.json
#   BUILD_DIR=build
#   cmake -S . -B $BUILD_DIR -G Ninja
#   cmake --build $BUILD_DIR
#   # -- POSTCONDITION: "$BUILD_DIR/compile_commands.json" exists
#
#   # -- STEP: Use "$BUILD_DIR/compile_commands.json" with clang-tidy, ...
#   clang-tidy -p $BUILD_DIR false-negative/*.cpp
#   run-clang-tidy -p $BUILD_DIR
#
# SEE ALSO:
#  * https://github.com/polystat/clang-tidy-mistakes
#  * https://releases.llvm.org/16.0.0/tools/clang/tools/extra/docs/clang-tidy/index.html
# ===========================================================================

cmake_minimum_required(VERSION 3.20..3.26)

if(CMAKE_CURRENT_SOURCE_DIR STREQUAL CMAKE_SOURCE_DIR)
    # -- SCOPE: MASTER_PROJECT
    message(STATUS "cmake.version: ${CMAKE_VERSION}")
endif()

# --------------------------------------------------------------------------
# PROJECT:
# ---------------------------------------------------------------------------
project(clang_tidy_mistakes VERSION 0.1 LANGUAGES CXX)

if(NOT DEFINED CMAKE_EXPORT_COMPILE_COMMANDS)
    set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
endif()
if(NOT DEFINED CMAKE_CXX_STANDARD)
    set(CMAKE_CXX_STANDARD 17)
endif()
if(NOT DEFINED CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug)
endif()
message(STATUS "USING: CMAKE_CXX_STANDARD=${CMAKE_CXX_STANDARD}")
message(STATUS "USING: CMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}")
message(STATUS "USING: CMAKE_CONFIG_TYPE=$ENV{CMAKE_CONFIG_TYPE}")


# ---------------------------------------------------------------------------
# SECTION: LIBS
# ---------------------------------------------------------------------------
set(_SOURCE_PREFIX "clang-tidy-mistakes/")
add_library(cxx_false_negative)
target_sources(cxx_false_negative PRIVATE
    "${_SOURCE_PREFIX}false-negative/buffer-overrun.cpp"
    "${_SOURCE_PREFIX}false-negative/const-assignment.cpp"
    "${_SOURCE_PREFIX}false-negative/data-execution.cpp"
    "${_SOURCE_PREFIX}false-negative/dependency-loop.cpp"
    "${_SOURCE_PREFIX}false-negative/destructor-exception.cpp"
    "${_SOURCE_PREFIX}false-negative/duplicated-delete.cpp"
    "${_SOURCE_PREFIX}false-negative/float-loop.cpp"
    "${_SOURCE_PREFIX}false-negative/function-cast.cpp"
    "${_SOURCE_PREFIX}false-negative/global-null.cpp"
    "${_SOURCE_PREFIX}false-negative/infinite-recursion.cpp"
    "${_SOURCE_PREFIX}false-negative/inifite-goto.cpp"
    "${_SOURCE_PREFIX}false-negative/long-loop.cpp"
    "${_SOURCE_PREFIX}false-negative/memcpy-buffer-overrun.cpp"
    "${_SOURCE_PREFIX}false-negative/noexcept-crash.cpp"
    "${_SOURCE_PREFIX}false-negative/null-escaping.cpp"
    "${_SOURCE_PREFIX}false-negative/stack-corruption.cpp"
    "${_SOURCE_PREFIX}false-negative/thread-invalid-stack.cpp"
    "${_SOURCE_PREFIX}false-negative/thread-recursion.cpp"
    "${_SOURCE_PREFIX}false-negative/unhandled-exception.cpp"
    "${_SOURCE_PREFIX}false-negative/virtual-call-constructor.cpp"
    "${_SOURCE_PREFIX}false-negative/virtual-div-by-zero.cpp"
)
