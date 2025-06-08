import logging
import multiprocessing as mp
import time
from utils.processes import ConversationManager, recording_process, transcription_process

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def main():
    # Create a manager for shared state
    with mp.Manager() as manager:
        # Create a queue for communication between processes
        queue = mp.Queue()
        
        # Create an event for stopping processes
        stop_event = mp.Event()
        
        # Create conversation manager with shared state
        conversation_manager = ConversationManager(manager)
        
        # Create and start processes
        recording_proc = mp.Process(
            target=recording_process,
            args=(queue, stop_event)
        )
        
        transcription_proc = mp.Process(
            target=transcription_process,
            args=(queue, conversation_manager, stop_event)
        )
        
        try:
            logger.info("Starting processes...")
            recording_proc.start()
            transcription_proc.start()
            
            # Keep the main process running
            while True:
                if stop_event.is_set():
                    logger.info("Stop event detected, shutting down...")
                    break
                time.sleep(0.1)  # Small sleep to prevent busy waiting
                    
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received, shutting down...")
            stop_event.set()
            
        finally:
            # Wait for processes to finish
            logger.info("Waiting for processes to finish...")
            recording_proc.join(timeout=5)
            transcription_proc.join(timeout=5)
            
            # Force terminate if still running
            if recording_proc.is_alive():
                logger.info("Recording process still running, terminating...")
                recording_proc.terminate()
            if transcription_proc.is_alive():
                logger.info("Transcription process still running, terminating...")
                transcription_proc.terminate()
            
            # Log final conversation state
            logger.info("\n" + "="*50)
            logger.info("FINAL CONVERSATION STATE")
            logger.info("="*50)
            conversation_manager.log_conversation_state()
            logger.info("="*50 + "\n")
                
            logger.info("All processes terminated")

if __name__ == "__main__":
    main()