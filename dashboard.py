import streamlit as st
from db import init_db, add_channel, remove_channel, get_channels

# Inicializa banco
init_db()

st.set_page_config(page_title="Bot GMGM - Dashboard", layout="centered")
st.title("📡 Painel do Bot GMGM")
st.markdown("Gerencie os canais onde o bot enviará mensagens diariamente às 15h.")

# 🔍 Listar canais registrados com mensagens
st.subheader("🔁 Canais Registrados")
channels = get_channels()  # agora retorna lista de (id, custom_message)

if channels:
    for ch_id, msg in channels:
        st.write(f"🟢 Canal ID: `{ch_id}` — Mensagem: \"{msg}\"")
else:
    st.info("Nenhum canal cadastrado ainda.")

st.markdown("---")

# ➕ Adicionar / Editar canal com mensagem personalizada
st.subheader("➕ Cadastrar / Atualizar Canal")
new_channel_id = st.text_input("ID do Canal (Channel ID do Discord)", "")
new_custom_message = st.text_area("Mensagem personalizada (deixe em branco para 'gmgm')", value="gmgm")

if st.button("Cadastrar / Atualizar Canal"):
    if new_channel_id.isdigit():
        msg_to_save = new_custom_message.strip() if new_custom_message.strip() else "gmgm"
        add_channel(new_channel_id, msg_to_save)
        st.success(f"Canal {new_channel_id} cadastrado/atualizado com a mensagem: \"{msg_to_save}\"")
    else:
        st.error("ID do canal inválido. Deve conter apenas números.")

st.markdown("---")

# ➖ Remover canal
st.subheader("➖ Remover Canal")
if channels:
    selected = st.selectbox("Selecione um canal para remover", [ch[0] for ch in channels])
    if st.button("Remover Canal"):
        remove_channel(selected)
        st.success(f"Canal {selected} removido!")
else:
    st.info("Nenhum canal para remover.")
