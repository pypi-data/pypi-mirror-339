# C3.7S

import pytest
from cpkmetrics.process_capability import ProcessCapability


class TestProcessCapability:
    """Tests for the ProcessCapability class."""

    def test_initialization_with_valid_inputs(self, monkeypatch):
        """Test initialization with valid inputs."""
        # Mock print_table to avoid printing in tests
        monkeypatch.setattr("cpkmetrics.utils.tableprinter.print_table", lambda x: None)

        # Test with both USL and LSL
        pc = ProcessCapability(mean=10, stddev=1, usl=13, lsl=7)
        assert pc.process_capability == 1.0
        assert pc.process_capability_index == 1.0

        # Test with only USL
        pc = ProcessCapability(mean=10, stddev=1, usl=13)
        assert pc.process_capability is None
        assert pc.process_capability_index == 1.0

        # Test with only LSL
        pc = ProcessCapability(mean=10, stddev=1, lsl=7)
        assert pc.process_capability is None
        assert pc.process_capability_index == 1.0

        # Test with print_results=False
        pc = ProcessCapability(mean=10, stddev=1, usl=13, lsl=7, print_results=False)
        assert pc.process_capability == 1.0

    @pytest.mark.parametrize(
        "mean, stddev, usl, lsl, expected_error, expected_message",
        [
            ("string", 1, 13, 7, TypeError, "Mean must be numeric."),
            (10, "string", 13, 7, TypeError, "Standard deviation must be numeric."),
            (10, 1, "string", 7, TypeError, "USL must be numeric or None."),
            (10, 1, 13, "string", TypeError, "LSL must be numeric or None."),
            (10, 0, 13, 7, ValueError, "Standard deviation must be positive."),
            (10, -1, 13, 7, ValueError, "Standard deviation must be positive."),
            (
                10,
                1,
                None,
                None,
                ValueError,
                "At least one specification limit (USL or LSL) must be provided.",
            ),
            (10, 1, 10, 10, ValueError, "USL and LSL cannot be equal."),
            (10, 1, 7, 13, ValueError, "LSL (13) cannot be greater than USL (7)."),
        ],
    )
    def test_initialization_with_invalid_inputs(
        self, mean, stddev, usl, lsl, expected_error, expected_message, monkeypatch
    ):
        """Test initialization with invalid inputs."""
        monkeypatch.setattr("cpkmetrics.utils.tableprinter.print_table", lambda x: None)

        with pytest.raises(expected_error, match=expected_message):
            ProcessCapability(mean=mean, stddev=stddev, usl=usl, lsl=lsl)

    @pytest.mark.parametrize(
        "mean, stddev, usl, lsl, expected_cp",
        [
            (10, 1, 13, 7, 1.0),  # (13-7)/(6*1) = 1.0
            (10, 2, 16, 4, 1.0),  # (16-4)/(6*2) = 1.0
            (10, 0.5, 13, 7, 2.0),  # (13-7)/(6*0.5) = 2.0
            (10, 1, 16, 4, 2.0),  # (16-4)/(6*1) = 2.0
            (10, 1, 13, None, None),  # One-sided spec, Cp is None
            (10, 1, None, 7, None),  # One-sided spec, Cp is None
        ],
    )
    def test_process_capability(self, mean, stddev, usl, lsl, expected_cp, monkeypatch):
        """Test process_capability (Cp) calculation."""
        monkeypatch.setattr("cpkmetrics.utils.tableprinter.print_table", lambda x: None)

        pc = ProcessCapability(mean=mean, stddev=stddev, usl=usl, lsl=lsl)
        assert pc.process_capability == expected_cp

    @pytest.mark.parametrize(
        "mean, stddev, usl, expected_cpu",
        [
            (10, 1, 13, 1.0),  # (13-10)/(3*1) = 1.0
            (10, 2, 16, 1.0),  # (16-10)/(3*2) = 1.0
            (8, 1, 14, 2.0),  # (14-8)/(3*1) = 2.0
            (10, 1, None, None),  # No USL, Cpu is None
        ],
    )
    def test_process_capability_upper(self, mean, stddev, usl, expected_cpu, monkeypatch):
        """Test process_capability_upper (Cpu) calculation."""
        monkeypatch.setattr("cpkmetrics.utils.tableprinter.print_table", lambda x: None)

        pc = ProcessCapability(mean=mean, stddev=stddev, usl=usl, lsl=7 if usl is None else None)
        assert pc.process_capability_upper == expected_cpu

    @pytest.mark.parametrize(
        "mean, stddev, lsl, expected_cpl",
        [
            (10, 1, 7, 1.0),  # (10-7)/(3*1) = 1.0
            (10, 2, 4, 1.0),  # (10-4)/(3*2) = 1.0
            (14, 1, 8, 2.0),  # (14-8)/(3*1) = 2.0
            (10, 1, None, None),  # No LSL, Cpl is None
        ],
    )
    def test_process_capability_lower(self, mean, stddev, lsl, expected_cpl, monkeypatch):
        """Test process_capability_lower (Cpl) calculation."""
        monkeypatch.setattr("cpkmetrics.utils.tableprinter.print_table", lambda x: None)

        pc = ProcessCapability(mean=mean, stddev=stddev, usl=13 if lsl is None else None, lsl=lsl)
        assert pc.process_capability_lower == expected_cpl

    @pytest.mark.parametrize(
        "mean, stddev, usl, lsl, expected_cpk",
        [
            (10, 1, 13, 7, 1.0),  # min(1.0, 1.0) = 1.0
            (11, 1, 13, 7, 0.67),  # min((13-11)/(3*1), (11-7)/(3*1)) = min(0.67, 1.33) = 0.67
            (9, 1, 13, 7, 0.67),  # min((13-9)/(3*1), (9-7)/(3*1)) = min(1.33, 0.67) = 0.67
            (12, 1, 13, 7, 0.33),  # min((13-12)/(3*1), (12-7)/(3*1)) = min(0.33, 1.67) = 0.33
            (10, 1, 13, None, 1.0),  # Only USL, Cpk = Cpu = 1.0
            (10, 1, None, 7, 1.0),  # Only LSL, Cpk = Cpl = 1.0
        ],
    )
    def test_process_capability_index(self, mean, stddev, usl, lsl, expected_cpk, monkeypatch):
        """Test process_capability_index (Cpk) calculation."""
        monkeypatch.setattr("cpkmetrics.utils.tableprinter.print_table", lambda x: None)

        pc = ProcessCapability(mean=mean, stddev=stddev, usl=usl, lsl=lsl)
        assert (
            abs(pc.process_capability_index - expected_cpk) < 0.01
        )  # Allow for small float precision differences

    @pytest.mark.parametrize(
        "mean, stddev, usl, lsl, expected_cpa",
        [
            (10, 1, 13, 7, 0),  # (10-(13+7)/2)/(13-7) = 0
            (11, 1, 13, 7, 0.17),  # (11-10)/(13-7) = 0.17
            (9, 1, 13, 7, -0.17),  # (9-10)/(13-7) = -0.17
            (13, 1, 13, 7, 0.5),  # (13-10)/(13-7) = 0.5
            (7, 1, 13, 7, -0.5),  # (7-10)/(13-7) = -0.5
            (10, 1, 13, None, None),  # One-sided spec, Cpa is None
            (10, 1, None, 7, None),  # One-sided spec, Cpa is None
        ],
    )
    def test_process_accuracy(self, mean, stddev, usl, lsl, expected_cpa, monkeypatch):
        """Test process_accuracy (Cpa) calculation."""
        monkeypatch.setattr("cpkmetrics.utils.tableprinter.print_table", lambda x: None)

        pc = ProcessCapability(mean=mean, stddev=stddev, usl=usl, lsl=lsl)
        if expected_cpa is None:
            assert pc.process_accuracy is None
        else:
            assert (
                abs(pc.process_accuracy - expected_cpa) < 0.01
            )  # Allow for small float precision differences

    @pytest.mark.parametrize(
        "cpk, expected_rating",
        [
            (-0.5, "Abnormally Poor"),
            (0, "Abnormally Poor"),
            (0.25, "Poor"),
            (0.5, "Poor"),
            (0.75, "Low"),
            (1, "Low"),
            (1.2, "Good"),
            (1.33, "Good"),
            (1.5, "Great"),
            (1.67, "Great"),
            (1.8, "Excellent"),
            (2, "Excellent"),
            (2.5, "Abnormally High"),
        ],
    )
    def test_process_capability_index_rating_direct(self, cpk, expected_rating):
        """Test process_capability_index_rating directly by setting internal _cpk value."""
        pc = ProcessCapability(mean=10, stddev=1, usl=13, lsl=7, print_results=False)

        # Set the internal _cpk attribute directly for testing
        pc._cpk = cpk
        # Recalculate the rating
        pc._cpk_rating = pc._calculate_cpk_rating()

        assert pc.process_capability_index_rating == expected_rating

    @pytest.mark.parametrize(
        "cpa, expected_rating",
        [
            (0, "Level A"),
            (0.1, "Level A"),
            (0.124, "Level A"),
            (0.125, "Level B"),
            (0.2, "Level B"),
            (0.249, "Level B"),
            (0.25, "Level C"),
            (0.4, "Level C"),
            (0.499, "Level C"),
            (0.5, "Level D"),
            (0.75, "Level D"),
            (1, "Level D"),
        ],
    )
    def test_process_accuracy_rating(self, cpa, expected_rating, monkeypatch):
        """Test process_accuracy_rating calculation."""
        monkeypatch.setattr("cpkmetrics.utils.tableprinter.print_table", lambda x: None)

        # Calculate mean that will give the desired Cpa
        # Using the formula: Cpa = (mean - (usl+lsl)/2)/(usl-lsl)
        stddev = 1
        usl = 13
        lsl = 7
        spec_midpoint = (usl + lsl) / 2
        spec_range = usl - lsl
        # Calculate mean to get the desired Cpa
        mean = spec_midpoint + (cpa * spec_range)

        pc = ProcessCapability(mean=mean, stddev=stddev, usl=usl, lsl=lsl)
        assert pc.process_accuracy_rating == expected_rating

    @pytest.mark.parametrize(
        "cpa, expected_rating",
        [
            (0, "Level A"),
            (0.1, "Level A"),
            (0.124, "Level A"),
            (0.125, "Level B"),
            (0.2, "Level B"),
            (0.249, "Level B"),
            (0.25, "Level C"),
            (0.4, "Level C"),
            (0.499, "Level C"),
            (0.5, "Level D"),
            (0.75, "Level D"),
            (1, "Level D"),
        ],
    )
    def test_process_accuracy_rating_direct(self, cpa, expected_rating):
        """Test process_accuracy_rating directly by setting internal _cpa value."""
        pc = ProcessCapability(mean=10, stddev=1, usl=13, lsl=7, print_results=False)

        # Set the internal _cpa attribute directly
        pc._cpa = cpa
        # Recalculate the rating
        pc._cpa_rating = pc._calculate_cpa_rating()

        assert pc.process_accuracy_rating == expected_rating

    @pytest.mark.parametrize(
        "cpk, expected_sigma_level",
        [
            (-0.5, "Completely out of specification"),
            (0, "Completely out of specification"),
            (0.34, "1σ"),
            (0.67, "2σ"),
            (1, "3σ"),
            (1.34, "4σ"),
            (1.67, "5σ"),
            (2, "6σ"),
            (2.34, "7σ"),
            (2.67, "8σ"),
            (3, "9σ"),
            (3.33, "Abnormally High"),
        ],
    )
    def test_sigma_level_direct(self, cpk, expected_sigma_level):
        """Test sigma_level directly by setting internal _cpk and _sigma_level values."""
        pc = ProcessCapability(mean=10, stddev=1, usl=13, lsl=7, print_results=False)

        # Set the internal attributes directly for testing
        pc._cpk = cpk
        pc._sigma_level = cpk * 3

        assert pc.sigma_level == expected_sigma_level

    def test_metrics_dictionary(self, monkeypatch):
        """Test the metrics dictionary contains all the expected keys."""
        monkeypatch.setattr("cpkmetrics.utils.tableprinter.print_table", lambda x: None)

        pc = ProcessCapability(mean=10, stddev=1, usl=13, lsl=7)
        metrics = pc.metrics

        expected_keys = [
            "Process Capability",
            "Process Capability Index",
            "Process Capability Upper",
            "Process Capability Lower",
            "Process Accuracy",
            "Process Sigma Level",
            "Process Capability Index Rating",
            "Process Accuracy Rating",
        ]

        for key in expected_keys:
            assert key in metrics
