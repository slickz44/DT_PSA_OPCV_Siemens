# DT_PSA_OPCV — Siemens

The Siemens port of [DT_PSA_OPCV](https://github.com/Preliy/DT_PSA_OPCV) — the Digital Twin for Laser Welding & Assembly System (PSA OPCV), a complete production line that exists as a
digital twin and is driven by a real PLC program.

> **Work in progress. There is no TIA program here yet.**
>
> What exists is the Unity side — this vendor has its own scene, its own operator panel and its own
> context export — and those live in the **main** repository, because the twin is one project and
> every vendor scene instances the same machine prefab. This repository holds the source material a
> TIA implementation will start from, and nothing else.

## How this is used

It is a module of the main repository: you clone it **into** that repo's root, as `Siemens/`.

```bash
git clone https://github.com/Preliy/DT_PSA_OPCV.git
cd DT_PSA_OPCV
git clone https://github.com/Preliy/DT_PSA_OPCV_Siemens.git Siemens
```

The main repo gitignores `/Siemens/`, so the two git repositories do not collide — inside here
everything is an ordinary checkout on an ordinary branch. Which versions pair with which is in the
main repo's [COMPATIBILITY.md](https://github.com/Preliy/DT_PSA_OPCV/blob/master/COMPATIBILITY.md).

## What is here

| Path | What |
|---|---|
| `CLAUDE.md` | The module's contract: what is real, what is not, and the rules a TIA implementation has to plug in under |
| `module.json` | This module's identity — name, version, which main-repo version it needs |
| `_data/` | Source material: PLC tag exports (`PLCTags_*.xlsx`), project tree info, design notes |
| `TIA_1/` | **A parked TwinCAT template, not the TIA program** — see below |

## `TIA_1/` is not the TIA program

Despite the name, `TIA_1/` contains a default **TwinCAT** project left over from an earlier
iteration of this work. It is scratch, kept only because it may hold a stray note worth recovering.

**Do not read it to answer a question, do not generate against it, and do not document it.** Nothing
in this project treats it as a source.

## What it will become

The shape is already settled, and it is the same one the Beckhoff module uses — a published `_docs/`
holding a committed machine handoff, a generated knowledge base and hand-written platform
reference, a `_workflow/` holding the skills and the machine handoff, and a gitignored `_private/`
holding the Python tools.
`CLAUDE.md` has the layout and the four rules that govern it.

The machine's **behaviour** is not defined here and never will be. Sequences, interlocks, fault
codes and the reset model are machine-level contracts every control platform must honour, and they
live in the main repository's
[`_docs/reference/`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/reference/transport-behaviour.md).
This module will document its *realisation* of them, never a second version of them.

Help is welcome — see the main repo's
[CONTRIBUTING.md](https://github.com/Preliy/DT_PSA_OPCV/blob/master/CONTRIBUTING.md) and
[How to connect a control system](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/05-connecting-a-control-system.md).

## License

[GPL-3.0](https://github.com/Preliy/DT_PSA_OPCV/blob/master/LICENSE) — Copyright © 2026 Viktor Gaponenko.
