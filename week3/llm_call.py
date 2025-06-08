from dotenv import load_dotenv
import argparse
import os
import sys
from together import Together
import textwrap


from pydantic import BaseModel, Field
from typing import List
class ConversationHelper(BaseModel):
    ai_response_sentence: str
    nouns: List[str] = Field(min_items=5, max_items=5)
    adjectives: List[str] = Field(min_items=5, max_items=5)
    verbs: List[str] = Field(min_items=5, max_items=5)

def prompt_llm(prompt, with_linebreak=False):
    # Get API key from environment variable or command line argument
    # parsing command line argument if there are additional arguments
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser()
        parser.add_argument("-k", "--api_key", type=str, default=None)
        args = parser.parse_args()
    else:
        # Load environment variables from .env file
        load_dotenv()

    api_key = os.getenv("TOGETHER_API_KEY") or args.api_key

    if not api_key:
        raise ValueError("API key not found. Please set TOGETHER_API_KEY in .env file or provide it via -k/--api_key argument")


    # Client Initialization for Together API
    client = Together(api_key=api_key)

    # model
    #model = "meta-llama/Meta-Llama-3-8B-Instruct-Lite"
    model = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
    
    # Make the API call
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={
            "type": "json_object",
            "schema": {
                "type": "object",
                "properties": {
                    "ai_response_sentence": {"type": "string"},
                    "nouns": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 5,
                        "maxItems": 5
                    },
                    "adjectives": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 5,
                        "maxItems": 5
                    },
                    "verbs": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 5,
                        "maxItems": 5
                    }
                },
                "required": ["ai_response_sentence", "nouns", "adjectives", "verbs"]
            }
        }
    )
    output = response.choices[0].message.content

    # considering to remove this linebreak option
    if with_linebreak:
        # Wrap the output
        wrapped_output = textwrap.fill(output, width=50)
    
        return wrapped_output
    else:
        return output


PROMPT_TEMPLATE_basic_user_request = """
help the user with the following request:
{user_request}
""" 


PROMPT_TEMPLATE_get_conversation_helper_json = """
# Language Learning Conversation Assistant

You are helping people practice speaking in a new language. Two people are having a conversation, and you need to provide assistance when they get stuck or need vocabulary support.

## Your Task
Analyze the ongoing conversation and generate an output in the following JSON format:

{{
  "ai_response_sentence": "A natural sentence that could continue the conversation",
  "nouns": ["word1", "word2", "word3", "word4", "word5"],
  "adjectives": ["word1", "word2", "word3", "word4", "word5"],
  "verbs": ["word1", "word2", "word3", "word4", "word5"]
}}

## Guidelines

### For Word Lists (nouns, adjectives, verbs):
- Provide exactly 5 words in each category
- Choose words that are relevant to the current conversation topic
- Include words that might naturally come up as the conversation continues
- Focus on practical, commonly used words that learners can easily incorporate
- Consider the conversation's direction and potential next topics

### For AI Response Sentence:
- Create ONE complete, natural sentence that could logically continue the conversation
- Make it something either speaker could realistically say next
- Keep it at an appropriate difficulty level for language learners
- Ensure it flows naturally from the conversation context
- This serves as a "lifeline" when both speakers are completely stuck

## Current Conversation:
{conversation_doc}

## Important Notes:
- Respond ONLY with the JSON format above
- No additional explanations or text outside the JSON
- Words should be in the target language being practiced
- The ai_response_sentence should sound natural and conversational, not formal or robotic
"""