import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('NEWS_API_KEY')
BASE_URL = 'https://newsapi.org/v2/everything'

def buscar_noticias():
    headers = {"X-Api-Key": API_KEY}
    params = {
        "q": "cybersecurity vulnerability",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 20
    }
    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()["articles"]
    else:
        print(f"Erro: {response.status_code}")
        return []
if __name__ == "__main__":
    artigos = buscar_noticias()
    print(f"Total de artigos recebidos: {len(artigos)}")
    print(artigos[0])