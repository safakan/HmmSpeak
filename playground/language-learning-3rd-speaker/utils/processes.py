import os
import time
import logging
import multiprocessing as mp
from queue import Empty
from datetime import datetime
from utils.record_continuously_with_vad_and_min_max import record_continuously_with_vad_and_min_max
from utils.transcribe_an_audio import transcribe_audio

logger = logging.getLogger(__name__)

class ConversationManager:
    def __init__(self, manager=None):
        # Use a shared list from manager if provided, otherwise create a new one
        self.conversation_doc = manager.list() if manager else []
        self.lock = mp.Lock()

    def add_transcription(self, transcription: str):
        try:
            with self.lock:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.conversation_doc.append({
                    "timestamp": timestamp,
                    "text": transcription
                })
                logger.info(f"Added transcription to conversation doc: {transcription[:50]}...")
                self.log_conversation_state()
        except Exception as e:
            logger.error(f"Error adding transcription: {str(e)}", exc_info=True)

    def log_conversation_state(self):
        try:
            with self.lock:
                logger.info("Current conversation state:")
                for entry in self.conversation_doc:
                    logger.info(f"[{entry['timestamp']}] {entry['text']}")
        except Exception as e:
            logger.error(f"Error logging conversation state: {str(e)}", exc_info=True)

def recording_process(queue: mp.Queue, stop_event: mp.Event):
    """Process that continuously records audio and puts new recordings in the queue."""
    logger.info("Starting recording process")
    
    def on_chunk_saved(filename: str):
        logger.info(f"New recording saved: {filename}")
        logger.info("Recording process continuing to record...")
        queue.put(filename)
    
    try:
        logger.info("Recording process initialized and starting to record...")
        record_continuously_with_vad_and_min_max(
            output_dir="recordings",
            on_chunk_saved=on_chunk_saved
        )
    except Exception as e:
        logger.error(f"Error in recording process: {str(e)}", exc_info=True)
        stop_event.set()

def transcription_process(queue: mp.Queue, conversation_manager: ConversationManager, stop_event: mp.Event):
    """Process that monitors the queue for new recordings and transcribes them."""
    logger.info("Starting transcription process")
    
    while not stop_event.is_set():
        try:
            # Check for new recordings with a timeout
            filename = queue.get(timeout=1)
            logger.info(f"Processing new recording: {filename}")
            
            try:
                # Transcribe the audio file
                transcript = transcribe_audio(filename)
                logger.info(f"Transcription completed: {transcript[:50]}...")
                
                # Add to conversation document
                conversation_manager.add_transcription(transcript)
                
                # Print current conversation state after each transcription
                logger.info("\n=== Current Conversation State ===")
                conversation_manager.log_conversation_state()
                logger.info("=== End of Current State ===\n")
                
            except Exception as e:
                logger.error(f"Error transcribing {filename}: {str(e)}", exc_info=True)
                
        except Empty:
            # No new recordings, continue waiting
            continue
        except KeyboardInterrupt:
            logger.info("Transcription process received keyboard interrupt")
            stop_event.set()
            break
        except Exception as e:
            logger.error(f"Error in transcription process: {str(e)}", exc_info=True)
            stop_event.set()
            break 