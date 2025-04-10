import pytest
from ctapipe.core import run_tool

from lstcam_calib.conftest import (
    test_data,
    test_drs4_pedestal_file,
    test_run_summary_file,
)


def test_create_drs4_time_file(tmp_path):
    """Test drs4 time calibration file creation script.

    Because we have way to few events in the test file and a full run would
    take too long, we expect the exception about some capacitors not having
    enough data, but the rest of the script is expected to work.
    """

    from lstcam_calib.tools.create_drs4_time_file import DRS4TimeCorrection

    input_file = test_data / "real/R0/20200218/LST-1.1.Run02006.0000_first50.fits.fz"
    output_file = tmp_path / "test_drs4_time_calibration.h5"

    with pytest.raises(RuntimeError) as exc_info:
        run_tool(
            DRS4TimeCorrection(),
            argv=[
                "lstcam_calib_create_drs4_time_file",
                f"--input-file={input_file}",
                f"--output-file={output_file}",
                f"--pedestal-file={test_drs4_pedestal_file}",
                f"--run-summary-file={test_run_summary_file}",
            ],
            cwd=tmp_path,
        )

    assert "No enough statistics for some capacitors " in str(exc_info.value)
