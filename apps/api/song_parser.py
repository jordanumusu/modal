import json
import os
import uuid
import logging
import re
from openai import OpenAI
from scraper import search_duckduckgo, fetch_chords_sectioned
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

VECTOR_STORE_ID = "vs_67fc460cd6388191bf2ed8aab1ab223e"
CHORD_FILE_PATH = "chords_dynamic.json"
CHORD_FILE_ID_PATH = "chords_file_id.txt"  # to store latest uploaded file ID

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def extract_songs_and_artists(query: str) -> list[dict]:
    prompt = f"""
You are a music-aware parser. Extract all song titles and their most likely artist(s) from the query below.
If an artist is not explicitly mentioned, infer the most well-known or original performer.
Only return a valid JSON array like:
[{{"title": "...", "artist": "..."}}]

Query: "{query}"
"""
    try:
        response = client.responses.create(
            model="gpt-4o",
            input=[{"role": "user", "content": prompt}]
        )
        content = response.output_text.strip()
        cleaned = re.sub(r"^```(?:json)?|```$", "", content, flags=re.IGNORECASE).strip()
        return json.loads(cleaned)
    except Exception as e:
        logger.error(f"Parsing error: {e}")
        return []

def results_contain_chords(results) -> bool:
    for item in results.data:
        for block in item.content:
            if hasattr(block, "text") and "chord progression" in block.text.lower():
                return True
    return False

def read_current_file_id() -> str | None:
    if os.path.exists(CHORD_FILE_ID_PATH):
        with open(CHORD_FILE_ID_PATH, "r") as f:
            return f.read().strip()
    return None

def write_current_file_id(file_id: str):
    with open(CHORD_FILE_ID_PATH, "w") as f:
        f.write(file_id.strip())

def format_chords_block(title, artist, chords):
    sections = []
    for section, chords_list in chords.items():
        chord_line = " ".join(chords_list)
        sections.append(f"In the {section.lower()} section, the progression is: {chord_line}.")
    body = " ".join(sections)
    return f"'{title}' by {artist} features the following chord progression: {body}"

async def fetch_and_update_chord_file(parsed_songs: list[dict]) -> str | None:
    for entry in parsed_songs:
        title, artist = entry["title"], entry["artist"]
        logger.info(f"Scraping chords for: {title} by {artist}")
        query = f"{title} {artist} site:ultimate-guitar.com"
        url = search_duckduckgo(query)
        if not url:
            logger.warning(f"No UG URL found for: {title} by {artist}")
            continue

        chords = fetch_chords_sectioned(url)
        if not chords:
            logger.warning(f"No chords found for: {title} from {url}")
            continue

        block = format_chords_block(title, artist, chords)
        logger.info(f"Fetched chords for {title}, appending and uploading.")

        # Step 1: Load or create local chord file
        data = []
        if os.path.exists(CHORD_FILE_PATH):
            with open(CHORD_FILE_PATH, "r") as f:
                data = json.load(f)

        data.append({"id": str(uuid.uuid4()), "text": block})

        with open(CHORD_FILE_PATH, "w") as f:
            json.dump(data, f, indent=2)

        # Step 2: Delete previous vector file (if exists)
        old_file_id = read_current_file_id()
        if old_file_id:
            try:
                client.vector_stores.files.delete(
                    vector_store_id=VECTOR_STORE_ID,
                    file_id=old_file_id
                )
                logger.info(f"Deleted old chord file: {old_file_id}")
            except Exception as e:
                logger.warning(f"Failed to delete old file: {e}")

        # Step 3: Upload new file
        upload = client.vector_stores.files.upload_and_poll(
            vector_store_id=VECTOR_STORE_ID,
            file=open(CHORD_FILE_PATH, "rb")
        )
        new_file_id = upload.id
        write_current_file_id(new_file_id)
        logger.info(f"Uploaded new chord file: {new_file_id}")

        return block

    return None
