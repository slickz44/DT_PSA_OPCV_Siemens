# v1.1.0 - PROFIdrive Telegram 111

This release adds PROFIdrive telegram 111 support for the two lift axes of the digital twin.

## What's new

- Updated TIA Portal V19 project archive with PROFIdrive integration.
- Telegram 111 drive behaviour simulation in the TwinCAT EmulationUnit.
- Lift process-data mapping: 24 bytes in each direction, starting at byte 1020 for Lift01 and byte 1044 for Lift02.
- Corrected Lift02 reference-speed assignment and updated actuator drive type.
- Updated drive setup documentation and TwinCAT configuration screenshot.

## Download and setup

Retrieve `DT_PSA_OPCV.zap19` in TIA Portal V19. The archive is included under `TIA_1/Archive/` in the source ZIP; it can also be attached to this release as a separate download.

Use the Siemens archive and TwinCAT EmulationUnit from this same release together. Follow the [setup guide](https://github.com/slickz44/DT_PSA_OPCV_Siemens/blob/v1.1.0/_docs/setup.md) and [lift drive documentation](https://github.com/slickz44/DT_PSA_OPCV_Siemens/blob/v1.1.0/_docs/lift-drives.md) for communication, telegram mapping and scaling.

## Simulation scope

The drive model supports the implemented telegram 111 positioning behaviour; it is not a complete simulation of every SINAMICS function. The lift drive documentation lists the supported behaviour and remaining limitations.

Thank you to @Preliy for the digital twin and the contribution to the lift drive simulation.
