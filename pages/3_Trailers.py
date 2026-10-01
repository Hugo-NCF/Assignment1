import streamlit as st

# Configure the page title, icon, and wide layout for this page.
st.set_page_config(page_title="Anime Trailers", page_icon="🎬", layout="wide")

st.title("🎬 Famous Anime Trailers")
st.write(
    "Watch trailers and previews from five famous anime series."
)

# Use tabs so each anime has its own section.
tabs = st.tabs(
    [
        "Attack on Titan",
        "Naruto",
        "Demon Slayer",
        "Jujutsu Kaisen",
        "One Piece",
    ]
)

# Display the Attack on Titan trailer.
with tabs[0]:
    st.header("Attack on Titan")
    st.write("**Genres:** Action, Drama, Fantasy")
    st.write(
        "Humanity fights for survival against enormous creatures known as Titans."
    )
    st.video("https://www.youtube.com/watch?v=MUCN-JwUvbY")

# Display the Naruto trailer.
with tabs[1]:
    st.header("Naruto")
    st.write("**Genres:** Action, Adventure, Fantasy")
    st.write(
        "Naruto Uzumaki dreams of becoming Hokage while training "
        "to become a powerful ninja."
    )
    st.video("https://www.youtube.com/watch?v=-G9BqkgZXRA")

# Display the Demon Slayer trailer.
with tabs[2]:
    st.header("Demon Slayer")
    st.write("**Genres:** Action, Adventure, Fantasy")
    st.write(
        "Tanjiro becomes a demon slayer after his family is attacked "
        "and his sister Nezuko is transformed into a demon."
    )
    st.video("https://www.youtube.com/watch?v=t6MXHczeEqc")

# Display the Jujutsu Kaisen trailer.
with tabs[3]:
    st.header("Jujutsu Kaisen")
    st.write("**Genres:** Action, Supernatural")
    st.write(
        "Yuji Itadori enters the world of Jujutsu Sorcerers "
        "after encountering a cursed object."
    )
    st.video("https://www.youtube.com/watch?v=pkKu9hLT-t8")

# Display the One Piece trailer.
with tabs[4]:
    st.header("One Piece")
    st.write("**Genres:** Action, Adventure, Fantasy")
    st.write(
        "Monkey D. Luffy and his crew travel across the seas searching "
        "for the legendary treasure known as the One Piece."
    )
    st.video("https://www.youtube.com/watch?v=MCb13lbVGE0")