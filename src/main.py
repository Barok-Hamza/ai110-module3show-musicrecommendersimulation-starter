"""
Command line runner for the Music Recommender Simulation.

Phase 4 (Evaluate and Explain): runs the recommender for four different user
profiles, then re-runs the same profiles with an experimental set of weights so
the two rankings can be compared.
"""

# Support both ways of running the program:
#   python src/main.py       -> "from recommender import ..." works
#   python -m src.main       -> "from src.recommender import ..." works
try:
    from recommender import load_songs, recommend_songs, recommend_songs_experiment
except ModuleNotFoundError:
    from src.recommender import load_songs, recommend_songs, recommend_songs_experiment


# The four profiles we evaluate. The fourth is deliberately conflicting: it asks
# for the metal genre but also low energy and acoustic music, which no single
# song can satisfy at once.
PROFILES = [
    ("High-Energy Pop", {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.90,
        "likes_acoustic": False,
    }),
    ("Chill Lofi", {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "likes_acoustic": True,
    }),
    ("Deep Intense Rock", {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.85,
        "likes_acoustic": False,
    }),
    ("Adversarial / Conflicting", {
        "favorite_genre": "metal",
        "favorite_mood": "melancholic",
        "target_energy": 0.20,
        "likes_acoustic": True,
    }),
]


def print_recommendations(label, user_prefs, songs, recommend_fn, k=5):
    """Print the top k recommendations for one profile, with scores and reasons."""
    print("=====================================")
    print(f"PROFILE: {label}")
    print(
        f"  genre={user_prefs['favorite_genre']}, "
        f"mood={user_prefs['favorite_mood']}, "
        f"target_energy={user_prefs['target_energy']}, "
        f"likes_acoustic={user_prefs['likes_acoustic']}"
    )
    print("=====================================")

    recommendations = recommend_fn(user_prefs, songs, k=k)
    for rank, rec in enumerate(recommendations, start=1):
        song = rec["song"]
        print(f"{rank}. {song['title']}")
        print(f"   Artist: {song['artist']}")
        print(f"   Score: {rec['score']:.2f}")
        print("   Reasons:")
        for reason in rec["reasons"]:
            print(f"     - {reason}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    print("\n########################################################")
    print("# ORIGINAL WEIGHTS: genre 2.0, mood 1.5, energy 1.0, acoustic 1.0")
    print("########################################################\n")
    for label, prefs in PROFILES:
        print_recommendations(label, prefs, songs, recommend_songs)

    print("\n########################################################")
    print("# EXPERIMENT WEIGHTS: genre 1.0, mood 1.5, energy 2.0, acoustic 1.0")
    print("# (evaluation only - the real recommender is unchanged)")
    print("########################################################\n")
    for label, prefs in PROFILES:
        print_recommendations(label, prefs, songs, recommend_songs_experiment)


if __name__ == "__main__":
    main()
