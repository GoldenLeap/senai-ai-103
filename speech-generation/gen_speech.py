import os
from pathlib import Path
from playsound3 import playsound
from dotenv import load_dotenv

# Import namespaces
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

def main():
    try:
        # Clear the console
        os.system('cls' if os.name == 'nt' else 'clear')

        # Get Configuration Settings
        load_dotenv()
        endpoint=os.getenv("TTS_ENDPOINT")
        model_deployment=os.getenv("TTS_MODEL")
        speech_file_path = Path(__file__).parent / "speech.mp3"


        # Create the Azure OpenAI client
        credentials = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(
            credentials, "https://ai.azure.com/.default"
        )
        
        client = AzureOpenAI(
            azure_endpoint=endpoint,
            azure_ad_token_provider=token_provider,
            api_version="2025-03-01-preview"
        )
        


        # Generate speech and save to file
        with client.audio.speech.with_streaming_response.create(
            model=model_deployment,
            voice="ballad",
            input="I'd like to have a cup of tea",
            instructions="Speak in a funny way",
        ) as response:
            response.stream_to_file(speech_file_path)


        # Play the generated speech file
        playsound(speech_file_path)

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main() 
