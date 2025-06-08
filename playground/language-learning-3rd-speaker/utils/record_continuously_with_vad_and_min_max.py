import webrtcvad
import wave
import os
import pyaudio
import time
import logging
from datetime import datetime
from typing import Optional, Callable

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def record_continuously_with_vad_and_min_max(
    output_dir: str = "recordings",
    sample_rate: int = 16000,
    min_thresh: int = 5,
    max_thresh: int = 15,
    silence_thresh: int = 2,
    vad_aggressiveness: int = 1,
    frame_duration_ms: int = 30,
    channels: int = 1,
    format: int = pyaudio.paInt16,
    filename_pattern: str = "audio_chunk_{timestamp}.wav",
    timestamp_format: str = "%Y%m%d_%H%M%S",
    on_chunk_saved: Optional[Callable[[str], None]] = None,
    on_error: Optional[Callable[[Exception], None]] = None,
    on_start: Optional[Callable[[dict], None]] = None,
    on_stop: Optional[Callable[[], None]] = None
):
    """
    Continuously records audio using Voice Activity Detection (VAD) and saves chunks to separate files.
    Each chunk must be at least min_thresh seconds long and will stop after either:
    - silence_thresh seconds of silence (if recording is longer than min_thresh seconds)
    - max_thresh seconds of continuous recording (regardless of silence)
    
    Args:
        output_dir (str): Directory where audio chunks will be saved. Defaults to "recordings".
        sample_rate (int): Audio sample rate in Hz. Defaults to 16000.
        min_thresh (int): Minimum duration of recording in seconds. Defaults to 5.
        max_thresh (int): Maximum duration of recording in seconds. Defaults to 15.
        silence_thresh (int): Duration of silence in seconds to stop recording. Defaults to 2.
        vad_aggressiveness (int): VAD aggressiveness (0-3). Defaults to 1.
        frame_duration_ms (int): Frame duration in milliseconds. Defaults to 30.
        channels (int): Number of audio channels. Defaults to 1.
        format (int): Audio format. Defaults to pyaudio.paInt16.
        filename_pattern (str): Pattern for filename with {timestamp} placeholder. Defaults to "audio_chunk_{timestamp}.wav".
        timestamp_format (str): Format string for timestamp. Defaults to "%Y%m%d_%H%M%S".
        on_chunk_saved (Callable[[str], None]): Optional callback when a chunk is saved. Receives filename.
        on_error (Callable[[Exception], None]): Optional callback for errors. Receives exception.
        on_start (Callable[[dict], None]): Optional callback when recording starts. Receives parameters dict.
        on_stop (Callable[[], None]): Optional callback when recording stops.
    
    Returns:
        None: This function runs indefinitely until interrupted.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    logger.info(f"Output directory created/verified: {output_dir}")
    
    # Initialize VAD with specified aggressiveness
    vad = webrtcvad.Vad(vad_aggressiveness)
    logger.info(f"VAD initialized with aggressiveness level: {vad_aggressiveness}")
    
    # Initialize PyAudio
    p = pyaudio.PyAudio()
    logger.info("PyAudio initialized")
    
    # Calculate frame size for specified duration
    frame_size = int(sample_rate * frame_duration_ms / 1000)  # samples per frame
    logger.debug(f"Frame size calculated: {frame_size} samples")
    
    # Open audio stream with specified parameters
    stream = p.open(
        format=format,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=frame_size
    )
    logger.info("Audio stream opened successfully")
    
    # Calculate thresholds in frames
    silence_threshold = int(silence_thresh * 1000 / frame_duration_ms)  # convert seconds to frames
    min_frames = int(min_thresh * sample_rate / frame_size)
    max_frames = int(max_thresh * sample_rate / frame_size)
    logger.debug(f"Thresholds calculated - Silence: {silence_threshold} frames, Min: {min_frames} frames, Max: {max_frames} frames")
    
    # Prepare parameters dict for callbacks
    params = {
        "output_dir": output_dir,
        "sample_rate": sample_rate,
        "min_thresh": min_thresh,
        "max_thresh": max_thresh,
        "silence_thresh": silence_thresh,
        "vad_aggressiveness": vad_aggressiveness,
        "frame_duration_ms": frame_duration_ms,
        "channels": channels,
        "format": format,
        "filename_pattern": filename_pattern,
        "timestamp_format": timestamp_format
    }
    
    # Call on_start callback if provided
    if on_start:
        on_start(params)
    else:
        logger.info("Recording started with parameters:")
        for key, value in params.items():
            logger.info(f"- {key}: {value}")
        logger.info("Press Ctrl+C to stop")
    
    try:
        while True:  # Main recording loop
            frames = []  # Store frames for current chunk
            silence_counter = 0
            is_recording = False
            logger.debug("Starting new recording chunk")
            
            # Record until silence threshold is reached or max duration reached
            while True:
                data = stream.read(frame_size)
                is_speech = vad.is_speech(data, sample_rate)
                
                if is_speech:
                    if not is_recording:
                        logger.debug("Speech detected, starting recording")
                    silence_counter = 0
                    is_recording = True
                    frames.append(data)
                elif is_recording:  # Only count silence if we've started recording
                    silence_counter += 1
                    frames.append(data)
                    
                    # Stop if we have minimum duration and silence threshold reached
                    if silence_counter >= silence_threshold and len(frames) >= min_frames:
                        logger.debug(f"Silence threshold reached after {len(frames)} frames")
                        break
                
                # Stop if we've reached maximum duration
                if len(frames) >= max_frames:
                    logger.debug(f"Maximum duration reached: {len(frames)} frames")
                    break
            
            # Generate filename using pattern
            timestamp = datetime.now().strftime(timestamp_format)
            filename = os.path.join(output_dir, filename_pattern.format(timestamp=timestamp))
            
            # Save the audio chunk
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(channels)
                wf.setsampwidth(p.get_sample_size(format))
                wf.setframerate(sample_rate)
                wf.writeframes(b''.join(frames))
            
            logger.info(f"Audio chunk saved: {filename} ({len(frames)} frames)")
            
            # Call on_chunk_saved callback if provided
            if on_chunk_saved:
                on_chunk_saved(filename)
    
    except KeyboardInterrupt:
        logger.info("Recording stopped by user")
        if on_stop:
            on_stop()
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)
        if on_error:
            on_error(e)
        raise
    finally:
        # Clean up resources
        logger.info("Cleaning up resources")
        stream.stop_stream()
        stream.close()
        p.terminate()
        logger.info("Resources cleaned up successfully")
