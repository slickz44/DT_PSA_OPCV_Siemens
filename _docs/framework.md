# Siemens machine-control framework

Start here to operate the demo, then explore how the PLC framework connects machine control, stations, actuators and sequences.

## First steps: get the machine running

Complete the [Siemens setup guide](setup.md) first: load the project into the **DT_PSA_OPCV** PLCSIM Advanced instance, put the Siemens CPU and TwinCAT EmulationUnit into **RUN**, connect OC Assistant, open the Siemens digital-twin scene and start the HMI simulation.

![Machine operator panel with Control On/Off, Op Mode, Single Step, Auto Start, Auto Stop, Error Ack. and Reset](images/machine-operator-panel.png)

Use the controls on the machine's operator panel in this order:

| Step | Action | What to observe |
|---|---|---|
| 1 | Switch **CONTROL ON/OFF** on. | The control starts up. Its indicator flashes during startup. |
| 2 | Wait for **CONTROL ON/OFF** to show a steady light. | The configured startup readiness conditions are satisfied. |
| 3 | Turn **OP MODE** to the right to select automatic mode. | **RESET** flashes: the homing sequence is selected. Selecting automatic mode alone does not start motion. |
| 4 | Press **AUTO START**. | The selected homing sequence runs and brings the stations to their home positions. |
| 5 | Wait until **RESET** lights steadily. | All stations are in their home positions. |
| 6 | Press **AUTO START** again. | The automatic production sequence starts, provided the required conditions and releases are satisfied. |

**Reset selects homing; Auto Start executes it.** The first start performs homing, and the next start begins production.

Startup readiness can include functions such as starting external camera computers or enabling the main compressed-air supply and waiting for pressure. These are examples of how the framework can be used; they are not a claim that every such device is implemented in this demo.

## Controls and indicator meanings

| Control | Function | Indicator meaning |
|---|---|---|
| **CONTROL ON/OFF** | Enables the control and starts the machine startup sequence. | Flashing: startup in progress. Steady: configured readiness conditions met. |
| **OP MODE** | Selects manual or automatic operation; turn right for automatic mode. | Select the required mode before issuing commands. |
| **RESET** | Selects the homing sequence. | Flashing: homing selected. Steady: all stations at home. |
| **AUTO START** | Starts selected homing or automatic production. | Flashing: not all stations are running in automatic operation. |
| **SINGLE STEP** | Executes a single step across the stations in automatic mode. | Lit while the step is executing; goes out once the participating sequences reach `jogdone`. |
| **AUTO STOP** | Requests an orderly stop of automatic production. | Stations continue to their home positions and then stop. |
| **ERROR ACK.** | Acknowledges faults after their causes have been resolved. | Check the HMI alarm list to see which conditions still require attention. |

A lit **SINGLE STEP** indicator means that step execution is in progress, rather than simply indicating a permanently selected mode. Wait for it to go out before requesting the next step.

## Stopping and restarting

### Normal automatic stop

Press **AUTO STOP**. All stations finish their work up to their home positions and remain there. Allow this sequence to complete; this is an orderly process stop.

### Sequence or station fault

The framework handles a sequence fault in stages:

1. The faulty sequence stops in its fault state.
2. Other sequences in the same station continue to their defined wait or hold steps.
3. That station then resets its `releaseCycle`.
4. Other stations continue to their home positions, where their own `releaseCycle` is reset in response to the station or machine fault.

Here, reaching home means completing the applicable sequence to its home position; it is not a separate commanded homing run. Inspect the HMI alarms and the affected sequence before restarting.

### Restart after an emergency stop

After an emergency stop, homing is selected for all stations. Once the emergency-stop condition has been cleared and the required acknowledgement completed:

1. Press **AUTO START** to execute homing.
2. Wait for all stations to reach home (**RESET** steady).
3. Press **AUTO START** again to start production.

Acknowledgement alone does not restart production. The sequence-fault behavior described above must not be interpreted as the emergency-stop response. This page describes operation of the supplied virtual-commissioning demo.

## How the framework is organized

The framework combines reusable control blocks with station-specific actuator calls and process sequences.

| Component | Responsibility |
|---|---|
| `MachineMain` | Organizes machine control and the function-group calls. |
| `MachineControl` | Reusable library block for machine-wide commands and states: control startup, operating mode, homing, automatic operation, single step and acknowledgement. |
| `FGxxControl` | Station-specific composition of the common functions and the station's own behavior. |
| `StationControl` | Reusable library block that derives station control signals and releases from the machine commands and local conditions. |
| `StationState` | Handles station-state information. |
| `StationCycleTime` | Handles station cycle-time information. |
| `FGxxActorControl` | Groups the calls to the station's actuator blocks. The selection and wiring depend on the station. |
| `FGxxStepSequences` | Groups the station-specific sequence calls; GRAPH sequences describe the process. |

`FGxxControl` follows a common structure but may include additional functions required by a particular station. The reusable elements are `MachineControl`, `StationControl` and the actuator library blocks. The station composition and its sequences are adapted to the application.

“Station-specific” describes the code's purpose, not its PLC block type: for example, `FG01StepSequences` is an FC, while FBs and GRAPH sequences use their associated instance data.

## Manual operation and automatic actuator commands

Every actuator block receives station signals and interfaces to both manual operation and the automatic sequence:

| Interface | Purpose |
|---|---|
| `ManualMovements` | Global DB passed down to the actuator blocks. During initialization, each actuator is assigned its own movement entry. The HMI setup rows use these entries for manual commands and display. |
| `FGxxActors` | Station-specific command and status interface used by the automatic GRAPH sequences and actuator control. It includes actuator commands, feedback, interlocks and fault states. |
| Station signals | Provide the common operating context and station-level releases to the actuator blocks. |

This lets the HMI use a consistent setup interface while each station has its own actuators and automatic process.

## Communication between stations

`FGxxGlobals` provides signal exchange between function groups. The current implementation does **not** enforce a strict rule that only the owning station writes to its globals.

For example, the workpiece-carrier lifts belong to `FGTransport`. Transport sets a `release` when a carrier has been lifted and is ready for a station. The station performs its work and resets that release in `FGTransport` when finished. When extending this handshake, account for both writers and the order of the PLC calls.

## Where developers should start

1. Run the machine with the first-start procedure above and observe the panel and HMI states.
2. Open `MachineMain` and follow the `MachineControl` call to understand the machine-wide commands.
3. Inspect one function group, such as `FG01Control`, including `StationControl`, `StationState` and `StationCycleTime`.
4. Trace one actuator through `FG01ActorControl`, its `ManualMovements` entry and its interface in `FG01Actors`.
5. Follow the matching GRAPH sequence in `FG01StepSequences`, including its transitions, wait/hold steps and home state.
6. Inspect the station's exchange with `FGTransport` before changing cross-station releases.

This guide documents the behavior and structure described by the framework author. Check the downloaded TIA project's implementation when making changes. Planned additions are listed in the [roadmap](../README.md#roadmap).

## If the machine does not start

| Observation | Check |
|---|---|
| Control indicator keeps flashing | Startup readiness conditions and HMI messages. |
| Reset flashes but there is no motion | Homing is selected; use **AUTO START** to execute it. |
| Reset is steady after the first start, but production has not begun | Press **AUTO START** again for production. |
| Auto Start flashes | Not all stations are running automatically; inspect their states, alarms and releases. |
| Single Step stays lit | A participating sequence has not yet reached `jogdone`; inspect its active step and transition conditions. |
| No communication or no actuator response | Follow the [setup troubleshooting checks](setup.md#troubleshooting), especially the exact PLCSIM instance name and OC Assistant connection. |

[Back to the README](../README.md) · [Setup guide](setup.md) · [Watch the demonstration](https://youtu.be/DnUcnGoN3U8)
