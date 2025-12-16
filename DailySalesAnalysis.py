from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# Load and enrich data
Sales_df = pd.read_csv("data/Combined_Sales_df.csv").drop(columns=["Unnamed: 0"], errors="ignore")
Sales_df["date"] = pd.to_datetime(Sales_df["date"])
Sales_df["revenue"] = Sales_df["price"] * Sales_df["quantity"]
Sales_df = Sales_df.sort_values("date")

# Options for filters
product_options = sorted(Sales_df["product"].unique())
region_options = sorted(Sales_df["region"].unique())

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H2("Daily Sales Dashboard"),
        html.Div(
            [
                dcc.Dropdown(
                    id="product-filter",
                    options=[{"label": p.title(), "value": p} for p in product_options],
                    value=product_options,
                    multi=True,
                    placeholder="Select product(s)",
                ),
                dcc.Dropdown(
                    id="region-filter",
                    options=[{"label": r.title(), "value": r} for r in region_options],
                    value=region_options,
                    multi=True,
                    placeholder="Select region(s)",
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
    Input("product-filter", "value"),
    Input("region-filter", "value"),
)
def update_dashboard(selected_products, selected_regions):
    df = Sales_df.copy()

    if selected_products:
        df = df[df["product"].isin(selected_products)]
    if selected_regions:
        df = df[df["region"].isin(selected_regions)]

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
        trendline="ols",
        title="Price vs quantity",
        labels={"quantity": "Quantity", "price": "Price", "product": "Product"},
    )

    return revenue_trend, region_share, quantity_box, price_quantity


if __name__ == "__main__":
    app.run(debug=True)
