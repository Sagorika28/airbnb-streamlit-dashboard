import pandas as pd
import streamlit as st


@st.cache_data
def load_airbnb(csv_path: str) -> pd.DataFrame:
    # Loading is being cached so widget changes are not re-reading the CSV repeatedly.
    df = pd.read_csv(csv_path)

    # Converting types is being done to keep charting consistent.
    df["last_review"] = pd.to_datetime(df["last_review"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["reviews_per_month"] = pd.to_numeric(df["reviews_per_month"], errors="coerce")

    # Dropping nulls is being done for required fields in map + filters.
    df = df.dropna(subset=["latitude", "longitude", "price", "room_type", "neighbourhood_group", "neighbourhood"])

    # Removing non-sensical values is preventing broken axes and misleading bins.
    df = df[df["price"] > 0]
    df = df[df["minimum_nights"] > 0]

    return df