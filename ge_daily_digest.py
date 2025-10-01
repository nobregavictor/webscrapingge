#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GE (Globo Esporte) - Script para enviar um resumo diário das principais manchetes do site GE (ge.globo.com)

Instalação:
    pip install -r requirements.txt

Variáveis de ambiente (.env):
    SMTP_HOST=smtp.gmail.com
    SMTP_PORT=465
    SMTP_USER=seu_email@gmail.com
    SMTP_PASS=sua_senha_ou_app_password
    FROM_EMAIL=seu_email@gmail.com
    TO_EMAIL=destinatario@exemplo.com
    # Opcional
    RSS_URL=https://ge.globo.com/rss/feeds/home.xml
    HTML_URL=https://ge.globo.com/


"""

import os
import time
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from typing import List, Tuple

# Dependências
import requests
from bs4 import BeautifulSoup
try:
    import feedparser
except Exception:
    feedparser = None

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

def load_env():
    if load_dotenv:
        # carrega .env se existir
        load_dotenv()
    env = {
        "SMTP_HOST": os.getenv("SMTP_HOST", "smtp.gmail.com"),
        "SMTP_PORT": int(os.getenv("SMTP_PORT", "465")),
        "SMTP_USER": os.getenv("SMTP_USER", ""),
        "SMTP_PASS": os.getenv("SMTP_PASS", ""),
        "FROM_EMAIL": os.getenv("FROM_EMAIL", os.getenv("SMTP_USER", "")),
        "TO_EMAIL": os.getenv("TO_EMAIL", ""),
        "RSS_URL": os.getenv("RSS_URL", "https://ge.globo.com/rss/feeds/home.xml"),
        "HTML_URL": os.getenv("HTML_URL", "https://ge.globo.com/"),
        "DIGEST_LIMIT": int(os.getenv("DIGEST_LIMIT", "10")),
        "REQUEST_TIMEOUT": int(os.getenv("REQUEST_TIMEOUT", "20")),
        "PAUSE_SEC": float(os.getenv("PAUSE_SEC", "0.5")),
    }
    return env

def fetch_rss_headlines(rss_url: str, limit: int, timeout: int) -> List[Tuple[str, str]]:
    if not feedparser:
        return []
    d = feedparser.parse(rss_url)
    items = []
    for entry in d.entries[:limit*2]:  # pega um pouco mais e depois deduplica
        title = getattr(entry, "title", "").strip()
        link = getattr(entry, "link", "").strip()
        if title and link:
            items.append((title, link))
    return dedupe(items)[:limit]

def fetch_html_headlines(html_url: str, limit: int, timeout: int) -> List[Tuple[str, str]]:
    """
    Fallback: tenta extrair manchetes da home do GE.
    Observação: Seletores podem mudar com o tempo.
    Aqui usamos padrões comuns do CMS da Globo (classe 'feed-post-link').
    """
    resp = requests.get(html_url, timeout=timeout, headers={
        "User-Agent": "Mozilla/5.0 (compatible; GE-Digest/1.0)"
    })
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    results = []

    # 1) Seletores comuns no ecossistema globo.com
    for a in soup.select("a.feed-post-link"):
        title = (a.get_text() or "").strip()
        href = a.get("href", "").strip()
        if title and href:
            results.append((title, href))

    # 2) Outro seletor possível de manchetes
    if len(results) < limit:
        for a in soup.select("a[href*='ge.globo.com'] h2, a[href*='ge.globo.com'] h3"):
            parent = a.find_parent("a")
            if parent:
                title = (a.get_text() or "").strip()
                href = parent.get("href", "").strip()
                if title and href:
                    results.append((title, href))

    results = dedupe(results)
    return results[:limit]

def dedupe(items: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    seen = set()
    out = []
    for t, l in items:
        key = (t.lower(), l.lower())
        if key not in seen:
            seen.add(key)
            out.append((t, l))
    return out

def build_email_html(headlines: List[Tuple[str, str]]) -> str:
    lis = "\n".join([f'<li><a href="{link}">{title}</a></li>' for title, link in headlines])
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    return f"""
    <html>
    <body>
        <h2>Top {len(headlines)} manchetes do GE — {now}</h2>
        <ol>
            {lis}
        </ol>
        <p style="color:#666;font-size:12px;">
           Enviado automaticamente por um script pessoal de estudo (Python).
        </p>
    </body>
    </html>
    """.strip()

def send_email(env, subject: str, html_body: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = env["FROM_EMAIL"]
    msg["To"] = env["TO_EMAIL"]

    # Versão texto simples (fallback)
    plain = BeautifulSoup(html_body, "html.parser").get_text("\n")
    msg.attach(MIMEText(plain, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(env["SMTP_HOST"], env["SMTP_PORT"], context=context) as server:
        server.login(env["SMTP_USER"], env["SMTP_PASS"])
        server.sendmail(env["FROM_EMAIL"], [env["TO_EMAIL"]], msg.as_string())

def main():
    env = load_env()

    if not env["SMTP_USER"] or not env["SMTP_PASS"] or not env["TO_EMAIL"]:
        raise SystemExit("Configure SMTP_USER, SMTP_PASS e TO_EMAIL (use .env).")

    limit = env["DIGEST_LIMIT"]
    timeout = env["REQUEST_TIMEOUT"]

    # 1) Tenta RSS primeiro (mais estável e educado com o site)
    headlines = fetch_rss_headlines(env["RSS_URL"], limit, timeout)

    # 2) Se o RSS não funcionar, tenta HTML fallback
    if not headlines:
        time.sleep(env["PAUSE_SEC"])
        headlines = fetch_html_headlines(env["HTML_URL"], limit, timeout)

    if not headlines:
        raise SystemExit("Não foi possível obter manchetes (RSS e HTML falharam).")

    html = build_email_html(headlines)
    subject = f"GE — Top {len(headlines)} manchetes do dia"
    send_email(env, subject, html)
    print(f"OK: email enviado com {len(headlines)} manchetes para {env['TO_EMAIL']}")

if __name__ == "__main__":
    main()
