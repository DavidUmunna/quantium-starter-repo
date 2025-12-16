from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# Load and enrich data
Sales_df = pd.read_csv("data/pink_morsel_df.csv").drop(columns=["Unnamed: 0"], errors="ignore")
Sales_df["date"] = pd.to_datetime(Sales_df["date"])
Sales_df["revenue"] = Sales_df["price"] * Sales_df["quantity"]
Sales_df = Sales_df.sort_values("date")
FOCAL_DATE = pd.to_datetime("2021-01-15")
try:
    import statsmodels.api  # noqa: F401
    TRENDLINE_MODE = "ols"
except ImportError:
    TRENDLINE_MODE = None

# Options for filters
product_options = sorted(Sales_df["product"].unique())
region_options = sorted(Sales_df["region"].unique())
region_radio_options = [{"label": "All regions", "value": "all"}] + [
    {"label": r.title(), "value": r} for r in region_options
]

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H2("Daily Sales Dashboard"),
        html.Div(
            [
                dcc.Dropdown(
                    id="product-filter",
                    options=[{"label": p.title(), "value": p} for p in product_options],
                    value=["pink morsel"],
                    multi=True,
                    placeholder="Select product(s)",
                ),
                dcc.RadioItems(
                    id="region-radio",
                    options=region_radio_options,
                    value="all",
                    inline=True,
                ),
            ],
            style={"display": "flex", "gap": "12px", "marginBottom": "12px"},
        ),
        html.Div(
            [
                dcc.Graph(id="revenue-trend", style={"flex": 2}),
                dcc.Graph(id="region-share", style={"flex": 1}),
            ],
            style={"display": "flex", "gap": "12px", "marginBottom": "12px"},
        ),
        html.Div(
            [
                dcc.Graph(id="quantity-box", style={"flex": 1}),
                dcc.Graph(id="price-quantity", style={"flex": 1}),
                dcc.Graph(id="price-quantity-hist", style={"flex": 1}),
            ],
            style={"display": "flex", "gap": "12px"},
        ),
    ],
    style={"padding": "20px", "fontFamily": "Arial, sans-serif"},
)


@callback(
    Output("revenue-trend", "figure"),
    Output("region-share", "figure"),
    Output("quantity-box", "figure"),
    Output("price-quantity", "figure"),
    Output("price-quantity-hist", "figure"),
    Input("product-filter", "value"),
    Input("region-radio", "value"),
)
def update_dashboard(selected_products, selected_region):
    df = Sales_df.copy()

    # Keep rows that match current filters
    if selected_products:
        df = df[df["product"].isin(selected_products)]
    if selected_region and selected_region != "all":
        df = df[df["region"] == selected_region]

    if df.empty:
        empty_fig = px.scatter(title="No data for the selected filters")
        return empty_fig, empty_fig, empty_fig, empty_fig, empty_fig

    daily_revenue = (
        df.groupby(["date", "product"], as_index=False)
        .agg(revenue=("revenue", "sum"))
    )
    revenue_trend = px.line(
        daily_revenue,
        x="date",
        y="revenue",
        color="product",
        markers=True,
        title="Daily revenue by product",
        labels={"revenue": "Revenue", "date": "Date", "product": "Product"},
    )
    revenue_trend.add_shape(
        type="line",
        x0=FOCAL_DATE,
        x1=FOCAL_DATE,
        y0=0,
        y1=1,
        xref="x",
        yref="paper",
        line=dict(color="red", dash="dot"),
    )
    revenue_trend.add_annotation(
        x=FOCAL_DATE,
        y=1,
        yref="paper",
        text="15 Jan 2021 price rise",
        showarrow=False,
        xanchor="left",
        yanchor="bottom",
        font=dict(color="red"),
    )

    region_revenue = df.groupby("region", as_index=False).agg(revenue=("revenue", "sum"))
    region_share = px.bar(
        region_revenue,
        x="region",
        y="revenue",
        color="region",
        title="Revenue share by region",
        labels={"revenue": "Revenue", "region": "Region"},
    )

    quantity_box = px.box(
        df,
        x="product",
        y="quantity",
        color="product",
        points="all",
        title="Quantity distribution by product",
        labels={"quantity": "Quantity", "product": "Product"},
    )

    price_quantity = px.scatter(
        df,
        x="quantity",
        y="price",
        color="product",
        trendline=TRENDLINE_MODE,
        title="Price vs quantity",
        labels={"quantity": "Quantity", "price": "Price", "product": "Product"},
    )

    price_quantity_hist = px.histogram(
        df,
        x="quantity",
        y="price",
        histfunc="avg",
        nbins=25,
        color="product",
        title="Average price by quantity bin",
        labels={"quantity": "Quantity", "price": "Price", "product": "Product"},
    )

    return revenue_trend, region_share, quantity_box, price_quantity, price_quantity_hist


if __name__ == "__main__":
    app.run(debug=True)
