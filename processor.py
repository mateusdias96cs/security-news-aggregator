import re
from urllib.parse import urlparse
from datetime import datetime


# ── SANITIZAÇÃO ──

def sanitizar_texto(texto, max_len=500):
    """Remove tags HTML, caracteres perigosos e limita tamanho."""
    if not texto or not isinstance(texto, str):
        return ""

    # Remove tags HTML
    texto = re.sub(r'<[^>]+>', '', texto)

    # Escapa caracteres perigosos para HTML
    texto = texto.replace('&', '&amp;')
    texto = texto.replace('<', '&lt;')
    texto = texto.replace('>', '&gt;')
    texto = texto.replace('"', '&quot;')
    texto = texto.replace("'", '&#x27;')

    # Remove javascript: e data: URIs escondidos em texto
    texto = re.sub(r'javascript\s*:', '', texto, flags=re.IGNORECASE)
    texto = re.sub(r'data\s*:', '', texto, flags=re.IGNORECASE)
    texto = re.sub(r'vbscript\s*:', '', texto, flags=re.IGNORECASE)

    # Remove caracteres de controle
    texto = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', texto)

    # Normaliza espaços
    texto = ' '.join(texto.split())

    return texto[:max_len].strip()


def sanitizar_url(url):
    """Valida e sanitiza URLs — aceita apenas http e https."""
    if not url or not isinstance(url, str):
        return "#"

    url = url.strip()

    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return "#"
        if not parsed.netloc:
            return "#"
        # Bloqueia javascript: e data: URIs
        if re.search(r'javascript\s*:', url, re.IGNORECASE):
            return "#"
        if re.search(r'data\s*:', url, re.IGNORECASE):
            return "#"
        return url
    except Exception:
        return "#"


def sanitizar_imagem(url):
    """Valida URL de imagem — aceita apenas http e https."""
    url_limpa = sanitizar_url(url)
    if url_limpa == "#":
        return ""
    return url_limpa


def sanitizar_fonte(fonte, max_len=80):
    """Sanitiza nome da fonte."""
    if not fonte or not isinstance(fonte, str):
        return "Desconhecido"
    # Permite apenas alfanuméricos, espaços e alguns caracteres seguros
    fonte = re.sub(r'[<>"\'&;]', '', fonte)
    return fonte[:max_len].strip() or "Desconhecido"


def sanitizar_data(data):
    if not data or not isinstance(data, str):
        return ""
    data = data.strip()
    # Tenta formatos conhecidos
    formatos = [
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S GMT",
        "%Y-%m-%d",
    ]
    for fmt in formatos:
        try:
            dt = datetime.strptime(data[:30], fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    # Fallback: retorna apenas os 10 primeiros caracteres se parecer data ISO
    if re.match(r'^\d{4}-\d{2}-\d{2}', data):
        return data[:10]
    return ""


# ── PROCESSAMENTO ──

def processar_noticias(artigos):
    noticias = []

    for artigo in artigos:
        # Valida estrutura mínima
        fonte_raw = artigo.get("source", {})
        if not isinstance(fonte_raw, dict):
            continue

        fonte_nome = fonte_raw.get("name", "")
        titulo_raw = artigo.get("title", "")
        url_raw = artigo.get("url", "")

        # Campos obrigatórios
        if not titulo_raw or not url_raw or not fonte_nome:
            continue

        # Sanitiza todos os campos
        titulo = sanitizar_texto(titulo_raw, max_len=200)
        fonte = sanitizar_fonte(fonte_nome)
        autor = sanitizar_texto(artigo.get("author") or "", max_len=100)
        data = sanitizar_data(artigo.get("publishedAt") or "")
        url = sanitizar_url(url_raw)
        resumo = sanitizar_texto(artigo.get("description") or "", max_len=300) or "Sem resumo"
        imagem = sanitizar_imagem(artigo.get("urlToImage") or artigo.get("image") or "")

        # Descarta artigo se título ou URL ficaram inválidos após sanitização
        if not titulo or url == "#":
            continue

        noticias.append({
            "titulo": titulo,
            "fonte":  fonte,
            "autor":  autor,
            "data":   data,
            "url":    url,
            "resumo": resumo,
            "imagem": imagem
        })

    return noticias