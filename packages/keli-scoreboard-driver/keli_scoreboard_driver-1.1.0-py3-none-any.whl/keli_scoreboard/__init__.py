from serial import Serial, SerialException

from .protocol import get_text_frame, get_settings_bytes


class KeliScoreboard:
    """
    Basic scoreboard interactor class. If this provides too
    low functionality and customization you can implement your own
    like this.
    """
    def __init__(self, device: str, bitrate=4800):
        self._port = Serial(device, bitrate)

    def print_text(self, text: str) -> None:
        """ Upload a text command into scoreboard """
        self._port.write(get_text_frame(text) + get_settings_bytes())

    def print_weight(self, weight: int) -> None:
        """
        Print a numerical value on scoreboard. Note you should recall it very quickly
        because the scoreboard can interrupt weight showing
        """
        self._port.write((str(weight).zfill(7)[::-1] + '=').encode('ascii'))

    def __enter__(self) -> 'KeliScoreboard':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if not self._port.closed:
            self.close()

    def close(self) -> None:
        self._port.close()


__all__ = ('KeliScoreboard', 'SerialException')
