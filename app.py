import streamlit as st
import pandas as pd
from anime_api import get_anime_data

# Configure the page title, icon, and wide layout for this app.
st.set_page_config(page_title="Anime Explorer", page_icon="🎌", layout="wide")

# Initialize the preferred anime type the first time the app runs.
if "preferred_type" not in st.session_state:
    st.session_state["preferred_type"] = "All types"

# Display the app title and description.
st.title("🎌 Anime Explorer")
st.markdown(
    "Explore popular anime, filter titles, compare anime data, "
    "and watch trailers from famous anime series."
)

# Show the problem statement required for the project.
with st.expander("Why I Built This App — Problem Statement", expanded=True):
    st.write(
        "**Who is this for?** Anime viewers who want an easier way "
        "to decide what anime they might want to watch."
    )

    st.write(
        "**What problem are they facing?** Anime catalogs contain thousands "
        "of titles with different scores, episode counts, formats, and "
        "popularity levels."
    )

    st.write(
        "**Why does it matter?** A focused anime explorer can make it easier "
        "to compare anime and decide what to watch."
    )

# Load the anime data from the API.
try:
    anime_df = get_anime_data()
except Exception as error:
    st.error("Anime data could not be loaded right now.")
    st.caption(f"Technical detail: {error}")
    st.stop()

st.subheader("Live Anime Snapshot")

# Create three columns for the summary metrics.
columns = st.columns(3)

# Show the number of anime loaded.
columns[0].metric("Anime Loaded", len(anime_df))

# Calculate and show the average score.
average_score = anime_df["score"].dropna().mean()
if pd.notna(average_score):
    columns[1].metric("Average Score", f"{average_score:.2f}")
else:
    columns[1].metric("Average Score", "N/A")

# Calculate and show the average episode count.
average_episodes = anime_df["episodes"].dropna().mean()
if pd.notna(average_episodes):
    columns[2].metric("Average Episodes", f"{average_episodes:.1f}")
else:
    columns[2].metric("Average Episodes", "N/A")

st.divider()

st.subheader("Choose Your Preferred Anime Type")
st.write(
    "Your selection will be remembered when you visit the "
    "Anime List and Graphs pages."
)

# Build the list of anime types from the DataFrame.
anime_types = sorted(anime_df["type"].dropna().unique().tolist())
type_options = ["All types"] + anime_types

# Find the current Session State value in the options list.
current_type = st.session_state["preferred_type"]

if current_type in type_options:
    default_index = type_options.index(current_type)
else:
    default_index = 0

# Let the user choose a preferred anime type.
preferred_type = st.selectbox(
    "Preferred Anime Type",
    type_options,
    index=default_index,
)

# Save the selection in Session State.
st.session_state["preferred_type"] = preferred_type

st.success(f"Current preferred type: **{preferred_type}**")

# Explain how the pages are organized.
with st.expander("How the App is Organized"):
    st.write(
        "**📚 Anime List** — Find anime using filters and sorting."
    )

    st.write(
        "**📊 Graphs** — Explore grouped data and summary statistics."
    )

    st.write(
        "**🎬 Trailers** — Watch trailers from five famous anime."
    )

st.caption("Anime data is retrieved from the Kitsu API.")