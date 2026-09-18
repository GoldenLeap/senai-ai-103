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
        endpoint = os.getenv("STT_ENDPOINT")
        model_deployment = os.getenv("STT_MODEL")
        file_path = Path(__file__).parent / "speech.wav"
        
        # Play the speech file
        playsound(file_path)
        
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

        
        # Call model to transcribe audio file
        audio_file= open(file_path, 'rb')
        trasncription = client.audio.transcriptions.create(
            model=model_deployment,
            file=audio_file,
            response_format='text'
        )
        print(trasncription)


    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()