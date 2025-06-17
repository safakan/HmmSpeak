from flask import Blueprint, render_template, request, jsonify
import os
import sys
import logging
import json
from json import JSONDecodeError

from app.utils.transcribe_an_audio import transcribe_audio
from app.utils.llm_call import prompt_llm, PROMPT_TEMPLATE_get_conversation_helper_json

main = Blueprint('main', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/process-audio', methods=['POST'])
def process_audio():

    ### GET THE AUDIO
    logger.info('Received request at /process-audio')
    if 'audio' not in request.files:
        logger.error('No audio file provided in request')
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    logger.info(f"Audio file received: filename={audio_file.filename}, content_type={audio_file.content_type}, content_length={request.content_length}")


    try:
        # Ensure the stream is at the beginning before reading its content
        audio_file.stream.seek(0)
        
        ### TRANSCRIBE
        logger.info('Calling transcribe_audio...')
        transcription = transcribe_audio(audio_file)
        logger.info(f'Transcription result: {transcription}')

        ### FORMAT AS INPUT TO LLM
        prompt = PROMPT_TEMPLATE_get_conversation_helper_json.format(
            conversation_doc=transcription
        )

        ### REQUEST RESPONSE FROM LLM
        llm_response = prompt_llm(prompt)
        response_data = json.loads(llm_response)
        
        ##### BELOW PART I NEED TO UNDERSTAND BETTER IN HOW INTERACTS...
        # Add transcription to response
        response_data['transcription'] = transcription

        logger.info(f'Response to frontend: {response_data}')
        return jsonify(response_data)
    except Exception as e:
        logger.error(f'Error during processing: {e}', exc_info=True)
        return jsonify({'error': str(e)}), 500 

@main.route('/llm-call', methods=['POST'])
def llm_call():
    logger.info('Received request at /llm-call')
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            logger.error('No prompt provided in request')
            return jsonify({'error': 'No prompt provided'}), 400

        prompt = data['prompt']
        logger.info(f'Calling LLM with prompt...')
        
        llm_response = prompt_llm(prompt)
        try:
            response_data = json.loads(llm_response)
        except JSONDecodeError as jde:
            logger.error(f'JSON decoding error: {jde}')
            logger.error(f'Malformed LLM response: {llm_response}')
            return jsonify({
                'error': 'Failed to parse LLM response as JSON',
                'details': str(jde),
                'raw_llm_response': llm_response
            }), 500
        
        logger.info(f'LLM response: {response_data}')
        return jsonify(response_data)
    except Exception as e:
        logger.error(f'Error during LLM processing: {e}', exc_info=True)
        return jsonify({'error': str(e)}), 500 