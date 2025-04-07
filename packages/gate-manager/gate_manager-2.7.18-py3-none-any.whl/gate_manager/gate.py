# -*- coding: utf-8 -*-
"""
Gate and GatesGroup Classes for Nanonis System Interface.

This module defines the `Gate` and `GatesGroup` classes, which enable interaction with the Nanonis
system for controlling experimental gates. The `Gate` class allows individual gate voltage setting
and reading, while `GatesGroup` facilitates simultaneous control of multiple gates.

Classes:
    Gate: Manages voltage and currents measurement on a single gate in the Nanonis system.
    GatesGroup: Provides collective control over a group of gates.

Created on Tue Oct 22 16:08:06 2024
@author: Chen Huang <chen.huang23@imperial.ac.uk>
"""

import time

from .connection import SemiqonLine, NanonisSource


class Gate:
    """
    A class representing a gate used in experiments interfacing with the Nanonis system.
    """

    def __init__(
        self,
        source: NanonisSource = None,
        lines: list[SemiqonLine] = None,
        amplification: float = 1.0,
        label: str = None,
    ):
        self.source = source
        self.lines = lines
        self.amplification = amplification
        if label is None:
            if self.lines is not None:
                self.label = "&".join(line.label for line in self.lines)
            else:
                self.label = ""
        else:
            self.label = label
        self.nanonisInstance = self.source.nanonisInstance
        self._voltage = None  # Initialize the currents voltage

    def verify(self, target_voltage) -> None:
        """
        Verifies that the target voltage is within the allowed range (-2V to 2V).

        Args:
            target_voltage (float): The target voltage to verify.

        Raises:
            ValueError: If the target voltage is out of the specified range.
        """
        min_voltage = -2.5
        max_voltage = 2.5
        if target_voltage < min_voltage or target_voltage > max_voltage:
            raise ValueError(
                f"{self.label} target voltage {target_voltage} is out of range {(min_voltage, max_voltage)}."
            )

    def set_slew_rate(self, slew_rate: float) -> None:
        """
        Sets the slew rate for the gate.

        Args:
            slew_rate (float): The slew rate to set.
        """
        self.nanonisInstance.UserOut_SlewRateSet(self.source.write_index, slew_rate)
        self.slew_rate = slew_rate

    def set_volt(self, target_voltage: float) -> None:
        """
        Sets the voltage for the gate, if it is writable.

        Args:
            target_voltage (float): The target voltage to set.

        Raises:
            ValueError: If the gate is read-only (write_index is not defined).
        """
        self.verify(target_voltage)
        if self.source.write_index is None:
            raise ValueError(
                f"'{self.label}' cannot set voltage because write_index is not defined."
            )
        else:
            # Set voltage via Nanonis instance
            self.nanonisInstance.UserOut_ValSet(self.source.write_index, target_voltage)

    def get_volt(self) -> float:
        """
        Retrieves the current voltage from the gate.

        Returns:
            float: The current voltage.
        """
        self._voltage = self.nanonisInstance.Signals_ValsGet(
            [self.source.read_index], True
        )[2][1][0][0]
        return self._voltage

    def voltage(self, target_voltage: float = None, is_wait: bool = True) -> float:
        """
        Gets or sets the voltage for the gate. If a target voltage is provided, it sets the voltage.
        If no value is provided, it returns the currents voltage.

        Args:
            target_voltage (float, optional): The voltage to set. If None, returns the currents voltage.
            is_wait (bool): If True, waits until the voltage reaches the target.

        Returns:
            float: The target voltage.
        """
        if target_voltage is None:
            # If no target is given, just return the currents voltage
            self.get_volt()
            return self._voltage
        else:
            # Set voltage and optionally wait until reaching target
            self.set_volt(target_voltage)
            if is_wait:
                while not self.is_at_target_voltage(target_voltage):
                    time.sleep(0.001)

    def turn_off(self, is_wait: bool = True):
        """
        Sets the gate voltage to zero.

        Args:
            is_wait (bool): If True, waits until the voltage reaches zero.
        """
        self.voltage(0.0, is_wait)

    def is_at_target_voltage(
        self, target_voltage: float, tolerance: float = 1e-6
    ) -> bool:
        """
        Checks if the currents voltage is within a specified tolerance of the target voltage.

        Args:
            target_voltage (float): The voltage to compare against.
            tolerance (float): The allowable deviation from the target voltage.

        Returns:
            bool: True if the voltage is within tolerance, False otherwise.
        """
        self.get_volt()
        return abs(self._voltage - target_voltage) < tolerance

    def read_current(self) -> float:
        """
        Reads the currents from the gate

        Returns:
            float: The adjusted currents.
        """
        return (
            self.nanonisInstance.Signals_ValGet(self.source.read_index, True)[2][0]
            * 10 ** (6)
            / self.amplification
        )


class GatesGroup:
    """
    A class to manage a group of gates, allowing simultaneous control of multiple gates.

    Attributes:
        gates (list of Gate): A list of Gate instances in the group.
    """

    def __init__(self, gates: list[Gate], labels: str = None):
        self.gates = gates
        if labels is None:
            self.labels = " & ".join(gate.label for gate in self.gates)
        else:
            self.labels = labels

    def set_volt(self, target_voltage: float) -> None:
        """
        Sets the voltage of all gates in the group to a target value.

        Args:
            target_voltage (float): The voltage to set for all gates.
        """
        for gate in self.gates:
            gate.set_volt(target_voltage)

    def voltage(self, target_voltage: float, is_wait: bool = True) -> None:
        """
        Sets or retrieves the voltage for all gates in the group.

        Args:
            target_voltage (float): The voltage to set for all gates.
            is_wait (bool): If True, waits until all gates reach the target voltage.
        """
        for gate in self.gates:
            gate.voltage(target_voltage, False)
        if is_wait:
            while not all(
                gate.is_at_target_voltage(target_voltage) for gate in self.gates
            ):
                time.sleep(0.001)

    def turn_off(self) -> None:
        """
        Turns off all gates in the group by setting their voltages to zero.
        """
        self.voltage(0.0)
