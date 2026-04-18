import json
import os
import base64

TAG_MAP = {
    'ransomware': 'RANSOMWARE',
    'phishing': 'PHISHING',
    'zero-day': 'ZERO-DAY',
    'zero day': 'ZERO-DAY',
    '0-day': 'ZERO-DAY',
    'apt': 'APT',
    'advanced persistent': 'APT',
    'malware': 'MALWARE',
    'trojan': 'MALWARE',
    'backdoor': 'MALWARE',
    'vulnerabilit': 'VULNERABILIDADE',
    'cve': 'VULNERABILIDADE',
    'patch': 'VULNERABILIDADE',
    'exploit': 'VULNERABILIDADE',
    'breach': 'INCIDENTE',
    'leak': 'INCIDENTE',
    'attack': 'INCIDENTE',
    'incident': 'INCIDENTE',
    'ai': 'IA & SEGURANÇA',
    'artificial intelligence': 'IA & SEGURANÇA',
    'llm': 'IA & SEGURANÇA',
    'government': 'GOVERNO',
    'cisa': 'GOVERNO',
    'nsa': 'GOVERNO',
    'federal': 'GOVERNO',
    'critical infrastructure': 'INFRAESTRUTURA CRÍTICA',
    'industrial': 'INFRAESTRUTURA CRÍTICA',
    'ics': 'INFRAESTRUTURA CRÍTICA',
    'scada': 'INFRAESTRUTURA CRÍTICA',
}

def get_tags(title, resumo):
    text = (title + ' ' + resumo).lower()
    found = set()
    for keyword, tag in TAG_MAP.items():
        if keyword in text:
            found.add(tag)
    return list(found) if found else ['INCIDENTE']

def get_source_label(fonte):
    labels = {
        "bleepingcomputer": "BC",
        "the hacker news": "THN",
        "hackread": "HR",
        "infosecurity magazine": "INFO",
        "securityweek": "SW"
    }
    key = fonte.lower().strip()
    for k, v in labels.items():
        if k in key:
            return v
    return "SEC"

def gerar_thumbnail_svg(fonte, titulo):
    label = get_source_label(fonte)
    titulo_curto = titulo[:50] + "..." if len(titulo) > 50 else titulo
    titulo_curto = titulo_curto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    
    color = "#c8f135"  # Accent lime
    bg1 = "#111111"    # Background surface
    bg2 = "#0a0a0a"    # Dark background
    txt = "#f5f0e8"    # Title color
    
    svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='800' height='1000' viewBox='0 0 800 1000'>
  <defs>
    <linearGradient id='g' x1='0%' y1='0%' x2='100%' y2='100%'>
      <stop offset='0%' style='stop-color:{bg1}'/>
      <stop offset='100%' style='stop-color:{bg2}'/>
    </linearGradient>
    <pattern id='grid' width='40' height='40' patternUnits='userSpaceOnUse'>
      <path d='M 40 0 L 0 0 0 40' fill='none' stroke='{color}' stroke-width='0.5' opacity='0.08'/>
    </pattern>
  </defs>
  <rect width='800' height='1000' fill='url(#g)'/>
  <rect width='800' height='1000' fill='url(#grid)'/>
  
  <text x='50' y='80' font-family='monospace' font-size='22' font-weight='700' fill='{color}' opacity='0.9' letter-spacing='4'>{label}</text>
  <line x1='50' y1='100' x2='200' y2='100' stroke='{color}' stroke-width='2' opacity='0.4'/>
  
  <text x='50' y='450' font-family='sans-serif' font-size='38' font-weight='600' fill='{txt}' opacity='0.9'>
    <tspan x='50' dy='0'>{titulo_curto[:35]}</tspan>
    <tspan x='50' dy='50'>{titulo_curto[35:70] if len(titulo_curto) > 35 else ''}</tspan>
  </text>
  
  <rect x='0' y='980' width='800' height='20' fill='{color}' opacity='0.6'/>
</svg>"""

    svg_b64 = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    return f"data:image/svg+xml;base64,{svg_b64}"

def gerar_html(noticias=None):
    if noticias is None:
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "noticias.json")
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                noticias = json.load(f)
        except:
            noticias = []

    from storage import ler_json
    historico = ler_json("historico.json")
    noticias_br = ler_json("noticias_br.json")

    urls_hoje = {n.get("url") for n in noticias}
    noticias_semana = [
        n for n in historico
        if n.get("url") not in urls_hoje
    ]

    cards = ""
    for i, n in enumerate(noticias[:20], 1):
        data = n.get("data", "")[:10]
        titulo = n.get("titulo", "Sem título")
        fonte = n.get("fonte", "Desconhecido")
        resumo = n.get("resumo", "Sem resumo") or "Sem resumo"
        resumo = resumo[:250] + "..." if len(resumo) > 250 else resumo
        url = n.get("url", "#")
        imagem = n.get("imagem", "") or n.get("image", "")

        if imagem and imagem.startswith("http"):
            thumb = imagem
            use_svg = False
        else:
            thumb = gerar_thumbnail_svg(fonte, titulo)
            use_svg = True

        fallback = gerar_thumbnail_svg(fonte, titulo)
        onerror = "" if use_svg else f"onerror=\"this.src='{fallback}'\""

        tags_json = json.dumps(get_tags(titulo, resumo))

        # Formatação do número editorial (#01, #02, etc.)
        num_str = f"#{i:02d}"

        cards += f"""
        <article class="feed-card" data-index="{i}" data-tags='{tags_json}'>
            <div class="card-inner">
                <div class="card-left">
                    <div class="card-img-wrap">
                        <img src="{thumb}" alt="{titulo}" loading="lazy" class="reveal-img" {onerror}>
                        <div class="img-overlay"></div>
                    </div>
                </div>
                
                <div class="card-right">
                    <div class="card-meta">
                        <span class="card-num">{num_str}</span>
                    </div>
                    
                    <div class="meta-row reveal-txt">
                        <span class="live-dot"></span>
                        <span class="card-source">{fonte}</span>
                    </div>
                    
                    <h2 class="card-title split-text">{titulo}</h2>
                    
                    <div class="card-submeta reveal-txt">
                        <span class="card-date">{data}</span>
                    </div>
                    
                    <p class="card-resumo reveal-txt">{resumo}</p>
                    
                    <div class="btn-wrap reveal-txt">
                        <a href="{url}" target="_blank" rel="noopener noreferrer" class="read-btn">Ler artigo &rarr;</a>
                    </div>
                </div>
            </div>
        </article>"""

    br_html = ""
    if noticias_br:
        br_cards = ""
        for i, n in enumerate(noticias_br[:10], 1):
            data = n.get("data", "")[:10]
            titulo = n.get("titulo", "Sem título")
            fonte = n.get("fonte", "Desconhecido")
            resumo = n.get("resumo", "Sem resumo") or "Sem resumo"
            resumo = resumo[:250] + "..." if len(resumo) > 250 else resumo
            url = n.get("url", "#")
            imagem = n.get("imagem", "") or n.get("image", "")

            if imagem and imagem.startswith("http"):
                thumb = imagem
                use_svg = False
            else:
                thumb = gerar_thumbnail_svg(fonte, titulo)
                use_svg = True

            fallback = gerar_thumbnail_svg(fonte, titulo)
            onerror = "" if use_svg else f"onerror=\"this.src='{fallback}'\""

            tags_json = json.dumps(get_tags(titulo, resumo))
            num_str = f"BR#{i:02d}"

            br_cards += f"""
            <article class="feed-card" data-index="br-{i}" data-tags='{tags_json}'>
                <div class="card-inner">
                    <div class="card-left">
                        <div class="card-img-wrap">
                            <img src="{thumb}" alt="{titulo}" loading="lazy" class="reveal-img" {onerror}>
                            <div class="img-overlay"></div>
                        </div>
                    </div>
                    
                    <div class="card-right">
                        <div class="card-meta">
                            <span class="card-num">{num_str}</span>
                        </div>
                        
                        <div class="meta-row reveal-txt">
                            <span class="live-dot"></span>
                            <span class="card-source">{fonte}</span>
                        </div>
                        
                        <h2 class="card-title split-text">{titulo}</h2>
                        
                        <div class="card-submeta reveal-txt">
                            <span class="card-date">{data}</span>
                        </div>
                        
                        <p class="card-resumo reveal-txt">{resumo}</p>
                        
                        <div class="btn-wrap reveal-txt">
                            <a href="{url}" target="_blank" rel="noopener noreferrer" class="read-btn">Ler artigo &rarr;</a>
                        </div>
                    </div>
                </div>
            </article>"""
        
        br_html = f'''
<section class="br-section">
    <div class="br-header">
        <div class="br-flag">🇧🇷</div>
        <div>
            <span class="br-label">BRASIL</span>
            <h2 class="br-title">
                <span class="br-serif">Segurança</span>
                <span class="br-sans">Digital BR</span>
            </h2>
            <p class="br-sub">
                Notícias de cibersegurança em português, 
                das principais fontes brasileiras
            </p>
        </div>
    </div>
    <div class="feed">
{br_cards}
    </div>
</section>
'''
    else:
        br_html = '''
<section class="br-section">
    <div class="br-header">
        <div class="br-flag">🇧🇷</div>
        <div>
            <span class="br-label">BRASIL</span>
            <h2 class="br-title">
                <span class="br-serif">Segurança</span>
                <span class="br-sans">Digital BR</span>
            </h2>
            <p class="br-sub">
                Notícias brasileiras serão exibidas na próxima atualização.
            </p>
        </div>
    </div>
</section>
'''

    weekly_html = ""
    if noticias_semana:
        weekly_cards = ""
        for w_n in noticias_semana[:30]:
            w_data = w_n.get("data", "")[:10]
            w_titulo = w_n.get("titulo", "Sem título")
            w_fonte = w_n.get("fonte", "Desconhecido")
            w_url = w_n.get("url", "#")
            w_imagem = w_n.get("imagem", "") or w_n.get("image", "")

            w_thumb = w_imagem if (w_imagem and w_imagem.startswith("http")) else gerar_thumbnail_svg(w_fonte, w_titulo)
            w_onerror = f"onerror=\"this.src='{gerar_thumbnail_svg(w_fonte, w_titulo)}'\"" if (w_imagem and w_imagem.startswith("http")) else ""

            weekly_cards += f'''
        <div class="weekly-card reveal-txt">
            <img src="{w_thumb}" alt="{w_titulo}" loading="lazy" {w_onerror}>
            <div>
                <div class="weekly-meta">
                    <span class="weekly-source">{w_fonte}</span> &middot; {w_data}
                </div>
                <h3 class="weekly-title">{w_titulo}</h3>
                <a href="{w_url}" class="weekly-link" target="_blank" rel="noopener noreferrer">Acessar arquivo &rarr;</a>
            </div>
        </div>'''
        
        weekly_html = f'''
<section class="weekly-section">
    <div class="weekly-header">
        <span class="weekly-label">ARQUIVO DA SEMANA</span>
        <span class="weekly-count">{len(noticias_semana)} artigos</span>
    </div>
    <div class="weekly-feed">
{weekly_cards}
    </div>
</section>
'''

    html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monitor de Ameaças | Cibersegurança</title>
    <meta name="description" content="Monitor de ameaças cibernéticas — notícias atualizadas diariamente sobre segurança digital">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Playfair+Display:ital,wght@0,700;0,900;1,700;1,900&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        :root {{
            --bg: #0a0a0a;
            --surface: #111111;
            --border: #1a1a1a;
            --text-main: #f5f0e8;
            --text-muted: #999999;
            --text-meta: #666666;
            --accent: #c8f135;
            
            --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
            --ease-in-out-expo: cubic-bezier(0.87, 0, 0.13, 1);
        }}

        * {{
            margin: 0; padding: 0; box-sizing: border-box;
        }}
        
        body {{
            background: transparent; /* Changed for fixed canvas */
            background-color: var(--bg);
            color: var(--text-main);
            font-family: 'Outfit', sans-serif;
            min-height: 100vh;
            overflow-x: hidden;
            cursor: none; 
            font-size: 16px;
            scroll-behavior: auto;
        }}

        /* --- GLOBAL CANVAS --- */
        #bg-canvas {{
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            z-index: 0;
            pointer-events: none;
        }}

        /* SVG Grain Texture Filter via pseudo-element */
        body::after {{
            content: '';
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 9998;
            opacity: 0.05;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='1'/%3E%3C/svg%3E");
        }}

        a, button {{ cursor: none; }}

        /* --- CUSTOM CURSOR --- */
        #cursor-dot {{
            position: fixed; width: 6px; height: 6px;
            background: var(--text-main); border-radius: 50%;
            pointer-events: none; z-index: 9999;
            transform: translate(-50%, -50%);
            transition: opacity 0.3s, background 0.3s;
        }}
        #cursor-ring {{
            position: fixed; width: 30px; height: 30px;
            border: 1px solid rgba(245, 240, 232, 0.5); border-radius: 50%;
            pointer-events: none; z-index: 9997;
            transform: translate(-50%, -50%);
            transition: width 0.4s var(--ease-out-expo), height 0.4s var(--ease-out-expo),
                        border-color 0.4s, background 0.4s;
            display: flex; align-items: center; justify-content: center;
        }}
        #cursor-ring::after {{
            content: '+';
            color: var(--bg);
            font-size: 20px;
            font-weight: 300;
            opacity: 0;
            transition: opacity 0.3s;
        }}
        #cursor-ring.hover-news {{
            width: 50px; height: 50px;
            border-color: var(--accent);
            background: rgba(200, 241, 53, 0.05);
            backdrop-filter: blur(2px);
        }}
        #cursor-ring.hover-link {{
            width: 40px; height: 40px;
            background: var(--accent);
            border-color: var(--accent);
        }}
        #cursor-ring.hover-link::after {{
            opacity: 1;
        }}
        #cursor-dot.hidden {{ opacity: 0; }}

        @media (hover: none) and (pointer: coarse) {{
            #cursor-dot, #cursor-ring {{ display: none !important; }}
            body, a, button {{ cursor: auto; }}
        }}

        /* --- LOADING SCREEN --- */
        #loader {{
            position: fixed; inset: 0; background: var(--bg); z-index: 10000;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            transition: opacity 1s var(--ease-out-expo), visibility 1s;
        }}
        #loader.done {{ opacity: 0; visibility: hidden; pointer-events: none; }}
        
        .loader-squares {{
            position: absolute; inset: 40px; pointer-events: none;
            display: flex; justify-content: space-between; align-items: space-between; flex-wrap: wrap;
            opacity: 0.1;
        }}
        .sq-corner {{ width: 10px; height: 10px; border: 1px solid white; }}
        .sq-top {{ width: 100%; display: flex; justify-content: space-between; }}
        .sq-bottom {{ width: 100%; display: flex; justify-content: space-between; align-self: flex-end; position: absolute; bottom: 0; }}

        .loader-center {{ text-align: center; display: flex; flex-direction: column; gap: 30px; }}
        .loader-title {{
            font-family: 'Playfair Display', serif; font-size: 32px; font-style: italic; color: var(--text-main);
        }}
        .loader-status {{
            font-family: 'Space Mono', monospace; font-size: 14px; text-transform: uppercase; color: var(--text-muted);
            letter-spacing: 2px;
        }}
        .loader-status span {{ display: inline-block; width: 30px; text-align: left; }}
        .loader-counter {{
            font-family: 'Space Mono', monospace; font-size: 80px; color: var(--accent); font-weight: 700;
            line-height: 1; margin-top: 10px;
        }}
        .loader-completed {{
            position: absolute; font-family: 'Space Mono', monospace; font-size: 14px; color: var(--accent);
            opacity: 0; transform: translateY(10px); transition: 0.4s;
        }}
        #loader.completed .loader-counter {{ opacity: 0; }}
        #loader.completed .loader-completed {{ opacity: 1; transform: translateY(0); }}

        /* --- HERO SECTION --- */
        #hero {{
            position: relative; width: 100vw; height: 100vh;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            overflow: hidden; text-align: center;
        }}
        .hero-content {{
            position: relative; z-index: 10; pointer-events: none;
            display: flex; flex-direction: column; align-items: center;
        }}
        header {{
            position: relative;
            z-index: 100;
        }}
        .hero-tag {{
            font-family: 'Space Mono', monospace; font-size: 12px; color: var(--accent);
            letter-spacing: 4px; text-transform: uppercase; margin-bottom: 2rem;
            opacity: 0; transform: translateY(20px); animation: fadeUp 1s var(--ease-out-expo) 1s forwards;
        }}
        .hero-title {{
            display: flex; align-items: center; justify-content: center; gap: 20px;
            margin-bottom: 1.5rem;
        }}
        .hero-title-serif {{
            font-family: 'Playfair Display', serif; font-style: italic; font-weight: 700;
            font-size: clamp(60px, 10vw, 140px); color: var(--text-main); line-height: 1;
        }}
        .hero-title-sans {{
            font-family: 'Outfit', sans-serif; font-weight: 800;
            font-size: clamp(60px, 10vw, 140px); color: var(--text-main); line-height: 1; text-transform: uppercase;
        }}
        .hero-subtitle {{
            font-family: 'Outfit', sans-serif; font-size: clamp(16px, 2vw, 22px);
            color: var(--text-muted); max-width: 600px; font-weight: 300; line-height: 1.5;
            opacity: 0; transform: translateY(20px); animation: fadeUp 1s var(--ease-out-expo) 1.2s forwards;
        }}
        .hero-badge {{
            margin-top: 3rem; display: inline-flex; align-items: center; gap: 10px;
            padding: 8px 16px; border: 1px solid rgba(200, 241, 53, 0.3); border-radius: 100px;
            font-family: 'Space Mono', monospace; font-size: 11px; text-transform: uppercase; color: var(--text-main);
            background: rgba(17, 17, 17, 0.4); backdrop-filter: blur(4px);
            opacity: 0; transform: translateY(20px); animation: fadeUp 1s var(--ease-out-expo) 1.4s forwards;
        }}
        .live-dot {{
            width: 8px; height: 8px; background: var(--accent); border-radius: 50%;
            animation: pulse-badge 2s infinite; display: inline-block;
        }}
        @keyframes pulse-badge {{ 0%, 100% {{opacity: 1; transform: scale(1);}} 50% {{opacity: 0.4; transform: scale(0.8);}} }}
        @keyframes fadeUp {{ to {{ opacity: 1; transform: translateY(0); }} }}

        .scroll-down {{
            position: absolute; bottom: 40px; left: 50%; transform: translateX(-50%);
            width: 1px; height: 60px; background: linear-gradient(to bottom, var(--accent), transparent);
            animation: scrollLine 2s infinite cubic-bezier(1,0,0,1);
            z-index: 10;
        }}
        @keyframes scrollLine {{ 0%{{transform: translate(-50%, -100%); opacity:0;}} 50%{{opacity:1;}} 100%{{transform: translate(-50%, 100%); opacity:0;}} }}

        /* --- MARQUEE DUPLO --- */
        .marquee-wrapper {{
            border-top: 1px solid var(--border); border-bottom: 1px solid var(--border);
            padding: 20px 0; overflow: hidden;
            position: relative; z-index: 10;
        }}
        .marquee-track {{ display: flex; width: max-content; }}
        .marquee-track.left {{ animation: marquee-left 40s linear infinite; margin-bottom: 12px; }}
        .marquee-track.right {{ animation: marquee-right 35s linear infinite; }}
        .marquee-content {{
            white-space: nowrap; font-family: 'Space Mono', monospace; font-size: 12px;
            letter-spacing: 2px; text-transform: uppercase; color: var(--text-muted);
            display: flex; align-items: center;
        }}
        .marquee-content .dot {{ color: var(--accent); margin: 0 30px; font-size: 16px; line-height: 0; }}
        
        @keyframes marquee-left {{ 0% {{transform: translateX(0);}} 100% {{transform: translateX(-50%);}} }}
        @keyframes marquee-right {{ 0% {{transform: translateX(-50%);}} 100% {{transform: translateX(0);}} }}
        
        /* --- TAGS SECTION --- */
        .tags-section {{
            position: relative;
            z-index: 10;
            padding: 32px 60px;
            border-bottom: 1px solid var(--border);
        }}
        .tags-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 16px;
        }}
        .tags-label {{
            font-family: 'Space Mono', monospace;
            font-size: 10px;
            letter-spacing: 3px;
            color: var(--text-meta);
            text-transform: uppercase;
        }}
        .tag-clear {{
            font-family: 'Space Mono', monospace;
            font-size: 10px;
            letter-spacing: 2px;
            color: var(--accent);
            background: none;
            border: 1px solid var(--accent);
            padding: 4px 12px;
            cursor: none;
            transition: all 0.3s;
            display: none;
        }}
        .tag-clear.visible {{ display: block; }}
        .tag-clear:hover {{
            background: var(--accent);
            color: var(--bg);
        }}
        .tags-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}
        .tag-btn {{
            font-family: 'Space Mono', monospace;
            font-size: 10px;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            background: none;
            border: 1px solid var(--border);
            color: var(--text-muted);
            padding: 6px 14px;
            cursor: none;
            transition: all 0.25s;
            border-radius: 2px;
        }}
        .tag-btn:hover {{
            border-color: var(--text-muted);
            color: var(--text-main);
        }}
        .tag-btn.active {{
            background: var(--accent);
            border-color: var(--accent);
            color: var(--bg);
            font-weight: 700;
        }}

        /* --- FEED EDITORIAL --- */
        /* Transparent backgrounds so global canvas shows through */
        .feed {{
            display: flex; flex-direction: column; width: 100%; position: relative; z-index: 10;
        }}
        .feed-card {{
            min-height: 50vh; border-bottom: 1px solid var(--border);
            padding: 10vh 5vw; display: flex; align-items: center;
            position: relative; z-index: 10;
            transition: opacity 0.5s;
        }}
        .card-inner {{
            display: flex; width: 100%; max-width: 1400px; margin: 0 auto; gap: 6vw;
            align-items: center; position: relative;
        }}
        
        /* Left: Thumbnail */
        .card-left {{
            width: 45%; flex-shrink: 0; position: relative;
        }}
        .card-img-wrap {{
            width: 100%; aspect-ratio: 4/3; position: relative; overflow: hidden; border-radius: 4px;
            transform: translateX(60px); opacity: 0; will-change: transform, opacity;
            transition: all 1s var(--ease-out-expo);
        }}
        .feed-card.is-visible .card-img-wrap {{
            transform: translateX(0); opacity: 1;
        }}
        .reveal-img {{
            width: 100%; height: 100%; object-fit: cover;
            transition: transform 0.6s var(--ease-out-expo);
        }}
        .img-overlay {{
            position: absolute; inset: 0; background: rgba(0,0,0,0);
            transition: background 0.6s; pointer-events: none;
        }}
        .card-img-wrap:hover .reveal-img {{ transform: scale(1.03); }}
        .card-img-wrap:hover .img-overlay {{ background: rgba(0,0,0,0.2); }}

        /* Right: Content */
        .card-right {{
            flex: 1; display: flex; flex-direction: column; justify-content: center;
        }}
        .card-num {{
            position: absolute; top: 0; left: -2vw;
            font-family: 'Space Mono', monospace; font-size: 14px; color: var(--accent);
            opacity: 0; transform: translateX(-20px); transition: all 1s var(--ease-out-expo);
        }}
        .feed-card.is-visible .card-num {{ opacity: 1; transform: translateX(0); }}

        .meta-row {{
            display: flex; align-items: center; gap: 8px; margin-bottom: 24px;
            font-family: 'Space Mono', monospace; font-size: 11px; text-transform: uppercase; color: var(--accent);
            letter-spacing: 1px;
        }}
        
        .card-title {{
            font-family: 'Playfair Display', serif; font-size: clamp(28px, 3vw, 42px);
            font-weight: 700; line-height: 1.2; color: var(--text-main); margin-bottom: 20px;
        }}
        .card-submeta {{
            font-family: 'Space Mono', monospace; font-size: 11px; color: var(--text-meta);
            margin-bottom: 24px; text-transform: uppercase;
        }}
        .card-resumo {{
            font-family: 'Outfit', sans-serif; font-size: 16px; color: var(--text-muted);
            line-height: 1.7; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;
            overflow: hidden; margin-bottom: 40px; max-width: 90%;
        }}

        .read-btn {{
            display: inline-flex; align-items: center; justify-content: center;
            padding: 12px 24px; border: 1px solid var(--accent); border-radius: 2px;
            background: transparent; color: var(--accent);
            font-family: 'Space Mono', monospace; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;
            text-decoration: none; transition: 0.3s var(--ease-out-expo);
            position: relative; overflow: hidden;
            pointer-events: auto;
        }}
        .read-btn:hover {{
            background: var(--accent); color: var(--bg);
        }}

        /* Content Reveal Animations */
        .reveal-txt {{
            opacity: 0; transform: translateX(-60px);
            transition: all 1s var(--ease-out-expo);
        }}
        .feed-card.is-visible .reveal-txt {{ opacity: 1; transform: translateX(0); }}
        
        .feed-card.is-visible .meta-row {{ transition-delay: 0.1s; }}
        .feed-card.is-visible .card-submeta {{ transition-delay: 0.2s; }}
        .feed-card.is-visible .card-resumo {{ transition-delay: 0.3s; }}
        .feed-card.is-visible .btn-wrap {{ transition-delay: 0.4s; }}

        /* SplitText Simulation styles */
        .split-wrap {{
            overflow: hidden; display: inline-block; vertical-align: bottom;
        }}
        .split-char {{
            display: inline-block;
            transform: translateY(100%) rotate(7deg); opacity: 0;
            transform-origin: bottom left;
            transition: transform 1s var(--ease-out-expo), opacity 1s;
        }}
        .feed-card.is-visible .split-char,
        header.is-visible .split-char,
        #footer-sec.is-visible .split-char {{
            transform: translateY(0) rotate(0deg); opacity: 1;
        }}

        /* --- FOOTER SECTION --- */
        #footer-sec {{
            position: relative; width: 100vw; height: 80vh; overflow: hidden;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            border-top: 1px solid var(--border);
            z-index: 10;
        }}
        .footer-content {{
            position: relative; z-index: 10; text-align: center; pointer-events: none;
        }}
        .footer-title {{
            font-family: 'Playfair Display', serif; font-style: italic; font-weight: 700;
            font-size: clamp(50px, 8vw, 100px); color: var(--text-main); margin-bottom: 20px;
        }}
        .footer-subtitle {{
            font-family: 'Outfit', sans-serif; font-size: 18px; color: var(--text-muted);
            margin-bottom: 60px; font-weight: 300;
        }}
        .footer-bottom {{
            font-family: 'Space Mono', monospace; font-size: 11px; text-transform: uppercase;
            color: var(--text-meta); display: flex; flex-direction: column; gap: 10px;
        }}
        .footer-bottom a {{
            color: var(--accent); pointer-events: auto; text-decoration: none;
        }}

        /* --- BR SECTION --- */
        .br-section {{
            position: relative;
            z-index: 10;
            border-top: 2px solid var(--accent);
            padding-top: 80px;
        }}
        .br-header {{
            display: flex;
            align-items: center;
            gap: 24px;
            padding: 0 60px 60px;
            border-bottom: 1px solid var(--border);
        }}
        .br-flag {{
            font-size: 48px;
            line-height: 1;
        }}
        .br-label {{
            font-family: 'Space Mono', monospace;
            font-size: 10px;
            letter-spacing: 4px;
            color: var(--accent);
            text-transform: uppercase;
            display: block;
            margin-bottom: 8px;
        }}
        .br-title {{
            display: flex;
            align-items: baseline;
            gap: 12px;
            margin-bottom: 8px;
        }}
        .br-serif {{
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-size: 48px;
            font-weight: 900;
            color: var(--text-main);
        }}
        .br-sans {{
            font-family: 'Outfit', sans-serif;
            font-size: 48px;
            font-weight: 800;
            color: var(--accent);
        }}
        .br-sub {{
            font-family: 'Outfit', sans-serif;
            font-size: 14px;
            color: var(--text-muted);
            max-width: 400px;
        }}

        /* --- WEEKLY SECTION --- */
        .weekly-section {{
            position: relative;
            z-index: 10;
            padding: 60px;
            border-top: 1px solid var(--border);
        }}
        .weekly-label {{
            font-family: 'Space Mono', monospace;
            font-size: 10px;
            letter-spacing: 3px;
            color: var(--accent);
            text-transform: uppercase;
        }}
        .weekly-count {{
            font-family: 'Space Mono', monospace;
            font-size: 10px;
            color: var(--text-meta);
        }}
        .weekly-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
        }}
        .weekly-card {{
            display: flex;
            gap: 32px;
            padding: 24px 0;
            border-bottom: 1px solid var(--border);
            align-items: flex-start;
        }}
        .weekly-card img {{
            width: 200px;
            height: 130px;
            object-fit: cover;
            border-radius: 4px;
            flex-shrink: 0;
            filter: brightness(0.85);
        }}
        .weekly-title {{
            font-family: 'Playfair Display', serif;
            font-size: 20px;
            font-weight: 700;
            color: var(--text-main);
            line-height: 1.3;
            margin-bottom: 8px;
            opacity: 0.8;
        }}
        .weekly-meta {{
            font-family: 'Space Mono', monospace;
            font-size: 10px;
            color: var(--text-meta);
            letter-spacing: 1px;
            margin-bottom: 8px;
        }}
        .weekly-source {{
            font-family: 'Space Mono', monospace;
            font-size: 10px;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        .weekly-link {{
            font-family: 'Space Mono', monospace;
            font-size: 10px;
            color: var(--text-muted);
            text-decoration: none;
            border-bottom: 1px solid var(--border);
            padding-bottom: 2px;
            transition: color 0.3s, border-color 0.3s;
            display: inline-block;
            margin-top: 8px;
        }}
        .weekly-link:hover {{
            color: var(--accent);
            border-color: var(--accent);
        }}

        @media (max-width: 900px) {{
            .card-inner {{ flex-direction: column; gap: 40px; }}
            .card-left, .card-right {{ width: 100%; transform: translateY(40px); }}
            .feed-card.is-visible .card-left, .feed-card.is-visible .card-right {{ transform: translateY(0); }}
            .card-img-wrap {{ transform: translateY(0); opacity: 1; }}
            .reveal-txt {{ transform: translateY(0); opacity: 1; }}
            .tags-section {{ padding: 24px 20px; }}
            .weekly-section {{ padding: 30px 20px; }}
            .weekly-card {{ flex-direction: column; gap: 16px; }}
            .weekly-card img {{ width: 100%; height: auto; }}
        }}

        /* --- NAVBAR --- */
        .site-nav {{
            position: fixed;
            top: 0; left: 0; right: 0;
            z-index: 500;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 60px;
            height: 56px;
            background: rgba(10, 10, 10, 0.85);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border);
            transition: opacity 0.3s;
        }}
        .site-nav.hidden {{ opacity: 0; pointer-events: none; }}
        .nav-logo {{
            font-size: 16px;
            font-weight: 700;
            letter-spacing: -0.5px;
        }}
        .nav-logo-serif {{
            font-family: 'Playfair Display', serif;
            font-style: italic;
            color: var(--text-main);
        }}
        .nav-logo-sans {{
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            color: var(--accent);
        }}
        .nav-links {{
            display: flex;
            gap: 4px;
        }}
        .nav-link {{
            font-family: 'Space Mono', monospace;
            font-size: 10px;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            background: none;
            border: 1px solid transparent;
            color: var(--text-muted);
            padding: 6px 16px;
            cursor: none;
            transition: all 0.25s;
            border-radius: 2px;
        }}
        .nav-link:hover {{
            color: var(--text-main);
            border-color: var(--border);
        }}
        .nav-link.active {{
            color: var(--accent);
            border-color: var(--accent);
            background: rgba(200, 241, 53, 0.05);
        }}
        @media (max-width: 768px) {{
            .site-nav {{ padding: 0 20px; }}
            .nav-link {{ font-size: 9px; padding: 5px 10px; }}
        }}
    </style>
</head>
<body>

<!-- Global Canvas Fixed -->
<div id="bg-canvas"></div>

<!-- Cursor -->
<div id="cursor-dot"></div>
<div id="cursor-ring"></div>

<!-- Navbar -->
<nav class="site-nav" id="siteNav">
    <div class="nav-logo">
        <span class="nav-logo-serif">Cyber</span><span class="nav-logo-sans">Intel</span>
    </div>
    <div class="nav-links">
        <button class="nav-link active" onclick="scrollToSection('feed')">
            🌐 Internacional
        </button>
        <button class="nav-link" onclick="scrollToSection('br-section')">
            🇧🇷 Brasil
        </button>
        <button class="nav-link" onclick="scrollToSection('weekly-section')">
            📁 Arquivo Semanal
        </button>
    </div>
</nav>

<!-- Loader -->
<div id="loader">
    <div class="loader-squares sq-top"><div class="sq-corner"></div><div class="sq-corner"></div></div>
    <div class="loader-center">
        <div class="loader-title">Cybersecurity<br>Intelligence Feed.</div>
        <div class="loader-status">LOADING <span id="l-dots">.</span></div>
        <div class="loader-counter-wrap">
            <div class="loader-counter" id="loader-count">000</div>
            <div class="loader-completed">COMPLETED</div>
        </div>
    </div>
    <div class="loader-squares sq-bottom"><div class="sq-corner"></div><div class="sq-corner"></div></div>
</div>

<!-- Hero -->
<section id="hero">
    <header class="hero-content">
        <div class="hero-tag">INTELIGÊNCIA EM CIBERSEGURANÇA</div>
        <h1 class="hero-title">
            <span class="hero-title-serif split-text">Notícias</span>
            <span class="hero-title-sans split-text">Cibersegurança</span>
        </h1>
        <p class="hero-subtitle">Acompanhe em tempo real as principais ameaças, vulnerabilidades e incidentes de segurança digital</p>
        <div class="hero-badge">
            <span class="live-dot"></span> Live Feed
        </div>
    </header>
    <div class="scroll-down"></div>
</section>

<!-- Marquee -->
<section class="marquee-wrapper">
    <div class="marquee-track left">
        <div class="marquee-content">THREAT INTEL<span class="dot">&middot;</span>CVE<span class="dot">&middot;</span>ZERO-DAY<span class="dot">&middot;</span>RANSOMWARE<span class="dot">&middot;</span>APT<span class="dot">&middot;</span>PHISHING<span class="dot">&middot;</span>MALWARE<span class="dot">&middot;</span>DATA BREACH<span class="dot">&middot;</span></div>
        <div class="marquee-content" aria-hidden="true">THREAT INTEL<span class="dot">&middot;</span>CVE<span class="dot">&middot;</span>ZERO-DAY<span class="dot">&middot;</span>RANSOMWARE<span class="dot">&middot;</span>APT<span class="dot">&middot;</span>PHISHING<span class="dot">&middot;</span>MALWARE<span class="dot">&middot;</span>DATA BREACH<span class="dot">&middot;</span></div>
    </div>
    <div class="marquee-track right">
        <div class="marquee-content">BLEEPINGCOMPUTER<span class="dot">&middot;</span>THE HACKER NEWS<span class="dot">&middot;</span>HACKREAD<span class="dot">&middot;</span>INFOSECURITY<span class="dot">&middot;</span>SECURITYWEEK<span class="dot">&middot;</span>HELP NET SECURITY<span class="dot">&middot;</span></div>
        <div class="marquee-content" aria-hidden="true">BLEEPINGCOMPUTER<span class="dot">&middot;</span>THE HACKER NEWS<span class="dot">&middot;</span>HACKREAD<span class="dot">&middot;</span>INFOSECURITY<span class="dot">&middot;</span>SECURITYWEEK<span class="dot">&middot;</span>HELP NET SECURITY<span class="dot">&middot;</span></div>
    </div>
</section>

<!-- Tags Section -->
<section class="tags-section">
  <div class="tags-header">
    <span class="tags-label">FILTRAR POR TEMA</span>
    <button class="tag-clear" id="tagClear">VER TODAS</button>
  </div>
  <div class="tags-list" id="tagsList">
    <!-- tags geradas dinamicamente pelo JS -->
  </div>
</section>

<!-- Feed -->
<main class="feed" id="feed">
{cards}
</main>

{br_html}

{weekly_html}

<!-- Footer -->
<footer id="footer-sec">
    <div class="footer-content">
        <h2 class="footer-title split-text">Stay Protected.</h2>
        <p class="footer-subtitle">Inteligência de ameaças atualizada diariamente</p>
        <div class="footer-bottom">
            <span>Security News Aggregator &mdash; Mateus Camara Dias</span>
            <span>Dados via NewsAPI &middot; Atualização diária automática</span>
        </div>
    </div>
</footer>

<script>
    // --- 0. NAVBAR SCROLL ---
    function scrollToSection(id) {{
        const el = document.getElementById(id) 
                 || document.querySelector('.' + id)
                 || document.querySelector('[id="' + id + '"]');
        if (el) {{
            el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
        }}
    }}

    const navSections = [
        {{ id: 'feed', btn: 0 }},
        {{ id: 'br-section', btn: 1 }},
        {{ id: 'weekly-section', btn: 2 }}
    ];
    window.addEventListener('scroll', () => {{
        const navLinks = document.querySelectorAll('.nav-link');
        let current = 0;
        navSections.forEach((s, i) => {{
            const el = document.getElementById(s.id) 
                    || document.querySelector('.' + s.id);
            if (el) {{
                const rect = el.getBoundingClientRect();
                if (rect.top <= window.innerHeight * 0.4) current = i;
            }}
        }});
        navLinks.forEach(l => l.classList.remove('active'));
        if (navLinks[current]) navLinks[current].classList.add('active');
    }}, {{ passive: true }});

    // Ocultar navbar durante o loader
    const navEl = document.getElementById('siteNav');
    if (navEl) navEl.classList.add('hidden');

    // --- 1. LOADER ---
    const loader = document.getElementById('loader');
    const countEl = document.getElementById('loader-count');
    const dotsEl = document.getElementById('l-dots');
    let pct = 0;
    
    // Dot animation
    let dC = 0;
    const dInt = setInterval(() => {{
        dC = (dC + 1) % 4;
        dotsEl.textContent = '.'.repeat(dC);
    }}, 400);

    // Counter
    const intv = setInterval(() => {{
        pct += Math.floor(Math.random() * 15) + 5;
        if (pct >= 100) {{
            pct = 100;
            clearInterval(intv);
            clearInterval(dInt);
            countEl.textContent = '100';
            loader.classList.add('completed');
            setTimeout(() => {{
                loader.classList.add('done');
                document.querySelector('#hero header').classList.add('is-visible');
                if (navEl) navEl.classList.remove('hidden');
            }}, 800);
        }} else {{
            countEl.textContent = pct.toString().padStart(3, '0');
        }}
    }}, 50);

    // --- 2. CUSTOM CURSOR ---
    const dot = document.getElementById('cursor-dot');
    const ring = document.getElementById('cursor-ring');
    let mx = window.innerWidth/2, my = window.innerHeight/2;
    let rx = mx, ry = my;

    document.addEventListener('mousemove', e => {{
        mx = e.clientX; my = e.clientY;
        if (dot) dot.style.transform = `translate(${{mx}}px, ${{my}}px)`;
    }});

    function cursorLoop() {{
        rx += (mx - rx) * 0.12; // 12% lag
        ry += (my - ry) * 0.12;
        if (ring) ring.style.transform = `translate(${{rx}}px, ${{ry}}px)`;
        requestAnimationFrame(cursorLoop);
    }}
    cursorLoop();

    // Hover states
    document.querySelectorAll('.feed-card').forEach(el => {{
        el.addEventListener('mouseenter', () => ring.classList.add('hover-news'));
        el.addEventListener('mouseleave', () => ring.classList.remove('hover-news'));
    }});
    // Using dynamic elements binding logic for hover
    function bindCursorHovers() {{
        document.querySelectorAll('a, button, .read-btn, .tag-btn, .tag-clear').forEach(el => {{
            el.addEventListener('mouseenter', () => {{
                dot.classList.add('hidden');
                ring.classList.add('hover-link');
                ring.classList.remove('hover-news');
            }});
            el.addEventListener('mouseleave', () => {{
                dot.classList.remove('hidden');
                ring.classList.remove('hover-link');
            }});
        }});
    }}
    bindCursorHovers();

    // --- 3. SPLIT TEXT ENGINE ---
    document.querySelectorAll('.split-text').forEach(el => {{
        const text = el.innerText;
        el.innerHTML = '';
        const words = text.split(' ');
        words.forEach((word, wIdx) => {{
            const wordSpan = document.createElement('span');
            wordSpan.style.display = 'inline-block';
            wordSpan.style.whiteSpace = 'nowrap';
            
            const chars = word.split('');
            chars.forEach((c, cIdx) => {{
                const cw = document.createElement('span');
                cw.className = 'split-wrap';
                const charSpan = document.createElement('span');
                charSpan.className = 'split-char';
                charSpan.innerText = c;
                charSpan.style.transitionDelay = `${{(wIdx * 0.1) + (cIdx * 0.03)}}s`;
                cw.appendChild(charSpan);
                wordSpan.appendChild(cw);
            }});
            el.appendChild(wordSpan);
            if(wIdx < words.length - 1) el.appendChild(document.createTextNode(' '));
        }});
    }});

    // --- 4. SCROLL OBSERVER ---
    const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
            if(entry.isIntersecting) {{
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            }}
        }});
    }}, {{ threshold: 0.15, rootMargin: '0px 0px -50px 0px' }});

    document.querySelectorAll('.feed-card, #footer-sec').forEach(card => observer.observe(card));

    // --- 5. TAGS LOGIC ---
    const allTags = new Set();
    document.querySelectorAll('.feed-card').forEach(card => {{
        const tags = JSON.parse(card.dataset.tags || '[]');
        tags.forEach(t => allTags.add(t));
    }});

    const tagsList = document.getElementById('tagsList');
    allTags.forEach(tag => {{
        const btn = document.createElement('button');
        btn.className = 'tag-btn';
        btn.textContent = '#' + tag;
        btn.dataset.tag = tag;
        btn.addEventListener('click', () => filterByTag(tag, btn));
        tagsList.appendChild(btn);
    }});
    bindCursorHovers(); // re-bind to new buttons

    let activeTag = null;
    function filterByTag(tag, btn) {{
        if (activeTag === tag) {{
            // Desativa filtro
            activeTag = null;
            document.querySelectorAll('.tag-btn')
                .forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.feed-card')
                .forEach(c => {{
                    c.style.display = '';
                    c.style.opacity = '1';
                }});
            document.getElementById('tagClear')
                .classList.remove('visible');
            return;
        }}
        activeTag = tag;
        document.querySelectorAll('.tag-btn')
            .forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');
        document.getElementById('tagClear')
            .classList.add('visible');
        
        document.querySelectorAll('.feed-card').forEach(card => {{
            const tags = JSON.parse(card.dataset.tags || '[]');
            if (tags.includes(tag)) {{
                card.style.display = '';
                card.style.opacity = '1';
            }} else {{
                card.style.display = 'none';
            }}
        }});
    }}

    document.getElementById('tagClear')
        .addEventListener('click', () => {{
            if (activeTag) filterByTag(activeTag, null);
        }});

    // --- 6. GLOBAL THREE.JS CANVAS CONTROLLER ---
    // Global mouse state for webgl tilt
    let tMouse = new THREE.Vector2(0, 0);
    let targetRotation = new THREE.Vector2(0, 0);
    
    document.addEventListener('mousemove', (e) => {{
        tMouse.x = (e.clientX / window.innerWidth) * 2 - 1;
        tMouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
        targetRotation.x = tMouse.y * 0.2;
        targetRotation.y = tMouse.x * 0.2;
    }});

    function initBackgroundScene() {{
        const container = document.getElementById('bg-canvas');
        if(!container) return;
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(60, window.innerWidth/window.innerHeight, 0.1, 1000);
        camera.position.z = 250;

        const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);

        // --- GROUP 1: NETWORK GRAPH ---
        const networkGroup = new THREE.Group();
        const numNodes = 80;
        const positions = new Float32Array(numNodes * 3);
        const nodeGeometry = new THREE.SphereGeometry(1.5, 8, 8);
        const nodeMaterialBase = new THREE.MeshBasicMaterial({{ color: 0xffffff, transparent: true, opacity: 1 }});
        const nodeMaterialAccent = new THREE.MeshBasicMaterial({{ color: 0xc8f135, transparent: true, opacity: 1 }});
        
        const nodesWrapper = new THREE.Group();
        const nodeData = [];

        for(let i=0; i<numNodes; i++) {{
            const x = (Math.random() - 0.5) * 400;
            const y = (Math.random() - 0.5) * 400;
            const z = (Math.random() - 0.5) * 300;
            positions[i*3] = x; positions[i*3+1] = y; positions[i*3+2] = z;
            
            const isAccent = Math.random() > 0.85;
            const mesh = new THREE.Mesh(nodeGeometry, isAccent ? nodeMaterialAccent : nodeMaterialBase);
            mesh.position.set(x,y,z);
            nodesWrapper.add(mesh);
            
            nodeData.push({{
                mesh: mesh,
                baseScale: 1,
                pulsing: isAccent || Math.random() > 0.7,
                phase: Math.random() * Math.PI * 2
            }});
        }}
        networkGroup.add(nodesWrapper);

        // Lines
        const lineMaterial = new THREE.LineBasicMaterial({{ 
            color: 0xc8f135, transparent: true, opacity: 0.15 
        }});
        const linesGeometry = new THREE.BufferGeometry();
        const linesMesh = new THREE.LineSegments(linesGeometry, lineMaterial);
        networkGroup.add(linesMesh);

        function updateLines() {{
            const p = [];
            for(let i=0; i<numNodes; i++) {{
                for(let j=i+1; j<numNodes; j++) {{
                    const m1 = nodeData[i].mesh.position;
                    const m2 = nodeData[j].mesh.position;
                    const dist = m1.distanceTo(m2);
                    if(dist < 80) {{
                        p.push(m1.x, m1.y, m1.z);
                        p.push(m2.x, m2.y, m2.z);
                    }}
                }}
            }}
            linesGeometry.setAttribute('position', new THREE.Float32BufferAttribute(p, 3));
        }}

        scene.add(networkGroup);

        // --- GROUP 2: SHIELD ---
        const shieldGroup = new THREE.Group();
        
        const shieldShape = new THREE.Shape();
        shieldShape.moveTo(0, 30);
        shieldShape.quadraticCurveTo(30, 30, 40, 20);
        shieldShape.lineTo(40, -10);
        shieldShape.quadraticCurveTo(40, -40, 0, -60);
        shieldShape.quadraticCurveTo(-40, -40, -40, -10);
        shieldShape.lineTo(-40, 20);
        shieldShape.quadraticCurveTo(-30, 30, 0, 30);

        const extrudeSettings = {{
            depth: 4, bevelEnabled: true, bevelSegments: 2, steps: 2, bevelSize: 1, bevelThickness: 1
        }};
        const sGeometry = new THREE.ExtrudeGeometry(shieldShape, extrudeSettings);
        
        // Solid dark core
        const materialCore = new THREE.MeshBasicMaterial({{ color: 0x111111, transparent: true, opacity: 0 }});
        const meshCore = new THREE.Mesh(sGeometry, materialCore);
        shieldGroup.add(meshCore);

        // Wireframe edges
        const edges = new THREE.EdgesGeometry(sGeometry);
        const materialLines = new THREE.LineBasicMaterial({{ color: 0xc8f135, transparent: true, opacity: 0 }});
        const sLineMesh = new THREE.LineSegments(edges, materialLines);
        shieldGroup.add(sLineMesh);

        // Central lock icon
        const lockShape = new THREE.Shape();
        lockShape.absarc(0, 5, 8, Math.PI, 0, false);
        lockShape.lineTo(8, -5); lockShape.lineTo(-8, -5); lockShape.lineTo(-8, 5);
        const lockGeo = new THREE.ExtrudeGeometry(lockShape, {{depth: 8, bevelEnabled:false}});
        const lockMat = new THREE.MeshBasicMaterial({{color: 0xc8f135, wireframe: true, transparent: true, opacity: 0}});
        const lockMesh = new THREE.Mesh(lockGeo, lockMat);
        lockMesh.position.z = -2;
        shieldGroup.add(lockMesh);

        shieldGroup.position.set(0, 0, 100); // bring it slightly closer
        shieldGroup.scale.set(0.8, 0.8, 0.8); // Reduced scale by 20%
        shieldGroup.visible = false;
        scene.add(shieldGroup);

        // --- ZONE DETECTOR ---
        let inShieldZone = false;
        let pOpacityNetwork = 1.0;
        let pOpacityShield = 0.0;
        const opacityLerpRate = 0.04;

        window.addEventListener('scroll', () => {{
            const article10 = document.querySelector('[data-index="10"]');
            if (!article10) return;
            const rect = article10.getBoundingClientRect();
            // Enter shield zone when article 10 is near viewport center
            inShieldZone = rect.top < window.innerHeight * 0.7;
        }});

        // Render loop
        let time = 0;
        function animate() {{
            requestAnimationFrame(animate);
            time += 0.02;

            // Opacity Crossfade calculation
            const targetNetworkOpacity = inShieldZone ? 0 : 1;
            const targetShieldOpacity = inShieldZone ? 1 : 0;
            
            pOpacityNetwork += (targetNetworkOpacity - pOpacityNetwork) * opacityLerpRate;
            pOpacityShield += (targetShieldOpacity - pOpacityShield) * opacityLerpRate;

            // Visibility toggle to save performance
            networkGroup.visible = pOpacityNetwork > 0.01;
            shieldGroup.visible = pOpacityShield > 0.01;

            if (networkGroup.visible) {{
                // Apply network opacity
                nodeMaterialBase.opacity = pOpacityNetwork;
                nodeMaterialAccent.opacity = pOpacityNetwork;
                lineMaterial.opacity = pOpacityNetwork * 0.15; // baseline opacity ratio

                // Network animation
                nodesWrapper.rotation.y = time * 0.05;
                nodeData.forEach(nd => {{
                    if(nd.pulsing) {{
                        const s = nd.baseScale + Math.sin(time * 2 + nd.phase) * 0.4;
                        nd.mesh.scale.set(s,s,s);
                    }}
                }});
                updateLines();
            }}

            if (shieldGroup.visible) {{
                // Apply shield opacity
                materialCore.opacity = pOpacityShield * 0.04; // Solid inner opacity
                materialLines.opacity = pOpacityShield * 0.18; // Wireframe opacity
                lockMat.opacity = pOpacityShield * 0.18; // Lock opacity (wireframe style so using wireframe opacity)

                // Shield animation
                shieldGroup.rotation.y = ((Math.sin(time) * 0.3) + (time * 0.2)) * 0.7; // Speed reduced by 30%
                shieldGroup.position.y = Math.sin(time * 2) * 5;
            }}

            // Global Parallax mouse tilt
            scene.rotation.x += (targetRotation.x - scene.rotation.x) * 0.05;
            scene.rotation.y += (targetRotation.y - scene.rotation.y) * 0.05;

            renderer.render(scene, camera);
        }}
        animate();

        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});
    }}
    
    // Initialize
    initBackgroundScene();

</script>
</body>
</html>"""

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("[OK] Redesign Premium gerado com sucesso!")

if __name__ == "__main__":
    gerar_html()
