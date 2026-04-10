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
    <meta name="description" content="Monitoramento em tempo real das principais ameaças de cibersegurança globais.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Outfit:wght@300;400;600;700;800&family=Playfair+Display:ital,wght@0,900;1,900&display=swap" rel="stylesheet">
    <style>
        /* ── CSS VARIABLES ── */
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

        /* ── ETAPA 1: GRAIN TEXTURE OVERLAY ── */
        /* Grão de filme sutil sobreposto a toda a interface para profundidade visual */
        body::after {{
            content: '';
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 9998;
            opacity: 0.04;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)' opacity='1'/%3E%3C/svg%3E");
            background-size: 200px 200px;
        }}

        body {{
            background: var(--bg);
            color: var(--text);
            font-family: 'Outfit', sans-serif;
            min-height: 100vh;
            overflow-x: hidden;
            cursor: none;
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

        /* ── ETAPA 3: CUSTOM CURSOR ── */
        /* Ponto preciso + anel com lag suave de 12% por frame */
        #cursor-dot {{
            position: fixed;
            width: 6px;
            height: 6px;
            background: var(--accent);
            border-radius: 50%;
            pointer-events: none;
            z-index: 9999;
            transform: translate(-50%, -50%);
            transition: opacity 0.3s;
        }}

        #cursor-ring {{
            position: fixed;
            width: 32px;
            height: 32px;
            border: 1px solid rgba(0, 229, 255, 0.45);
            border-radius: 50%;
            pointer-events: none;
            z-index: 9997;
            transform: translate(-50%, -50%);
            transition: width 0.3s ease, height 0.3s ease, border-color 0.3s ease;
        }}

        #cursor-ring.cursor-hover {{
            width: 56px;
            height: 56px;
            border-color: var(--accent);
        }}

        /* Oculta cursor customizado em dispositivos de toque */
        @media (hover: none) {{
            #cursor-dot, #cursor-ring {{ display: none; }}
            body {{ cursor: auto; }}
        }}

        /* ── ETAPA 4: LOADING SCREEN ── */
        /* Tela de inicialização com barra de progresso e contador */
        #loader {{
            position: fixed;
            inset: 0;
            background: var(--bg);
            z-index: 10000;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            gap: 18px;
            transition: opacity 0.7s ease, visibility 0.7s ease;
        }}

        #loader.done {{
            opacity: 0;
            visibility: hidden;
        }}

        .loader-label {{
            font-family: 'Space Mono', monospace;
            font-size: 11px;
            letter-spacing: 5px;
            color: var(--accent);
            text-transform: uppercase;
        }}

        .loader-bar {{
            width: 240px;
            height: 1px;
            background: var(--border);
            position: relative;
            overflow: hidden;
        }}

        .loader-bar-fill {{
            position: absolute;
            left: 0; top: 0; bottom: 0;
            width: 0%;
            background: var(--accent);
            transition: width 0.05s linear;
            box-shadow: 0 0 10px var(--accent);
        }}

        .loader-count {{
            font-family: 'Space Mono', monospace;
            font-size: 11px;
            color: var(--text-dim);
            letter-spacing: 2px;
        }}

        /* ── ETAPA 5: HEADER EDITORIAL ── */
        /* Tipografia com contraste serif itálico × sans bold inspirado no synchronized.studio */
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
            margin-bottom: 16px;
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

        /* H1 editorial: serif itálico + sans bold em contraste */
        h1 {{
            display: flex;
            align-items: baseline;
            gap: 14px;
            flex-wrap: wrap;
            line-height: 1;
        }}

        .h1-serif {{
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-weight: 900;
            font-size: clamp(44px, 5.5vw, 76px);
            letter-spacing: -2px;
            color: var(--text-bright);
        }}

        .h1-sans {{
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: clamp(44px, 5.5vw, 76px);
            letter-spacing: -3px;
            color: var(--accent);
        }}

        .header-sub {{
            font-size: 15px;
            color: var(--text-dim);
            margin-top: 12px;
            font-weight: 300;
        }}

        /* Linha diagonal decorativa: detalhe visual inspirado no synchronized.studio */
        .header-accent-line {{
            position: absolute;
            right: 240px;
            top: 28px;
            width: 1px;
            height: 70px;
            background: linear-gradient(to bottom, transparent, var(--accent), transparent);
            opacity: 0.5;
            transform: rotate(22deg);
            transform-origin: top center;
        }}

        .header-right {{
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 10px;
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
            50%        {{ opacity: 0.4; transform: scale(0.8); }}
        }}

        .header-count {{
            font-family: 'Space Mono', monospace;
            font-size: 11px;
            color: var(--text-dim);
            letter-spacing: 2px;
        }}

        .scroll-hint {{
            font-size: 11px;
            color: var(--text-dim);
            font-family: 'Space Mono', monospace;
        }}

        /* ── ETAPA 2: MARQUEE TICKER DUPLO ── */
        /* Dois tickers em direções opostas: termos cyber e fontes de notícia */
        .marquee-section {{
            position: relative;
            z-index: 10;
            overflow: hidden;
            border-top: 1px solid var(--border);
            border-bottom: 1px solid var(--border);
            background: rgba(13, 16, 24, 0.7);
            backdrop-filter: blur(4px);
        }}

        .marquee-track {{
            display: flex;
            width: max-content;
        }}

        .marquee-track-a {{
            animation: marquee-left 35s linear infinite;
        }}

        .marquee-track-b {{
            animation: marquee-right 28s linear infinite;
        }}

        @keyframes marquee-left {{
            from {{ transform: translateX(0); }}
            to   {{ transform: translateX(-50%); }}
        }}

        @keyframes marquee-right {{
            from {{ transform: translateX(-50%); }}
            to   {{ transform: translateX(0); }}
        }}

        .marquee-content {{
            white-space: nowrap;
            font-family: 'Space Mono', monospace;
            font-size: 10px;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: var(--text-dim);
            padding: 10px 0;
            user-select: none;
        }}

        .marquee-content .sep {{
            color: var(--accent);
            margin: 0 16px;
            opacity: 0.55;
        }}

        /* Divider original substituído pelo marquee */
        .divider {{ display: none; }}

        /* ── TRACK (horizontal scroll) ── */
        .track-wrap {{
            position: relative;
            z-index: 10;
            padding: 40px 60px 60px;
            overflow-x: scroll;
            overflow-y: hidden;
            cursor: none;
            user-select: none;
        }}

        .track-wrap:active {{ cursor: none; }}

        /* Scrollbar temática fina com glow */
        .track-wrap::-webkit-scrollbar {{ height: 2px; }}
        .track-wrap::-webkit-scrollbar-track {{ background: var(--bg2); }}
        .track-wrap::-webkit-scrollbar-thumb {{
            background: var(--accent);
            border-radius: 2px;
            box-shadow: 0 0 6px var(--accent);
        }}

        .track {{
            display: flex;
            gap: 24px;
            width: max-content;
        }}

        /* ── ETAPA 7: SCROLL REVEAL (IntersectionObserver) ── */
        /* Estado inicial: invisível e deslocado — JS adiciona .card-visible */
        .card-wrapper {{
            width: var(--card-w);
            height: var(--card-h);
            perspective: 1200px;
            cursor: none;
            flex-shrink: 0;
            opacity: 0;
            transform: translateY(30px) scale(0.97);
            transition: opacity 0.55s ease, transform 0.55s ease;
        }}

        .card-wrapper.card-visible {{
            opacity: 1;
            transform: translateY(0) scale(1);
        }}

        .card-inner {{
            width: 100%;
            height: 100%;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.7s cubic-bezier(0.4, 0, 0.2, 1);
            border-radius: 16px;
        }}

        /* !important garante precedência sobre o tilt magnético no flip */
        .card-wrapper.flipped .card-inner {{
            transform: rotateY(180deg) !important;
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

        /* ── ETAPA 6: HOVER GLOW SOFISTICADO ── */
        .card-wrapper:hover .card-front,
        .card-wrapper:hover .card-back {{
            border-color: rgba(0, 229, 255, 0.4);
            box-shadow:
                0 0 0 1px rgba(0, 229, 255, 0.06),
                0 8px 40px rgba(0, 229, 255, 0.09),
                0 0 80px rgba(0, 229, 255, 0.03);
        }}

        .card-front {{
            background: var(--surface);
            display: flex;
            flex-direction: column;
        }}

        /* ── ETAPA 6: SCAN LINE no hover ── */
        /* Linha de varredura que percorre o card de cima a baixo ao hover */
        .card-front::after {{
            content: '';
            position: absolute;
            left: 0;
            top: -100%;
            width: 100%;
            height: 35%;
            background: linear-gradient(
                to bottom,
                transparent,
                rgba(0, 229, 255, 0.04),
                transparent
            );
            pointer-events: none;
            transition: top 0.55s ease;
            z-index: 5;
        }}

        .card-wrapper:hover .card-front::after {{
            top: 120%;
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
            transform: scale(1.07);
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

        /* ── ETAPA 9: PONTO PULSANTE antes do nome da fonte ── */
        .card-source {{
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: var(--accent);
            font-family: 'Space Mono', monospace;
            display: flex;
            align-items: center;
            gap: 7px;
        }}

        .card-source::before {{
            content: '';
            display: inline-block;
            width: 5px;
            height: 5px;
            border-radius: 50%;
            background: currentColor;
            animation: pulse 2s infinite;
            flex-shrink: 0;
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

        /* Card back (verso após o flip) */
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

        /* ── ETAPA 9: FOOTER REFINADO ── */
        footer {{
            position: relative;
            z-index: 10;
            padding: 24px 60px;
            border-top: 1px solid var(--border);
            background: rgba(0, 0, 0, 0.35);
            backdrop-filter: blur(12px);
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            color: var(--text-dim);
            font-family: 'Space Mono', monospace;
        }}

        footer a {{ color: var(--accent); text-decoration: none; }}

        /* ── RESPONSIVIDADE ── */
        @media (max-width: 768px) {{
            header {{ padding: 40px 24px 30px; }}
            .header-accent-line {{ display: none; }}
            .track-wrap {{ padding: 20px 24px 40px; }}
            footer {{ padding: 20px 24px; flex-direction: column; gap: 8px; text-align: center; }}
            :root {{ --card-w: 300px; --card-h: 480px; }}
        }}
    </style>
</head>
<body>

<!-- Etapa 3: Elementos do cursor customizado -->
<div id="cursor-dot"></div>
<div id="cursor-ring"></div>

<!-- Etapa 4: Loading screen de inicialização -->
<div id="loader">
    <div class="loader-label">Initializing Threat Feed</div>
    <div class="loader-bar">
        <div class="loader-bar-fill" id="loader-progress"></div>
    </div>
    <div class="loader-count" id="loader-count">0%</div>
</div>

<!-- Etapa 5: Header editorial com contraste tipográfico -->
<header>
    <div class="header-left">
        <div class="header-tag">Cybersecurity Intelligence</div>
        <h1>
            <span class="h1-serif">Threat</span>
            <span class="h1-sans">Intel</span>
        </h1>
        <p class="header-sub">Monitoramento em tempo real das principais ameaças globais</p>
    </div>
    <div class="header-right">
        <div class="live-badge">
            <div class="live-dot"></div>
            Live Feed
        </div>
        <div class="header-count" id="news-count">20 artigos</div>
        <div class="scroll-hint">← arraste para navegar →</div>
    </div>
    <!-- Linha diagonal decorativa inspirada no synchronized.studio -->
    <div class="header-accent-line"></div>
</header>

<!-- Divider legado (oculto, substituído pelo marquee) -->
<div class="divider"></div>

<!-- Etapa 2: Marquee ticker duplo — termos cyber (→) e fontes (←) -->
<div class="marquee-section">
    <div class="marquee-track marquee-track-a">
        <div class="marquee-content">THREAT INTEL<span class="sep">·</span>CVE MONITOR<span class="sep">·</span>RANSOMWARE<span class="sep">·</span>APT<span class="sep">·</span>ZERO-DAY<span class="sep">·</span>PHISHING<span class="sep">·</span>MALWARE<span class="sep">·</span>DATA BREACH<span class="sep">·</span>VULNERABILITY<span class="sep">·</span>EXPLOIT<span class="sep">·</span>INCIDENT RESPONSE<span class="sep">·</span>THREAT ACTOR<span class="sep">·</span>IOC<span class="sep">·</span>DARK WEB<span class="sep">·</span>SUPPLY CHAIN<span class="sep">·</span></div>
        <div class="marquee-content" aria-hidden="true">THREAT INTEL<span class="sep">·</span>CVE MONITOR<span class="sep">·</span>RANSOMWARE<span class="sep">·</span>APT<span class="sep">·</span>ZERO-DAY<span class="sep">·</span>PHISHING<span class="sep">·</span>MALWARE<span class="sep">·</span>DATA BREACH<span class="sep">·</span>VULNERABILITY<span class="sep">·</span>EXPLOIT<span class="sep">·</span>INCIDENT RESPONSE<span class="sep">·</span>THREAT ACTOR<span class="sep">·</span>IOC<span class="sep">·</span>DARK WEB<span class="sep">·</span>SUPPLY CHAIN<span class="sep">·</span></div>
    </div>
    <div class="marquee-track marquee-track-b">
        <div class="marquee-content">BLEEPINGCOMPUTER<span class="sep">·</span>THE HACKER NEWS<span class="sep">·</span>HACKREAD<span class="sep">·</span>INFOSECURITY MAGAZINE<span class="sep">·</span>SECURITYWEEK<span class="sep">·</span>HELP NET SECURITY<span class="sep">·</span>EFF<span class="sep">·</span>KREBS ON SECURITY<span class="sep">·</span>WIRED<span class="sep">·</span>DARK READING<span class="sep">·</span>THREATPOST<span class="sep">·</span>CYBERSCOOP<span class="sep">·</span></div>
        <div class="marquee-content" aria-hidden="true">BLEEPINGCOMPUTER<span class="sep">·</span>THE HACKER NEWS<span class="sep">·</span>HACKREAD<span class="sep">·</span>INFOSECURITY MAGAZINE<span class="sep">·</span>SECURITYWEEK<span class="sep">·</span>HELP NET SECURITY<span class="sep">·</span>EFF<span class="sep">·</span>KREBS ON SECURITY<span class="sep">·</span>WIRED<span class="sep">·</span>DARK READING<span class="sep">·</span>THREATPOST<span class="sep">·</span>CYBERSCOOP<span class="sep">·</span></div>
    </div>
</div>

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
    // ── ETAPA 4: LOADING SCREEN ──
    // Progresso pseudo-aleatório que completa em ~1 segundo
    let pct = 0;
    const prog = document.getElementById('loader-progress');
    const cnt  = document.getElementById('loader-count');
    const iv = setInterval(() => {{
        pct += Math.random() * 15 + 4;
        if (pct >= 100) {{
            pct = 100;
            clearInterval(iv);
            setTimeout(() => document.getElementById('loader').classList.add('done'), 280);
        }}
        prog.style.width = Math.min(pct, 100) + '%';
        cnt.textContent  = Math.floor(Math.min(pct, 100)) + '%';
    }}, 55);

    // ── ETAPA 3: CUSTOM CURSOR ──
    // Ponto segue o mouse com precisão; anel segue com lag linear de 12% por frame
    const dot  = document.getElementById('cursor-dot');
    const ring = document.getElementById('cursor-ring');
    let mx = window.innerWidth / 2, my = window.innerHeight / 2;
    let rx = mx, ry = my;

    document.addEventListener('mousemove', e => {{
        mx = e.clientX;
        my = e.clientY;
        dot.style.left = mx + 'px';
        dot.style.top  = my + 'px';
    }});

    function animateCursor() {{
        rx += (mx - rx) * 0.12;
        ry += (my - ry) * 0.12;
        ring.style.left = rx + 'px';
        ring.style.top  = ry + 'px';
        requestAnimationFrame(animateCursor);
    }}
    animateCursor();

    // Expande o anel ao entrar nos cards
    document.querySelectorAll('.card-wrapper').forEach(c => {{
        c.addEventListener('mouseenter', () => ring.classList.add('cursor-hover'));
        c.addEventListener('mouseleave', () => ring.classList.remove('cursor-hover'));
    }});

    // ── FLIP DO CARD (lógica original preservada) ──
    function flipCard(el) {{
        el.classList.toggle('flipped');
    }}

    // ── DRAG TO SCROLL (lógica original preservada) ──
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
    }});

    wrap.addEventListener('mousemove', (e) => {{
        if (!isDragging) return;
        const dx = e.pageX - startX;
        if (Math.abs(dx) > 5) moved = true;
        wrap.scrollLeft = scrollLeft - dx;
    }});

    wrap.addEventListener('mouseup', () => {{ isDragging = false; }});
    wrap.addEventListener('mouseleave', () => {{ isDragging = false; }});

    wrap.addEventListener('click', (e) => {{
        if (moved) e.stopPropagation();
    }}, true);

    // Suporte a touch (lógica original preservada)
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

    // ── ETAPA 7: SCROLL REVEAL COM IntersectionObserver ──
    // Substitui o setTimeout stagger: anima somente ao entrar no viewport
    const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                entry.target.classList.add('card-visible');
                observer.unobserve(entry.target); // anima uma única vez
            }}
        }});
    }}, {{
        threshold: 0.08,
        rootMargin: '0px 60px'  // margem lateral para scroll horizontal
    }});

    document.querySelectorAll('.card-wrapper').forEach((card, i) => {{
        // Delay escalonado baseado no índice do card
        card.style.transitionDelay = `${{i * 45}}ms`;
        observer.observe(card);
    }});

    // ── ETAPA 8: TILT MAGNÉTICO 3D ──
    // Card inclina suavemente seguindo o mouse — desativado quando virado
    document.querySelectorAll('.card-wrapper').forEach(card => {{
        const inner = card.querySelector('.card-inner');

        card.addEventListener('mousemove', e => {{
            if (card.classList.contains('flipped')) return;
            const r = card.getBoundingClientRect();
            const x = (e.clientX - r.left  - r.width  / 2) / (r.width  / 2);
            const y = (e.clientY - r.top   - r.height / 2) / (r.height / 2);
            inner.style.transform = `rotateX(${{-y * 5}}deg) rotateY(${{x * 5}}deg) translateY(-6px)`;
        }});

        card.addEventListener('mouseleave', () => {{
            // Reseta o tilt ao sair — apenas se não estiver virado
            if (!card.classList.contains('flipped')) {{
                inner.style.transform = '';
            }}
        }});
    }});
</script>

</body>
</html>"""

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("[OK] index.html gerado com sucesso!")


if __name__ == "__main__":
    gerar_html()
