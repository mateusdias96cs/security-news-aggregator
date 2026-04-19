from fetcher import buscar_noticias, buscar_noticias_br
from processor import processar_noticias
from storage import salvar_json, ler_json, atualizar_historico
from display import mostrar_top10
import subprocess

def main():
    print("🔍 Buscando notícias internacionais...")
    artigos = buscar_noticias()

    print("🇧🇷 Buscando notícias brasileiras...")
    artigos_br = buscar_noticias_br()

    if not artigos:
        print("Nenhum artigo encontrado.")
        return

    print("⚙️  Processando notícias...")
    noticias = processar_noticias(artigos)
    salvar_json(noticias)
    atualizar_historico(noticias)

    if artigos_br:
        noticias_br = processar_noticias(artigos_br)
        salvar_json(noticias_br, "noticias_br.json")
        print(f"✅ {len(noticias_br)} notícias BR salvas")

    mostrar_top10(noticias)
    subprocess.run(["python3", "gerar_html.py"])

if __name__ == "__main__":
    main()