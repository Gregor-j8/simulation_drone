# Coding standard (seed) — finalized in M6

Production-grade code: clean, maintainable, well-structured, built on a small set
of well-chosen libraries rather than hand-rolled substitutes. MISRA-C *in spirit*
where it does not fight maintainability — the goal is to show awareness of what
safety-critical embedded code demands and apply it where it is cheap.

## Dependencies

**`fcs/` (C++) — curated allowlist, nothing else:**

| Library | Use | Notes |
|---|---|---|
| Eigen | linear algebra (attitude, EKF, filters) | header-only; fixed-size types only in the loop path (no dynamic `MatrixXd`) |
| ETL (Embedded Template Library) | fixed-capacity containers, state machines | STL-shaped API without heap |
| a units library (e.g. `mp-units`) | compile-time unit safety on physical quantities | keeps NED / SI discipline enforced by the type system |
| GoogleTest | tests only | not linked into `fcs` |

Adding anything else to `fcs/` is a reviewed decision recorded in
`docs/deviations.md`. `sim/` and `tools/` (Python) use numpy / scipy / pandas /
matplotlib / pyyaml freely.

## C++ (`fcs/`)

- **Language:** C++20, no compiler extensions (`-std=c++20 -pedantic`).
- **Warnings are errors:** `-Wall -Wextra -Werror -Wconversion -Wshadow`.
- **No heap allocation after init** in the loop path; fixed-capacity containers
  (ETL) only.
- **No exceptions, no RTTI** in the loop path. Errors return a single `Result<T>`
  / status enum; status returns are `[[nodiscard]]`.
- **No implicit narrowing.** Fixed-width integers; physical quantities carry
  units via the type system.
- **`enum class` only**; every `switch` over an enum is exhaustive (`-Werror=switch`,
  no catch-all `default`).
- **Bounded loops** — every loop has a statically reasoned bound.
- **`const` / `constexpr` by default**; no mutable globals — dependencies are
  injected.
- **Core modules (estimator, controller, FSM, mixer, voter, dsp, power) stay
  STL-free / behind a thin porting layer** so they compile under Zephyr and run
  inside Renode.
- Formatting: `clang-format` (LLVM base, 100 cols). Lint: `clang-tidy` +
  `cppcheck`, both clean.
- **Deviations** recorded in `docs/deviations.md` with an ID, rule, reason, scope.

## Comments

Comments explain **why**, not **what**. Delete restating comments, commented-out
code, and boilerplate banners. Keep: rationale for a non-obvious choice, the units
/ frame of a quantity where the type does not carry it, references to a
requirement ID or a datasheet, and warnings about ordering or timing hazards.
Every public function has a one-line doc comment stating its contract.

## Python (`sim/`, `tools/`)

- `ruff` clean (lint + format), `mypy --strict` clean.
- Type hints on all public functions. No bare `except`.
- Physics constants and units documented at definition; SI everywhere, NED frame.
- Every electrical / physical model parameter cites its source (datasheet or
  ngspice result) and traces to `docs/hardware.md` (HW-003).
