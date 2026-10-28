# RFID read/write head — P+F IQT1 Expert Mode

The TIA program drives an RFID read/write head with Pepperl+Fuchs'
**`IQT1-xx-IO-V1_ExpertMode_Basic`** block (V2.1). The head is an IQT1-xx-IO-V1 behind an IO-Link
master, and its process data is a 32-byte Expert Mode telegram. In the emulation unit the head is
simulated by `FB_RFID_IQT1` in `TIA_1/EmulationUnit/SIM_1/Library/RFID_IQT1/`.

**Status: behaviour model only.** The block exists in the library and compiles, but no function
group uses it yet. There are no telegram addresses and no twin device for it.

## How the tag gets to TwinCAT

The tag and its data come from Open Commissioning's **product data** on the Unity side
(`OC_Unity_Core`, `Runtime/Scripts/Data` and `Components/TagReader.cs`):

1. A payload carries a **`PayloadTag`**. When the payload is enabled, OC writes its product data
   file into every product data directory listed in the tag's `DirectoryId`.
2. A **Payload Tag Reader** (`TagReader`, link type `FB_Reader`) puts the payload's `UniqueId` on
   `StatusData` while the payload is in its volume, and 0 when it leaves. That number is the
   **MDS number**.
3. `FB_RFID_IQT1` **extends OC_Core `FB_Reader`**, so it receives that number as `nResult`. On
   each read or write it opens the payload's file from the **`sDirectory`** input.

| | Unity side (OC `ProductDataFactory`) | `FB_RFID_IQT1` |
|---|---|---|
| Folder | a `ProductDataDirectory` path; `streamingassets:` resolves to `Application.streamingAssetsPath` | `sDirectory`, the same folder as an absolute path. A trailing `\` or `/` is optional |
| File | `ID<UniqueId>.data`, UniqueId in decimal | the same, from `stConfig.sFilePrefix` / `sFileExtension` |
| Content | 32,000 bytes, packed by the template `Type<TypeId>.xml` in the same folder | the head's user memory: byte address *n* is byte *n* of the file |

The file is read **whole** and written back **whole**, so it never changes size under Unity. It is
reloaded on every command and never cached. A write is answered only after the file is written,
so the next head reads it back.

## What to know about the data

- **Unity rewrites the file** from its template whenever the payload is enabled. Data the PLC
  wrote is gone when the payload is created again, for example after a scene restart.
- **No template, no file:** if the folder has no `Type<TypeId>.xml`, Unity writes nothing. The
  head then creates a zeroed 32,000-byte file on its first access, so the tag reads as blank.
- **Byte order:** OC packs `INT16`, `INT32`, `UINT16` and `UINT32` entries little-endian (.NET
  `BitConverter`), but the S7 reads big-endian. `CHARS` and `BYTES` entries are byte-exact. A
  numeric entry the TIA program reads must be swapped on one side, or stored as `BYTES`.
- **One folder per data path:** a `PayloadTag` with several `DirectoryId`s gets one independent
  copy per folder. Heads that should see each other's writes must use the **same** `sDirectory`.
- **Built player:** a `streamingassets:` directory resolves to `<Build>_Data\StreamingAssets\…`
  in the player, but to `Assets\StreamingAssets\…` in the editor. Give `sDirectory` the one in use.

## Where the behaviour comes from

The telegram is derived from the **master side**, the P+F block, not from the P+F manual. Every
byte the model writes is one the block reads or tests. Where the block leaves a value open, the
model uses a value the block reads correctly. Those choices are listed under
[Open points](#open-points).

Built the Open Commissioning way, like the [lift drives](lift-drives.md): `pControl` / `pStatus`
point into the PLCSIM image. It is bytes only, so nothing is swapped; the address and count words
in the telegram are high byte first. For testing without Unity, `bSimulateTag` + `nSimulatedUid`
replace the reader.

## Telegram layout

32 bytes from the PLC (`%QB`), 34 to the PLC (`%IB`): 32 data bytes plus the PQI at byte 32. The
Murr IO-Link master sends the PQI as a WORD, which is why the block reads 34.

| Byte | PLC → head (request) | Head → PLC (first response frame) |
|---:|---|---|
| 0 | handshake bits | handshake bits |
| 1 | frame length | frame length = last used index + 1 |
| 2 | fragment counter | frames still to come, 0 = last |
| 3–4 | telegram length | telegram length = 4 + data bytes |
| 5 | command | command echo |
| 6–7 | byte address (Change Tag: [6] = tag type) | [6] status, then data from [7] |
| 8–9 | byte count | data |
| 10–31 | write data, at most 22 bytes | data — 25 bytes in frame 1 |
| 32 | — | PQI, `stConfig.nPQI` (shown by the block, not evaluated) |

A read longer than 25 bytes is fragmented. Each further frame carries `[1]` frame length, `[2]`
counter, and 29 data bytes in `[3..31]`. That matches the block's `ReadData` offsets 0, 25, 54,
83 and so on.

### Handshake (byte 0)

| Bit | Name | Rule |
|---|---|---|
| `16#80` | Delete | The PLC toggles it in its init routine. The head drops whatever is in flight and mirrors it |
| `16#40` | UpdateMaster | **Equal** on both sides means a request is waiting. The head takes it and makes them differ, which permits the next request. While busy, the head leaves them equal and the block retries |
| `16#20` | UpdateSlave | The head makes them **equal** to publish a frame. The PLC writes the inverse back every scan, so **different** means consumed |

**The head publishes one frame per acknowledgement**, with the data and the toggle in the same
cycle. The emulation task runs at 1 ms and PLCSIM is far slower: a frame written before the PLC
has consumed the last one is lost.

## Commands

The tag is sampled when the command starts: a `UniqueId` of 0 is **no tag**.

| Code | Command | Answer |
|---|---|---|
| `16#04` | Change Tag (the block's init) | `00`. Any tag type is accepted |
| `16#02` | Quit | `00` |
| `16#10` | Single Read 4-byte block | `00` + data, fragmented. `04` if the range leaves `stConfig.nMemorySize` or exceeds 192 bytes, if `sDirectory` is empty, or on a file error. `05` without a tag |
| `16#40` | Single Write 4-byte block | `00` once the file is written. `04` if the range leaves `stConfig.nMemorySize` or exceeds 22 bytes, if `sDirectory` is empty, or on a file error. `05` without a tag |
| `16#01` | Single Read Fixcode | `00` + the 8-byte `UniqueId`, most significant first. `05` without a tag |
| `16#19` `16#1A` `16#1D` | Enhanced Read / Write / Read Fixcode | `04`: not modelled |
| other | Special (tunnelled) commands | `04`: not modelled |

Status `00` = OK, `04` = error, `05` = no data carrier. These are the only codes the block
evaluates. A no-tag answer is exactly frame length 7, telegram length 4 and status `05`, which is
the pattern the block tests for.

## Parameters

| | Default | Meaning |
|---|---|---|
| `sDirectory` (input) | — | folder of the product data files, as above |
| `stConfig.sFilePrefix` / `sFileExtension` | `ID` / `.data` | OC's file name. Change only together with the Unity side |
| `stConfig.nMemorySize` | 32000 | bytes the PLC may address. Set the real tag's size to get `04` beyond it |
| `stConfig.nMaxReadLength` | 192 | bytes per Single Read; the block's `ReadData` holds 192 |
| `stConfig.tAccessTime` | 30 ms | modelled air time per command. Must stay well inside the block's `I_T_Timeout` (10 s) |
| `stConfig.nPQI` | `16#A0` | IO-Link port qualifier, shown by the block only |

## Not modelled

Enhanced (continuous) commands, Special commands, tag-type behaviour, alignment of the address to
4-byte blocks, RSSI, and the timing statistics the block records (`Time_Status_00` and so on are
still filled by the block from its own clock).

## Open points

- **Unverified against the P+F manual:** the frame length of continuation frames, the direction of
  the fragment counter, and the status a real head gives for an out-of-range address. The block
  reads the model's choices correctly; a real head may differ.
- **Possible bug in the P+F block (V2.1):** frame 1 is copied with
  `MOVE_BLK(Resp_Telegram_1[7], COUNT := 26)` from a `0..31` array, which is one byte past its
  end. If TIA refuses that copy (`ENO = 0`), `ReadData[0..24]` stays empty. Check this in the first
  PLCSIM test.
- **A continuation frame of exactly 4 data bytes** has frame length 7. If its data bytes `[4]` and
  `[6]` happen to be `16#04` and `16#05`, the block mistakes it for a no-tag answer. This is
  harmless for any other length.
- **Next step:**
  - Put a `TagReader` and `PayloadTag`s in the twin, with a product data directory and template.
  - Make the reader's link an `FB_RFID_IQT1` instead of the default `FB_Reader`.
  - Instance the head in a function group, setting `sDirectory` and the telegram addresses from
    the TIA hardware configuration.
