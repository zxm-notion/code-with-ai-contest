import pytest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import load_data, get_color_by_rsrp, DATA_PATH

@pytest.fixture
def sample_data():
    data = {
        "Latitude": [31.209143, 31.214219, 31.249965],
        "Longitude": [121.482867, 121.484829, 121.453557],
        "CellID": [1926, 1457, 1941],
        "Band": ["n28", "n78", "n28"],
        "RSRP_dBm": [-94.94, -105.47, -82.27],
        "SINR_dB": [5.44, 20.67, 18.28],
        "TerminalType": ["Smartphone", "CPE", "Smartphone"],
        "Download_Mbps": [138.21, 837.84, 36.23]
    }
    return pd.DataFrame(data)

class TestLoadData:
    def test_load_data_success(self):
        df = load_data(DATA_PATH)
        assert df is not None
        assert len(df) > 0
        assert "Latitude" in df.columns
        assert "Longitude" in df.columns
        assert "RSRP_dBm" in df.columns

    def test_load_data_columns(self):
        df = load_data(DATA_PATH)
        required_columns = ["Latitude", "Longitude", "CellID", "Band", "RSRP_dBm", "SINR_dB", "TerminalType", "Download_Mbps"]
        for col in required_columns:
            assert col in df.columns, f"Missing column: {col}"

class TestGetColorByRsrp:
    def test_strong_signal_green(self):
        color = get_color_by_rsrp(-80)
        assert color == [0, 255, 0, 200]

    def test_medium_signal_yellow(self):
        color = get_color_by_rsrp(-100)
        assert color[1] > 0
        assert color[0] > 0
        assert color[2] == 0

    def test_weak_signal_red(self):
        color = get_color_by_rsrp(-120)
        assert color == [255, 0, 0, 200]

    def test_boundary_high(self):
        color = get_color_by_rsrp(-90)
        assert color == [0, 255, 0, 200]

    def test_boundary_low(self):
        color = get_color_by_rsrp(-110)
        assert color[1] > 0
        assert color[0] > 0
        assert color[2] == 0

class TestDataIntegrity:
    def test_rsrp_range(self, sample_data):
        df = load_data(DATA_PATH)
        assert df["RSRP_dBm"].min() >= -140
        assert df["RSRP_dBm"].max() <= -40

    def test_sinr_range(self, sample_data):
        df = load_data(DATA_PATH)
        assert df["SINR_dB"].min() >= -10
        assert df["SINR_dB"].max() <= 40

    def test_band_values(self, sample_data):
        df = load_data(DATA_PATH)
        valid_bands = ["n28", "n41", "n78"]
        for band in df["Band"].unique():
            assert band in valid_bands, f"Invalid band: {band}"

    def test_terminal_types(self, sample_data):
        df = load_data(DATA_PATH)
        valid_types = ["Smartphone", "CPE", "IoT"]
        for t in df["TerminalType"].unique():
            assert t in valid_types, f"Invalid terminal type: {t}"

class TestFiltering:
    def test_band_filter(self, sample_data):
        filtered = sample_data[sample_data["Band"] == "n28"]
        assert len(filtered) == 2
        assert all(filtered["Band"] == "n28")

    def test_rsrp_filter(self, sample_data):
        filtered = sample_data[(sample_data["RSRP_dBm"] >= -100) & (sample_data["RSRP_dBm"] <= -90)]
        assert len(filtered) == 1
        assert filtered.iloc[0]["RSRP_dBm"] == -94.94

if __name__ == "__main__":
    pytest.main([__file__, "-v"])