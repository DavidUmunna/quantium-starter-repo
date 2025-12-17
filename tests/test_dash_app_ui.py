import pytest

import DailySalesAnalysis


@pytest.mark.usefixtures("dash_duo")
def test_header_present(dash_duo):
    dash_duo.start_server(DailySalesAnalysis.app)
    dash_duo.wait_for_text_to_equal("h2", "Daily Sales Dashboard", timeout=10)


@pytest.mark.usefixtures("dash_duo")
def test_visualisation_present(dash_duo):
    dash_duo.start_server(DailySalesAnalysis.app)
    graph = dash_duo.find_element("#revenue-trend")
    assert graph is not None


@pytest.mark.usefixtures("dash_duo")
def test_region_picker_present(dash_duo):
    dash_duo.start_server(DailySalesAnalysis.app)
    radio = dash_duo.find_element("#region-radio")
    assert radio is not None
