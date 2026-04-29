"""Run the CLI-first music recommender simulation."""

import logging

from src.recommender import load_songs, recommend_songs

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")


def _format_table(rows: list[list[str]], headers: list[str]) -> str:
    """Render a simple ASCII table without external dependencies."""
    widths = [len(header) for header in headers]
    for row in rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))

    def format_row(row: list[str]) -> str:
        return "| " + " | ".join(cell.ljust(widths[index]) for index, cell in enumerate(row)) + " |"

    separator = "+-" + "-+-".join("-" * width for width in widths) + "-+"
    table_lines = [separator, format_row(headers), separator]
    for row in rows:
        table_lines.append(format_row(row))
    table_lines.append(separator)
    return "\n".join(table_lines)


def print_profile_results(profile_name: str, user_prefs: dict, songs: list[dict], mode: str) -> None:
    """Print the ranked recommendations for one user profile and scoring mode."""
    recommendations = recommend_songs(user_prefs, songs, k=5, mode=mode, apply_diversity=True)

    rows: list[list[str]] = []
    for index, rec in enumerate(recommendations, start=1):
        song, score, confidence, explanation = rec
        rows.append(
            [
                str(index),
                song["title"],
                song["artist"],
                song["genre"],
                song["mood"],
                f"{score:.2f}",
                f"{confidence:.2f}",
                explanation,
            ]
        )

    print(f"\n=== {profile_name} | Mode: {mode} ===")
    print(f"Preferences: {user_prefs}\n")
    print(
        _format_table(
            rows,
            ["#", "Title", "Artist", "Genre", "Mood", "Score", "Confidence", "Reasons"],
        )
    )


def main() -> None:
    songs = load_songs("data/songs.csv")
    selected_mode = "genre_first"

    evaluation_profiles = {
        "High-Energy Pop": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "acousticness": 0.25,
            "tempo_bpm": 120,
            "target_popularity": 85,
            "preferred_decade": "2010s",
            "detailed_mood_tag": "uplifting",
            "vocal_intensity": 0.70,
            "lyrical_depth": 0.45,
            "replay_value": 0.88,
        },
        "Chill Lofi": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.38,
            "acousticness": 0.80,
            "tempo_bpm": 78,
            "target_popularity": 68,
            "preferred_decade": "2020s",
            "detailed_mood_tag": "study",
            "vocal_intensity": 0.18,
            "lyrical_depth": 0.58,
            "replay_value": 0.82,
        },
        "Deep Intense Rock": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.92,
            "acousticness": 0.10,
            "tempo_bpm": 150,
            "target_popularity": 78,
            "preferred_decade": "2000s",
            "detailed_mood_tag": "adrenaline",
            "vocal_intensity": 0.88,
            "lyrical_depth": 0.50,
            "replay_value": 0.75,
        },
        "Edge Case: Sad but High Energy": {
            "genre": "pop",
            "mood": "sad",
            "energy": 0.90,
            "acousticness": 0.20,
            "tempo_bpm": 130,
            "target_popularity": 80,
            "preferred_decade": "2020s",
            "detailed_mood_tag": "somber",
            "vocal_intensity": 0.65,
            "lyrical_depth": 0.70,
            "replay_value": 0.82,
        },
    }

    for profile_name, user_prefs in evaluation_profiles.items():
        print_profile_results(profile_name, user_prefs, songs, mode=selected_mode)


if __name__ == "__main__":
    main()
