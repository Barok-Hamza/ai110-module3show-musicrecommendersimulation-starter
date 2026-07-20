"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

# Support both ways of running the program:
#   python src/main.py       -> "from recommender import ..." works
#   python -m src.main       -> "from src.recommender import ..." works
try:
    from recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Example user profile (the Phase 2 profile): a calm, acoustic study listener.
    user_prefs = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "likes_acoustic": True,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rank, rec in enumerate(recommendations, start=1):
        song = rec["song"]

        print("-------------------------------------")
        print(f"{rank}. {song['title']}")
        print(f"Artist: {song['artist']}")
        print(f"Score: {rec['score']:.2f}")
        print()
        print("Reasons:")
        for reason in rec["reasons"]:
            print(f"- {reason}")
        print()

    print("-------------------------------------")


if __name__ == "__main__":
    main()
