import streamlit as st
import hashlib
import random

from dh_module import *
from rsa_module import *
from aes_module import encrypt

st.set_page_config(layout="wide")
st.title("TLS Handshake Simulation")

# FORM NHẬP (giống input())
with st.form("tls_form"):
    plaintext = st.text_area("Nhập plaintext:", "Hello, my name's Linh")
    submit = st.form_submit_button("Start TLS Handshake")

# XỬ LÝ KHI NHẤN NÚT
if submit:

    # 1. CLIENT HELLO
    client_random = random.randint(1, 1_000_000)

    # 2. SERVER HELLO + CERT
    server_random = random.randint(1, 1_000_000)

    pub_key, priv_key = generate_keys()
    certificate = pub_key

    # 3. DIFFIE-HELLMAN
    p, g = generate_params()

    a = generate_private_key(p)
    b = generate_private_key(p)

    A = compute_public_key(g, a, p)
    B = compute_public_key(g, b, p)

    shared_client = compute_shared_key(B, a, p)
    shared_server = compute_shared_key(A, b, p)

    # 4. SESSION KEY
    master_secret = str(shared_client) + str(client_random) + str(server_random)
    session_key = hashlib.sha256(master_secret.encode()).hexdigest()
    key_bytes = list(bytes.fromhex(session_key[:32]))

    # 5. ENCRYPT
    cipher = encrypt(plaintext, key_bytes)

    # HIỂN THỊ UI
    col1, col2 = st.columns(2)

    with col1:
        st.header("🧑 Client")

        st.write("**ClientHello**")
        st.write(f"client_random: {client_random}")

        st.write("**Gửi DH public key A:**")
        st.write(A)

        st.write("**Shared Secret:**")
        st.write(shared_client)

        st.write("**Session Key:**")
        st.code(session_key)

        st.write("**Plaintext gửi:**")
        st.write(plaintext)

    with col2:
        st.header("🖥️ Server")

        st.write("**ServerHello**")
        st.write(f"server_random: {server_random}")

        st.write("**Certificate (RSA Public Key):**")
        st.write(certificate)

        st.write("**Nhận DH public key A và gửi B:**")
        st.write(B)

        st.write("**Shared Secret:**")
        st.write(shared_server)

        st.write("**Session Key:**")
        st.code(session_key)

        st.write("**Ciphertext nhận:**")
        st.write(cipher)


    # TLS FLOW
    st.divider()
    st.subheader("TLS Process Flow")

    st.markdown(f"""
    1. Client → Server: ClientHello (random = {client_random})  
    2. Server → Client: ServerHello (random = {server_random}) + Certificate  
    3. Client ↔ Server: Diffie-Hellman Exchange  
    4. Shared Secret = {shared_client}  
    5. Session Key = SHA256(shared + randoms)  
    6. AES Encryption bắt đầu  
    """)

    st.success("TLS Handshake Completed!")