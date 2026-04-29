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

I tested the model with four profiles: `High-Energy Pop`, `Chill Lofi`, `Deep Intense Rock`, and `Edge Case: Sad but High Energy`. I compared the top results to my own musical intuition and checked whether the printed reasons matched the scoring logic.

I also used automated tests as a reliability check. The latest test run passed `5 out of 5` tests. The tests check that recommendations are sorted correctly, explanations are produced, confidence scores stay between `0` and `1`, recommendation output includes confidence and explanations, and diversity penalties reduce repeated artists.

The strongest top recommendations had confidence scores between `0.78` and `1.00`. The weakest behavior appeared in the `sad but high energy` profile because the small song catalog does not contain many songs with that exact combination.

## Intended Use and Non-Intended Use

This system is intended for classroom exploration and learning about recommendation logic. It is good for showing how a simple content-based recommender can rank songs from a small dataset. It should not be used for real users, high-stakes decisions, or claims about someone's true music taste.

## Ideas for Improvement

- Add many more songs and more varied mood combinations.
- Improve the diversity rule so the top results do not cluster around one genre or artist.
- Let users express dislikes or hard constraints, such as "not pop" or "low tempo only."
- Add more validation rules for missing or unusual listener inputs.

## AI Collaboration Reflection

I used AI assistance to help improve the structure of the project, add a browser interface, write clearer documentation, and strengthen the reliability tests. AI collaboration was useful for quickly suggesting implementation patterns, but I still had to review the code, run the system, check the outputs, and decide whether the recommendations made sense.

The main lesson was that AI can speed up problem-solving, but it does not remove the need for human judgment. I had to choose what counted as a good recommendation, notice when the dataset was too limited, and make sure the final project was understandable to another person.

## Personal Reflection

My biggest learning moment was seeing how much the dataset shapes the recommendations, even before the scoring math does. AI tools helped me move faster when drafting scoring logic and comparing profiles, but I still had to double-check the outputs because a suggestion can sound reasonable while still producing repetitive or misleading rankings. What surprised me most was that a simple point system can already feel like a real recommender when the output is explained clearly. If I kept going, I would try adding more user signals and a better way to balance similarity with diversity.
