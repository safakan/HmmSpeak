# suppress warnings
import warnings
warnings.filterwarnings("ignore")

import os
import json
from datetime import datetime

from llm_call import prompt_llm, PROMPT_TEMPLATE_basic_user_request, PROMPT_TEMPLATE_get_conversation_helper_json


if __name__ == "__main__":
    # Example usage with a predefined conversation document
    ## user input will be users speaking between themselves and it will be parsed into a conversation doc
    example_conversation_file_path = os.path.join(os.path.dirname(__file__), "data", "documents", "conversation_doc_2025_06_08_1600.md")
    with open(example_conversation_file_path, 'r', encoding='utf-8') as file:
        conversation_doc = file.read().strip()

    
    # Prompting LLM with conversation doc to get result json
    prompt = PROMPT_TEMPLATE_get_conversation_helper_json.format(conversation_doc=conversation_doc)
    response = prompt_llm(prompt)
    

    # Parse the structured string response into JSON
    response_json = json.loads(response)


    # Create timestamp for filename
    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M")
    results_dir = os.path.join(os.path.dirname(__file__), "data", "results")
    output_file = os.path.join(results_dir, f"conversation_result_{timestamp}.json")

    # Write JSON to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(response_json, f, indent=4)

    print(f"Results written to: {output_file}")

