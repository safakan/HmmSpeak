import os
import logging
from dotenv import load_dotenv
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def transcribe_audio(audio_file_path: str, model: str = "whisper-1") -> str:
    """
    Transcribe the given audio file using OpenAI Whisper API.
    Args:
        audio_file_path: Path to the audio file.
        model: OpenAI model to use for transcription. Options:
            - whisper-1 (default)
            - gpt-4o-mini-transcribe
            - gpt-4o-transcribe
    Returns:
        Transcribed text.
    Raises:
        FileNotFoundError: If the audio file doesn't exist
        ValueError: If the model is not supported
    """
    # Validate audio file exists
    if not os.path.exists(audio_file_path):
        logger.error(f"Audio file not found: {audio_file_path}")
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

    # Validate model
    supported_models = ["whisper-1", "gpt-4o-mini-transcribe", "gpt-4o-transcribe"]
    if model not in supported_models:
        logger.error(f"Unsupported model: {model}. Supported models are: {supported_models}")
        raise ValueError(f"Unsupported model: {model}. Supported models are: {supported_models}")

    logger.info(f"Starting transcription of {audio_file_path} using model: {model}")
    
    # Load environment variables from .env file
    load_dotenv()
    client = OpenAI()
    logger.debug("OpenAI client initialized")

    try:
        with open(audio_file_path, "rb") as audio_file:
            logger.debug("Audio file opened successfully")
            transcription = client.audio.transcriptions.create(
                model=model, 
                file=audio_file
            )
            logger.info("Transcription completed successfully")
            return transcription.text
    except Exception as e:
        logger.error(f"Error during transcription: {str(e)}", exc_info=True)
        raise
