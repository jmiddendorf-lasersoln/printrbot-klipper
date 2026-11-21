# Printrbot Klipper Setup

Migration of a Printrbot Simple Metal from custom Marlin to Klipper, hosted on a BeagleBone Black. A Printrbot Plus on an SKR Mini E3 V3.0 is a later machine and is not in `printer.cfg`.

The requirements are in [docs/spec.md](docs/spec.md). The baseline config is [printer.cfg](printer.cfg), meant to be checked out on the BeagleBone as `~/printer_data/config`.

## Status

Nothing has been flashed. `printer.cfg` is a baseline for the Simple Metal:

- SKR Mini E3 V2.0, one Z motor
- Travel 152.4 mm (6 inches) on X, Y, and Z
- Hotend `smooth_time: 3.0` and `max_temp: 270`
- X and Y are both reversed from the first Klipper setup, a 180° rotation so the Cura view matches the machine. X homes to 0 at its switch. Y homes to 152.4 at its switch. Slices stay unmirrored.

Steps/mm, PID, and the probe offset were copied from the surviving Marlin file. That file had been resaved for the Plus. An `M503` from the Simple Metal replaces any value that disagrees.

Still open:

- Web UI: Fluidd unless you choose Mainsail
- BeagleBone boot: SD card only, or also flash the eMMC
- Probe Z offset, measured on this machine
- Input shaper values, after the ADXL345 measurement

## Hardware

- Host: BeagleBone Black, USB to the SKR Mini, separate 5 V supply
- MCU: BigTreeTech SKR Mini E3 V2.0
- Display: BigTreeTech TFT, emulated 12864 mode, existing EXP1 wiring
- Accelerometer: BTT ADXL345 V2, for Input Shaping
- Hotend: Ubis 13s (noisy thermistor, spikes about +50 °C)
- Extruder: stock Printrbot direct drive

## Layout

- `docs/spec.md` — migration spec
- `printer.cfg` — Simple Metal baseline
