"""
Process Capability

This module defines the main logic for the process capability class. Minimal design with no third party dependencies to enable an ultra light weight (a.k.a feather weight) and fast package

"""

from typing import Optional

from .utils.tableprinter import print_table


class ProcessCapability:
    """
    A class to calculate process capability metrics and their ratings.
    """

    def __init__(
        self,
        mean: float,
        stddev: float,
        usl: Optional[float] = None,
        lsl: Optional[float] = None,
        print_results=True,
    ):
        """
        Initialize the ProcessCapability class with the necessary parameters.

        Args:
            mean: The mean of the process data.
            stddev: The standard deviation of the process data.
            usl: The upper specification limit. Defaults to None. Set as Optional to allow for single sided spec cases
            lsl: The lower specification limit. Defaults to None. Set as Optional to allow for single sided spec cases
            print_results: If True, print calculated metrics. Defaults to True.

        Raises:
        - TypeError: If any of the arguments are not of type float.
        """

        self._validate_inputs(mean, stddev, usl, lsl)

        self._mean = float(mean)
        self._stddev = float(stddev)
        self._usl = float(usl) if usl is not None else None
        self._lsl = float(lsl) if lsl is not None else None

        self._calculate_metrics()

        if print_results:
            print_table(self.metrics)

    def _validate_inputs(
        self,
        mean: float,
        stddev: float,
        usl: Optional[float],
        lsl: Optional[float],
    ):
        """Validates the input parameters.

        Raises:
            TypeError: If mean or stddev are not numeric.
            TypeError: If usl or lsl are provided but not numeric.
            ValueError: If stddev is not positive.
            ValueError: If neither USL nor LSL is provided.
            ValueError: If USL and LSL are equal.
            ValueError: If LSL is greater than USL.
        """
        if not isinstance(mean, (int, float)):
            raise TypeError("Mean must be numeric.")
        if not isinstance(stddev, (int, float)):
            raise TypeError("Standard deviation must be numeric.")
        if stddev <= 0:
            raise ValueError("Standard deviation must be positive.")
        if usl is not None and not isinstance(usl, (int, float)):
            raise TypeError("USL must be numeric or None.")
        if lsl is not None and not isinstance(lsl, (int, float)):
            raise TypeError("LSL must be numeric or None.")
        if usl is None and lsl is None:
            raise ValueError("At least one specification limit (USL or LSL) must be provided.")
        if usl is not None and lsl is not None:
            if usl == lsl:
                raise ValueError("USL and LSL cannot be equal.")
            if lsl > usl:
                raise ValueError(f"LSL ({lsl}) cannot be greater than USL ({usl}).")

    def _calculate_metrics(self):
        """Calculates all process capability metrics."""

        # Initialize values to None (instead of needing separate declarations in conditionals)
        self._cp = None
        self._cpa = None
        self._cpa_rating = None
        self._cpu = None
        self._cpl = None
        self._cpk = None
        self._sigma_level = None
        self._cpk_rating = None

        # Calculate metrics requiring both USL and LSL
        if self._usl is not None and self._lsl is not None:
            spec_range = self._usl - self._lsl
            spec_midpoint = (self._usl + self._lsl) / 2

            # Cp: Process potential
            self._cp = spec_range / (6 * self._stddev)

            # Cpa: Process accuracy/centering
            self._cpa = (self._mean - spec_midpoint) / (
                self._usl - self._lsl
            )  # ! Need to check if formula is correct
            self._cpa_rating = self._calculate_cpa_rating()

        # Calculate metrics requiring at least one limit
        if self._usl is not None:
            self._cpu = (self._usl - self._mean) / (3 * self._stddev)

        if self._lsl is not None:
            self._cpl = (self._mean - self._lsl) / (3 * self._stddev)

        # Calculate Cpk
        if self._cpu is not None and self._cpl is not None:
            self._cpk = min(self._cpu, self._cpl)
        elif self._cpu is not None:
            self._cpk = self._cpu
        elif self._cpl is not None:
            self._cpk = self._cpl

        # Calculate Sigma Level and Cpk Rating
        if self.process_capability_index is not None:
            self._sigma_level = self.process_capability_index * 3
            self._cpk_rating = self._calculate_cpk_rating()

    # All metrics items calculated above are made available as read-only properties from attributes with the following 8 decorators
    #     The property methods are valuable because they provide read-only access to the calculated metrics, preventing accidental modification of these values from outside the class. They also encapsulate the internal attribute names, allowing changing the internal representation without affecting the external interface. The sigma_level property demonstrates the ability to perform calculations or logic before returning a value. Removing them would expose the internal attributes directly, making the code more fragile and less maintainable.

    @property
    def metrics(self) -> dict:
        """Dictionary containing all calculated metrics and ratings."""

        metrics_compilation: dict = {
            "Process Capability": self.process_capability,
            "Process Capability Index": self.process_capability_index,
            "Process Capability Upper": self.process_capability_upper,
            "Process Capability Lower": self.process_capability_lower,
            "Process Accuracy": self.process_accuracy,
            "Process Sigma Level": self.sigma_level,
            "Process Capability Index Rating": self.process_capability_index_rating,
            "Process Accuracy Rating": self.process_accuracy_rating,
        }
        return metrics_compilation

    @property
    def process_capability(self) -> float | None:
        """
        **Cp:** *Process Capability*

        Formula: (USL - LSL)/(6 * Std Dev)

        The spec range divided by 6 times the standard deviation. Often also referred to as *process potential*.
        """

        return self._cp

    @property
    def process_capability_upper(self) -> float | None:
        """
        **Cpu:** *Upper Process Capability*

        Formula: (USL - Mean)/(3 * Std Dev)

        The difference of the upper spec limit and the mean divided by 3 times the standard deviation.
        """
        return self._cpu

    @property
    def process_capability_lower(self) -> float | None:
        """
        **Cpl:** *Lower Process Capability*

        Formula: (Mean - LSL)/(3 * Std Dev)

        The difference of the mean and the lower spec limit divided by 3 times the standard deviation.
        """
        return self._cpl

    @property
    def process_capability_index(self) -> float | None:
        """
        **Cpk:** *Process Capability Index*

        Formula: Min((USL - Mean)/(3 * Std Dev), (Mean - LSL)/(3 * Std Dev))

        The minimum of the upper and lower process capabilities. Normally considered the *key metric* of process quality
        """
        return self._cpk

    @property
    def process_accuracy(self) -> float | None:
        """
        **Cpa:** *Process Accuracy*

        Formula: (Mean - (Midpoint between USL and LSL))/(USL - LSL)

        Indicates entering relative to specification limits midpoint. Value is normalized deviation and smaller the better.
        0 indicates perfect centering. +/-1 indicates mean is at a spec limit. Negative values indicate population mean is shifted towards lower limit and positive values indicate population mean is shifted towards upper limit.
        """
        return self._cpa

    @property
    def process_capability_index_rating(self) -> str | None:
        """
        **Cpk Rating:** *Process Capability Index Rating*

        Provides a qualitative rating of the Cpk value based on the following criteria:
        - Abnormally Poor: Cpk <= 0
        - Poor: 0 < Cpk <= 0.5
        - Low: 0.5 < Cpk <= 1
        - Good: 1 < Cpk <= 1.33
        - Great: 1.33 < Cpk <= 1.67
        - Excellent: 1.67 < Cpk <= 2
        - Abnormally High: Cpk > 2
        """
        return self._cpk_rating

    @property
    def process_accuracy_rating(self) -> str | None:
        """
        **Cpa Rating:** *Process Accuracy Rating*

        Provides a qualitative rating of the Cpa (Process Accuracy) absolute value based on its absolute value:
        - Level A: Cpa < 0.125
        - Level B: 0.125 <= Cpa < 0.25
        - Level C: 0.25 <= Cpa < 0.5
        - Level D: Cpa >= 0.5
        """
        return self._cpa_rating

    @property
    def sigma_level(self):
        """
        The sigma level that the process is operating at: it is 3 Sigma level if it is 1-1.33, 4 Sigma between 1.33-1.67, 5 Sigma between 1.67-2 and so forth.
        It is numerically effectively the value of Cpk if there was no division by 3, i.e. it is equal to Cpk multiplied by 3 and rounded down to the nearest integer.
        """
        if self._sigma_level is None:
            return None
        elif self._sigma_level <= 0:
            return "Completely out of specification"
        elif 0 < self._sigma_level <= 9:
            sigma_level_display = self._sigma_level // 1
            return f"{sigma_level_display:.0f}\u03c3"
        elif self._sigma_level > 9:
            return "Abnormally High"
        else:
            raise ValueError

    def _calculate_cpk_rating(self) -> str:
        """
        Calculate the rating for the Cpk value.

        Returns:
        - str: The rating of the Cpk value.
        """
        cpk: float = self._cpk  # mypy driven assignment
        if cpk <= 0:
            return "Abnormally Poor"
        elif 0 < cpk <= 0.5:
            return "Poor"
        elif 0.5 < cpk <= 1:
            return "Low"
        elif 1 < cpk <= 1.33:
            return "Good"
        elif 1.33 < cpk <= 1.67:
            return "Great"
        elif 1.67 < cpk <= 2:
            return "Excellent"
        elif cpk > 2:
            return "Abnormally High"
        else:
            raise ValueError

    def _calculate_cpa_rating(self) -> str:
        """
        Calculate the rating for the Cpa value.

        Returns:
        - str: The rating of the Cpa value.
        """
        cpa: float = abs(self._cpa)
        if cpa < 0.125:
            return "Level A"
        elif cpa < 0.25:
            return "Level B"
        elif cpa < 0.5:
            return "Level C"
        else:
            return "Level D"
