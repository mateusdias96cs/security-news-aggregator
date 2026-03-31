[README-security-news-aggregator.md](https://github.com/user-attachments/files/26387889/README-security-news-aggregator.md)
# 🛡️ Security News Aggregator

> Agregador automático de notícias de cibersegurança em tempo real — desenvolvido em Python com geração de interface HTML dinâmica.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![Status](https://img.shields.io/badge/Status-Funcional-00ff41?style=for-the-badge)
![Fontes](https://img.shields.io/badge/Fontes-10+-blue?style=for-the-badge)

---

## 📋 Sobre o Projeto

O **Security News Aggregator** é uma ferramenta desenvolvida em Python que coleta, processa e exibe automaticamente as últimas notícias de cibersegurança das principais fontes do mundo. Ao executar o programa, um arquivo HTML é gerado e atualizado com as notícias mais recentes, organizadas em cards interativos com título, fonte, data, autor e link para o artigo completo.

Projeto desenvolvido como iniciativa pessoal para acompanhar o cenário de ameaças e vulnerabilidades em tempo real.

---

## 🌐 Fontes Monitoradas

| Fonte | Tipo | Foco |
|---|---|---|
| 🔴 **BleepingComputer** | Portal especializado | Malware, vulnerabilidades, incidentes |
| 🔴 **The Hacker News** | Portal especializado | Segurança ofensiva e defensiva |
| 🔴 **CISA.gov** | Governo americano | CVEs e alertas oficiais |
| 🔵 **Talos Intelligence** | Cisco | Threat intelligence |
| 🔵 **Infosecurity Magazine** | Revista especializada | Tendências e análises |
| 🔵 **HackRead** | Portal especializado | Hacking e privacidade |
| 🟢 **TechRadar** | Portal de tecnologia | Segurança e tecnologia |
| 🟢 **SiliconANGLE** | Portal de tecnologia | Enterprise security |
| 🟢 **Tom's Hardware** | Portal de tecnologia | Hardware e segurança |
| 🟢 **Science Daily** | Ciência | Pesquisa em segurança |

---

## ⚙️ Arquitetura do Projeto

```
security-news-aggregator/
│
├── main.py          # Orquestrador principal — executa o pipeline completo
├── fetcher.py       # Coleta as notícias via RSS/scraping das fontes
├── processor.py     # Processa e normaliza os dados coletados
├── storage.py       # Armazena os dados em noticias.json
├── display.py       # Lógica de exibição dos dados
├── gerar_html.py    # Gera o arquivo index.html com os cards de notícias
├── index.html       # Interface HTML gerada automaticamente
├── noticias.json    # Banco de dados local das notícias
└── requirements.txt # Dependências do projeto
```

### Fluxo de execução

```
main.py
   │
   ├── fetcher.py    → Busca notícias nas fontes (RSS/HTTP)
   │
   ├── processor.py  → Normaliza título, data, autor, fonte, link
   │
   ├── storage.py    → Salva em noticias.json
   │
   └── gerar_html.py → Gera index.html com interface em cards
                              │
                              └── index.html  ← Abre no navegador
```

---

## 🚀 Como usar

### Pré-requisitos

- Python 3.8+
- pip

### Instalação

```bash
# Clone o repositório
git clone https://github.com/mateusdias96cs/security-news-aggregator.git

# Acesse a pasta
cd security-news-aggregator

# Instale as dependências
pip install -r requirements.txt
```

### Execução

```bash
python main.py
```

Após a execução, abra o arquivo `index.html` no navegador para visualizar as notícias atualizadas.

---

## 🖥️ Interface

A interface exibe os artigos em formato de cards contendo:

- **Número** do artigo na listagem
- **Título** clicável que abre o artigo original
- **Fonte** — nome do portal de origem
- **Data** de publicação
- **Autor** (quando disponível)
- **Resumo** do conteúdo
- **Link** para leitura completa

---

## 🔧 Melhorias Planejadas

- [ ] Frontend com atualização automática (sem precisar rodar o script manualmente)
- [ ] Filtro por categoria (malware, CVE, pentest, etc.)
- [ ] Busca por palavra-chave
- [ ] Agendamento automático com `cron` ou `Task Scheduler`
- [ ] Deploy em servidor web
- [ ] Notificações para alertas críticos da CISA

---

## 👨‍💻 Autor

**Mateus Camara Dias**
Estudante de Cibersegurança — SENAC | Hackers do Bem — SENAI

[![GitHub](https://img.shields.io/badge/GitHub-mateusdias96cs-0d1117?style=flat&logo=github)](https://github.com/mateusdias96cs)
[![TryHackMe](https://img.shields.io/badge/TryHackMe-mateusdias96cs-212C42?style=flat&logo=tryhackme&logoColor=red)](https://tryhackme.com/p/mateusdias96cs)

---

> *Projeto desenvolvido para fins educacionais e acompanhamento do cenário de ameaças em cibersegurança.*
