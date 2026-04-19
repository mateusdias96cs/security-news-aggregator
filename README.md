# 🛡️ Security News Aggregator

> Agregador automático de notícias de cibersegurança em tempo real — Python + HTML com deploy automatizado via GitHub Actions.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![Three.js](https://img.shields.io/badge/Three.js-000000?style=for-the-badge&logo=three.js&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Status](https://img.shields.io/badge/Status-Funcional-00ff41?style=for-the-badge)

**🌐 [Ver ao vivo](https://mateusdias96cs.github.io/security-news-aggregator/)**

---

## 📋 Sobre o Projeto

O **Security News Aggregator** coleta, processa e exibe automaticamente as últimas notícias de cibersegurança das principais fontes internacionais e brasileiras. A interface foi completamente redesenhada com estética editorial premium — animações 3D via Three.js, scroll vertical fluido, tipografia expressiva e experiência visual imersiva. O conteúdo é atualizado automaticamente todo dia via GitHub Actions.

---

## ✨ Funcionalidades

### Interface e Design
- Design editorial premium com paleta escura e acento verde-limão
- Animações 3D via Three.js — rede de nós conectados e escudo wireframe como fundo interativo
- Cursor personalizado com ponto e anel animado
- Loading screen estilo terminal com contador 000 a 100
- Marquee duplo com termos de cibersegurança e nomes das fontes
- Scroll vertical fluido com layout editorial — thumbnail à esquerda, texto à direita
- Navbar fixa com navegação entre Internacional, Brasil e Arquivo Semanal
- Scroll reveal com animação ao entrar no viewport
- Grain texture sutil para profundidade visual

### Conteúdo
- 20 notícias internacionais atualizadas diariamente via NewsAPI
- Seção brasileira com notícias de portais 100% especializados em cibersegurança via RSS
- Arquivo semanal com histórico dos últimos 7 dias sem duplicatas
- Thumbnails reais extraídas via og:image scraping
- SVG placeholder temático gerado automaticamente como fallback

### Filtragem e Navegação
- Sistema de tags — filtre por RANSOMWARE, PHISHING, ZERO-DAY, APT, MALWARE, VULNERABILIDADE, INCIDENTE, IA e SEGURANÇA, GOVERNO, INFRAESTRUTURA CRÍTICA
- Numeração editorial (#01, #02 / BR#01, BR#02)
- Botão Ler artigo visível diretamente sem interação adicional

---

## 🌐 Fontes Monitoradas

### Internacionais via NewsAPI
| Fonte | Foco |
|---|---|
| BleepingComputer | Malware, vulnerabilidades, incidentes |
| The Hacker News | Segurança ofensiva e defensiva |
| HackRead | Hacking e privacidade |
| Infosecurity Magazine | Tendências e análises |
| SecurityWeek | Ameaças e análises de mercado |

### Brasileiras via RSS direto
| Fonte | Foco |
|---|---|
| CISO Advisor | Alertas CVE e threat intel |
| Boletim Sec | Boletim semanal de segurança |
| Security Leaders | Maior plataforma cyber do Brasil |

### Execução

```bash
python3 main.py
xdg-open index.html
```

---

## 🤖 Atualização Automática

O projeto usa GitHub Actions para atualizar as notícias todo dia às 8h UTC (5h Brasília). O workflow roda o main.py, gera novo index.html e faz commit automaticamente.

Para rodar manualmente: Actions → Update Security News → Run workflow

A chave da NewsAPI fica como GitHub Secret — nunca exposta no código.

---

## 🔒 Segurança

- Tags HTML removidas de títulos, resumos e autores
- Caracteres perigosos escapados
- URLs validadas — apenas http e https
- Bloqueio de javascript, data e vbscript URIs
- Datas normalizadas para YYYY-MM-DD

---

## 🔧 Roadmap

- [x] Filtro por tema com sistema de tags
- [x] Seção brasileira com fontes especializadas via RSS
- [x] Histórico semanal automático
- [x] Design editorial premium com Three.js
- [x] Thumbnails reais via og:image scraping
- [x] Navbar de navegação por seção
- [ ] Busca por palavra-chave
- [ ] Notificações para alertas críticos da CISA
- [ ] Modo claro

---

## 👨‍💻 Autor

**Mateus Camara Dias**
Estudante de Cibersegurança — SENAC | Hackers do Bem — SENAI

[![GitHub](https://img.shields.io/badge/GitHub-mateusdias96cs-0d1117?style=flat&logo=github)](https://github.com/mateusdias96cs)
[![TryHackMe](https://img.shields.io/badge/TryHackMe-mateusdias96cs-212C42?style=flat&logo=tryhackme&logoColor=red)](https://tryhackme.com/p/mateusdias96cs)

---

> Projeto desenvolvido para fins educacionais e acompanhamento do cenário de ameaças em cibersegurança.
ENDOFFILE
