import streamlit as st
import pandas as pd


def render_sidebar(df: pd.DataFrame) -> bool:
    # Sidebar is being rendered once so it is driving both tabs consistently.
    # Returning a boolean is allowing app.py to decide whether it should rerun after reset.
    with st.sidebar:
        st.subheader("Filters")

        st.multiselect(
            "Borough (neighbourhood_group)",
            options=sorted(df["neighbourhood_group"].unique()),
            key="boroughs",
        )

        st.multiselect(
            "Room type",
            options=sorted(df["room_type"].unique()),
            key="room_types",
        )

        p_min = int(df["price"].min())
        p_max_default = int(df["price"].quantile(0.99))
        p_max_slider = int(df["price"].quantile(0.995))

        st.slider(
            "Price range (USD)",
            min_value=p_min,
            max_value=max(p_max_slider, p_max_default),
            key="price_range",
        )

        st.slider(
            "Max minimum nights",
            min_value=1,
            max_value=int(max(30, df["minimum_nights"].quantile(0.99))),
            key="min_nights_max",
        )

        st.slider(
            "Availability range (days per year)",
            min_value=0,
            max_value=365,
            key="availability_range",
        )

        st.slider(
            "Max points on map (sampling for speed)",
            min_value=500,
            max_value=8000,
            step=500,
            key="max_map_points",
        )

        st.radio(
            "Aggregation for borough price chart",
            options=["Median", "Mean"],
            key="agg_metric",
            horizontal=False,
        )

        did_click_reset = st.button("Reset filters")

    return did_click_reset


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    # Filters are being applied in one place so logic is not duplicated across tabs.
    b = st.session_state["boroughs"]
    r = st.session_state["room_types"]
    p_lo, p_hi = st.session_state["price_range"]
    nights_hi = st.session_state["min_nights_max"]
    a_lo, a_hi = st.session_state["availability_range"]

    f = df[
        df["neighbourhood_group"].isin(b)
        & df["room_type"].isin(r)
        & df["price"].between(p_lo, p_hi)
        & (df["minimum_nights"] <= nights_hi)
        & df["availability_365"].between(a_lo, a_hi)
    ].copy()

    return f