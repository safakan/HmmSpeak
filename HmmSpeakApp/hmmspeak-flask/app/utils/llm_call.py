from dotenv import load_dotenv
import os
from together import Together
import textwrap
import logging

# Configure logging for this module
logger = logging.getLogger(__name__)

def prompt_llm(prompt):
    logger.info("=== LLM API CALL START ===")
    logger.info(f"Prompt length: {len(prompt)} characters")
    logger.info(f"Prompt preview: {prompt[:200]}...")
    
    # Load environment variables from .env file
    load_dotenv()
    api_key = os.getenv("TOGETHER_API_KEY")

    if not api_key:
        logger.error("API key not found. TOGETHER_API_KEY not set in .env file")
        raise ValueError("API key not found. Please set TOGETHER_API_KEY in .env file")

    logger.info("API key loaded successfully")

    # Client Initialization for Together API
    try:
        client = Together(api_key=api_key)
        logger.info("Together API client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Together API client: {e}")
        raise

    # model
    # model = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
    # model = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
    model = "meta-llama/Llama-3.3-70B-Instruct-Turbo"
    logger.info(f"Using model: {model}")
    
    # Make the API call
    try:
        logger.info("Initiating API call to Together...")
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
                            "items": {"type": "string"}
                        },
                        "adjectives": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "verbs": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["ai_response_sentence", "nouns", "adjectives", "verbs"]
                }
            }
        )
        logger.info("API call completed successfully")
        logger.info(f"Response object type: {type(response)}")
        
        output = response.choices[0].message.content
        logger.info(f"Raw LLM response length: {len(output)} characters")
        logger.info(f"Raw LLM response: {output}")
        logger.info("=== LLM API CALL END ===")
        
        return output
        
    except Exception as e:
        logger.error(f"API call failed: {e}", exc_info=True)
        logger.error("=== LLM API CALL FAILED ===")
        raise


PROMPT_TEMPLATE_get_conversation_helper_json = """
# Language Learning Conversation Assistant

You are a helpful assistant that process conversation keywords, a conversation document with guidance of these instructions.
The mentioned conversation keywords and the conversation document exists at the end of this prompt. 
Based on entirety of this prompt process the conversation keywords and the conversation document and return ONLY a JSON as you are already programmed to do so.


## MAIN CONTEXT

- This is inside of a language learning app specifically designed to help people practice speaking in English in real time in the same physical environmnet.
- The conversation keywords include keywords speakers enter about their conversation and their feelings. These keywords should redirect/guide the entire conversation.
- This conversation document contains the transcription result of a conversation happening in real time.
- There could be two or more people speaking in real time with each other and practicing speaking.
- Your goal is to understand what they're speaking about, predict what they might speak about and make suggestions.

Your suggestions are shown on a screen, and people look at this screen when they get stuck within their conversation.
Your task is to inspire them with suggestions words related to their conversation and where that conversation might lead to.
You make positive and upbeat suggestions/predictions. 

Even if people start to speak in different languages you always generate English content, and try to force people speaking English.
If things don't make sense, just generate random positive words and a question about a random topic.

## STRICT OUTPUT REQUIREMENTS
You must follow these requirements exactly:
1. Return EXACTLY 5 nouns - no more, no less
2. Return EXACTLY 5 adjectives - no more, no less
3. Return EXACTLY 5 verbs - no more, no less
4. Return EXACTLY 1 ai_response_sentence - no more, no less

## STRICT OUTPUT FORMAT REQUIREMENTS
Your response must be in this exact JSON format:
{{
  "ai_response_sentence": "A single sentence asking a question to contribute to the conversation.",
  "nouns": ["word1", "word2", "word3", "word4", "word5"],
  "adjectives": ["word1", "word2", "word3", "word4", "word5"],
  "verbs": ["word1", "word2", "word3", "word4", "word5"]
}}



## Final Reminder
- Respond ONLY with the JSON format above
- No additional explanations or text outside the JSON
- Words should be in the target language being practiced
- The ai_response_sentence should be a question aimed to open up topics within a conversation.
- REMEMBER: EXACTLY 5 words in each list and EXACTLY 1 response sentence

Even if people start to speak in different languages you always generate English content, and try to force people speaking English.
If things don't make sense, just generate random positive words and a question about a random topic.

## Current Conversation Keywords:
{conversation_keywords}

## Current Conversation Doc:
{conversation_doc}
"""





# PROMPT_TEMPLATE_get_conversation_helper_json0 = """
# # Language Learning Conversation Assistant

# You are helping people practice speaking in a new language. Two people are having a conversation, and you need to provide assistance when they get stuck or need vocabulary support.

# ## STRICT OUTPUT REQUIREMENTS
# You must follow these requirements exactly:
# 1. Return EXACTLY 5 nouns - no more, no less
# 2. Return EXACTLY 5 adjectives - no more, no less
# 3. Return EXACTLY 5 verbs - no more, no less
# 4. Return EXACTLY 1 ai_response_sentence - no more, no less

# ## Output Format
# Your response must be in this exact JSON format:
# {{
#   "ai_response_sentence": "A single natural sentence that could continue the conversation",
#   "nouns": ["word1", "word2", "word3", "word4", "word5"],
#   "adjectives": ["word1", "word2", "word3", "word4", "word5"],
#   "verbs": ["word1", "word2", "word3", "word4", "word5"]
# }}

# ## Guidelines

# ### For Word Lists (nouns, adjectives, verbs):
# - You MUST provide EXACTLY 5 words in each category
# - Choose words that are relevant to the current conversation topic
# - Include words that might naturally come up as the conversation continues
# - Focus on practical, commonly used words that learners can easily incorporate
# - Consider the conversation's direction and potential next topics
# - If you can't think of enough relevant words, use generic words to complete the list

# ### For AI Response Sentence:
# - Create EXACTLY ONE complete, natural sentence
# - Make it something either speaker could realistically say next
# - Keep it at an appropriate difficulty level for language learners
# - Ensure it flows naturally from the conversation context
# - This serves as a "lifeline" when both speakers are completely stuck

# ## Current Conversation Doc:
# {conversation_doc}

# ## Final Reminder
# - Respond ONLY with the JSON format above
# - No additional explanations or text outside the JSON
# - Words should be in the target language being practiced
# - The ai_response_sentence should sound natural and conversational
# - REMEMBER: EXACTLY 5 words in each list and EXACTLY 1 response sentence
# """