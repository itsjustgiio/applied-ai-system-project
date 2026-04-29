import csv
import logging
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

SCORING_MODES = {
    "balanced": {
        "genre_match": 2.0,
        "mood_match": 1.5,
        "energy_similarity": 2.0,
        "acousticness_similarity": 1.0,
        "tempo_similarity": 0.5,
        "popularity_similarity": 0.8,
        "release_decade_match": 1.2,
        "detailed_mood_tag_match": 1.0,
        "vocal_intensity_similarity": 0.8,
        "lyrical_depth_similarity": 0.7,
        "replay_value_similarity": 0.6,
    },
    "genre_first": {
        "genre_match": 3.2,
        "mood_match": 1.0,
        "energy_similarity": 1.4,
        "acousticness_similarity": 0.8,
        "tempo_similarity": 0.4,
        "popularity_similarity": 0.6,
        "release_decade_match": 1.0,
        "detailed_mood_tag_match": 0.8,
        "vocal_intensity_similarity": 0.5,
        "lyrical_depth_similarity": 0.5,
        "replay_value_similarity": 0.4,
    },
    "mood_first": {
        "genre_match": 1.3,
        "mood_match": 2.8,
        "energy_similarity": 1.8,
        "acousticness_similarity": 0.9,
        "tempo_similarity": 0.4,
        "popularity_similarity": 0.5,
        "release_decade_match": 0.8,
        "detailed_mood_tag_match": 1.8,
        "vocal_intensity_similarity": 0.7,
        "lyrical_depth_similarity": 0.8,
        "replay_value_similarity": 0.4,
    },
    "energy_focused": {
        "genre_match": 1.2,
        "mood_match": 1.0,
        "energy_similarity": 3.4,
        "acousticness_similarity": 0.7,
        "tempo_similarity": 0.8,
        "popularity_similarity": 0.6,
        "release_decade_match": 0.7,
        "detailed_mood_tag_match": 0.7,
        "vocal_intensity_similarity": 0.9,
        "lyrical_depth_similarity": 0.4,
        "replay_value_similarity": 0.6,
    },
}

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by match to the user profile."""
        scored_songs = sorted(
            self.songs,
            key=lambda song: self._score_song_object(user, song)[0],
            reverse=True,
        )
        return scored_songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a short explanation for why a song was recommended."""
        _, reasons = self._score_song_object(user, song)
        return ", ".join(reasons) if reasons else "General similarity match."

    def _score_song_object(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "acousticness": 0.8 if user.likes_acoustic else 0.2,
        }
        song_dict = {
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "tempo_bpm": song.tempo_bpm,
            "valence": song.valence,
            "danceability": song.danceability,
            "acousticness": song.acousticness,
        }
        return score_song(user_prefs, song_dict)


def _resolve_mode_weights(mode: str) -> Dict[str, float]:
    """Return the weight preset for the selected scoring mode."""
    if mode not in SCORING_MODES:
        logger.warning("Unknown scoring mode '%s'; falling back to balanced mode.", mode)
    return SCORING_MODES.get(mode, SCORING_MODES["balanced"])


def _closeness_points(max_points: float, gap: float) -> float:
    """Convert a normalized feature gap into a bounded similarity score."""
    return max(0.0, max_points * (1 - gap))


def confidence_from_score(score: float, mode: str = "balanced") -> float:
    """Convert a raw recommendation score into a 0-1 confidence estimate."""
    weights = _resolve_mode_weights(mode)
    max_possible_score = sum(weights.values())
    if max_possible_score <= 0:
        logger.warning("Cannot calculate confidence because max possible score is non-positive.")
        return 0.0
    return max(0.0, min(1.0, score / max_possible_score))

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from CSV and convert numeric fields for scoring."""
    songs: List[Dict] = []
    int_fields = {"id", "popularity"}
    float_fields = {
        "energy",
        "tempo_bpm",
        "valence",
        "danceability",
        "acousticness",
        "vocal_intensity",
        "lyrical_depth",
        "replay_value",
    }

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            parsed_row: Dict[str, object] = {}
            for key, value in row.items():
                if key in int_fields:
                    parsed_row[key] = int(value)
                elif key in float_fields:
                    parsed_row[key] = float(value)
                else:
                    parsed_row[key] = value
            songs.append(parsed_row)

    logger.info("Loaded %s songs from %s.", len(songs), csv_path)
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict, mode: str = "balanced") -> Tuple[float, List[str]]:
    """Score one song and explain the strongest matching features."""
    score = 0.0
    reasons: List[str] = []
    weights = _resolve_mode_weights(mode)

    if song.get("genre") == user_prefs.get("genre"):
        points = weights["genre_match"]
        score += points
        reasons.append(f"genre match (+{points:.1f})")

    if song.get("mood") == user_prefs.get("mood"):
        points = weights["mood_match"]
        score += points
        reasons.append(f"mood match (+{points:.1f})")

    if song.get("release_decade") == user_prefs.get("preferred_decade"):
        points = weights["release_decade_match"]
        score += points
        reasons.append(f"release decade match (+{points:.1f})")

    if song.get("detailed_mood_tag") == user_prefs.get("detailed_mood_tag"):
        points = weights["detailed_mood_tag_match"]
        score += points
        reasons.append(f"detailed mood tag match (+{points:.1f})")

    target_energy = user_prefs.get("energy")
    if target_energy is not None and song.get("energy") is not None:
        energy_points = _closeness_points(
            weights["energy_similarity"],
            abs(song["energy"] - target_energy),
        )
        score += energy_points
        reasons.append(f"energy similarity (+{energy_points:.2f})")

    target_acousticness = user_prefs.get("acousticness")
    if target_acousticness is not None and song.get("acousticness") is not None:
        acoustic_points = _closeness_points(
            weights["acousticness_similarity"],
            abs(song["acousticness"] - target_acousticness),
        )
        score += acoustic_points
        reasons.append(f"acousticness similarity (+{acoustic_points:.2f})")

    target_tempo = user_prefs.get("tempo_bpm")
    if target_tempo is not None and song.get("tempo_bpm") is not None:
        tempo_points = _closeness_points(
            weights["tempo_similarity"],
            min(abs(song["tempo_bpm"] - target_tempo), 100) / 100,
        )
        score += tempo_points
        reasons.append(f"tempo similarity (+{tempo_points:.2f})")

    target_popularity = user_prefs.get("target_popularity")
    if target_popularity is not None and song.get("popularity") is not None:
        popularity_points = _closeness_points(
            weights["popularity_similarity"],
            min(abs(song["popularity"] - target_popularity), 100) / 100,
        )
        score += popularity_points
        reasons.append(f"popularity similarity (+{popularity_points:.2f})")

    target_vocal_intensity = user_prefs.get("vocal_intensity")
    if target_vocal_intensity is not None and song.get("vocal_intensity") is not None:
        vocal_points = _closeness_points(
            weights["vocal_intensity_similarity"],
            abs(song["vocal_intensity"] - target_vocal_intensity),
        )
        score += vocal_points
        reasons.append(f"vocal intensity similarity (+{vocal_points:.2f})")

    target_lyrical_depth = user_prefs.get("lyrical_depth")
    if target_lyrical_depth is not None and song.get("lyrical_depth") is not None:
        lyrical_points = _closeness_points(
            weights["lyrical_depth_similarity"],
            abs(song["lyrical_depth"] - target_lyrical_depth),
        )
        score += lyrical_points
        reasons.append(f"lyrical depth similarity (+{lyrical_points:.2f})")

    target_replay_value = user_prefs.get("replay_value")
    if target_replay_value is not None and song.get("replay_value") is not None:
        replay_points = _closeness_points(
            weights["replay_value_similarity"],
            abs(song["replay_value"] - target_replay_value),
        )
        score += replay_points
        reasons.append(f"replay value similarity (+{replay_points:.2f})")

    return score, reasons


def _apply_diversity_penalty(song: Dict, selected_songs: List[Dict]) -> Tuple[float, List[str]]:
    """Penalize repeated artists and genres in the emerging top-k list."""
    penalty = 0.0
    reasons: List[str] = []

    if any(selected["artist"] == song["artist"] for selected in selected_songs):
        penalty += 1.0
        reasons.append("artist diversity penalty (-1.00)")

    same_genre_count = sum(1 for selected in selected_songs if selected["genre"] == song["genre"])
    if same_genre_count >= 1:
        genre_penalty = 0.35 * same_genre_count
        penalty += genre_penalty
        reasons.append(f"genre diversity penalty (-{genre_penalty:.2f})")

    return penalty, reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = "balanced",
    apply_diversity: bool = True,
) -> List[Tuple[Dict, float, float, str]]:
    """Rank songs by score, optionally apply diversity penalties, and return top-k."""
    scored_results: List[Tuple[Dict, float, str]] = []

    if not songs:
        logger.warning("No songs were provided to recommend_songs.")
        return []

    logger.info("Scoring %s songs with mode '%s'.", len(songs), mode)

    for song in songs:
        score, reasons = score_song(user_prefs, song, mode=mode)
        scored_results.append((song, score, reasons))

    ranked_results = sorted(scored_results, key=lambda item: item[1], reverse=True)

    if not apply_diversity:
        return [
            (
                song,
                score,
                confidence_from_score(score, mode),
                ", ".join(reasons) if reasons else "General similarity match.",
            )
            for song, score, reasons in ranked_results[:k]
        ]

    selected_results: List[Tuple[Dict, float, float, str]] = []
    selected_songs: List[Dict] = []
    remaining_results = ranked_results[:]

    while remaining_results and len(selected_results) < k:
        best_index = 0
        best_adjusted_score: Optional[float] = None
        best_penalty_reasons: List[str] = []

        for index, (song, base_score, reasons) in enumerate(remaining_results):
            penalty, penalty_reasons = _apply_diversity_penalty(song, selected_songs)
            adjusted_score = base_score - penalty
            if best_adjusted_score is None or adjusted_score > best_adjusted_score:
                best_index = index
                best_adjusted_score = adjusted_score
                best_penalty_reasons = penalty_reasons

        song, base_score, reasons = remaining_results.pop(best_index)
        penalty, _ = _apply_diversity_penalty(song, selected_songs)
        final_score = base_score - penalty
        confidence = confidence_from_score(final_score, mode)
        explanation_parts = reasons + best_penalty_reasons
        explanation = ", ".join(explanation_parts) if explanation_parts else "General similarity match."
        selected_results.append((song, final_score, confidence, explanation))
        selected_songs.append(song)

    return selected_results
