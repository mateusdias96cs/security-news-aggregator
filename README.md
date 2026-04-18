# 🛡️ Security News Aggregator

> Agregador automático de notícias de cibersegurança em tempo real — Python + HTML com deploy automatizado via GitHub Actions.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Status](https://img.shields.io/badge/Status-Funcional-00ff41?style=for-the-badge)

**🌐 [Ver ao vivo](https://mateusdias96cs.github.io/security-news-aggregator/)**

---

## 📋 Sobre o Projeto

O **Security News Aggregator** coleta, processa e exibe automaticamente as últimas notícias de cibersegurança das principais fontes do mundo. A interface é gerada em HTML com cards interativos — ao clicar em um card ele vira e exibe o resumo da notícia. O conteúdo é atualizado automaticamente todo dia via GitHub Actions, sem nenhuma intervenção manual.

Projeto desenvolvido como iniciativa pessoal para acompanhamento do cenário de ameaças e vulnerabilidades em tempo real.

---

## ✨ Funcionalidades

- **Cards interativos** com efeito flip — frente exibe a thumbnail e título, verso exibe o resumo
- **Scroll horizontal com drag** — arraste os cards com o mouse ou toque
- **Thumbnails dinâmicas por fonte** — cada portal tem gradiente e identidade visual própria quando não há imagem
- **Atualização automática diária** via GitHub Actions (todo dia às 8h UTC)
- **Sanitização contra XSS** — todos os dados externos são sanitizados antes de entrar no HTML
- **Deploy no GitHub Pages** — acessível publicamente sem precisar rodar nada localmente

---

## 🌐 Fontes Monitoradas

| Fonte | Tipo | Foco |
|---|---|---|
| 🔵 **BleepingComputer** | Portal especializado | Malware, vulnerabilidades, incidentes |
| 🔴 **The Hacker News** | Portal especializado | Segurança ofensiva e defensiva |
| 🟣 **HackRead** | Portal especializado | Hacking e privacidade |
| 🟢 **Infosecurity Magazine** | Revista especializada | Tendências e análises |
| 🟡 **SecurityWeek** | Portal especializado | Ameaças e análises de mercado |
| ⚪ **NewsAPI** | Agregador | Fontes diversas em tempo real |

---

## ⚙️ Arquitetura do Projeto

```
security-news-aggregator/
│
├── main.py               # Orquestrador — executa o pipeline completo
├── fetcher.py            # Coleta notícias via RSS e NewsAPI
├── processor.py          # Sanitiza e normaliza os dados coletados
├── storage.py            # Salva os dados em noticias.json
├── display.py            # Exibe top 10 no terminal
├── gerar_html.py         # Gera index.html com interface de cards
├── index.html            # Interface gerada automaticamente
├── static/
│   ├── style.css         # (legado — estilos agora inline no gerar_html.py)
│   └── placeholder.svg   # Fallback de imagem
├── .github/
│   └── workflows/
│       └── update-news.yml  # Workflow de atualização automática
├── .gitignore
├── requirements.txt
└── README.md
```

### Fluxo de execução

```
main.py
   │
   ├── fetcher.py    → Coleta notícias (RSS + NewsAPI)
   │
   ├── processor.py  → Sanitiza e normaliza dados
   │
   ├── storage.py    → Salva em noticias.json
   │
   └── gerar_html.py → Gera index.html com cards interativos
                              │
                              └── GitHub Pages ← deploy automático
```

---

## 🚀 Como usar localmente

### Pré-requisitos

- Python 3.10+
- pip
- Chave da [NewsAPI](https://newsapi.org/)

### Instalação

```bash
git clone https://github.com/mateusdias96cs/security-news-aggregator.git
cd security-news-aggregator
pip install -r requirements.txt
```

### Configuração

Cria um arquivo `.env` na raiz do projeto:

```
NEWS_API_KEY=sua_chave_aqui
```

### Execução

```bash
python main.py
```

Abre o `index.html` gerado no navegador para visualizar as notícias.

---

## 🤖 Atualização Automática

O projeto usa **GitHub Actions** para atualizar as notícias automaticamente todo dia às 8h UTC (5h horário de Brasília). O workflow roda o `main.py` na nuvem, gera um novo `index.html` e faz commit automaticamente — o GitHub Pages é atualizado em seguida.

Para rodar manualmente: **Actions → Update Security News → Run workflow**

A chave da NewsAPI é armazenada como **GitHub Secret** e nunca fica exposta no código.

---

## 🔒 Segurança

Todos os dados externos são sanitizados antes de entrar no HTML:

- Tags HTML removidas de títulos, resumos e autores
- Caracteres perigosos escapados (`<`, `>`, `"`, `'`, `&`)
- URLs validadas — aceita apenas `http://` e `https://`
- Bloqueio de `javascript:`, `data:` e `vbscript:` URIs
- Datas normalizadas para formato `YYYY-MM-DD`

---

## 🔧 Melhorias Planejadas

- [ ] Filtro por fonte ou categoria
- [ ] Busca por palavra-chave
- [ ] Modo claro/escuro
- [ ] Notificações para alertas críticos da CISA

---

## 👨‍💻 Autor

**Mateus Camara Dias**
Estudante de Cibersegurança — SENAC | Hackers do Bem — SENAI

[![GitHub](https://img.shields.io/badge/GitHub-mateusdias96cs-0d1117?style=flat&logo=github)](https://github.com/mateusdias96cs)
[![TryHackMe](https://img.shields.io/badge/TryHackMe-mateusdias96cs-212C42?style=flat&logo=tryhackme&logoColor=red)](https://tryhackme.com/p/mateusdias96cs)

---

> *Projeto desenvolvido para fins educacionais e acompanhamento do cenário de ameaças em cibersegurança.*