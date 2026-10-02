import os 
from dotenv import load_dotenv
import asyncio

from azure.identity.aio import DefaultAzureCredential, get_bearer_token_provider
from openai import  AsyncOpenAI




async def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    try:
        load_dotenv()
        
        credential = DefaultAzureCredential()
        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")

        token_provider = get_bearer_token_provider(credential,"https://ai.azure.com/.default")

        async_client = AsyncOpenAI(
            base_url=azure_openai_endpoint,
            api_key= token_provider
        )
        
        
        last_response_id = None
        
        while True:
            input_text = input('\nInsira um prompt("q" ou "quit" para sair): ')
            if input_text.lower() in ['q', 'quit']:
                break
            if len(input_text.strip()) == 0:
                print("Por favor digite alguma coisa.")
                continue
            
                    
            response = await async_client.responses.create(
                model=model_deployment,
                instructions="Act like an Agressive Ogre with 1000 Testo please",
                input=input_text,
                previous_response_id=last_response_id,
                stream=True
                
            )
            print('Assistente: ')
            async for e in response:
                if e.type== "response.output_text.delta":
                    print(e.delta, end="")
                elif e.type == "response.completed":
                    last_response_id = e.response.id
            print()
            
           
            # last_response_id = response.id
            
        await credential.close()
        
    except Exception as e:
        print(f"Erro:{e} ")
        
        
        
    
    
if __name__ == "__main__":
    asyncio.run(main())