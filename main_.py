import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv


def main():
    load_dotenv("a.env")
    promts = sys.argv[1:]

    if len(promts) == 0:
        print("No prompt provided")
        sys.exit(1)

    verbose_active = False
    if "--verbose" in promts:
        verbose_active = True
        promts.remove("--verbose")

    user_promt = ""

    for i in [0, len(promts) - 1]:
        if promts[i] != "--verbose":
            user_promt += " " + promts[i]
        
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_promt)])
    ]
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
    )

    if verbose_active:
        print("User prompt: " + user_promt + "\n")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)

    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
