from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scraper import search_duckduckgo, fetch_chords_sectioned
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
app = FastAPI()
router = APIRouter()
client = OpenAI()


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Define request/response models
class Message(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str

class GenerateAnswerRequest(BaseModel):
    conversation_id: str = None
    query: str

class SongRequest(BaseModel):
    song_name: str
    artist_name: str
    
@router.post("/generate-answer")
async def generate_answer(request: GenerateAnswerRequest):
    previous_conversation_id = request.conversation_id

    try:
        response = client.responses.create(
            model="gpt-4o", 
            previous_response_id=previous_conversation_id if previous_conversation_id else None,
            input=[{"role": "user", "content": request.query}],
        )
        
        result = {
            "resp_id": response.id,
            "output": response.output_text,
            "status": response.status,
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")

@router.post("/fetch-and-store-chords")
async def fetch_and_store_chords(request: SongRequest):
    # Step 1: Search for the song on DuckDuckGo and fetch the Ultimate Guitar URL
    query = f"{request.song_name} {request.artist_name} site:ultimate-guitar.com"
    url = search_duckduckgo(query)
    
    if not url:
        return {"error": "Song not found on Ultimate Guitar."}
    
    # Step 2: Fetch the chord progressions from the URL
    chords_by_section = fetch_chords_sectioned(url)
    
    if not chords_by_section:
        return {"error": "No chords found on the page."}

    # Step 3: Store the chords in ChromaDB
    collection = get_or_create_collection(f"{request.song_name}-{request.artist_name}")
    documents = [{"id": f"{section}-{request.song_name}", "text": " ".join(chords), "metadata": {"section": section}} for section, chords in chords_by_section.items()]
    collection.add(documents=documents)

    return {"message": f"Chords for '{request.song_name}' by {request.artist_name} uploaded to vector database."}

app.include_router(router, prefix="/api")
