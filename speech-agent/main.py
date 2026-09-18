from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

import os 

def main():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        load_dotenv()
        
        foundry_endpoint = os.getenv('FOUNDRY_ENDPOINT') 
        agent_name = os.getenv('AGENT_NAME') 
        
        project_client = AIProjectClient(
            endpoint=foundry_endpoint,
            credential=DefaultAzureCredential(),
        )
        
        openai_client = project_client.get_openai_client()
        # Looping principal
        while True:
            prompt = input("Insira seu prompt ('q' ou 'quit' para sair): ")
            if prompt.lower() in ['quit', 'q']  or len(prompt) == 0:
                break;
            
            else: 
                response = openai_client.responses.create(
                    input=[{"role": "user", "content": prompt}],
                    extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"} },)
                print(f"{agent_name}: {response.output_text}")
    except Exception as e:
        print(e)
        
        
if __name__ == "__main__":
    main()
        
        
        
        