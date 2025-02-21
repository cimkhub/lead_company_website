# LLM_check.py
from LLM_call_API import get_openai_response

def generate_description(AI_role, custom_prompt):
    """
    Calls the get_openai_response function with a given role and custom_prompt.
    Expects a JSON output from the LLM (e.g. {"Company_Description": "..."}).
    Parses or returns the string as is.
    """
    response_text = get_openai_response(AI_role, custom_prompt)

    # Optionally, you might parse or verify the JSON. For now, return the raw string.
    return response_text