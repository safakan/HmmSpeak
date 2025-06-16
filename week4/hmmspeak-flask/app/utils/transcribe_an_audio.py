import os
import logging
from dotenv import load_dotenv
from openai import OpenAI
import io

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def transcribe_audio(audio_file, model: str = "whisper-1") -> str:
    """
    Transcribe the given audio file using OpenAI Whisper API.
    Args:
        audio_file: File-like object (e.g., from Flask's request.files['audio'])
        model: OpenAI model to use for transcription. Options:
            - whisper-1 (default)
            - gpt-4o-mini-transcribe
            - gpt-4o-transcribe
    Returns:
        Transcribed text.
    Raises:
        ValueError: If the model is not supported
    """
    # Validate model
    supported_models = ["whisper-1", "gpt-4o-mini-transcribe", "gpt-4o-transcribe"]
    if model not in supported_models:
        logger.error(f"Unsupported model: {model}. Supported models are: {supported_models}")
        raise ValueError(f"Unsupported model: {model}. Supported models are: {supported_models}")

    logger.info(f"Starting transcription using model: {model}")
    
    # Load environment variables from .env file
    load_dotenv()
    client = OpenAI()
    logger.debug("OpenAI client initialized")

    try:
        # Read the entire stream into an in-memory BytesIO object
        audio_bytes = io.BytesIO(audio_file.read())
        # The seek(0) is now handled in routes.py for the original stream

        # Pass a tuple (filename, file-object, mimetype) for OpenAI compatibility
        file_tuple = (audio_file.filename, audio_bytes, audio_file.mimetype)
        transcription = client.audio.transcriptions.create(
            model=model, 
            file=file_tuple
        )
        logger.info("Transcription completed successfully")
        return transcription.text
    except Exception as e:
        logger.error(f"Error during transcription: {str(e)}", exc_info=True)
        raise
