# Siemens — TIA port

**Work in progress.** The Unity side is real: this vendor has its own scene, its own operator panel
and its own context export, and the root build reads them. The **control** side does not exist yet —
there is no TIA program, no knowledge base and no tooling in this module.

**This module is its own git repository**, cloned into the main repo's root as `Siemens/` and
gitignored there so the two do not collide. It is declared in the main repo's
`_workflow/config/modules.json` with `knowledgeBase: false`, which is how the root pages know it exists
while linking to no page it has not written. It publishes **zero wiki pages, by design.**

Read the main repo's [`CLAUDE.md`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/CLAUDE.md)
for the machine, the twin, and the behaviour contracts a Siemens implementation will have to honour.

## What is real

The Unity scene and its exports live in the **main** repository, not here — the twin is one project
and every vendor scene instances the same prefab.

| Path | What |
|---|---|
| main repo `Unity/Assets/Demo_1/Scenes/VC_Demo_1_Siemens_1.unity` | This vendor's scene. Instances `Machine_1.prefab` and adds the Siemens operator panel |
| main repo `Unity/Assets/StreamingAssets/VC_Demo_1_Siemens_1_Context.json` | Its context export, read by the root build |
| main repo `Unity/Assets/StreamingAssets/VC_Demo_1_Siemens_1_Project_Tree.xml` | Its device tree — byte-identical to Beckhoff's, because the panel buttons are aggregated and generate no device of their own |
| `module.json` | This module's identity — name, vendor, version, platform. **`version` is written by the release**, never by hand |
| `.github/workflows/release.yml` | **This module's own release line.** semantic-release on `master`: previews the version on the PR, then writes `module.json` and `CHANGELOG.md`, tags, and publishes. No wiki job — there is no `_docs/` yet |
| `.releaserc.json` | The semantic-release plugin list. **No `@semantic-release/npm`** — there is no `package.json` here, so `module.json` is the version record |
| `_workflow/tools/set_module_version.py` | Writes that version. Called from `.releaserc.json`'s exec step; run it bare to read the current one |
| `_data/` | Vendor source material — PLC tag exports (`PLCTags_*.xlsx`), the project tree info, notes. **Read only on explicit permission from the user** |

**The first release must be preceded by a `v0.1.0` tag.** With no tag in the repository
semantic-release publishes **1.0.0** whatever `module.json` reads, and this module is deliberately
on a 0.x line — the control side does not exist, and the main repo declares it as `tested: 0.1.0`.
Push `v0.1.0` first and the bumps start from there. The workflow's header says so too, because that
is where somebody will be standing when it matters.

### The Siemens operator panel

`H_ControlPanel` → `MAIN.FG_System.H_ControlPanel_Siemens`, a `PanelSampler` aggregating seven
controls: `CONTROL ON/OFF`, `OP MODE` (a `SwitchRotary`, not a button), `SINGLE STEP`, `AUTO START`,
`AUTO STOP`, `ERROR ACK`, `RESET`.

This is the **only** thing that differs from the Beckhoff scene — 171 of the twin's nodes are
identical, because they all come from the shared `Machine_1` prefab. The root pages are rendered
from the Beckhoff scene, so this panel does not appear there; what does appear is Beckhoff's,
marked `†` to say it is one vendor's example rather than the machine's.

**The panel is under-documented.** The `H_ControlPanel` node itself carries no authored context at
all, and `CONTROL ON/OFF` carries none either — the other six have a `Function`. Those are gaps, not
facts: ask the user and author them with `authoring-context-nodes`, do not infer them from the
Beckhoff panel, whose buttons are PackML states and mean different things.

## What is not here

| Path | What |
|---|---|
| `TIA_1/` | **A parked TwinCAT template, not the TIA program.** The default project from an earlier iteration, kept as scratch. Do not read it to answer a question, do not generate against it, and do not document it |

## When the control side becomes real

It needs the same shape every vendor module has, and nothing more:

```
Siemens/
  module.json          already here - `version` is the release's to write, not yours
  CLAUDE.md            tracked one-line stub: @_workflow/CLAUDE.md
  _docs/               TRACKED - what the machine is, on this platform
    01-*.md ...        user documentation - setup, usage, architecture
    context/           GENERATED - what TIA makes of the machine
    reference/         hand-written, platform-specific
  _workflow/           TRACKED - how this module is worked on
    CLAUDE.md          this file, rewritten with the platform's own hard rules
    README.md          how the skills chain
    skills/            directory-scoped, appearing as Siemens:<name>
    config/handoff/    the COMMITTED copy of .machine.json. Creating it is the opt-in
    tools/             already here: set_module_version.py. Add build_wiki.py and
                       publish_wiki.py beside it when _docs/ appears, and give
                       release.yml the wiki gate and the wiki job Beckhoff's has
  _private/            GITIGNORED - its own repository
    tools/             a builder that reads _workflow/config/handoff/.machine.json
```

The split is the same one the main repository uses, and it falls in one place: **`_private/` is the
Python generators and nothing else.** Everything about *how* the module is built — the skills, the
guideline, the config — is public in `_workflow/`, because a reader is entitled to it. The handoff
is a generator input, but it must be *committed* for this module to build from a standalone clone,
so it sits with the other configs under `_workflow/config/`.

Then flip `knowledgeBase` to `true` in the main repo's `_workflow/config/modules.json`, and the root pages
start linking these pages instead of saying none exist yet.

Four rules govern how it plugs in, all already enforced on the Beckhoff side:

- **Read `_workflow/config/handoff/.machine.json` — this module's own committed copy — never the Unity
  export, never the root generator, and never a path across `../`.** That copy is the whole coupling
  to the main repo: the machine's structure as JSON, schema-versioned, written there by
  `build_knowledge.py` and copied here by `sync_machine.py`. It is committed so this module builds
  from a standalone clone, where the main repository is simply absent. A consumer that does not
  recognise the schema must refuse rather than guess.
- **A link back to the main repo is an absolute URL.** `../../../_docs/…` climbs out of this
  repository and is dead in a standalone clone.
- **Read `vendors["Siemens"]`, not `groups`.** The top-level `groups` is the *reference* scene, which
  is Beckhoff's; `vendors["Siemens"].groups` is this scene's own view, complete, with this panel in
  it. Taking the reference would silently document Beckhoff's panel as Siemens'.
- **Behaviour is not written here.** Sequences, interlocks, fault codes and the reset model live in
  [`_docs/reference/`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/reference/transport-behaviour.md)
  in the main repo, as machine-level contracts. This module documents its *realisation* of them,
  never a second version of them.

**One line in the main repo makes these pages visible:** `knowledgeBase: true` in
`_workflow/config/modules.json`. That is deliberate rather than discovered — the root pages are tracked, so
their content must not depend on which optional modules a given user happened to clone.
