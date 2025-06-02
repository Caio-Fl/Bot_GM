import os
import time
import threading
import streamlit as st
from datetime import datetime
import pytz
from streamlit_autorefresh import st_autorefresh

from db import init_db, add_channel, remove_channel, get_channels
from discord_bot import run_bot, send_gmgm
from dotenv import load_dotenv

# Define timezone para São Paulo (UTC-3)
os.environ['TZ'] = 'America/Sao_Paulo'
#time.tzset()

load_dotenv()

def main():
    st.set_page_config(page_title="Bot GM - Dashboard", layout="centered")
    # Inicia o bot como uma thread em segundo plano (compatível com Render)
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # Inicializa banco
    init_db()

    # Atualiza a cada 60 segundos
    st_autorefresh(interval=60000, key="refresh")

    # Hora atual no Brasil
    brazil_time = datetime.now(pytz.timezone('America/Sao_Paulo'))

    
    st.title("📡 Painel do Bot GM")

    st.markdown(f"🕒 Horário atual no Brasil (UTC-3): **{brazil_time.strftime('%d/%m/%Y %H:%M:%S')}**")

    # Indicador de atividade (LED)
    st.markdown("""
    <style>
    .led {
        height: 20px;
        width: 20px;
        background-color: #00FF00;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px #00FF00;
        animation: blink 1s infinite;
    }

    @keyframes blink {
        0%   {opacity: 1;}
        50%  {opacity: 0.3;}
        100% {opacity: 1;}
    }
    </style>

    <p><span class="led"></span> <strong>Bot ativo</strong></p>
    """, unsafe_allow_html=True)

    st.markdown("Gerencie os canais onde o bot enviará mensagens diariamente.")

    st.subheader("🔁 Canais Registrados")
    channels = get_channels()

    if channels:
        for ch_id, msg in channels:
            st.write(f"🟢 Canal ID: `{ch_id}` — Mensagem: \"{msg}\"")
    else:
        st.info("Nenhum canal cadastrado ainda.")

    st.markdown("---")

    st.subheader("➕ Cadastrar / Atualizar Canal")
    new_channel_id = st.text_input("ID do Canal (Channel ID do Discord)", "")
    new_custom_message = st.text_area("Mensagem personalizada (deixe em branco para 'gmgm')", value="gmgm")

    if st.button("Cadastrar / Atualizar Canal"):
        if new_channel_id.isdigit():
            msg_to_save = new_custom_message.strip() if new_custom_message.strip() else "gmgm"
            add_channel(new_channel_id, msg_to_save)
            st.success(f"Canal {new_channel_id} cadastrado/atualizado com a mensagem: '{msg_to_save}'")
        else:
            st.error("ID do canal inválido. Deve conter apenas números.")

    st.markdown("---")

    st.subheader("➖ Remover Canal")
    if channels:
        selected = st.selectbox("Selecione um canal para remover", [ch[0] for ch in channels])
        if st.button("Remover Canal"):
            remove_channel(selected)
            st.success(f"Canal {selected} removido!")
    else:
        st.info("Nenhum canal para remover.")
    
    st.markdown("---")
    st.subheader("🚀 Enviar Mensagem Agora")

    if st.button("Enviar mensagem manualmente para todos os canais"):
        send_gmgm()
        st.success("Mensagens enviadas manualmente com sucesso!")

if __name__ == "__main__":
    main()
