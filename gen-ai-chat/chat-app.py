import os
from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

def main():
    os.system('cls' if os.name == "nt" else 'clear')
    
    try:
        load_dotenv()
        
        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")    
        model_deployment = os.getenv("MODEL_DEPLOYMENT")    

        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(),
            "https://ai.azure.com/.default"
        )
        
        
        client = OpenAI(
            base_url=azure_openai_endpoint,
            api_key=token_provider
        )
        
        last_response_id = None
        
        
        while True:
            
            
            
            input_text = input('\nInsira um prompt( ou digite q para sair): ')
            if input_text.lower() == "quit" or input_text.lower() == 'q':
                break
            if len(input_text) == 0:
                print('Por favor insira um prompt')
                continue
            
            
           # Get a response
            stream = client.responses.create(
                        model=model_deployment,
                        instructions="You are a helpful AI assistant that answers questions and provides information.",
                        input=input_text,
                        previous_response_id=last_response_id,
                        stream=True
            )
            for event in stream:
                if event.type == "response.output_text.delta":
                    print(event.delta, end="")
                elif event.type == "response.completed":
                    last_response_id = event.response.id
            print()

    except Exception as e:
        print(f"Erro: {e}")
        
    


if __name__ == "__main__":
    main()