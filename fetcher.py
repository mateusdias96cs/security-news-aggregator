import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('NEWS_API_KEY')
BASE_URL = 'https://newsapi.org/v2/everything'

def buscar_noticias():
    """Notícias internacionais em inglês"""
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
        print(f"Erro EN: {response.status_code}")
        return []

def buscar_noticias_br():
    """
    Busca notícias de cibersegurança em português.
    Usa termos técnicos específicos para garantir relevância.
    Filtra resultados irrelevantes no Python após a busca.
    """
    headers = {"X-Api-Key": API_KEY}
    
    # Termos muito específicos de cibersegurança
    # que raramente aparecem em outros contextos
    params = {
        "q": (
            '"cibersegurança" OR "ransomware" OR '
            '"vazamento de dados" OR "ataque hacker" OR '
            '"malware" OR "phishing" OR "vulnerabilidade CVE" OR '
            '"segurança da informação" OR "ataque cibernético" OR '
            '"LGPD" OR "pentest" OR "zero-day" OR '
            '"firewall" OR "DDoS" OR "engenharia social"'
        ),
        "language": "pt",
        "sortBy": "publishedAt",
        "pageSize": 40  # Busca mais para compensar filtragem
    }
    
    response = requests.get(BASE_URL, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"Erro PT-BR: {response.status_code}")
        return []
    
    artigos = response.json()["articles"]
    
    # Palavras-chave que indicam que o artigo É de cibersegurança
    CYBER_KEYWORDS = [
        'cibersegurança', 'ransomware', 'malware', 'phishing',
        'vulnerabilidade', 'ataque hacker', 'ataque cibernético',
        'vazamento de dados', 'lgpd', 'pentest', 'zero-day',
        'firewall', 'ddos', 'trojan', 'exploit', 'breach',
        'segurança da informação', 'criptografia', 'botnet',
        'engenharia social', 'apt', 'threat', 'hacker',
        'ciberataque', 'invasão', 'credencial', 'autenticação',
        'backdoor', 'spyware', 'keylogger', 'rootkit'
    ]
    
    # Palavras que indicam que NÃO é cibersegurança
    EXCLUDE_KEYWORDS = [
        'futebol', 'gol', 'campeonato', 'jogo de hoje',
        'astronauta', 'artemis', 'nasa', 'espaço',
        'receita', 'culinária', 'moda', 'celebridade',
        'novela', 'série', 'filme', 'música',
        'economia', 'bolsa de valores', 'dólar',
        'política', 'eleição', 'presidente',
        'reforma do estado', 'saúde pública'
    ]
    
    filtrados = []
    for artigo in artigos:
        titulo = (artigo.get('title') or '').lower()
        descricao = (artigo.get('description') or '').lower()
        texto = titulo + ' ' + descricao
        
        # Exclui se tiver palavras fora do tema
        if any(exc in texto for exc in EXCLUDE_KEYWORDS):
            continue
        
        # Inclui apenas se tiver pelo menos uma palavra cyber
        if any(kw in texto for kw in CYBER_KEYWORDS):
            artigo["idioma"] = "pt-br"
            filtrados.append(artigo)
    
    # Limita a 20 notícias após filtragem
    filtrados = filtrados[:20]
    
    print(f"Notícias BR encontradas: {len(artigos)}")
    print(f"Notícias BR relevantes após filtro: {len(filtrados)}")
    return filtrados
if __name__ == "__main__":
    artigos = buscar_noticias()
    print(f"Total de artigos recebidos: {len(artigos)}")
    print(artigos[0])