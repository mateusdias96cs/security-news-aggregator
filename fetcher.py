import requests
import os
from dotenv import load_dotenv
import feedparser
import time
from datetime import datetime, timezone

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

# Sites brasileiros 100% especializados em cibersegurança
# com seus RSS feeds verificados
BR_CYBER_FEEDS = [
    {
        "url": "https://www.cisoadvisor.com.br/feed/",
        "nome": "CISO Advisor"
    },
    {
        "url": "https://boletimsec.com/feed/",
        "nome": "Boletim Sec"
    },
    {
        "url": "https://caveiratech.com/feed/",
        "nome": "Caveira Tech"
    },
    {
        "url": "https://www.welivesecurity.com/pt/feed/",
        "nome": "WeLiveSecurity BR"
    },
    {
        "url": "https://securityleaders.com.br/feed/",
        "nome": "Security Leaders"
    },
    {
        "url": "https://www.securityreport.com.br/feed/",
        "nome": "Security Report"
    },
    {
        "url": "https://minutodaseguranca.com.br/feed/",
        "nome": "Minuto da Segurança"
    },
]

import urllib.request
import re as _re

def _fetch_og_image(url, timeout=5):
    """
    Busca o og:image de uma URL fazendo request leve apenas do
    início do HTML (primeiros 8KB são suficientes para o <head>).
    Retorna a URL da imagem ou string vazia em caso de falha.
    """
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': (
                    'Mozilla/5.0 (compatible; SecurityNewsBot/1.0)'
                ),
                'Range': 'bytes=0-8191'  # Pega só os primeiros 8KB
            }
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode('utf-8', errors='ignore')

        # Procura og:image em qualquer formato de atributo
        patterns = [
            r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\'](https?://[^"\'>\s]+)',
            r'<meta[^>]+content=["\'](https?://[^"\'>\s]+)[^>]+property=["\']og:image["\']',
            r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\'](https?://[^"\'>\s]+)',
        ]
        for pattern in patterns:
            match = _re.search(pattern, html, _re.IGNORECASE)
            if match:
                img_url = match.group(1)
                # Ignora imagens genéricas de logo/favicon
                if not any(skip in img_url.lower() for skip in
                          ['logo', 'favicon', 'icon', '1x1', 'pixel']):
                    return img_url
    except Exception:
        pass
    return ''


def extrair_imagem_rss(entry, fallback_url=''):
    """
    Tenta extrair imagem do entry RSS.
    Se não encontrar, busca og:image da página do artigo.
    """
    # 1. media:content
    if hasattr(entry, 'media_content') and entry.media_content:
        for mc in entry.media_content:
            url = mc.get('url', '')
            if url:
                return url

    # 2. media:thumbnail
    if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
        url = entry.media_thumbnail[0].get('url', '')
        if url:
            return url

    # 3. enclosures
    if hasattr(entry, 'enclosures') and entry.enclosures:
        for enc in entry.enclosures:
            if 'image' in enc.get('type', ''):
                return enc.get('url', '')

    # 4. Imagem no HTML do summary/content
    html_fields = []
    if hasattr(entry, 'content') and entry.content:
        html_fields.append(entry.content[0].get('value', ''))
    html_fields.append(entry.get('summary', '') or '')

    for html in html_fields:
        if not html:
            continue
        match = _re.search(
            r'<img[^>]+src=["\'](https?://[^"\']+\.(jpg|jpeg|png|webp))["\']',
            html, _re.IGNORECASE
        )
        if match:
            url = match.group(1)
            if 'pixel' not in url and '1x1' not in url:
                return url

    # 5. Fallback: busca og:image direto na página do artigo
    if fallback_url:
        return _fetch_og_image(fallback_url)

    return ''

def buscar_noticias_br():
    """
    Busca notícias de cibersegurança diretamente dos RSS feeds
    de sites brasileiros 100% especializados no tema.
    Não depende da NewsAPI — funciona independente do plano.
    """
    artigos = []
    urls_vistas = set()

    for feed_info in BR_CYBER_FEEDS:
        try:
            feed = feedparser.parse(feed_info["url"])
            
            # Verifica se o feed foi carregado com sucesso
            if feed.bozo and not feed.entries:
                print(f"[AVISO] Feed indisponível: {feed_info['nome']}")
                continue

            for entry in feed.entries[:5]:  # Máximo 5 por fonte
                url = entry.get("link", "")
                
                # Deduplicação por URL
                if not url or url in urls_vistas:
                    continue
                urls_vistas.add(url)

                # Extrai a data de publicação
                published = entry.get("published_parsed") or entry.get("updated_parsed")
                if published:
                    dt = datetime(*published[:6], tzinfo=timezone.utc)
                    data_str = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                else:
                    data_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

                # Passa a URL do artigo como fallback para buscar og:image
                imagem = extrair_imagem_rss(entry, fallback_url=url)

                # Limpa o resumo removendo HTML
                resumo = entry.get("summary", "") or entry.get("description", "")
                if resumo:
                    import re
                    resumo = re.sub(r'<[^>]+>', '', resumo).strip()
                    resumo = resumo[:300]

                artigos.append({
                    "titulo": entry.get("title", "Sem título"),
                    "fonte": feed_info["nome"],
                    "autor": entry.get("author", ""),
                    "data": data_str,
                    "url": url,
                    "imagem": imagem,
                    "resumo": resumo,
                    "idioma": "pt-br"
                })

        except Exception as e:
            print(f"[ERRO] Falha ao ler feed {feed_info['nome']}: {e}")
            continue

    # Ordena por data mais recente
    artigos.sort(key=lambda x: x.get("data", ""), reverse=True)
    
    total = len(artigos)
    print(f"Notícias BR via RSS: {total} artigos de {len(BR_CYBER_FEEDS)} fontes")
    
    if total == 0:
        print("[AVISO] Nenhuma notícia BR encontrada via RSS.")
    
    print("\n--- TESTE DE EXTRAÇÃO DE IMAGENS ---")
    for a in artigos[:5]:
        print(f"[{a['titulo']}] Imagem: {a.get('imagem') or 'sem imagem'}")
    print("------------------------------------\n")

    return artigos[:20]
if __name__ == "__main__":
    artigos = buscar_noticias()
    print(f"Total de artigos recebidos: {len(artigos)}")
    print(artigos[0])