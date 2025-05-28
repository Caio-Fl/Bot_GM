import os
import requests
import datetime
import time
from db import get_channels, init_db

# Configuração do horário fixo
SEND_HOUR = 19      # 20 horas (8 da noite)
SEND_MINUTE = 25     # 00 minutos

TOKEN = os.getenv("DISCORD_TOKEN")
HEADERS = {
    "Authorization": f"Bot {TOKEN}",
    "Content-Type": "application/json"
}

BASE_URL = "https://discord.com/api/v9/"

def send_gmgm():
    channels = get_channels()  # [(channel_id, custom_message), ...]

    for channel_id, custom_message in channels:
        url = f"{BASE_URL}/channels/{channel_id}/messages"
        content = custom_message.strip() if custom_message and custom_message.strip() else "gmgm"

        payload = {"content": content}

        try:
            response = requests.post(url, headers=HEADERS, json=payload)
            if response.status_code in [200, 201]:
                print(f"✅ '{content}' enviado para canal {channel_id}")
            else:
                print(f"⚠️ Erro ao enviar para {channel_id}: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Exceção ao enviar para {channel_id}: {e}")

if __name__ == "__main__":
    print("📡 Bot GMGM rodando. Aguardando o horário de envio...")
    init_db()
    last_sent_date = None

    while True:
        now = datetime.datetime.now()
        print(f"monitoring: " {now})
        if (
            now.hour == SEND_HOUR and
            now.minute == SEND_MINUTE and
            now.date() != last_sent_date
        ):
            print(f"sending")
            send_gmgm()
            last_sent_date = now.date()

        time.sleep(1)  # verifica a cada minuto
