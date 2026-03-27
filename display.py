def mostrar_top10(noticias):
    print("\n" + "="*50)
    print("   🛡️  TOP 10 SECURITY NEWS")
    print("="*50 + "\n")
    
    for i, noticia in enumerate(noticias[:10], 1):
        print(f"{i}. {noticia['titulo']}")
        print(f"   Fonte: {noticia['fonte']}")
        print(f"   Autor: {noticia['autor']}")
        print(f"   Data: {noticia['data']}")
        print(f"   URL: {noticia['url']}")
        print(f"   Resumo: {noticia['resumo'][:100]}...")
        print("-"*50)