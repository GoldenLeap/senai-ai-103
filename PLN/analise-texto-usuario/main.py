from azure.identity import DefaultAzureCredential
from azure.ai.textanalytics import TextAnalyticsClient
import dotenv
import os
# Carrega variaveis de ambiente
dotenv.load_dotenv()
os.system('cls' if os.name == "nt" else 'clear')
# login azure 
endpoint_foundry = os.getenv("FOUNDRY_ENDPOINT")

# Client do modelo
credentials = DefaultAzureCredential() # Espera que esteja logado pelo azure cli
ai_client = TextAnalyticsClient(endpoint=endpoint_foundry, credential=credentials)


# Pega o texto do usuario
texto = input("Digite um texto para ser analisado: ")
while(texto.strip() == "" or texto.strip() == None):
    texto = input("Texto vazio digite um texto valido: ")

# Analise de linguagem
lang_data = ai_client.detect_language(documents=[texto])[0]

# Analise de sentimentos
emot_data = ai_client.analyze_sentiment(documents=[texto])[0]
sentimento = emot_data.sentiment
sent_key = {
    "positive": "positivo",
    "negative": "negativo",
    "neutral": 'neutro',
    'mixed': "misturado"
}

positivo_perc = f"{emot_data.confidence_scores.positive * 100:.2f}%"
neutro_perc = f"{emot_data.confidence_scores.neutral * 100:.2f}%"
negativo_perc = f"{emot_data.confidence_scores.negative * 100:.2f}%"

# Extração de frase chave
key_phr = ai_client.extract_key_phrases(documents=[texto])[0]

# Extração de Entidades
entities = ai_client.recognize_entities(documents=[texto])[0]

print(f"Idioma principal do texto: {lang_data.primary_language}\n")
print(f"-"*200)
print(f"Analise de sentimento")
print(f"{'Sentimento|':<60} {'Positivo|':<50}| {'Neutro|':<40}| {'Negativo|':<30} ")
print(f"{sent_key[sentimento]+'|':<60} {positivo_perc+'|':<50} {neutro_perc+'|':<40}| {negativo_perc+"|":<30}")
print(f"-"*200)
print(f'Frases chaves')

for frases in key_phr.key_phrases:
    print(frases)
print(f'-'*200)
print("Entidades:")
print(f"{'Entidade|':<60} {'Categoria|':<50} {'Confiança|':<40}")


for e in entities.entities:
    confianca = f"{e.confidence_score * 100:.2f}%"
    print(f"{e.text:<60} {e.category:<50} {confianca:<40}")    
print("-"*200)



