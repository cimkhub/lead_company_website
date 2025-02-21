import os
from openai import OpenAI
from dotenv import load_dotenv
# Load environment variables from .env file

load_dotenv()
def get_openai_response(AI_role, custom_prompt):
    """
    Get a response from the OpenAI API based on a custom prompt and system role.
    Parameters:
      AI_role (str): The content for the system message (i.e. instructions for the AI).
      custom_prompt (str): The prompt provided by the user.
    Returns:
      str: The content of the response message.
    """
    # Set the API key from the environment variable
    
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
    )
    # Call the OpenAI Chat Completion endpoint
    response = client.chat.completions.create(
        model="gpt-4o",  # Replace with your desired model (e.g. "gpt-4" or "gpt-3.5-turbo")
        messages=[
            {"role": "system", "content": AI_role},
            {"role": "user", "content": custom_prompt},
        ],
        temperature=1.0,
        max_tokens=4000,
        stream=False,
    )
    print(response)
    # Return the content of the response message
    return response.choices[0].message.content



