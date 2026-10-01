# Anime Explorer

Anime Explorer is a multipage Streamlit application created for the Streamlit "Ship It" project.

The application uses live anime data from the Kitsu API to help users explore anime, filter titles, analyze anime trends, and view trailers from famous anime series.

## Problem Statement

Anime viewers can struggle to find shows that match their interests because anime catalogs contain thousands of titles with different formats, ratings, episode counts, and popularity levels.

Anime Explorer is designed for anime viewers who want a faster and simpler way to narrow their choices, compare anime data, and learn more about titles they may want to watch.

## App Pages

### Home

The Home page introduces the purpose of the application and displays summary metrics calculated from the live anime dataset.

Users can also choose a preferred anime type. This preference is stored using Streamlit Session State and can affect other pages.

### Anime List

The Anime List page allows users to explore anime using multiple filters.

Users can filter by:

- Title
- Anime type
- Score range
- Maximum number of episodes

The results can also be sorted by score, popularity, title, or episode count.

### Graphs

The Graphs page displays summary statistics and grouped charts created from the anime dataset.

Charts include:

- Average score by anime type
- Number of anime by type
- Average episode count by anime type

### Trailers

The Trailers page provides a visual preview of five famous anime series.

The page is separated into tabs so users can easily move between different trailers.

## API

The project uses the Kitsu API.

Kitsu provides public anime information without requiring an API key for the GET requests used by this application.

The application sends requests using `requests.get()`.

The JSON returned by the API is transformed into a Pandas DataFrame so that the data can be filtered, sorted, summarized, and visualized.

API calls are cached using `st.cache_data` to prevent unnecessary network requests every time Streamlit reruns the application.

## Streamlit Features

The application demonstrates:

- Multipage architecture
- Session State across pages
- Cached API calls
- `st.columns`
- `st.sidebar`
- `st.tabs`
- `st.expander`
- `st.text_input`
- `st.selectbox`
- `st.slider`
- `st.radio`
- `st.checkbox`
- `st.metric`
- `st.dataframe`
- Multiple filters applied together
- Sorting
- Derived summary metrics
- Grouped data
- Charts
- Empty-result handling

## Running the Project

Install the required packages:

`pip install -r requirements.txt`

Run the Streamlit application:

`streamlit run app.py`

## Data Source

Anime data is retrieved from the Kitsu API.