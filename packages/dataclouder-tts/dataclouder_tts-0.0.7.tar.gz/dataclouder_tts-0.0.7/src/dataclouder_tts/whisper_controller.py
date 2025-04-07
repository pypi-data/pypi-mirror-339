
from typing import Annotated

from dataclouder_core.exception import handler_exception
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.security import OAuth2PasswordBearer

from dataclouder_tts.whisper.whisper_groq import GroqWhisperClient

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/api/whisper", tags=["whisper"])

# Define dependency for GroqWhisperClient
def get_whisper_client() -> GroqWhisperClient:
    return GroqWhisperClient()

# Create a reusable annotated dependency
WhisperClientDep = Annotated[GroqWhisperClient, Depends(get_whisper_client)]


@router.get("/transcribe_uri", tags=["whisper"])
@handler_exception
async def transcribe_whisper(whisper_client: WhisperClientDep) -> dict[str, dict]:

    with open("./example_hi_whats_up_want_to.mp3", "rb") as f:
        audio = f.read()

    result = whisper_client.transcribe_bytes(audio, timestamp_granularities=["word"])
    return result



@router.post("/transcribe_bytes", tags=["whisper"])
@handler_exception
async def process_audio(
    file: Annotated[UploadFile, File()],
    whisper_client: WhisperClientDep
) -> dict:  # noqa: B008
    print('printing audio')
    contents = await file.read()
    print('audio read', contents)
    result = whisper_client.transcribe_bytes(contents, timestamp_granularities=["word"])
    return result
