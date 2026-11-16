# Printrbot Simple Metal → Klipper Migration Spec

## Goal

Migrate two existing Printrbot Simple Metal printers from custom Marlin (on SKR Mini boards) to Klipper. Use a BeagleBone Black as the Klipper host. Preserve (and improve) flexible-filament performance. Fix the intermittent hotend thermistor spike that currently causes overheating and nozzle clogs. Correct the inverted X-axis so parts no longer need to be mirrored in the slicer.

## Hardware Inventory

- **Host**: BeagleBone Black (8 GB microSD already installed)
- **MCU**: BigTreeTech SKR Mini E3 (V2.0 or V3.0 — confirm which) already installed in the printer
- **Display**: BigTreeTech TFT screen already wired to the SKR Mini (use emulated 12864 mode)
- **Accelerometer**: BTT ADXL345 V2 (for Input Shaping / resonance compensation)
- **Hotend**: Ubis 13s (thermistor is noisy — spikes ~+50 °C intermittently)
- **Extruder**: Stock Printrbot direct-drive style (excellent with flexible filaments)
- **Connection**: USB from BeagleBone → SKR Mini
- **Power**: Separate 5 V supply for the BeagleBone (recommended)

## Software Stack

- BeagleBone Debian IoT image (latest stable from beagleboard.org)
- Klipper (installed via official `install-beaglebone.sh`)
- Moonraker
- Fluidd or Mainsail (user preference — default to Fluidd unless specified)
- Input Shaping via ADXL345
- Pressure Advance (especially important for flexibles)
- Thermistor smoothing to suppress the +50 °C spikes

## Critical Configuration Requirements

1. **Thermistor spike mitigation**
   - Set `smooth_time: 2.5` to `4.0` on the extruder temperature sensor
   - Tighten `max_temp` protection
   - Optional hardware: 0.1 µF capacitor across the thermistor pins + strain relief on the cable

2. **BTT TFT**
   - Use `lcd_type: emulated_st7920` (or the equivalent for the specific TFT model)
   - Keep the existing SPI wiring to the SKR Mini

3. **Input Shaping**
   - Temporary ADXL345 wiring to the BeagleBone for resonance measurement
   - Generate and apply shaper values for both X and Y

4. **Flexible filament support**
   - Tune Pressure Advance carefully
   - Preserve the existing good direct-drive extruder setup

5. **X-axis direction correction**
   - X-axis is currently inverted in the existing Marlin firmware
   - Invert the `dir_pin` on `[stepper_x]` (add or remove the `!`) so the axis moves in the correct direction
   - Verify with a first test print that models no longer need to be mirrored in Cura

## Deliverables for This Project

- Working `printer.cfg` (with all of the above)
- Documented pin mappings for SKR Mini E3 + BTT TFT + ADXL345
- Step-by-step install notes (BeagleBone image → Klipper → Moonraker → Fluidd)
- Resonance measurement procedure and resulting shaper values
- GitHub repo structure ready for version control

## Known Unknowns / Decisions Still Needed

- Exact SKR Mini revision (E3 V2.0 vs V3.0)
- Preferred web interface (Fluidd vs Mainsail)
- Whether to run BeagleBone from SD only or also flash eMMC
- Final build volume / steps-per-mm values from the current Marlin firmware

## Immediate Next Steps

1. Confirm SKR Mini version and current steps/mm + build volume.
2. Flash BeagleBone with latest Debian IoT image (8 GB card is sufficient).
3. Install Klipper + Moonraker + Fluidd.
4. Create baseline `printer.cfg` with thermistor smoothing and correct X-axis direction.
5. Wire ADXL345 and run Input Shaping calibration.
