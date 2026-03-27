from fetcher import buscar_noticias
from processor import processar_noticias
from storage import salvar_json, ler_json
from display import mostrar_top10
import subprocess

def main():
    print("🔍 Buscando notícias de segurança...")

    artigos = buscar_noticias()

    if not artigos:
        print("Nenhum artigo encontrado.")
        return

    print("⚙️  Processando notícias...")
    noticias = processar_noticias(artigos)

    salvar_json(noticias)

    mostrar_top10(noticias)

    # Gera HTML automaticamente
    subprocess.run(["python", "gerar_html.py"])

if __name__ == "__main__":
    main()