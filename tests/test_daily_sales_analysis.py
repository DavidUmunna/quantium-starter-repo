import pandas as pd
import plotly.graph_objects as go

import DailySalesAnalysis as app


def test_sales_df_loaded_has_expected_columns():
    df = app.Sales_df
    expected = {"product", "price", "quantity", "date", "region", "revenue"}
    assert expected.issubset(df.columns)
    assert (df["price"] > 0).all()
    assert (df["quantity"] > 0).all()


def test_update_dashboard_returns_figures_tuple():
    figs = app.update_dashboard(["pink morsel"], "all")
    assert len(figs) == 5
    assert all(isinstance(fig, go.Figure) for fig in figs)


def test_region_filter_limits_data_points():
    region = "north"
    figs = app.update_dashboard(["pink morsel"], region)
    region_share = figs[1]
    # Bar chart x values should only include the selected region
    assert set(region_share.data[0].x) == {region}

    filtered = app.Sales_df[
        (app.Sales_df["product"] == "pink morsel")
        & (app.Sales_df["region"] == region)
    ]
    scatter = figs[3]
    first_trace = scatter.data[0]
    assert len(first_trace.x) == len(filtered)


def test_empty_filters_return_empty_state():
    figs = app.update_dashboard(["nonexistent"], "all")
    empty_fig = figs[0]
    assert "No data for the selected filters" in empty_fig.layout.title.text
    assert len(empty_fig.data) == 0 or all(
        (tr.x is None or len(tr.x) == 0) for tr in empty_fig.data
    )


def test_focal_date_marker_present():
    figs = app.update_dashboard(["pink morsel"], "all")
    revenue_trend = figs[0]
    shapes = revenue_trend.layout.shapes
    assert any(pd.to_datetime(shape.x0) == app.FOCAL_DATE for shape in shapes)
    assert any("price rise" in ann.text.lower() for ann in revenue_trend.layout.annotations)
