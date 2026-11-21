# Reject thermistor samples that move faster than the hardware can.
#
# Copyright (C) 2026  John Middendorf
#
# This file may be distributed under the terms of the GNU GPLv3 license.
import logging


class TemperatureRateLimit:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.heater_name = config.get_name().split()[-1]
        self.max_rate = config.getfloat('max_rate', above=0.)
        self._last_time = None
        self._last_good = None
        self._holding = False
        self._installed = False
        self.printer.register_event_handler('klippy:connect', self._install)

    def _install(self):
        if self._installed:
            return
        heaters = self.printer.lookup_object('heaters')
        heater = heaters.lookup_heater(self.heater_name)
        sensor = heater.sensor
        orig = sensor.temperature_callback
        def _wrapped(read_time, temp, orig=orig):
            self._sample(orig, read_time, temp)
        sensor.temperature_callback = _wrapped
        self._installed = True

    def _sample(self, orig, read_time, temp):
        if self._last_time is None:
            self._last_time = read_time
            self._last_good = temp
            orig(read_time, temp)
            return
        dt = read_time - self._last_time
        self._last_time = read_time
        # A stalled clock or the first sample after a long gap is accepted.
        # The MCU still shuts down if the ADC stays outside min_temp/max_temp.
        if dt <= 0. or dt > 5.:
            self._last_good = temp
            self._holding = False
            orig(read_time, temp)
            return
        limit = self.max_rate * dt
        delta = temp - self._last_good
        if delta > limit:
            accepted = self._last_good + limit
        elif delta < -limit:
            accepted = self._last_good - limit
        else:
            accepted = temp
        if accepted != temp:
            if not self._holding:
                logging.warning(
                    "temperature_rate_limit %s: sample %.2f C/s from %.1f "
                    "toward %.1f, limiting to %.1f C/s",
                    self.heater_name, delta / dt, self._last_good, temp,
                    self.max_rate)
            self._holding = True
        else:
            self._holding = False
        self._last_good = accepted
        orig(read_time, accepted)


def load_config_prefix(config):
    return TemperatureRateLimit(config)
