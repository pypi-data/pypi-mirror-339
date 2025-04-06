from ast import literal_eval
from enum import Enum, auto

from typing import List, Optional, Callable, Tuple
from .pcf8574_interface_api import PCF8574InterfaceApi

try:
    from pcf8574 import PCF8574, IOPort
except ImportError:
    print("No I2C bus module found. Starting simulation")
    from pcf8574_simulation import PCF8574, IOPort


class IoPortType(Enum):
    IN = auto()
    OUT = auto()


class IOPortInterface(IOPort):
    """
    Represents the PCF8574 IO port as a list of boolean values.
    """
    pcf8574: "PCF8574Interface"

    def __init__(self, pcf8574: "PCF8574Interface", update_unspoiled_in: Callable[[List[bool]], None]) -> None:
        super().__init__(pcf8574)
        self.__update_unspoiled_in = update_unspoiled_in

    def __repr__(self) -> str:
        original_repr: str = super().__repr__()

        # parse repr of original pcf8574 and modify data
        evaluated_values: List[bool] = literal_eval(original_repr)  # ToDo: this is not efficient
        flipped_values: List[bool] = self.pcf8574.flip_and_reverse(evaluated_values)

        # store original read data and replace with overrides
        self.__update_unspoiled_in(flipped_values)
        spoiled_values: List[bool] = self.pcf8574.replace_values_in(flipped_values)

        self.pcf8574.clients_notifier()
        return repr(spoiled_values)


class PCF8574Interface(PCF8574):
    """
    Software abstraction layer for a PCF8574 I/O expander chip.

    This class extends the base `PCF8574` functionality, providing additional features for more flexible
    and testable usage of the PCF8574 hardware. It allows dynamic manipulation of I/O port states,
    including value inversion, pin order reversal, and simulated override states for testing or alternative workflows.

    Features:
        - **External API Hook:**
          Allows integration with an external API (through `PCF8574InterfaceApi`) to notify clients of port changes.

        - **Value Overrides:**
          Supports temporary override of pin states for both inputs and outputs, useful for testing or simulations.
          Original (unspoiled) values are retained in the background.

        - **Inversion Option:**
          Invert logic levels to accommodate different hardware configurations, e.g., high-voltage logic.

        - **Pin Order Reversal:**
          Reverse bit/port order to match the physical layout of PCF8574 pins (as per datasheet).


    Args:
        i2c_bus_no (int): The I2C bus number.
        address (int): The I2C address of the PCF8574 device.
        io_type (IoPortType, optional): Defines port mode (input or output). Defaults to output.
        invert (bool, optional): If True, inverts all read/write logic levels. Defaults to True.
        reverse (bool, optional): If True, reverses pin order to match physical layout. Defaults to True.
        api (Optional[PCF8574InterfaceApi], optional): A custom API implementation used to notify external systems when the state of the IO ports changes. If not provided, notifications are disabled.
    """
    def __init__(
            self,
            i2c_bus_no: int,
            address: int,
            io_type: IoPortType = IoPortType.OUT,
            invert: bool = True,
            reverse: bool = True,
            api: Optional[PCF8574InterfaceApi] = None
    ) -> None:
        super().__init__(i2c_bus_no, address)
        self.api: Optional[PCF8574InterfaceApi] = api
        self.port_type: IoPortType = io_type
        self.invert: bool = invert
        self.reverse: bool = reverse
        self.__override: List[Optional[bool]] = [None] * 8
        self.__unspoiled_in: List[bool] = [False] * 8
        self.__unspoiled_out: List[bool] = [False] * 8

    @property
    def port(self) -> IOPort:
        """
        Represent IO port as a list of boolean values.
        """
        return IOPortInterface(self, self.__update_unspoiled_in)

    @port.setter
    def port(self, value: List[bool]) -> None:
        """
        Set the whole port using a list.
        """
        self.__unspoiled_out = value
        value = self.replace_values_out(value)
        value = self.flip_and_reverse(value)
        super(PCF8574Interface, type(self)).port.__set__(self, value)
        self.clients_notifier()

    def set_output(self, output_number: int, value: bool, force=False) -> None:
        """
        Set a specific output high (True) or low (False).
        If "force" is set to True, override states will be ignored.
        """
        if self.port_type == IoPortType.IN:
            return
        if self.__override[output_number] is None:
            self.__unspoiled_out[output_number] = value
        if force or self.__override[output_number] is None:
            value, output_number = self.flip_and_reverse_single(value, output_number)
            try:
                super().set_output(output_number, value)
            except IOError:
                print('\033[91m' + f"PCF8574 Port {self.address} on bus {self.bus_no} not found!" + '\033[0m')
            self.clients_notifier()

    def get_pin_state(self, pin_number: int) -> Optional[bool]:
        """
        Get the boolean state of an individual pin.
        """
        reversed_pin_number = self.reverse_pin(pin_number)
        try:
            value: bool = not super().get_pin_state(reversed_pin_number)
            # store original read data and replace with overrides
            self.__unspoiled_in[pin_number] = value
            value = self.replace_value_in(value, pin_number)

            self.clients_notifier()
            return value
        except IOError:
            print('\033[91m' + f"PCF8574 Port {self.address} on bus {self.bus_no} not found!" + '\033[0m')
            return None

    def set_override(self, override_list: List[Optional[bool]]) -> None:
        """
        Override read values or output values (depending on input type). Original values are kept in background.
        - e.g. useful for testing
        """
        old_list: List[Optional[bool]] = self.__override.copy()
        self.__override = override_list
        for i, o in enumerate(override_list):
            if old_list[i] is not None and o is None:
                self.set_output(i, self.__unspoiled_out[i])
            elif o is not None:
                self.set_output(i, o, True)

    def set_override_pin(self, pin_number: int, override_value: Optional[bool]) -> None:
        """
        Override a read value or an output value (depending on input type) of a single pin. Original value is kept in background.
        - e.g. useful for testing
        """
        self.__override[pin_number] = override_value
        self.set_override(self.__override)

    def clients_notifier(self) -> None:
        """
        This method is called when the port was updated.
        It triggers the notify_clients method of your custom api.
        The custom api can be implemented through subclassing PCF8574InterfaceApi.
        """
        if self.api is None:
            return
        self.api.notify_clients(
            (self.__unspoiled_out if self.port_type == IoPortType.OUT else self.__unspoiled_in),
            self.__override,
            self.bus_no,
            self.address
        )

    def get_override(self) -> List[Optional[bool]]:
        """
        Returns a list with all override values.
        """
        return self.__override

    def __update_unspoiled_in(self, values: List[bool]) -> None:
        """
        Update raw read values.
        """
        self.__unspoiled_in = values

    def replace_values_in(self, original_list: List[bool]) -> List[bool]:
        """
        Replace unspoiled read values with override values (if port type is INPUT).
        """
        if self.port_type == IoPortType.IN:
            return self.__replace_values(original_list)
        else:
            return original_list

    def replace_values_out(self, original_list: List[bool]) -> List[bool]:
        """
        Replace unspoiled output values with override values (if port type is OUTPUT).
        """
        if self.port_type == IoPortType.OUT:
            return self.__replace_values(original_list)
        else:
            return original_list

    def __replace_values(self, original_list: List[bool]) -> List[bool]:
        """
        Replace unspoiled read/output values with override values.
        """
        return [
            new if new is not None else original
            for original, new in zip(original_list, self.__override)
        ]

    def replace_value_in(self, value: bool, pin_number: int) -> bool:
        """
        Replace unspoiled read value with override value (if port type is OUTPUT).
        """
        if self.port_type == IoPortType.IN:
            return self.__replace_value(value, pin_number)
        else:
            return value

    def replace_value_out(self, value: bool, pin_number: int) -> bool:
        """
        Replace unspoiled output value with override value (if port type is OUTPUT).
        """
        if self.port_type == IoPortType.OUT:
            return self.__replace_value(value, pin_number)
        else:
            return value


    def __replace_value(self, value: bool, pin_number: int) -> bool:
        """
        Replace unspoiled read/output value with override value.
        """
        return self.__override[pin_number] if self.__override[pin_number] is not None else value

    def flip_and_reverse(self, values: List[bool]) -> List[bool]:
        """
        Reverse order of read/output list (if option 'reverse' = True) and invert values (if option 'invert' = True).
        """
        if self.reverse:
            values.reverse()
        if self.invert:
            values = [not value for value in values]
        return values

    def reverse_pin(self, pin_number: int) -> int:
        """
        Reverse pin-number (if option 'reverse' = True).
        """
        if self.reverse:
            return 7 - pin_number
        else:
            return pin_number

    def flip_and_reverse_single(self, value: bool, pin_number: int) -> Tuple[bool, int]:
        """
        Reverse pin-number (if option 'reverse' = True) and invert value (if option 'invert' = True).
        """
        if self.invert:
            value = not value
        pin_number = self.reverse_pin(pin_number)
        return value, pin_number
