import streamlit as st

from src.data import load_airbnb
from src.state import init_session_state, reset_filters
from src.filters import render_sidebar, apply_filters
from src.charts import price_hist, borough_price_bar, listings_map, price_vs_availability


# Page configuration is being set before any Streamlit elements are rendered.
st.set_page_config(page_title="NYC Airbnb", layout="wide")

st.title("NYC Airbnb Sample Dashboard")
st.caption("Two tabs, Plotly interactivity, hover tooltips on map, and modular code structure.")


# Data is being loaded once (cached) and then used throughout the app.
df = load_airbnb("data/AB_NYC_2019.csv")

# Session state is being initialized so filters are persisting across reruns and tab switches.
init_session_state(df)

# Sidebar is being rendered and reset behavior is being handled.
did_click_reset = render_sidebar(df)
if did_click_reset:
    reset_filters(df)
    st.rerun()

# Filters are being applied once so both tabs share the same subset.
f = apply_filters(df)

# Quick metrics are being shown to provide context for the current filter state. These are quick summaries of the current filtered subset. They update every time filters change.
c1, c2, c3 = st.columns(3)
c1.metric("Filtered listings", f"{len(f):,}")
c2.metric("Median price", f"${int(f['price'].median()) if len(f) else 0}")
c3.metric("Median reviews/month", f"{float(f['reviews_per_month'].median()) if len(f) else 0:.2f}")

# Two UI sections, but both are reading the same filtered dataframe f.
tab_overview, tab_explore = st.tabs(["Overview", "Map + Drilldown"])

with tab_overview:
    st.subheader("Price distribution and borough comparison")

    if len(f) == 0:
        st.warning("No rows match the current filters. Try widening the price range or selecting more boroughs.")
    else:
        colA, colB = st.columns(2)

        with colA:
            st.plotly_chart(price_hist(f), width="stretch")

        with colB:
            st.plotly_chart(borough_price_bar(f, st.session_state["agg_metric"]), width="stretch")

        st.subheader("Top neighborhoods by listing count")
        top = (
            f["neighbourhood"]
            .value_counts()
            .head(15)
            .rename_axis("neighbourhood")
            .reset_index(name="listings")
        )
        st.dataframe(top, width="stretch")

with tab_explore:
    st.subheader("Hoverable map + relationship view")

    if len(f) == 0:
        st.warning("No rows match the current filters. Try widening the filters to see the map and plots.")
    else:
        st.plotly_chart(listings_map(f, st.session_state["max_map_points"]), width="stretch")
        st.plotly_chart(price_vs_availability(f), width="stretch")

        st.subheader("Listings table (filtered, top 200 by price)")
        cols = [
            "name",
            "neighbourhood_group",
            "neighbourhood",
            "room_type",
            "price",
            "minimum_nights",
            "number_of_reviews",
            "reviews_per_month",
            "availability_365",
            "last_review",
        ]
        st.dataframe(
            f[cols].sort_values("price", ascending=False).head(200),
            width="stretch",
        )