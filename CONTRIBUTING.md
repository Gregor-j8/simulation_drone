# Contributing

## Commit discipline

- **Green tree, always.** Every commit builds, all tests pass, static analysis is
  clean. If a feature needs several commits, the intermediate ones still pass
  (mark not-yet-covered tests `skip`, never leave them red).
- **Small.** Aim for under ~300 lines of diff, one idea per commit.
- **Test lands with the code** in the same commit for a unit; a subsystem may
  split across commits.
- **Requirements move with the commit** that implements and tests them: flip the
  row in `docs/traceability.csv` from `planned` to `passing`, add it to
  `docs/requirements.md` if new.

## Commit message

```
area: imperative summary

Why this change (not what — the diff shows what).

Co-Authored-By: ...
Claude-Session: ...
```

`area` ∈ `sim` · `fcs` · `sitl` · `hw` · `tools` · `ci` · `docs`.

## Branching

One branch + PR per milestone (`m1-dynamics`, `m2-loop`, …). Track H commits go
on `track-h`. Never commit to `main` directly; never force-push or merge `main`.

## Local setup

```
python -m venv .venv
.venv/Scripts/python -m pip install -e ".[dev]"     # Windows
# source .venv/bin/activate on Linux/WSL

.venv/Scripts/python -m pytest -q                   # Python tests
cmake -S . -B build -G Ninja && cmake --build build && ctest --test-dir build
```

CI (GitHub Actions, Linux) is the source of truth. The order this is all built
in is [`docs/build-plan.md`](docs/build-plan.md).
