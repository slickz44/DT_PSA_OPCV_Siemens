# Siemens setup guide

## 1. Prepare the software

The available files and demonstration screenshots identify the following environment. This is an observed baseline, not a tested compatibility matrix.

| Component | Evidence in the supplied material |
|---|---|
| TIA Portal V19 | `.zap19` archive containing `DT_PSA_OPCV.ap19` |
| S7-PLCSIM Advanced V6.0 Update 1 | Demonstration screenshot |
| WinCC Runtime Advanced | Demonstration screenshot; exact version to be confirmed |
| S7-1500 / CPU 1516F-3 PN/DP | Demonstration screenshot |
| TwinCAT 3.1.4026 | EmulationUnit project metadata; files contain differing patch versions |
| Open Commissioning | Referenced by the emulation project; obtain the required dependencies separately |
| Unity digital twin | Separate [DT_PSA_OPCV repository](https://github.com/Preliy/DT_PSA_OPCV); matching revision to be confirmed |

Use a Windows engineering environment with the appropriate Siemens and Beckhoff components installed. TIA Portal will report any additional packages needed by the archived project.

## 2. Retrieve the TIA project

1. Download this repository with **Code → Download ZIP** and extract it.
2. Start TIA Portal V19.
3. Use the project retrieval/open workflow for `TIA_1/Archive/DT_PSA_OPCV.zap19` and choose a writable destination.
4. Open the retrieved project and inspect its device configuration.
5. Compile the PLC and HMI. Resolve missing packages or compilation errors before continuing.

The archive includes both a V19 project file and HMI-related data. Its completeness must be confirmed by retrieval and compilation in TIA Portal.

## 3. Prepare the simulated PLC

![PLCSIM Advanced control panel](images/plcsim-advanced.png)

The demonstration uses an S7-1500 instance named `DT_PSA_OPCV` and shows the **PLCSIM** online-access option.

1. Start PLCSIM Advanced.
2. Create/start the instance with the name `DT_PSA_OPCV`.
3. Select the corresponding simulated PLC in TIA Portal, download the project and put the simulated CPU into RUN.

The instance name matters: `OC.Assistant.xml` refers to that exact name. Adapt network settings to the local environment instead of assuming that an address visible in a screenshot applies to your machine.

## 4. Prepare the emulation connection

`TIA_1/EmulationUnit/` contains a TwinCAT solution used alongside the Siemens project. Its configuration declares:

| Setting | Supplied value |
|---|---|
| Plugin type | `PlcSimAdvanced` |
| Channel type | `TcAdsChannel` |
| PLC instance | `DT_PSA_OPCV` |
| Input/output size | 1024 bytes each |
| Input/output address range | `0-1023` |
| CycleTime value | `10` |

Open `EmulationUnit.sln` in the corresponding TwinCAT engineering environment and resolve its library references, including `OC_Core`. Generated runtime files, cached libraries and trial-license files are excluded from this package.

The XML establishes the intended PLCSIM connection; it does not by itself prove a working end-to-end setup. Confirm the Open Commissioning version, target selection, routing and activation order against the working demo before attempting a full run.

## 5. Connect the digital twin and start the HMI

Obtain the Unity project and follow the [main project's documentation](https://github.com/Preliy/DT_PSA_OPCV). Select the matching Siemens scene and verify its connection settings against the emulation project.

After the simulated PLC and communication are ready, start the HMI simulation from TIA Portal. Confirm communication before using the machine controls.

## 6. Verify the demonstration

- Confirm the simulated CPU is in RUN and the HMI reports valid PLC values.
- Check that a sensor change in the twin reaches the expected PLC input.
- Check that an individual manual actuator command reaches the correct simulated device.
- Check the home-position and readiness indications.
- Follow the machine's documented initialization sequence before starting automatic operation.
- Check single-step behavior and fault acknowledgement.

The exact operator sequence and expected starting state still require validation on the working demo. Do not use this draft as a commissioning procedure for physical machinery.

## Troubleshooting

| Symptom | First check |
|---|---|
| Archive cannot be retrieved | TIA Portal version and required installed components |
| PLC connection unavailable | Running PLCSIM instance and exact instance name |
| Emulation project does not compile | TwinCAT version and referenced libraries |
| HMI values unavailable | HMI connection and simulated PLC state |
| Twin does not respond | Matching Siemens scene, emulation connection and I/O mapping |
