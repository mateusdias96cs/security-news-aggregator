import json
import os


# ── GRADIENTES POR FONTE ──
SOURCE_THEMES = {
    "bleepingcomputer": {
        "gradient": "linear-gradient(135deg, #0d1f3c 0%, #1a3a6b 50%, #0066cc 100%)",
        "color": "#4da6ff",
        "icon": "🔵",
        "label": "BC"
    },
    "the hacker news": {
        "gradient": "linear-gradient(135deg, #1a0a00 0%, #3d1a00 50%, #cc4400 100%)",
        "color": "#ff6622",
        "icon": "🔴",
        "label": "THN"
    },
    "hackread": {
        "gradient": "linear-gradient(135deg, #0a001a 0%, #1a003d 50%, #5500cc 100%)",
        "color": "#aa44ff",
        "icon": "🟣",
        "label": "HR"
    },
    "infosecurity magazine": {
        "gradient": "linear-gradient(135deg, #001a0d 0%, #003d1a 50%, #007a35 100%)",
        "color": "#00cc66",
        "icon": "🟢",
        "label": "INFO"
    },
    "securityweek": {
        "gradient": "linear-gradient(135deg, #1a1a00 0%, #3d3d00 50%, #999900 100%)",
        "color": "#cccc00",
        "icon": "🟡",
        "label": "SW"
    },
    "default": {
        "gradient": "linear-gradient(135deg, #0d1520 0%, #1a2a40 50%, #00e5ff22 100%)",
        "color": "#00e5ff",
        "icon": "🛡️",
        "label": "SEC"
    }
}


def get_source_theme(fonte):
    key = fonte.lower().strip()
    for source_key, theme in SOURCE_THEMES.items():
        if source_key in key or key in source_key:
            return theme
    return SOURCE_THEMES["default"]


def gerar_thumbnail_svg(fonte, titulo):
    theme = get_source_theme(fonte)
    titulo_curto = titulo[:40] + "..." if len(titulo) > 40 else titulo
    titulo_curto = titulo_curto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    label = theme["label"]
    color = theme["color"]

    svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='380' height='200' viewBox='0 0 380 200'>
  <defs>
    <linearGradient id='g' x1='0%' y1='0%' x2='100%' y2='100%'>
      <stop offset='0%' style='stop-color:#0d1520'/>
      <stop offset='50%' style='stop-color:#1a2a40'/>
      <stop offset='100%' style='stop-color:#0d1f30'/>
    </linearGradient>
    <pattern id='grid' width='20' height='20' patternUnits='userSpaceOnUse'>
      <path d='M 20 0 L 0 0 0 20' fill='none' stroke='{color}' stroke-width='0.3' opacity='0.15'/>
    </pattern>
  </defs>
  <rect width='380' height='200' fill='url(#g)'/>
  <rect width='380' height='200' fill='url(#grid)'/>
  <circle cx='320' cy='40' r='60' fill='{color}' opacity='0.04'/>
  <circle cx='60' cy='160' r='40' fill='{color}' opacity='0.06'/>
  <text x='24' y='44' font-family='monospace' font-size='11' font-weight='700' fill='{color}' opacity='0.9' letter-spacing='2'>{label}</text>
  <line x1='24' y1='52' x2='100' y2='52' stroke='{color}' stroke-width='1' opacity='0.4'/>
  <text x='24' y='100' font-family='sans-serif' font-size='13' font-weight='600' fill='#c8d0e0' opacity='0.85'>
    <tspan x='24' dy='0'>{titulo_curto[:35]}</tspan>
    <tspan x='24' dy='18'>{titulo_curto[35:70] if len(titulo_curto) > 35 else ''}</tspan>
  </text>
  <text x='24' y='175' font-family='monospace' font-size='10' fill='{color}' opacity='0.5'>{fonte[:30]}</text>
  <rect x='0' y='190' width='380' height='2' fill='{color}' opacity='0.3'/>
</svg>"""

    import base64
    svg_b64 = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    return f"data:image/svg+xml;base64,{svg_b64}"


def gerar_html(noticias=None):
    if noticias is None:
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "noticias.json")
        with open(json_path, "r", encoding="utf-8") as f:
            noticias = json.load(f)

    cards = ""
    for i, n in enumerate(noticias[:20], 1):
        data = n.get("data", "")[:10]
        titulo = n.get("titulo", "Sem título")
        fonte = n.get("fonte", "Desconhecido")
        resumo = n.get("resumo", "Sem resumo") or "Sem resumo"
        resumo = resumo[:200] + "..." if len(resumo) > 200 else resumo
        url = n.get("url", "#")
        imagem = n.get("imagem", "") or n.get("image", "")
        autor = n.get("autor", "") or ""

        # Usa imagem real ou gera thumbnail SVG por fonte
        if imagem and imagem.startswith("http"):
            thumb = imagem
            use_svg = False
        else:
            thumb = gerar_thumbnail_svg(fonte, titulo)
            use_svg = True

        fallback = gerar_thumbnail_svg(fonte, titulo)
        onerror = "" if use_svg else f"onerror=\"this.src='{fallback}'\""
        img_tag = f'<img src="{thumb}" alt="{titulo}" loading="lazy" {onerror}>'

        cards += f"""
        <div class="card-wrapper" onclick="flipCard(this)">
            <div class="card-inner">
                <div class="card-front">
                    <div class="card-num">#{i:02d}</div>
                    <div class="card-img-wrap">
                        {img_tag}
                        <div class="card-img-overlay"></div>
                    </div>
                    <div class="card-front-content">
                        <span class="card-source">{fonte}</span>
                        <h2 class="card-title">{titulo}</h2>
                        <div class="card-meta">
                            <span class="card-date">{data}</span>
                            {'<span class="card-author">' + autor[:30] + '</span>' if autor else ''}
                        </div>
                        <div class="card-hint">Clique para ler o resumo →</div>
                    </div>
                </div>
                <div class="card-back">
                    <div class="card-back-source">{fonte}</div>
                    <h3 class="card-back-title">{titulo}</h3>
                    <p class="card-back-resumo">{resumo}</p>
                    <a href="{url}" target="_blank" rel="noopener noreferrer" class="card-back-link" onclick="event.stopPropagation()">
                        Ler artigo completo →
                    </a>
                    <div class="card-back-hint">Clique para voltar</div>
                </div>
            </div>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security News Aggregator</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Outfit:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #080a0f;
            --bg2: #0d1018;
            --surface: #111520;
            --border: #1e2535;
            --accent: #00e5ff;
            --accent2: #7c3aed;
            --green: #00ff9d;
            --text: #c8d0e0;
            --text-dim: #5a6480;
            --text-bright: #f0f4ff;
            --card-w: 380px;
            --card-h: 520px;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            background: var(--bg);
            color: var(--text);
            font-family: 'Outfit', sans-serif;
            min-height: 100vh;
            overflow-x: hidden;
        }}

        body::before {{
            content: '';
            position: fixed;
            inset: 0;
            background:
                radial-gradient(ellipse 60% 40% at 20% 20%, rgba(0,229,255,0.04) 0%, transparent 60%),
                radial-gradient(ellipse 50% 50% at 80% 80%, rgba(124,58,237,0.04) 0%, transparent 60%);
            pointer-events: none;
            z-index: 0;
        }}

        header {{
            position: relative;
            z-index: 10;
            padding: 60px 60px 40px;
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 20px;
        }}

        .header-tag {{
            font-family: 'Space Mono', monospace;
            font-size: 11px;
            color: var(--accent);
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .header-tag::before {{
            content: '';
            display: block;
            width: 24px;
            height: 1px;
            background: var(--accent);
        }}

        h1 {{
            font-size: clamp(36px, 5vw, 64px);
            font-weight: 800;
            color: var(--text-bright);
            letter-spacing: -2px;
            line-height: 1;
        }}

        h1 span {{ color: var(--accent); }}

        .header-sub {{
            font-size: 15px;
            color: var(--text-dim);
            margin-top: 10px;
            font-weight: 300;
        }}

        .header-right {{
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 8px;
        }}

        .live-badge {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 6px 14px;
            background: rgba(0,255,157,0.08);
            border: 1px solid rgba(0,255,157,0.2);
            border-radius: 20px;
            font-size: 12px;
            color: var(--green);
            font-family: 'Space Mono', monospace;
        }}

        .live-dot {{
            width: 6px;
            height: 6px;
            background: var(--green);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.4; transform: scale(0.8); }}
        }}

        .scroll-hint {{
            font-size: 11px;
            color: var(--text-dim);
            font-family: 'Space Mono', monospace;
        }}

        .divider {{
            position: relative;
            z-index: 10;
            margin: 0 60px 40px;
            height: 1px;
            background: linear-gradient(90deg, var(--accent), var(--accent2), transparent);
            opacity: 0.3;
        }}

        .track-wrap {{
            position: relative;
            z-index: 10;
            padding: 20px 60px 60px;
            overflow-x: scroll;
            overflow-y: hidden;
            cursor: grab;
            user-select: none;
        }}

        .track-wrap:active {{ cursor: grabbing; }}

        .track-wrap::-webkit-scrollbar {{ height: 4px; }}
        .track-wrap::-webkit-scrollbar-track {{ background: var(--bg2); }}
        .track-wrap::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 2px; }}

        .track {{
            display: flex;
            gap: 24px;
            width: max-content;
        }}

        .card-wrapper {{
            width: var(--card-w);
            height: var(--card-h);
            perspective: 1200px;
            cursor: pointer;
            flex-shrink: 0;
        }}

        .card-inner {{
            width: 100%;
            height: 100%;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.7s cubic-bezier(0.4, 0, 0.2, 1);
            border-radius: 16px;
        }}

        .card-wrapper.flipped .card-inner {{
            transform: rotateY(180deg);
        }}

        .card-front,
        .card-back {{
            position: absolute;
            inset: 0;
            backface-visibility: hidden;
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid var(--border);
            transition: border-color 0.3s, box-shadow 0.3s;
        }}

        .card-wrapper:hover .card-front,
        .card-wrapper:hover .card-back {{
            border-color: rgba(0,229,255,0.25);
            box-shadow: 0 0 30px rgba(0,229,255,0.06);
        }}

        .card-front {{
            background: var(--surface);
            display: flex;
            flex-direction: column;
        }}

        .card-num {{
            position: absolute;
            top: 16px;
            left: 16px;
            z-index: 3;
            font-family: 'Space Mono', monospace;
            font-size: 11px;
            color: var(--accent);
            background: rgba(8,10,15,0.8);
            padding: 4px 8px;
            border-radius: 4px;
            border: 1px solid rgba(0,229,255,0.2);
        }}

        .card-img-wrap {{
            position: relative;
            height: 200px;
            overflow: hidden;
            flex-shrink: 0;
        }}

        .card-img-wrap img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.5s ease;
        }}

        .card-wrapper:hover .card-img-wrap img {{
            transform: scale(1.05);
        }}

        .card-img-overlay {{
            position: absolute;
            inset: 0;
            background: linear-gradient(to bottom, transparent 40%, var(--surface) 100%);
        }}

        .card-front-content {{
            padding: 20px 22px 22px;
            display: flex;
            flex-direction: column;
            flex: 1;
            gap: 10px;
        }}

        .card-source {{
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: var(--accent);
            font-family: 'Space Mono', monospace;
        }}

        .card-title {{
            font-size: 16px;
            font-weight: 700;
            color: var(--text-bright);
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 4;
            -webkit-box-orient: vertical;
            overflow: hidden;
            flex: 1;
        }}

        .card-meta {{
            display: flex;
            gap: 10px;
            align-items: center;
            flex-wrap: wrap;
        }}

        .card-date {{
            font-size: 11px;
            color: var(--text-dim);
            font-family: 'Space Mono', monospace;
        }}

        .card-author {{
            font-size: 11px;
            color: var(--text-dim);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 160px;
        }}

        .card-hint {{
            font-size: 11px;
            color: var(--accent);
            opacity: 0;
            transition: opacity 0.3s;
            font-family: 'Space Mono', monospace;
        }}

        .card-wrapper:hover .card-hint {{ opacity: 1; }}

        .card-back {{
            background: linear-gradient(135deg, #0d1018 0%, #111830 100%);
            transform: rotateY(180deg);
            display: flex;
            flex-direction: column;
            padding: 30px 26px;
            gap: 16px;
            border-color: rgba(0,229,255,0.2);
        }}

        .card-back-source {{
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: var(--accent);
            font-family: 'Space Mono', monospace;
        }}

        .card-back-title {{
            font-size: 15px;
            font-weight: 700;
            color: var(--text-bright);
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}

        .card-back-resumo {{
            font-size: 13px;
            color: var(--text);
            line-height: 1.7;
            flex: 1;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 8;
            -webkit-box-orient: vertical;
        }}

        .card-back-link {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 18px;
            background: var(--accent);
            color: var(--bg);
            font-weight: 700;
            font-size: 12px;
            border-radius: 8px;
            text-decoration: none;
            transition: all 0.2s;
            width: fit-content;
        }}

        .card-back-link:hover {{
            background: #00b8cc;
            transform: translateY(-1px);
        }}

        .card-back-hint {{
            font-size: 10px;
            color: var(--text-dim);
            font-family: 'Space Mono', monospace;
            text-align: center;
        }}

        footer {{
            position: relative;
            z-index: 10;
            padding: 24px 60px;
            border-top: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            color: var(--text-dim);
            font-family: 'Space Mono', monospace;
        }}

        footer a {{ color: var(--accent); text-decoration: none; }}

        @media (max-width: 768px) {{
            header {{ padding: 40px 24px 30px; }}
            .divider {{ margin: 0 24px 30px; }}
            .track-wrap {{ padding: 10px 24px 40px; }}
            footer {{ padding: 20px 24px; flex-direction: column; gap: 8px; }}
            :root {{ --card-w: 300px; --card-h: 480px; }}
        }}
    </style>
</head>
<body>

<header>
    <div class="header-left">
        <div class="header-tag">Cybersecurity Intelligence</div>
        <h1>Security <span>News</span></h1>
        <p class="header-sub">Monitoramento em tempo real das principais ameaças globais</p>
    </div>
    <div class="header-right">
        <div class="live-badge">
            <div class="live-dot"></div>
            Atualizado automaticamente
        </div>
        <div class="scroll-hint">← arraste para navegar →</div>
    </div>
</header>

<div class="divider"></div>

<div class="track-wrap" id="trackWrap">
    <div class="track" id="track">
        {cards}
    </div>
</div>

<footer>
    <span>Security News Aggregator — Mateus Camara Dias</span>
    <span>Dados via NewsAPI · Atualização diária automática</span>
</footer>

<script>
    function flipCard(el) {{
        el.classList.toggle('flipped');
    }}

    const wrap = document.getElementById('trackWrap');
    let isDragging = false;
    let startX = 0;
    let scrollLeft = 0;
    let moved = false;

    wrap.addEventListener('mousedown', (e) => {{
        isDragging = true;
        moved = false;
        startX = e.pageX;
        scrollLeft = wrap.scrollLeft;
        wrap.style.cursor = 'grabbing';
    }});

    wrap.addEventListener('mousemove', (e) => {{
        if (!isDragging) return;
        const dx = e.pageX - startX;
        if (Math.abs(dx) > 5) moved = true;
        wrap.scrollLeft = scrollLeft - dx;
    }});

    wrap.addEventListener('mouseup', () => {{
        isDragging = false;
        wrap.style.cursor = 'grab';
    }});

    wrap.addEventListener('mouseleave', () => {{
        isDragging = false;
        wrap.style.cursor = 'grab';
    }});

    wrap.addEventListener('click', (e) => {{
        if (moved) e.stopPropagation();
    }}, true);

    let touchStartX = 0;
    let touchScrollLeft = 0;

    wrap.addEventListener('touchstart', (e) => {{
        touchStartX = e.touches[0].pageX;
        touchScrollLeft = wrap.scrollLeft;
    }}, {{ passive: true }});

    wrap.addEventListener('touchmove', (e) => {{
        const dx = e.touches[0].pageX - touchStartX;
        wrap.scrollLeft = touchScrollLeft - dx;
    }}, {{ passive: true }});

    const cards = document.querySelectorAll('.card-wrapper');
    cards.forEach((card, i) => {{
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        setTimeout(() => {{
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }}, 100 + i * 60);
    }});
</script>

</body>
</html>"""

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ index.html gerado com sucesso!")


if __name__ == "__main__":
    gerar_html()
