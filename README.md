# DT_PSA_OPCV — Siemens PLC & HMI

One machine. Reusable control modules. Virtual commissioning with TIA Portal.

## See it in action

![Virtual commissioning with TIA Portal — modularization and standardization](_docs/images/video-thumbnail.png)

The Siemens walkthrough is in preparation. The video link will be added here when it is ready.

## What is it?

The Siemens implementation of [DT_PSA_OPCV](https://github.com/Preliy/DT_PSA_OPCV) — the Digital Twin for Laser Welding & Assembly System (PSA OPCV).

**Maintained by [Andreas Fast (slickz44)](https://github.com/slickz44).** This module continues the Siemens repository originally provided by Viktor Gaponenko. The Unity digital twin remains in the main repository; this repository provides the Siemens PLC/HMI project and the associated emulation files.

The focus is **modularization and standardization**: a consistent structure for machine control, station control, actuators, step sequences and HMI operation. Explore the program against a simulated machine and follow how the same control pattern is applied across its function groups.

## Who is it for?

Controls engineers exploring a reusable PLC structure, students learning how machine and station control fit together, and anyone interested in virtual commissioning with Siemens TIA Portal.

## Getting started

**Want to inspect the PLC and HMI project?** [Open the TIA Portal V19 archive](TIA_1/Archive/DT_PSA_OPCV.zap19), select **Download raw file**, then retrieve it in TIA Portal V19.

**Want all Siemens files?** [Download this repository as a ZIP](https://github.com/slickz44/DT_PSA_OPCV_Siemens/archive/refs/heads/master.zip) and extract it. While this repository is private, sign in with an account that has access.

**Want to connect it to the digital twin?** Download or clone the main project and this Siemens module as shown below, then follow the [Siemens setup guide](_docs/setup.md). Siemens engineering software and the required runtime components are installed separately.

## How this is used

This is a module of the main repository. Clone it into the main repository's root as `Siemens/`:

```bash
git clone https://github.com/Preliy/DT_PSA_OPCV.git
cd DT_PSA_OPCV
git clone https://github.com/slickz44/DT_PSA_OPCV_Siemens.git Siemens
```

The main repository ignores `/Siemens/`, so the twin and the Siemens module keep their own Git histories. If a `Siemens/` folder already exists, use that checkout rather than cloning over it.

For a download without Git, use **Code → Download ZIP** on each repository. Extract this module into the main project's `Siemens/` folder.

## Download the Siemens project

**[TIA Portal V19 project archive](TIA_1/Archive/DT_PSA_OPCV.zap19)** — on the file page, select **Download raw file**.

The same archive is included when downloading the whole repository as a ZIP. Retrieve it in TIA Portal V19. The engineering software, runtime licenses and required third-party libraries must be installed separately.

## What is here

| Path | Contents |
|---|---|
| `TIA_1/Archive/` | Siemens TIA Portal V19 project archive |
| `TIA_1/EmulationUnit/` | TwinCAT-based emulation project and Open Commissioning connection configuration used with the Siemens environment |
| `_data/` | Existing source material, including PLC tag exports and project/design information |
| `_docs/` | Siemens setup documentation, architecture illustration and demonstration screenshots |
| `_workflow/` | Existing module workflow material and tooling |
| `.github/` | Existing GitHub automation |
| `module.json` | Module identity, version, repository and main-project reference |

`TIA_1/` now contains a Siemens project archive alongside the emulation project. The emulation project uses TwinCAT; the machine control program is supplied in the TIA archive.

## Siemens PLC architecture

![Modular PLC system architecture](_docs/images/plc-architecture.png)

The Siemens contribution organizes control into a machine layer and station-level function groups:

- `MachineMain` and `MachineControl` coordinate machine signals, operating modes, homing, automatic operation, single-step operation and fault acknowledgement.
- Function groups organize the individual stations and transport.
- Station control derives local signals for manual operation, automatic start/stop, fault handling and motion enable.
- Actor control provides dedicated calls for the station's motors, cylinders, valves and other actuators.
- Step sequences describe the station process and pause in defined states.
- Function-group data blocks hold station data and support signal exchange between groups.

The architecture illustration explains the intended structure; the retrieved TIA project is the source for its actual implementation.

## HMI operation

![Machine and function-group overview](_docs/images/hmi-overview.png)

The HMI overview shows the machine, function groups FG 1–5 and transport together. It supports inspecting their operating and status indications. The supplied screenshots use German HMI labels.

## Run the project

1. Obtain the main digital twin and this Siemens module.
2. Retrieve `TIA_1/Archive/DT_PSA_OPCV.zap19` in TIA Portal V19.
3. Compile the PLC and HMI and resolve any missing engineering components.
4. Prepare the PLCSIM Advanced instance and the emulation project.
5. Open the corresponding Siemens scene in the digital twin and check communication.
6. Start the HMI simulation and verify the machine's initial state before operation.

See the [Siemens setup guide](_docs/setup.md) for the observed software baseline and connection settings.

**Documentation status:** The screenshots show the demonstration environment. These instructions and the supplied archive have not yet been validated as a complete clean-install procedure. The exact matching twin revision, dependency versions and startup sequence remain to be recorded.

## Relationship to the main project

Machine behavior — sequences, interlocks, fault codes and the reset model — is defined by the main project's [reference documentation](https://github.com/Preliy/DT_PSA_OPCV/tree/master/_docs/reference). This module documents the Siemens implementation of those contracts.

The main project's [compatibility information](https://github.com/Preliy/DT_PSA_OPCV/blob/master/COMPATIBILITY.md) provides the shared compatibility context. The new maintainer URL and tested Siemens/twin version pairing should also be recorded there when coordinated with the main project.

## Contributing

For Siemens-specific questions and improvements, use this repository's Issues and pull requests. For changes to the shared machine or Unity twin, start with the main project's [contribution guide](https://github.com/Preliy/DT_PSA_OPCV/blob/master/CONTRIBUTING.md).

## Credits and license

- **Andreas Fast (slickz44)** — Siemens module maintainer and Siemens PLC/HMI contribution.
- **Viktor Gaponenko** — original repository foundation and the main digital-twin project.
- **Open Commissioning** — digital-twin and emulation framework.

[GPL-3.0](https://github.com/Preliy/DT_PSA_OPCV/blob/master/LICENSE). Original attribution retained: Copyright © 2026 Viktor Gaponenko. Existing third-party notices continue to apply to their respective components.
