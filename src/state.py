import streamlit as st
import pandas as pd


def init_session_state(df: pd.DataFrame) -> None:
    # Defaults are being set once so filters are persisting across reruns and tab switches.
    # default boroughs = all boroughs
    # default room types = all room types
    # default price range = (min price, p99) to avoid huge outliers by default
    # default min nights max = around p99, capped at 30
    # default availability range = (0, 365)
    # default map points = 2500
    # default agg metric = Median

    boroughs = sorted(df["neighbourhood_group"].unique())
    room_types = sorted(df["room_type"].unique())

    p_min = int(df["price"].min())
    p99 = int(df["price"].quantile(0.99))

    if "boroughs" not in st.session_state:
        st.session_state["boroughs"] = boroughs

    if "room_types" not in st.session_state:
        st.session_state["room_types"] = room_types

    if "price_range" not in st.session_state:
        st.session_state["price_range"] = (p_min, p99)

    if "min_nights_max" not in st.session_state:
        st.session_state["min_nights_max"] = int(min(df["minimum_nights"].quantile(0.99), 30))

    if "availability_range" not in st.session_state:
        st.session_state["availability_range"] = (0, 365)

    if "max_map_points" not in st.session_state:
        st.session_state["max_map_points"] = 2500

    if "agg_metric" not in st.session_state:
        st.session_state["agg_metric"] = "Median"

# This is reassigning those defaults back into session state when you click Reset.
def reset_filters(df: pd.DataFrame) -> None:
    # Reset is being provided so users can recover quickly after filtering to zero rows.
    boroughs = sorted(df["neighbourhood_group"].unique())
    room_types = sorted(df["room_type"].unique())

    p_min = int(df["price"].min())
    p99 = int(df["price"].quantile(0.99))

    st.session_state["boroughs"] = boroughs
    st.session_state["room_types"] = room_types
    st.session_state["price_range"] = (p_min, p99)
    st.session_state["min_nights_max"] = int(min(df["minimum_nights"].quantile(0.99), 30))
    st.session_state["availability_range"] = (0, 365)
    st.session_state["max_map_points"] = 2500
    st.session_state["agg_metric"] = "Median"