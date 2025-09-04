import numpy as np
import pandas as pd
import pytest

from kabu.features.undervalued_search.domain import EPS, resample_eps_to_daily

# Set plotly as the default backend for pandas plotting
pd.options.plotting.backend = "plotly"


def test_resample():
    """EPSをdailyに引き伸ばす."""
    v1 = 81.82
    v2 = np.nan
    v3 = 70.79

    eps_ls = [
        EPS(report_date="2023-12-31", value=v1),
        EPS(report_date="2024-03-31", value=v2),
        EPS(report_date="2024-06-30", value=v3),
    ]

    dailies = resample_eps_to_daily(eps_ls, "2025-01-01")
    with pytest.raises(KeyError):
        dailies["2023-12-30"]
    assert dailies["2023-12-31"] == v1
    assert dailies["2024-01-01"] == v1

    assert dailies["2024-03-30"] == v1
    assert np.isnan(dailies["2024-03-31"])
    assert np.isnan(dailies["2024-04-01"])

    assert np.isnan(dailies["2024-06-29"])
    assert dailies["2024-06-30"] == v3
    assert dailies["2024-07-01"] == v3

    assert dailies["2024-07-01"] == v3

    assert dailies["2024-12-31"] == v3
    assert dailies["2025-01-01"] == v3
    with pytest.raises(KeyError):
        dailies["2025-01-02"]


def test_find_undervalued_period():
    """割安期間を検出する."""
