import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")    
    args = parser.parse_args()
    load_dotenv("a.env")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    function_responses = []

    for _ in range(20):
        response = client.models.generate_content(    
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            )
        )

        if response.candidates[0]:
            for candidate in response.candidates:
                messages.append(response.candidates[0].content)

        if not response.usage_metadata:
            raise RuntimeError("Gemini API response appears to be malformed")

        if args.verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        if not response.function_calls:
            print("Response:")
            print(response.text)
            return

        for function_call in response.function_calls:
            result = call_function(function_call, args.verbose)
            if (
                not result.parts
                or not result.parts[0].function_response
                or not result.parts[0].function_response.response
            ):
                raise RuntimeError(f"Empty function response for {function_call.name}")
            if args.verbose:
                print(f"-> {result.parts[0].function_response.response}")
            function_responses.append(result.parts[0])
        messages.append(
            types.Content(
                role="user",
                parts=function_responses,
            )
        )

        if _ == 19:
            print(f"{_ + 1} steps was reached, which is the maximum defined. No more function calls possible")
            exit(1)





if __name__ == "__main__":
    main()
