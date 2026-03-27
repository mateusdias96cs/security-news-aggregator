import json

def salvar_json(noticias, arquivos="noticias.json"):
    with open(arquivos, "w", encoding="utf-8") as f:
        json.dump(noticias, f, indent=4, ensure_ascii=False)
    print(f"{len(noticias)} notícias salvas em '{arquivos}'")

def ler_json(arquivos="noticias.json"):
    try:
        with open(arquivos, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Arquivo '{arquivos}' não encontrado.")
        return []