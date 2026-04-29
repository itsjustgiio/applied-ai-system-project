# Model Card: Music Recommender Simulation

## Model Name

**VibeMatch CLI 1.0**

## Goal / Task

This model suggests songs that fit a user's preferred vibe. It tries to predict which songs from the small catalog are the best match for a user's genre, mood, energy, tempo, and acousticness preferences.

## Data Used

The system uses a CSV catalog with 18 songs. Each song includes `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`. The dataset is useful for a classroom demo, but it is very small and does not represent all music styles or mixed moods.

## Algorithm Summary

The model gives points for an exact genre match and an exact mood match. It then gives more points when a song's energy, acousticness, and tempo are close to the user's target values. After scoring every song, it sorts the list and returns the top matches.

## Observed Behavior / Biases

The system works best when the catalog already has songs close to the user's vibe. It can over-reward exact genre labels, so songs with similar feel but different tags may rank too low. The edge-case profile with `sad` mood and very high energy showed a weakness: the model returned energetic songs even when the mood did not really fit.

## Evaluation Process

I tested the model with four profiles: `High-Energy Pop`, `Chill Lofi`, `Deep Intense Rock`, and `Edge Case: Sad but High Energy`. I compared the top results to my own musical intuition and checked whether the printed reasons matched the scoring logic. I also ran one experiment where I doubled the energy weight and cut the genre weight in half to see how sensitive the rankings were.

## Intended Use and Non-Intended Use

This system is intended for classroom exploration and learning about recommendation logic. It is good for showing how a simple content-based recommender can rank songs from a small dataset. It should not be used for real users, high-stakes decisions, or claims about someone's true music taste.

## Ideas for Improvement

- Add many more songs and more varied mood combinations.
- Add a diversity rule so the top results do not cluster around one genre or artist.
- Let users express dislikes or hard constraints, such as "not pop" or "low tempo only."

## Personal Reflection

My biggest learning moment was seeing how much the dataset shapes the recommendations, even before the scoring math does. AI tools helped me move faster when drafting scoring logic and comparing profiles, but I still had to double-check the outputs because a suggestion can sound reasonable while still producing repetitive or misleading rankings. What surprised me most was that a simple point system can already feel like a real recommender when the output is explained clearly. If I kept going, I would try adding more user signals and a better way to balance similarity with diversity.
