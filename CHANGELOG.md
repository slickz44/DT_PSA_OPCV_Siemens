# Changelog

## 1.1.0 (2026-10-23)

### Features

- Add PROFIdrive telegram 111 positioning for both lift axes, with drive behaviour simulated in the TwinCAT EmulationUnit.
- Update the TIA Portal V19 project archive with PROFIdrive integration.
- Connect the lift telegrams to the PLC process image at bytes 1020-1043 (Lift01) and 1044-1067 (Lift02), with 24 bytes in each direction.

### Fixes and documentation

- Correct the reference-speed assignment for Lift02 in the emulation configuration.
- Update the actuator drive type in the TIA project.
- Document the telegram addresses and TwinCAT drive configuration, including an updated screenshot.

See [_docs/lift-drives.md](_docs/lift-drives.md) for configuration details and simulation limitations.

# 1.0.0 (2026-10-02)


### Bug Fixes

* CapsSourceStopper - changed output signals ([08edaac](https://github.com/slickz44/DT_PSA_OPCV_Siemens/commit/08edaac9b4df4abfa101c449bd4245fd9866c269))
* compatibility ([e90748f](https://github.com/slickz44/DT_PSA_OPCV_Siemens/commit/e90748f833eb7b0bd3bc1df01b7202e7d59dfadf))
* estop signals are dual channeled now ([e515e2f](https://github.com/slickz44/DT_PSA_OPCV_Siemens/commit/e515e2f30c586b79588fd3709087e5369071ab78))
* fg01 included missing actors ([1a376b0](https://github.com/slickz44/DT_PSA_OPCV_Siemens/commit/1a376b05603159323e56cab5f43846efeb242a57))
* fg02 added mapping for camera control ([0ebdfb0](https://github.com/slickz44/DT_PSA_OPCV_Siemens/commit/0ebdfb0891909d728aa5fed55338469ed3f18bf1))
* fg05 - included camera ([d417668](https://github.com/slickz44/DT_PSA_OPCV_Siemens/commit/d4176688e7195aa3327c92f63a333d6c1d0d905c))
* first archive created ([b64a84a](https://github.com/slickz44/DT_PSA_OPCV_Siemens/commit/b64a84abadf2e149261e5c937a2e476bbcfa0b40))
* init commit ([4e886c2](https://github.com/slickz44/DT_PSA_OPCV_Siemens/commit/4e886c27ee842d9b86eb80f3e87c70e6f53d82af))
* init state ([9a50be9](https://github.com/slickz44/DT_PSA_OPCV_Siemens/commit/9a50be971abb9669d2380c53ec3a1f8df53ab75d))
* mapping iteration ([89238a2](https://github.com/slickz44/DT_PSA_OPCV_Siemens/commit/89238a23a698f3f0fd31224049fbe095ac0153b6))
* mapping updated ([89d0ef3](https://github.com/slickz44/DT_PSA_OPCV_Siemens/commit/89d0ef36969b606175612ed6261cfa70b3b95c22))
* new version ([5e35c57](https://github.com/slickz44/DT_PSA_OPCV_Siemens/commit/5e35c57dc2a26ae65828e6b2624774c481baeef8))
* PLCSim Advanced: PLC Name changed ([4f7f9d8](https://github.com/slickz44/DT_PSA_OPCV_Siemens/commit/4f7f9d880aa6d25518ca9c6a66751303c5984d1a))
* updated automatic process ([adc69a4](https://github.com/slickz44/DT_PSA_OPCV_Siemens/commit/adc69a43b5173f85115e1db78639c941b27b785c))


### Features

* add Siemens project documentation and video preview [skip ci] ([4c1c5bf](https://github.com/slickz44/DT_PSA_OPCV_Siemens/commit/4c1c5bf4771a1f6bcf8d585dc2a3ede138ace2d1))
