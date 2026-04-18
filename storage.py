import json
import os
from datetime import datetime, timedelta

ARQUIVO_HOJE = "noticias.json"
ARQUIVO_HISTORICO = "historico.json"

def salvar_json(noticias, arquivo=ARQUIVO_HOJE):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(noticias, f, indent=4, ensure_ascii=False)
    print(f"{len(noticias)} notícias salvas em '{arquivo}'")

def ler_json(arquivo=ARQUIVO_HOJE):
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def atualizar_historico(noticias_hoje):
    """
    Adiciona as notícias de hoje ao histórico.
    Remove notícias com mais de 7 dias.
    Deduplica por URL.
    """
    historico = ler_json(ARQUIVO_HISTORICO)

    urls_existentes = {n.get("url") for n in historico}
    hoje = datetime.now().date()
    limite = hoje - timedelta(days=7)

    for noticia in noticias_hoje:
        url = noticia.get("url")
        if url and url not in urls_existentes:
            noticia["salvo_em"] = hoje.isoformat()
            historico.append(noticia)
            urls_existentes.add(url)

    # Remove notícias mais antigas que 7 dias
    historico = [
        n for n in historico
        if datetime.fromisoformat(
            n.get("salvo_em", hoje.isoformat())
        ).date() >= limite
    ]

    salvar_json(historico, ARQUIVO_HISTORICO)
    print(f"Histórico atualizado: {len(historico)} notícias (últimos 7 dias)")
    return historico