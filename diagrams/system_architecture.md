# System Architecture Diagram

```mermaid
flowchart TD
    A[Human User / Evaluation Profile] --> B[Streamlit App or CLI]
    C[data/songs.csv] --> D[Song Catalog Loader]
    B --> D
    D --> E[Recommender Logic]
    A --> E
    E --> F[Scoring System]
    F --> G[Confidence Score]
    F --> H[Diversity Adjustment]
    H --> I[Ranked Song Recommendations]
    G --> I
    I --> J[Recommendation Table + Explanations]

    K[tests/test_recommender.py] --> E
    K --> L[Reliability Checks]
    L --> M[Test Results]

    J --> N[Human Review]
    M --> N
```

The system takes a listener profile and compares it against songs from `data/songs.csv`. The recommender scores each song, adds a confidence estimate, applies a diversity adjustment, and returns ranked recommendations with explanations. Automated tests and human review are used to check whether the AI output is reliable and reasonable.
