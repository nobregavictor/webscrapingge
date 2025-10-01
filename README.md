<img width="740" height="451" alt="image" src="https://github.com/user-attachments/assets/d9081bff-7b3f-4670-8461-4d411fec8c51" />
<img width="484" height="59" alt="image" src="https://github.com/user-attachments/assets/e91ab881-88e2-43cf-a53f-c6aeb771c57b" />

# 📰 GE Daily Digest

Um script em Python que coleta automaticamente as 6 principais manchetes do **Globo Esporte** e envia um resumo diário por e-mail.  
Ideal para quem quer acompanhar rapidamente as notícias esportivas sem precisar acessar o site.

---

## ⚙️ Como funciona
O script tenta buscar as manchetes primeiro pelo **RSS oficial do GE** (mais rápido e estável).  
Se o RSS falhar, ele usa **web scraping** com `BeautifulSoup` para capturar títulos diretamente da homepage.  
Em seguida, monta um e-mail em HTML com os links das matérias e envia para o endereço configurado no arquivo `.env`.

---

## 🚀 Tecnologias utilizadas
- [Python 3](https://www.python.org/)  
- [Requests](https://docs.python-requests.org/)  
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)  
- [Feedparser](https://pypi.org/project/feedparser/)  
- [Python-dotenv](https://pypi.org/project/python-dotenv/)  
- SMTP (para envio de e-mails)  

---

## 📂 Estrutura do projeto
ge-daily-digest/
├── ge_daily_digest.py # Script principal
├── requirements.txt # Dependências
├── .env.example # Modelo de configuração
└── README.md # Documentação


---

## 🔑 Configuração

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/ge-daily-digest.git
   cd ge-daily-digest


Instale as dependências:

pip install -r requirements.txt


Configure suas credenciais no .env:

Copie o arquivo .env.example para .env

Edite e preencha com seus dados:

SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=seu_email@gmail.com
SMTP_PASS=sua_senha_app_google
FROM_EMAIL=seu_email@gmail.com
TO_EMAIL=destinatario@exemplo.com


⚠️ Para Gmail, você precisa usar uma Senha de App (não a senha normal).

▶️ Uso

Rode o script manualmente:

python ge_daily_digest.py


Se tudo estiver configurado corretamente, você receberá um e-mail como este:

Top 10 manchetes do GE — 01/10/2025

Time X vence clássico no fim

Técnico Y anuncia demissão
...

📅 Execução Automática

Você pode agendar o envio diário:

Linux/macOS (cron)

crontab -e
0 8 * * * /usr/bin/python3 /caminho/ge_daily_digest.py


Windows (Agendador de Tarefas)

Criar nova tarefa → “Iniciar um programa”

Programa/script: python

Argumentos: C:\caminho\ge_daily_digest.py

Agendar para o horário desejado

📌 Observações

Este projeto é educacional e voltado para uso pessoal.

Sempre prefira RSS quando disponível (mais estável e respeitoso com o site).

Caso o seletor HTML mude, ajuste a função fetch_html_headlines no código.
