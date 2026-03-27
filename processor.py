def processar_noticias(artigos):
    noticias = []
    for artigo in artigos:
        noticias.append({
            "titulo": artigo["title"],
            "fonte":  artigo["source"]["name"],
            "autor":  artigo["author"],
            "data":   artigo["publishedAt"],
            "url":    artigo["url"],
            "resumo": artigo["description"]
        })
    return noticias 