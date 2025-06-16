# Sidekick Chatbot

Towards a language learning assistant. It's a gradio app that uses together API and offers different ways of usign the app.

## Features

- Interactive chatbot interface
- Image generation based on conversation context
- Multiple operation modes for different use cases

## Prerequisites

- Python 3.x
- Together API key
- Required Python packages (install via pip):
  - gradio
  - together
  - Pillow
  - requests

## Usage

The app can be run in different modes using command-line arguments:

```bash
python main.py -o <option> -k <api_key>
```

### Available Options

1. **Text Generation Mode** (`-o 1`)
   - Generates poetic text based on a prompt
   - Example: `python main.py -o 1 -k YOUR_API_KEY`

2. **Image Generation Mode** (`-o 2`)
   - Creates an image based on a prompt
   - Saves the image to `results/image_option_2.png`
   - Example: `python main.py -o 2 -k YOUR_API_KEY`

3. **Combined Text and Image Mode** (`-o 3`)
   - Generates both text and an accompanying image
   - Saves the image to `results/image_option_3.png`
   - Example: `python main.py -o 3 -k YOUR_API_KEY`

4. **Interactive Chatbot Mode** (`-o 4`)
   - Launches a web interface for interactive language practice
   - Includes both text responses and generated images
   - Example: `python main.py -o 4 -k YOUR_API_KEY`

## Notes

- The app uses the Meta-Llama-3-8B-Instruct-Lite model for text generation
- Images are generated using the FLUX.1-schnell-Free model
- All generated images are saved in the `results` directory
- The chatbot interface is built using Gradio and provides a user-friendly web UI