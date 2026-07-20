import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

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
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dictionaries with correct types."""
    songs = []

    # newline="" is the recommended way to open files for the csv module.
    with open(csv_path, newline="", encoding="utf-8") as f:
        # DictReader uses the header row as the keys for each dictionary.
        reader = csv.DictReader(f)
        for row in reader:
            # Everything in a CSV is read as text, so we convert the number
            # columns to real numbers and leave the text columns as strings.
            song = {
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": int(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            }
            songs.append(song)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's preferences and list why it earned points."""
    score = 0.0
    reasons = []

    # Genre match: full points only when the labels are exactly the same.
    if song["genre"] == user_prefs["favorite_genre"]:
        score += 2.0
        reasons.append("Genre match (+2.0)")

    # Mood match: full points only when the labels are exactly the same.
    if song["mood"] == user_prefs["favorite_mood"]:
        score += 1.5
        reasons.append("Mood match (+1.5)")

    # Energy similarity: reward songs whose energy is CLOSE to the target,
    # not songs with the largest energy. Closest possible = 1.0.
    energy_score = 1 - abs(song["energy"] - user_prefs["target_energy"])
    score += energy_score
    reasons.append(f"Energy close (+{energy_score:.2f})")

    # Acoustic preference: reward acousticness if the user likes acoustic music,
    # otherwise reward the opposite (less acoustic).
    if user_prefs["likes_acoustic"]:
        acoustic_score = song["acousticness"]
    else:
        acoustic_score = 1 - song["acousticness"]
    score += acoustic_score
    reasons.append(f"Acoustic fit (+{acoustic_score:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Dict]:
    """Score every song, rank them highest-first, and return the top k as dicts."""
    scored = []

    # Give every song a score and remember why it earned it.
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append({"song": song, "score": score, "reasons": reasons})

    # We use sorted() instead of scored.sort() because sorted() returns a NEW
    # list and leaves the original list untouched. That keeps this function free
    # of side effects (it never secretly reorders the caller's data), which is
    # easier for a beginner to reason about. reverse=True puts the highest
    # score first.
    ranked = sorted(scored, key=lambda item: item["score"], reverse=True)

    return ranked[:k]

# ----------------------------------------------------------------------------
# PHASE 4 EVALUATION EXPERIMENT ONLY.
# The two functions below are a copy of the scoring/ranking logic with DIFFERENT
# weights so we can compare rankings. They do NOT change the real recommender:
# the original score_song() / recommend_songs() above are left exactly as-is.
# Experimental weights: genre 1.0 (down), mood 1.5 (same), energy 2.0 (up),
# acoustic 1.0 (same).
# ----------------------------------------------------------------------------

def score_song_experiment(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Experimental score: lower genre weight (1.0) and double energy weight (2.0)."""
    score = 0.0
    reasons = []

    # Genre match now worth only +1.0 (down from +2.0).
    if song["genre"] == user_prefs["favorite_genre"]:
        score += 1.0
        reasons.append("Genre match (+1.0)")

    # Mood match unchanged at +1.5.
    if song["mood"] == user_prefs["favorite_mood"]:
        score += 1.5
        reasons.append("Mood match (+1.5)")

    # Energy closeness is now doubled: energy_score stays in [0, 1], so the
    # contribution stays in a valid [0, 2] range.
    energy_score = 1 - abs(song["energy"] - user_prefs["target_energy"])
    score += 2.0 * energy_score
    reasons.append(f"Energy close (+{2.0 * energy_score:.2f})")

    # Acoustic fit unchanged at +1.0.
    if user_prefs["likes_acoustic"]:
        acoustic_score = song["acousticness"]
    else:
        acoustic_score = 1 - song["acousticness"]
    score += acoustic_score
    reasons.append(f"Acoustic fit (+{acoustic_score:.2f})")

    return score, reasons

def recommend_songs_experiment(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Dict]:
    """Same ranking as recommend_songs, but using the experimental weights."""
    scored = []
    for song in songs:
        score, reasons = score_song_experiment(user_prefs, song)
        scored.append({"song": song, "score": score, "reasons": reasons})

    ranked = sorted(scored, key=lambda item: item["score"], reverse=True)
    return ranked[:k]
