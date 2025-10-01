GE Daily Digest (Globo Esporte) — Python
===========================================

O que faz?
- Busca as 10 principais manchetes do GE (preferindo RSS; se falhar, faz scraping do HTML).
- Envia por e-mail um resumo diário (título + link).

1) Pré-requisitos
-----------------
- Python 3.10+
- `pip install -r requirements.txt`

2) Configurar credenciais
-------------------------
- Copie `.env.example` para `.env` e preencha:
    - SMTP_USER / SMTP_PASS (Gmail: use App Password)
    - FROM_EMAIL / TO_EMAIL
- Opcional: ajuste RSS_URL / HTML_URL / DIGEST_LIMIT

3) Rodar manualmente
--------------------
Linux/macOS:
    python3 ge_daily_digest.py

Windows (PowerShell/Prompt):
    python ge_daily_digest.py

4) Agendar execução diária
--------------------------
Linux (cron, 08:00 todo dia):
    crontab -e
    0 8 * * * /usr/bin/python3 /caminho/completo/ge_daily_digest.py

Windows (Agendador de Tarefas):
    - Criar Tarefa Básica -> "Iniciar um programa"
    - Programa/script: python
    - Argumentos: C:\caminho\ge_daily_digest.py
    - Agendar para execução diária no horário desejado.

Observações
-----------
- Este projeto é para fins educacionais. Use pausas e limite de requisições.
- Sempre prefira RSS (mais estável e respeitoso com o site).
- Se o seletor HTML mudar, ajuste a função `fetch_html_headlines`.
