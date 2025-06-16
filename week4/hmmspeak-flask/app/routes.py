from flask import Blueprint, render_template, request, jsonify
import os
import sys
import logging

from app.utils.transcribe_an_audio import transcribe_audio

main = Blueprint('main', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/process-audio', methods=['POST'])
def process_audio():
    logger.info('Received request at /process-audio')
    if 'audio' not in request.files:
        logger.error('No audio file provided in request')
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    logger.info(f"Audio file received: filename={audio_file.filename}, content_type={audio_file.content_type}, content_length={request.content_length}")

    try:
        # Ensure the stream is at the beginning before reading its content
        audio_file.stream.seek(0)
        logger.info('Calling transcribe_audio...')
        transcription = transcribe_audio(audio_file)
        logger.info(f'Transcription result: {transcription}')
        response_data = {
            'ai_response': 'This is a sample AI response.',
            'nouns': ['example', 'test'],
            'adjectives': ['sample', 'dummy'],
            'verbs': ['process', 'test'],
            'transcription': transcription
        }
        logger.info(f'Response to frontend: {response_data}')
        return jsonify(response_data)
    except Exception as e:
        logger.error(f'Error during processing: {e}', exc_info=True)
        return jsonify({'error': str(e)}), 500 