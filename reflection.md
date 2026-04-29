# Reflection Comparisons

`High-Energy Pop` vs `Chill Lofi`: The pop profile pushed bright, upbeat songs like `Sunrise City` and `Gym Hero` to the top, while the lofi profile strongly preferred softer, more acoustic tracks like `Library Rain` and `Midnight Coding`. That makes sense because the energy, mood, and acousticness targets are very different.

`High-Energy Pop` vs `Deep Intense Rock`: Both profiles liked high-energy songs, so there was some overlap in energetic tracks, but the rock profile moved `Storm Runner` to the top because it matched both the `rock` genre and `intense` mood. The pop profile instead rewarded happy songs with upbeat pacing.

`High-Energy Pop` vs `Edge Case: Sad but High Energy`: These outputs were surprisingly similar because the dataset does not really have sad high-energy pop songs. The system therefore leaned on shared genre and energy features, which is why `Gym Hero` and `Sunrise City` still rose to the top.

`Chill Lofi` vs `Deep Intense Rock`: These profiles produced almost opposite results. Chill lofi favored low-energy, acoustic, relaxed songs, while deep intense rock rewarded louder, faster, less acoustic tracks.

`Chill Lofi` vs `Edge Case: Sad but High Energy`: The lofi profile produced calm, focused songs, but the edge case produced energetic tracks even when the mood was wrong. This comparison shows that the current scoring logic trusts energy very strongly when it cannot find a true mood match.

`Deep Intense Rock` vs `Edge Case: Sad but High Energy`: Both profiles surfaced high-energy songs, but the rock profile had a much clearer top recommendation because `Storm Runner` matched its exact genre and mood. The edge case had weaker semantic matches, so its ranking looked more like a fallback to raw intensity.
