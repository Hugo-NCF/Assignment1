"""
Small wrapper around the Kitsu Anime API.

Why this API works well for this project:
- No key, no auth, no signup - a plain GET request
- Real, live anime data
- JSON results that can be converted into a DataFrame

st.cache_data keeps the results cached for an hour so Streamlit
does not call the API again every time a widget changes.
"""

import requests
import pandas as pd
import streamlit as st

# The base URL for the Kitsu Anime API.
KITSU_ANIME_URL = "https://kitsu.io/api/edge/anime"


# Convert one anime from Kitsu into a simpler dictionary.
def clean_anime(anime):
    attributes = anime.get("attributes", {})

    # Get the English title when possible.
    titles = attributes.get("titles", {})
    title = (
        titles.get("en")
        or titles.get("en_jp")
        or attributes.get("canonicalTitle")
        or "Unknown"
    )

    # Kitsu ratings are out of 100, so convert them to a 10-point score.
    rating = attributes.get("averageRating")
    if rating:
        score = float(rating) / 10
    else:
        score = None

    # Get the poster image.
    poster = attributes.get("posterImage") or {}
    image_url = poster.get("medium")

    # Get the year from the start date.
    start_date = attributes.get("startDate")
    if start_date:
        year = start_date[:4]
    else:
        year = None

    # Return the fields used in the Streamlit app.
    return {
        "title": title,
        "type": attributes.get("subtype"),
        "episodes": attributes.get("episodeCount"),
        "score": score,
        "popularity": attributes.get("popularityRank"),
        "year": year,
        "status": attributes.get("status"),
        "synopsis": attributes.get("synopsis"),
        "image_url": image_url,
    }


# Cache the anime data for one hour so reruns do not re-hit the network.
@st.cache_data(ttl=3600, show_spinner="Loading anime...")
def get_anime_data():
    all_results = []

    # Kitsu returns up to 20 results at a time.
    # Use three requests so the app has around 60 anime.
    offsets = [0, 20, 40]

    for offset in offsets:
        # Build the query parameters for the request.
        params = {
            "page[limit]": 20,
            "page[offset]": offset,
            "sort": "-averageRating",
        }

        # Send the GET request to the Kitsu API.
        response = requests.get(
            KITSU_ANIME_URL,
            params=params,
            timeout=20,
        )

        # Raise an error if the request failed.
        response.raise_for_status()

        # Parse the JSON response.
        payload = response.json()

        # Add the anime results to the full list.
        all_results.extend(payload.get("data", []))

    # Clean each result before creating the DataFrame.
    cleaned_results = []

    for anime in all_results:
        cleaned_results.append(clean_anime(anime))

    # Convert the cleaned list into a DataFrame.
    return pd.DataFrame(cleaned_results)