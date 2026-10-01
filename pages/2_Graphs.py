import streamlit as st
import pandas as pd
from anime_api import get_anime_data

# Configure the page title, icon, and wide layout for this page.
st.set_page_config(page_title="Anime Graphs", page_icon="📊", layout="wide")

# Initialize the preferred type if this page is opened first.
if "preferred_type" not in st.session_state:
    st.session_state["preferred_type"] = "All types"

st.title("📊 Anime Trends")
st.write(
    "Explore patterns in the anime data using summary metrics "
    "and grouped charts."
)

# Load the anime data.
try:
    df = get_anime_data()
except Exception as error:
    st.error("Anime data could not be loaded right now.")
    st.caption(f"Technical detail: {error}")
    st.stop()

# Read the preferred anime type from Session State.
preferred_type = st.session_state["preferred_type"]

# Let the user decide whether to use their saved preference.
use_preference = st.checkbox(
    f"Use preferred type: {preferred_type}",
    value=preferred_type != "All types",
    disabled=preferred_type == "All types",
)

# Start with the full dataset.
chart_df = df.copy()

# Filter the graph data if the preference is being used.
if use_preference and preferred_type != "All types":
    chart_df = chart_df[
        chart_df["type"] == preferred_type
    ]

# Stop if the filter leaves no results.
if len(chart_df) == 0:
    st.warning("There is no data for the current selection.")
    st.stop()

# Create four columns for summary metrics.
columns = st.columns(4)

columns[0].metric("Anime Analyzed", len(chart_df))

# Calculate the average score.
average_score = chart_df["score"].dropna().mean()

if pd.notna(average_score):
    columns[1].metric("Average Score", f"{average_score:.2f}")
else:
    columns[1].metric("Average Score", "N/A")

# Calculate the average number of episodes.
average_episodes = chart_df["episodes"].dropna().mean()

if pd.notna(average_episodes):
    columns[2].metric("Average Episodes", f"{average_episodes:.1f}")
else:
    columns[2].metric("Average Episodes", "N/A")

# Find the most common anime type.
most_common_type = chart_df["type"].dropna().mode()

if len(most_common_type) > 0:
    columns[3].metric("Most Common Type", most_common_type.iloc[0])
else:
    columns[3].metric("Most Common Type", "N/A")

st.divider()

# Use tabs to organize the three charts.
tabs = st.tabs(
    [
        "Average Score",
        "Anime Types",
        "Episodes",
    ]
)

with tabs[0]:
    st.subheader("Average Score by Anime Type")

    # Group anime by type and calculate the average score.
    score_by_type = (
        chart_df
        .dropna(subset=["type", "score"])
        .groupby("type")["score"]
        .mean()
        .sort_values(ascending=False)
    )

    if len(score_by_type) == 0:
        st.info("There is not enough data for this chart.")
    else:
        st.bar_chart(score_by_type)

with tabs[1]:
    st.subheader("Number of Anime by Type")

    # Count how many anime belong to each type.
    type_counts = chart_df["type"].dropna().value_counts()

    if len(type_counts) == 0:
        st.info("There is not enough data for this chart.")
    else:
        st.bar_chart(type_counts)

with tabs[2]:
    st.subheader("Average Episodes by Anime Type")

    # Group anime by type and calculate the average episode count.
    episodes_by_type = (
        chart_df
        .dropna(subset=["type", "episodes"])
        .groupby("type")["episodes"]
        .mean()
        .sort_values(ascending=False)
    )

    if len(episodes_by_type) == 0:
        st.info("There is not enough data for this chart.")
    else:
        st.bar_chart(episodes_by_type)

# Show the grouped values used in the charts.
with st.expander("See Grouped Data"):
    grouped_table = (
        chart_df
        .dropna(subset=["type"])
        .groupby("type")
        .agg(
            anime_count=("title", "count"),
            average_score=("score", "mean"),
            average_episodes=("episodes", "mean"),
        )
        .round(2)
        .reset_index()
    )

    st.dataframe(
        grouped_table,
        use_container_width=True,
        hide_index=True,
    )