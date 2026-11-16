# Printrbot Simple Metal → Klipper Migration Spec

## Goal

Migrate the Printrbot Simple Metal from custom Marlin to Klipper. Use a BeagleBone Black as the Klipper host. Preserve (and improve) flexible-filament performance. Fix the intermittent hotend thermistor spike that currently causes overheating and nozzle clogs. Reverse the X motor and home X to the maximum end so parts match the slicer without a mirror.

A second printer, a Printrbot Plus on an SKR Mini E3 V3.0, stays on Marlin until the Simple Metal is done.

## Hardware Inventory

- **Host**: BeagleBone Black (8 GB microSD already installed)
- **MCU**: BigTreeTech SKR Mini E3 V2.0, already installed. Single Z motor. The Plus has a V3.0 and is out of scope here.
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

5. **X-axis direction**
   - Invert the X motor from Marlin (`dir_pin: !PB12`) so G-code +X is the slicer's +X
   - The switch stays on the same physical end of the axis. That end is X max (`position_endstop: 152.4`), so homing still travels into the switch
   - Positive X then jogs toward the switch. A test print with text confirms the mirror is gone

## Deliverables for This Project

- Working `printer.cfg` (with all of the above)
- Documented pin mappings for SKR Mini E3 + BTT TFT + ADXL345
- Step-by-step install notes (BeagleBone image → Klipper → Moonraker → Fluidd)
- Resonance measurement procedure and resulting shaper values
- GitHub repo structure ready for version control

## Decisions

- Simple Metal MCU is an SKR Mini E3 V2.0. Confirmed, and it matches the September 8, 2023 Marlin binary named `Johns Simple Metal`.
- Travel is 6 inches, 152.4 mm, on X, Y, and Z. One Z motor.
- Steps/mm carried into `printer.cfg` from the surviving Marlin file: X 80, Y 80, Z 2020, E 94.5. That file was last saved for the Plus. Replace from an `M503` dump if the Simple Metal differs.
- Web UI stays Fluidd unless changed.
- BeagleBone from SD only, or also flash the eMMC, is still open.

## Immediate Next Steps

1. Flash BeagleBone with latest Debian IoT image (8 GB card is sufficient).
2. Install Klipper + Moonraker + Fluidd.
3. Review `printer.cfg`, set the MCU serial path, and flash the SKR Mini from the SD card.
4. Check endstops and the probe before the first Z home. Calibrate probe Z offset.
5. Wire ADXL345 and run Input Shaping calibration.
