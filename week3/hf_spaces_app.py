## SAME AS minimal_gradio.py
## EXCEPT LAUNCH SETTINGS
#demo.launch(
#        server_name="0.0.0.0",
#        server_port=7860,  
#        share=False,      
#        inbrowser=False         
#    )


import gradio as gr
import json
import os
from datetime import datetime



def load_data():
    try:
        with open('./data/results/conversation_result_for_ui.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {
            "ai_response_sentence": "File not found. Please check the file path.",
            "nouns": ["file", "path", "directory", "system", "error", "location", "name"],
            "adjectives": ["missing", "incorrect", "invalid", "empty", "nonexistent", "broken", "absolute"],
            "verbs": ["check", "locate", "open", "search", "fix", "verify", "rename"]
        }

def check_and_update_data():
    """Load data and return top 5 items from each list"""
    data = load_data()
    
    # Get top 5 items from each list, pad with empty strings if needed
    nouns = (data["nouns"][:5] + [''] * 5)[:5]
    adjectives = (data["adjectives"][:5] + [''] * 5)[:5]
    verbs = (data["verbs"][:5] + [''] * 5)[:5]
    
    return [data["ai_response_sentence"]] + nouns + adjectives + verbs

def toggle_recording(is_recording):
    if is_recording:
        return "Start Recording", False
    else:
        return "Stop Recording", True


with gr.Blocks() as demo:
    # Store recording state
    recording_state = gr.State(False)
    
    with gr.Row():
        record_button = gr.Button("Start Recording", variant="secondary")
    
    with gr.Row():
        ai_response_box = gr.Textbox(
            label="AI Response", 
            interactive=False
        )
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Nouns")
            noun_boxes = []
            for i in range(5):
                noun_boxes.append(gr.Textbox(interactive=False, show_label=False))
        
        with gr.Column():
            gr.Markdown("### Adjectives")
            adj_boxes = []
            for i in range(5):
                adj_boxes.append(gr.Textbox(interactive=False, show_label=False))
        
        with gr.Column():
            gr.Markdown("### Verbs")
            verb_boxes = []
            for i in range(5):
                verb_boxes.append(gr.Textbox(interactive=False, show_label=False))
    
    # Auto-update data every 2 seconds
    auto_refresh = gr.Timer(2)
    auto_refresh.tick(
        fn=check_and_update_data,
        outputs=[ai_response_box] + noun_boxes + adj_boxes + verb_boxes
    )
    
    record_button.click(
        fn=toggle_recording,
        inputs=[recording_state],
        outputs=[record_button, recording_state]
    )



# Force English language
os.environ['GRADIO_LANG'] = 'en'



# Launch with English interface
if __name__ == "__main__":
    demo.launch(
        inbrowser=True,
        server_name="127.0.0.1",
        share=False
    )