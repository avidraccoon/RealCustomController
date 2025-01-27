import struct
import time

from util import find_device


class Gamepad:

    def __init__(self, devices):

        self._gamepad_device = find_device(devices, usage_page=0x1, usage=0x05)

        # report[0] = buttons 1 - 8
        # report[1] = buttons 9 - 16
        self._report = bytearray(2)
        self._last_report = bytearray(2)

        self._buttons_state = 0

        try:
            self.reset_all()
        except:
            time.sleep(1)
            self.reset_all()

    def press_buttons(self, *buttons):
        for button in buttons:
            self._buttons_state |= 1 << self._validate_button_number(button) - 1
        self._send()

    def release_buttons(self, *buttons):
        for button in buttons:
            self._buttons_state &= ~(1 << self._validate_button_number(button) - 1)
        self._send()

    def _press_buttons_internal(self, *buttons):
        for button in buttons:
            self._buttons_state |= 1 << self._validate_button_number(button) - 1

    def _release_buttons_internal(self, *buttons):
        for button in buttons:
            self._buttons_state &= ~(1 << self._validate_button_number(button) - 1)

    def release_all_buttons(self):
        self._buttons_state = 0
        self._send()

    def click_buttons(self, *buttons):
        self.press_buttons(*buttons)
        self.release_buttons(*buttons)

    def reset_all(self):
        self._buttons_state = 0
        self._send(always=True)
    
    def _send(self, always=False):
        struct.pack_into(
            "<H",
            self._report,
            0,
            self._buttons_state,
        )
        if always or self._last_report != self._report:
            self._gamepad_device.send_report(self._report)
            self._last_report[:] = self._report

    @staticmethod
    def _validate_button_number(button):
        if not 1 <= button <= 16:
            raise ValueError("Button number must be in range 1 to 16")
        return button