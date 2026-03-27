import json

with open("noticias.json", "r", encoding="utf-8") as f:
    noticias = json.load(f)

cards = ""
for i, n in enumerate(noticias[:20], 1):
    data = n.get("data", "")[:10]
    titulo = n.get("titulo", "Sem título")
    fonte = n.get("fonte", "Desconhecido")
    autor = n.get("autor", "Desconhecido")
    resumo = n.get("resumo", "Sem resumo")
    if resumo:
        resumo = resumo[:150] + "..."
    url = n.get("url", "#")

    cards += f"""
    <div class="card">
        <div class="card-number">#{i}</div>
        <h2>{titulo}</h2>
        <div class="card-meta">
            <span class="badge fonte">{fonte}</span>
            <span class="badge data">{data}</span>
            <span class="badge">{autor}</span>
        </div>
        <p class="resumo">{resumo}</p>
        <a href="{url}" target="_blank">Ler artigo completo →</a>
    </div>
    """

html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Security News Aggregator</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', sans-serif; background: #0d1117; color: #e6edf3; padding: 2rem; }}
        header {{ text-align: center; margin-bottom: 2rem; padding: 2rem; border-bottom: 1px solid #30363d; }}
        header h1 {{ font-size: 2rem; color: #58a6ff; margin-bottom: 0.5rem; }}
        header p {{ color: #8b949e; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 1.5rem; max-width: 1200px; margin: 0 auto; }}
        .card {{ background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 1.5rem; transition: border-color 0.2s; }}
        .card:hover {{ border-color: #58a6ff; }}
        .card-number {{ font-size: 0.75rem; color: #58a6ff; font-weight: 600; margin-bottom: 0.5rem; }}
        .card h2 {{ font-size: 1rem; margin-bottom: 0.75rem; line-height: 1.5; }}
        .card-meta {{ display: flex; gap: 0.5rem; margin-bottom: 0.75rem; flex-wrap: wrap; }}
        .badge {{ font-size: 0.75rem; padding: 2px 10px; border-radius: 99px; background: #21262d; color: #8b949e; border: 1px solid #30363d; }}
        .badge.fonte {{ color: #58a6ff; border-color: #58a6ff55; }}
        .badge.data {{ color: #3fb950; border-color: #3fb95055; }}
        .resumo {{ font-size: 0.85rem; color: #8b949e; line-height: 1.6; margin-bottom: 1rem; }}
        .card a {{ font-size: 0.8rem; color: #58a6ff; text-decoration: none; }}
        .card a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
<header>
    <h1>🛡️ Security News Aggregator</h1>
    <p>Últimas notícias de cibersegurança</p>
</header>
<div class="grid">
{cards}
</div>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ index.html gerado com sucesso!")