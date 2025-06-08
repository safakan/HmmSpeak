# suppress warnings
import warnings
warnings.filterwarnings("ignore")

import os

from llm_call import prompt_llm, PROMPT_TEMPLATE_basic_user_request, PROMPT_TEMPLATE_get_conversation_helper_json


if __name__ == "__main__":
    ## Example usage with only a regular user request
    # user_request = "write a 1 line post about coffee"
    # prompt = PROMPT_TEMPLATE_basic_user_request.format(user_request=user_request)
    # response = prompt_llm(prompt)

    # Example usage with a predefined conversation document
    # conversation document
    example_conversation_file_path = os.path.join(os.path.dirname(__file__), "data", "documents", "conversation_2024_03_21_1430.md")
    with open(example_conversation_file_path, 'r', encoding='utf-8') as file:
        conversation_doc = file.read().strip()
    prompt = PROMPT_TEMPLATE_get_conversation_helper_json.format(conversation_doc=conversation_doc)
    response = prompt_llm(prompt)


    print("\nResponse:\n")
    print(response)
    print("-" * 100)