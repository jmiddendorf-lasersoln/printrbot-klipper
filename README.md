# Printrbot Klipper Setup

Migration of two Printrbot Simple Metal printers from custom Marlin on SKR Mini boards to Klipper, hosted on a BeagleBone Black.

The requirements are in [docs/spec.md](docs/spec.md).

`printer.cfg` will live at the root of this repo so the BeagleBone can check the repo out as its Klipper config directory (`~/printer_data/config`). No config is in the tree yet. Pin maps differ between SKR Mini E3 V2.0 and V3.0, and a guessed config can drive heaters or steppers on the wrong pins.

## Status

Repository started. Nothing has been flashed.

Still open:

- SKR Mini E3 revision (V2.0 or V3.0)
- Web UI: Fluidd unless you choose Mainsail
- BeagleBone boot: SD card only, or also flash the eMMC
- Build volume and steps/mm from the current Marlin firmware

## Hardware

- Host: BeagleBone Black, USB to the SKR Mini, separate 5 V supply
- MCU: BigTreeTech SKR Mini E3, already in the printer
- Display: BigTreeTech TFT, emulated 12864 mode, existing SPI wiring
- Accelerometer: BTT ADXL345 V2, for Input Shaping
- Hotend: Ubis 13s (noisy thermistor, spikes about +50 °C)
- Extruder: stock Printrbot direct drive

## Layout

- `docs/spec.md` — migration spec
- `printer.cfg` — added after the board revision, build volume, and steps/mm are confirmed
