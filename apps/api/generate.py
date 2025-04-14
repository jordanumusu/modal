import pandas as pd
import os
import json
import uuid
from math import ceil
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

# === CONFIG ===
CSV_PATH = "spotify_dataset.csv" 
NUM_CHUNKS = 100                 
TEMP_DIR = "vector_chunks_tmp"   #
VECTOR_STORE_NAME = "Modal Data" 

os.makedirs(TEMP_DIR, exist_ok=True)

# === Key Mapping (0–11) ===
KEY_MAP = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# === Fields to Keep ===
FIELDS = [
    "name", "album", "artists", "track_number", "explicit", "danceability", "energy",
    "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness",
    "liveness", "valence", "tempo", "duration_ms", "time_signature"
]

def format_song_sentence(row):
    try:
        key = KEY_MAP[int(row["key"])] if not pd.isna(row["key"]) else "Unknown"
        mode = "major" if row.get("mode", 1) == 1 else "minor"
        explicit = "explicit" if row.get("explicit", False) else "clean"
        duration_min = round(row["duration_ms"] / 60000, 2) if pd.notna(row["duration_ms"]) else "unknown duration"
        mood = "upbeat" if row.get("valence", 0) > 0.6 else "melancholic" if row.get("valence", 0) < 0.4 else "neutral"

        return (
            f"'{row['name']}' by {row['artists']} is a {explicit}, {mood} track "
            f"from the album '{row['album']}'. It is track {int(row['track_number'])} in the key of {key} {mode}, "
            f"with a tempo of {row['tempo']} BPM, loudness of {row['loudness']} dB, and duration of {duration_min} minutes. "
            f"Musical features include danceability {row['danceability']}, energy {row['energy']}, acousticness {row['acousticness']}, "
            f"instrumentalness {row['instrumentalness']}, liveness {row['liveness']}, speechiness {row['speechiness']}, "
            f"and a time signature of {int(row['time_signature'])}."
        )
    except Exception:
        return f"Incomplete data for song: {row.get('name', 'Unknown')}"

# === Load CSV ===
df = pd.read_csv(CSV_PATH, usecols=lambda col: col in FIELDS)
chunk_size = ceil(len(df) / NUM_CHUNKS)

client = OpenAI()
client.vector_stores.files.upload_and_poll(
    vector_store_id=vector_store_id,
    file=open("chords_dynamic.json", "rb")
)

# === Chunk, Format, Upload ===
for i in range(NUM_CHUNKS):
    chunk_df = df.iloc[i * chunk_size : (i + 1) * chunk_size]
    records = []

    for _, row in chunk_df.iterrows():
        text = format_song_sentence(row)
        records.append({
            "id": str(uuid.uuid4()),
            "text": text
        })

    file_path = os.path.join(TEMP_DIR, f"spotify_chunk_{i+1}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    print(f"Uploading chunk {i+1}/{NUM_CHUNKS}...")
    client.vector_stores.files.upload_and_poll(
        vector_store_id=vector_store.id,
        file=open(file_path, "rb")
    )
    print(f"Uploaded chunk {i+1}")

print("All chunks uploaded successfully!")