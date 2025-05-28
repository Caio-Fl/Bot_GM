import os
import requests
import datetime
import time
from db import get_channels, init_db  # get_channels agora retorna webhooks

# Inicializa banco
init_db()

def send_gmgm():
    now = datetime.datetime.now()
    if now.hour != 9:
        print("⏱️ Não é hora de enviar gmgm ainda.")
        return

    channels = get_channels()  # webhooks

    for webhook_url in channels:
        try:
            response = requests.post(webhook_url, json={"content": "gmgm"})
            if response.status_code == 204:
                print(f"✅ Mensagem enviada para {webhook_url}")
            else:
                print(f"⚠️ Falha ao enviar para {webhook_url}: {response.status_code}")
        except Exception as e:
            print(f"❌ Erro ao enviar para {webhook_url}: {e}")

# Loop manual simples
if __name__ == "__main__":
    print("📡 Bot GMGM iniciado...")
    while True:
        send_gmgm()
        time.sleep(3600)  # verifica a cada hora
