"""Browser interface for the music recommender."""

import logging

import pandas as pd
import streamlit as st

from src.recommender import SCORING_MODES, load_songs, recommend_songs

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")


@st.cache_data
def cached_songs() -> list[dict]:
    """Load the song catalog once for the Streamlit app."""
    return load_songs("data/songs.csv")


def unique_values(songs: list[dict], field: str) -> list[str]:
    """Return sorted unique string values for one song field."""
    return sorted({str(song[field]) for song in songs if song.get(field)})


def build_preferences(songs: list[dict]) -> dict:
    """Collect listener preferences from the sidebar."""
    genres = unique_values(songs, "genre")
    moods = unique_values(songs, "mood")
    decades = unique_values(songs, "release_decade")
    mood_tags = unique_values(songs, "detailed_mood_tag")

    st.sidebar.header("Listener Profile")
    return {
        "genre": st.sidebar.selectbox("Favorite genre", genres, index=genres.index("pop") if "pop" in genres else 0),
        "mood": st.sidebar.selectbox("Preferred mood", moods, index=moods.index("happy") if "happy" in moods else 0),
        "energy": st.sidebar.slider("Energy", 0.0, 1.0, 0.80, 0.01),
        "acousticness": st.sidebar.slider("Acousticness", 0.0, 1.0, 0.25, 0.01),
        "tempo_bpm": st.sidebar.slider("Tempo BPM", 60, 180, 120, 1),
        "target_popularity": st.sidebar.slider("Target popularity", 0, 100, 85, 1),
        "preferred_decade": st.sidebar.selectbox(
            "Preferred decade",
            decades,
            index=decades.index("2010s") if "2010s" in decades else 0,
        ),
        "detailed_mood_tag": st.sidebar.selectbox(
            "Detailed mood tag",
            mood_tags,
            index=mood_tags.index("uplifting") if "uplifting" in mood_tags else 0,
        ),
        "vocal_intensity": st.sidebar.slider("Vocal intensity", 0.0, 1.0, 0.70, 0.01),
        "lyrical_depth": st.sidebar.slider("Lyrical depth", 0.0, 1.0, 0.45, 0.01),
        "replay_value": st.sidebar.slider("Replay value", 0.0, 1.0, 0.88, 0.01),
    }


def main() -> None:
    st.set_page_config(page_title="Music Recommender", page_icon=None, layout="wide")
    st.title("Music Recommender Reliability System")
    st.write(
        "Choose a listener profile, then review ranked recommendations with scores, "
        "confidence estimates, and explanations."
    )

    songs = cached_songs()
    user_prefs = build_preferences(songs)

    st.sidebar.header("Recommendation Settings")
    mode = st.sidebar.selectbox("Scoring mode", list(SCORING_MODES.keys()), index=1)
    result_count = st.sidebar.slider("Number of songs", 1, 10, 5, 1)
    apply_diversity = st.sidebar.checkbox("Apply diversity adjustment", value=True)

    recommendations = recommend_songs(
        user_prefs,
        songs,
        k=result_count,
        mode=mode,
        apply_diversity=apply_diversity,
    )

    rows = []
    for rank, (song, score, confidence, explanation) in enumerate(recommendations, start=1):
        rows.append(
            {
                "Rank": rank,
                "Title": song["title"],
                "Artist": song["artist"],
                "Genre": song["genre"],
                "Mood": song["mood"],
                "Score": round(score, 2),
                "Confidence": round(confidence, 2),
                "Why it matched": explanation,
            }
        )

    st.subheader("Recommendations")
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

    if rows:
        top = rows[0]
        st.subheader("Top Match")
        st.metric("Confidence", f"{top['Confidence']:.2f}")
        st.write(f"**{top['Title']}** by **{top['Artist']}**")
        st.write(top["Why it matched"])

    with st.expander("Current listener profile"):
        st.json(user_prefs)


if __name__ == "__main__":
    main()
