from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from song_parser import extract_songs_and_artists, results_contain_chords, fetch_and_update_chord_file
import logging
import os

# === Setup ===
load_dotenv()
app = FastAPI()
router = APIRouter()
client = OpenAI()

VECTOR_STORE_ID = "vs_67fc460cd6388191bf2ed8aab1ab223e"


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

origins = ["http://localhost:3000", "https://modal-gory77o7m-jordanumusus-projects.vercel.app"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Models ===
class Message(BaseModel):
    role: str
    content: str

class GenerateAnswerRequest(BaseModel):
    prev_response_id: str = None
    query: str

# === Formatter ===
def format_results(results):
    formatted_results = ''
    for result in results:
        formatted_result = f"<result file_id='{result.file_id}' file_name='{result.filename}'>"
        for part in result.content:
            formatted_result += f"<content>{part.text}</content>"
        formatted_results += formatted_result + "</result>"
    return f"<sources>{formatted_results}</sources>"

# === Main route ===
@router.post("/generate-answer")
async def generate_answer(request: GenerateAnswerRequest):
    try:
        user_query = request.query
        logger.info(f"Received query: {user_query}")

        # 1. Classify query
        classification = client.responses.create(
            model="gpt-4o",
            input=[{
                "role": "user",
                "content": f"Is the following query about music or songs? Reply with only 'yes' or 'no'.\n\n{user_query}"
            }]
        )
        if "no" in classification.output_text.lower():
            response = client.responses.create(
                model="gpt-4o",
                previous_response_id=request.prev_response_id,
                input=[{"role": "user", "content": user_query}]
            )
            return {"id": response.id, "output": response.output_text, "status": response.status}

        # 2. Search vector DB
        results = client.vector_stores.search(
            vector_store_id=VECTOR_STORE_ID,
            query=user_query,
            rewrite_query=True,
            max_num_results=10
        )
        formatted_results = format_results(results.data)
        has_chords = results_contain_chords(results)

        # 3. Scrape if needed
        if not has_chords:
            parsed = extract_songs_and_artists(user_query)
            if parsed:
                chord_snippet = await fetch_and_update_chord_file(
                    parsed,
                )
                if chord_snippet:
                    formatted_results += f"\n<result file_id='file_xyz'><content>{chord_snippet}</content></result>"

        prompt = """You are a helpful and insightful music assistant with access to song metadata, chord progressions, and musical context.
            Your role is to help the user explore ideas, not just answer. Think like a curious, knowledgeable musician talking to another.

            When responding:

            - **Often start with an overview**: briefly highlight what makes the song or progression potentially interesting, emotionally impactful, or worth analyzing.
            - **Frequently (but not always)** offer follow-up directions or questions before going too deep. This helps guide users who may not know what to ask next.
            - For example:
                - "Would you like to focus on the harmony, overall structure, or how to improvise over this?"
                - "Should we look at similar songs in this key, or explain why this works emotionally?"

            Analysis guidance:
            - Use your knowledge of music theory to go beyond the source material.
            - Discuss movement, cadence, substitutions, borrowed chords, modal shifts, and tension/resolution when relevant.
            - If the progression is simple or repetitive, explain why it’s effective.
            - Don’t just restate — **interpret**.
            - It’s okay to make thoughtful inferences or assumptions based on genre or pattern — don't be overly cautious.

            Formatting:
            - Use **Markdown** to structure your answers.
            - Headings, bullet points, and bold emphasis should be used for clarity and insight.
            """

        # 4. Respond with context
        response = client.responses.create(
            model="gpt-4o",
            previous_response_id=request.prev_response_id,
            input=[
                {
                "role": "developer",
                "content": prompt
                },
                {"role": "user", "content": f"Sources:\n{formatted_results}\n\nQuery: '{user_query}'"}
            ],
        )
        return {"id": response.id, "output": response.output_text, "status": response.status}
    except Exception as e:
        logger.exception("An error occurred while generating the answer.")
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")

app.include_router(router, prefix="/api")
