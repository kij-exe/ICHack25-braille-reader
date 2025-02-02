import os  # For environment variables and OS interactions
import anthropic  # Official Anthropic SDK for Claude API
from dotenv import load_dotenv  # For loading .env files

def convert_braille_to_english(braille_input: str) -> str:
    #documentation - 😂😂🤓👍
    """
    Convert Braille text to English using Claude 3.5 Sonnet model.
    
    Args:
        braille_input (str): Braille text in Unicode format (U+2800 to U+28FF)
    
    Returns:
        str: Converted and corrected English text
    
    Raises:
        ValueError: For invalid input format or empty input
        EnvironmentError: Missing API key in environment
        ConnectionError: API connection issues
        RuntimeError: General API errors
    """
    # Validate input contains only Braille Unicode characters or whitespace
    # Braille Unicode range: U+2800 to U+28FF (6-dot Braille patterns)
    if not all('\u2800' <= char <= '\u28FF' or char.isspace() for char in braille_input):
        raise ValueError("Input contains non-Braille Unicode characters")

    # Check for empty or whitespace-only input
    if not braille_input.strip():
        raise ValueError("Braille input cannot be empty")

    # Load environment variables from .env file
    load_dotenv()
    
    # Retrieve API key from environment variables
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY not found in .env file")

    # Initialize Anthropic client with API key
    client = anthropic.Anthropic(api_key=api_key)

    try:
        # Create API request with strict translation instructions
        message = client.messages.create(
            max_tokens=4000,  # Limit response length for cost/safety
            system=(
                "You are a professional Braille translator. Follow these rules:\n"
                "1. MOST IMPORTANT: MAKE ALL WORDS MAKE SENSE EVEN IF YOU HAVE TO GUESS\n"
                "1. Convert Braille to English exactly\n"
                "2. Preserve ALL punctuation, numbers and formatting\n"
                "3. Remove any translator notes\n"
                "4. Maintain original line breaks\n"
                "5. Never add markdown formatting\n"
                "6. ICHACK may appear in short text answers\n"
                "Output ONLY the raw converted text."
            ),
            messages=[{"role": "user", "content": braille_input}],
            model="claude-3-5-sonnet-20240620",  # Latest Claude 3.5 model
            temperature=0.2  # Balance between creativity (0) and determinism (1)
        )
        
        # Post-process API response
        translated = message.content[0].text  # Extract text from response
        translated = translated.strip()  # Remove leading/trailing whitespace
        translated = ' '.join(translated.splitlines())  # Normalize line breaks
        return translated

    # Handle specific API connection errors
    except anthropic.APIConnectionError as e:
        raise ConnectionError(f"Connection error: {e.__cause__}") from e
    
    # Handle general API errors
    except anthropic.APIError as e:
        raise RuntimeError(f"API error: {e.message}") from e


#commented out argparse code for standalone use
# def cli_main():
#     """Command-line interface"""
#     parser = argparse.ArgumentParser(
#         description='Convert Braille text to English using Claude 3.5 Sonnet',
#         epilog='Example: python braille_converter.py "⠠⠃⠗⠁⠊⠇⠇⠑ ⠑⠭⠁⠍⠏⠇⠑ ⠞⠑⠭⠞"'
#     )
#     parser.add_argument('braille_input', type=str, 
#                       help='Braille text to convert (Unicode characters U+2800 to U+28FF)')
#     args = parser.parse_args()
    
#     try:
#         result = convert_braille_to_english(args.braille_input)
#         print("Translation Result:\n")
#         print(result)
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         exit(1)
# if __name__ == "__main__":
#     cli_main()
