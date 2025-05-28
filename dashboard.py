import streamlit as st
from db import init_db, add_channel, remove_channel, get_channels

# Inicializa banco
init_db()

st.set_page_config(page_title="Bot GMGM - Dashboard", layout="centered")
st.title("📡 Painel do Bot GMGM")
st.markdown("Gerencie os canais onde o bot enviará `gmgm` diariamente às 9h.")

# 🔍 Listar canais registrados
st.subheader("🔁 Canais Registrados")
channels = get_channels()

if channels:
    for ch in channels:
        st.write(f"🟢 Canal ID: `{ch}`")
else:
    st.info("Nenhum canal cadastrado ainda.")

# ➕ Adicionar novo canal
st.subheader("➕ Adicionar Canal")
new_channel_id = st.text_input("ID do Canal (Channel ID do Discord)", "")

if st.button("Cadastrar Canal"):
    if new_channel_id.isdigit():
        add_channel(new_channel_id)
        st.success(f"Canal {new_channel_id} adicionado!")
    else:
        st.error("ID do canal inválido. Deve ser apenas números.")

# ➖ Remover canal
st.subheader("➖ Remover Canal")
if channels:
    selected = st.selectbox("Selecione um canal para remover", channels)
    if st.button("Remover Canal"):
        remove_channel(selected)
        st.success(f"Canal {selected} removido!")
else:
    st.info("Nenhum canal para remover.")
