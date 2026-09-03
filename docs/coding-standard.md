# Coding standard (seed) — finalized in M6

MISRA-C *in spirit*, not to the letter. The point is to demonstrate awareness of
what safety-critical embedded code demands and to apply it where it is cheap.

## C++ (`fcs/`)

- **Language:** C++20, no compiler extensions (`-std=c++20 -pedantic`).
- **Warnings are errors:** `-Wall -Wextra -Werror -Wconversion -Wshadow`.
- **No heap allocation after init** in the loop path. No `new`/`delete` in hot
  code; fixed-capacity containers only.
- **No exceptions, no RTTI** in the loop path. Errors returned via a single
  `Result<T>` / status enum; status returns are `[[nodiscard]]`.
- **No implicit narrowing.** Fixed-width integer types (`std::int32_t` …).
- **`enum class` only**, and every `switch` over an enum is exhaustive (no
  `default:` that hides a missing case — rely on `-Werror=switch`).
- **One entry, bounded loops.** Every loop has a statically reasoned bound.
- **`const` by default**, `constexpr` where possible, no mutable globals (DI
  instead).
- **Core modules (estimator, controller, FSM, mixer, voter) stay STL-free or
  behind a thin porting layer** so they can compile under Zephyr.
- Formatting: `clang-format` (LLVM base, 100 cols). Lint: `clang-tidy` +
  `cppcheck`, both clean.
- **Deviations** are recorded in `docs/deviations.md` with an ID, the rule, the
  reason, and the scope.

## Python (`sim/`, `tools/`)

- `ruff` clean (lint + format), `mypy --strict` clean.
- Type hints on all public functions. No bare `except`.
- Physics constants and units documented at definition; SI everywhere, NED frame.
