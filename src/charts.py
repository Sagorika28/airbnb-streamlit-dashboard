import numpy as np
import pandas as pd
import plotly.express as px

# Returns a Plotly histogram of price
def price_hist(df: pd.DataFrame):
    # Histogram is being used to show skew and typical price ranges.
    fig = px.histogram(df, x="price", nbins=60, title="Price distribution")
    fig.update_layout(xaxis_title="Price (USD)", yaxis_title="Listings")
    return fig

# returns a bar chart with the listing count shown as text labels
def borough_price_bar(df: pd.DataFrame, agg_metric: str):
    # Aggregation choice is being supported to teach robustness (median) vs sensitivity (mean).
    if agg_metric == "Median":
        agg = df.groupby("neighbourhood_group", as_index=False).agg(
            price_value=("price", "median"),
            listings=("id", "count"),
        )
        title = "Median price by borough (text shows sample size)"
        y_label = "Median price (USD)"
    else:
        agg = df.groupby("neighbourhood_group", as_index=False).agg(
            price_value=("price", "mean"),
            listings=("id", "count"),
        )
        title = "Mean price by borough (text shows sample size)"
        y_label = "Mean price (USD)"

    agg = agg.sort_values("price_value", ascending=False)

    fig = px.bar(agg, x="neighbourhood_group", y="price_value", text="listings", title=title)
    fig.update_traces(textposition="outside")
    fig.update_layout(xaxis_title="Borough", yaxis_title=y_label)
    return fig


def listings_map(df: pd.DataFrame, max_points: int):
    # Sampling is being applied to keep the map responsive for larger filters.
    n = min(len(df), max_points)
    map_df = df.sample(n, random_state=42)

    # Mapbox style is being set to open-street-map so a token is not required.
    fig = px.scatter_mapbox(
        map_df,
        lat="latitude",
        lon="longitude",
        color="room_type",
        size=np.clip(map_df["number_of_reviews"], 1, 200),
        size_max=18,
        zoom=10,
        hover_name="name",
        hover_data={
            "neighbourhood_group": True,
            "neighbourhood": True,
            "price": ":.0f",
            "minimum_nights": True,
            "number_of_reviews": True,
            "availability_365": True,
            "latitude": False,
            "longitude": False,
        },
        title="Listings map (hover to inspect)",
    )
    fig.update_layout(mapbox_style="open-street-map", margin={"r": 0, "t": 40, "l": 0, "b": 0})
    return fig


def price_vs_availability(df: pd.DataFrame):
    # Sampling is being used to keep scatter plots readable and fast.
    scatter_df = df.sample(min(len(df), 4000), random_state=42)

    fig = px.scatter(
        scatter_df,
        x="availability_365",
        y="price",
        color="room_type",
        hover_name="name",
        hover_data={
            "neighbourhood_group": True,
            "neighbourhood": True,
            "minimum_nights": True,
            "number_of_reviews": True,
            "reviews_per_month": True,
        },
        opacity=0.55,
        title="Price vs availability (sampled for speed)",
    )
    fig.update_layout(xaxis_title="Availability (days/year)", yaxis_title="Price (USD)")
    return fig