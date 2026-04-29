from src.recommender import Song, UserProfile, Recommender, confidence_from_score, recommend_songs

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_confidence_score_stays_between_zero_and_one():
    assert confidence_from_score(-5.0, mode="balanced") == 0.0
    assert 0.0 < confidence_from_score(5.0, mode="balanced") < 1.0
    assert confidence_from_score(500.0, mode="balanced") == 1.0


def test_recommend_songs_includes_confidence_and_explanation():
    songs = [
        {
            "title": "Bright Test",
            "artist": "Example Artist",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.82,
            "acousticness": 0.22,
        }
    ]
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "acousticness": 0.2,
    }

    results = recommend_songs(user_prefs, songs, k=1, mode="balanced")
    song, score, confidence, explanation = results[0]

    assert song["title"] == "Bright Test"
    assert score > 0
    assert 0.0 <= confidence <= 1.0
    assert "genre match" in explanation


def test_diversity_penalty_reduces_repeated_artist_score():
    songs = [
        {
            "title": "First Match",
            "artist": "Same Artist",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "acousticness": 0.2,
        },
        {
            "title": "Second Match",
            "artist": "Same Artist",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "acousticness": 0.2,
        },
    ]
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "acousticness": 0.2,
    }

    results = recommend_songs(user_prefs, songs, k=2, mode="balanced", apply_diversity=True)

    assert results[1][1] < results[0][1]
    assert "artist diversity penalty" in results[1][3]
