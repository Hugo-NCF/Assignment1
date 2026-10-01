import streamlit as st
import pandas as pd
from anime_api import get_anime_data

# Configure the page title, icon, and wide layout for this page.
st.set_page_config(page_title="Anime List", page_icon="📚", layout="wide")

# Initialize the preferred type if this page is opened first.
if "preferred_type" not in st.session_state:
    st.session_state["preferred_type"] = "All types"

st.title("📚 Anime List")
st.write(
    "Use the filters to narrow down the anime list and find "
    "something that interests you."
)

# Load the anime data.
try:
    df = get_anime_data()
except Exception as error:
    st.error("Anime data could not be loaded right now.")
    st.caption(f"Technical detail: {error}")
    st.stop()

# Build the list of anime types.
anime_types = sorted(df["type"].dropna().unique().tolist())
type_options = ["All types"] + anime_types

# Use the type selected on the Home page as the default.
preferred_type = st.session_state["preferred_type"]

if preferred_type in type_options:
    default_type_index = type_options.index(preferred_type)
else:
    default_type_index = 0

# Put the filters in the sidebar.
with st.sidebar:
    st.header("Filter Anime")

    # Search anime by title.
    search_text = st.text_input(
        "Search Title",
        placeholder="Type an anime title...",
    )

    # Filter anime by type.
    selected_type = st.selectbox(
        "Anime Type",
        type_options,
        index=default_type_index,
    )

    # Filter anime by score.
    score_range = st.slider(
        "Score Range",
        min_value=0.0,
        max_value=10.0,
        value=(0.0, 10.0),
        step=0.1,
    )

    # Filter anime by maximum episodes.
    episode_limit = st.slider(
        "Maximum Episodes",
        min_value=1,
        max_value=500,
        value=500,
    )

    # Choose how the table should be sorted.
    sort_choice = st.radio(
        "Sort Results By",
        ["Score", "Popularity", "Title", "Episodes"],
    )

# Start with a copy of the full dataset.
filtered_df = df.copy()

# Filter by title if the user entered text.
if search_text:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(
            search_text,
            case=False,
            na=False,
        )
    ]

# Filter by anime type.
if selected_type != "All types":
    filtered_df = filtered_df[
        filtered_df["type"] == selected_type
    ]

# Filter by the selected score range.
filtered_df = filtered_df[
    filtered_df["score"].fillna(-1).between(
        score_range[0],
        score_range[1],
    )
]

# Filter by episode count.
filtered_df = filtered_df[
    filtered_df["episodes"].isna()
    | (filtered_df["episodes"] <= episode_limit)
]

# Sort the results based on the selected option.
if sort_choice == "Score":
    filtered_df = filtered_df.sort_values(
        "score",
        ascending=False,
    )

elif sort_choice == "Popularity":
    filtered_df = filtered_df.sort_values(
        "popularity",
        ascending=True,
        na_position="last",
    )

elif sort_choice == "Title":
    filtered_df = filtered_df.sort_values(
        "title",
        ascending=True,
    )

elif sort_choice == "Episodes":
    filtered_df = filtered_df.sort_values(
        "episodes",
        ascending=True,
        na_position="last",
    )

# Create three columns for filtered summary metrics.
columns = st.columns(3)

columns[0].metric("Matching Anime", len(filtered_df))

# Calculate the average score of the filtered anime.
average_score = filtered_df["score"].dropna().mean()

if pd.notna(average_score):
    columns[1].metric("Average Score", f"{average_score:.2f}")
else:
    columns[1].metric("Average Score", "N/A")

# Calculate the average number of episodes.
average_episodes = filtered_df["episodes"].dropna().mean()

if pd.notna(average_episodes):
    columns[2].metric("Average Episodes", f"{average_episodes:.1f}")
else:
    columns[2].metric("Average Episodes", "N/A")

st.divider()

# Handle the case where no anime match the filters.
if len(filtered_df) == 0:
    st.warning(
        "No anime match that combination of filters. "
        "Try changing one or more filters."
    )
    st.stop()

st.subheader("Results")

# Choose which columns should appear in the table.
preferred_columns = [
    "title",
    "type",
    "episodes",
    "score",
    "year",
    "status",
    "popularity",
]

st.dataframe(
    filtered_df[preferred_columns],
    use_container_width=True,
    hide_index=True,
)

st.subheader("Quick Details")

# Let the user select one anime from the filtered results.
selected_title = st.selectbox(
    "Choose an Anime to Inspect",
    filtered_df["title"].tolist(),
)

# Find the row belonging to the selected anime.
selected_anime = filtered_df[
    filtered_df["title"] == selected_title
].iloc[0]

# Create columns for the poster and anime information.
columns = st.columns([1, 2])

with columns[0]:
    image_url = selected_anime["image_url"]

    if isinstance(image_url, str) and image_url:
        st.image(image_url)

with columns[1]:
    st.subheader(selected_title)

    score = selected_anime["score"]

    if pd.notna(score):
        st.write(f"**Score:** {score:.1f}/10")
    else:
        st.write("**Score:** N/A")

    st.write(f"**Type:** {selected_anime['type']}")

    episodes = selected_anime["episodes"]

    if pd.notna(episodes):
        st.write(f"**Episodes:** {int(episodes)}")
    else:
        st.write("**Episodes:** Unknown")

    st.write(f"**Year:** {selected_anime['year']}")
    st.write(f"**Status:** {selected_anime['status']}")

    synopsis = selected_anime["synopsis"]

    if isinstance(synopsis, str) and synopsis:
        st.write(synopsis)
    else:
        st.write("No synopsis is available.")