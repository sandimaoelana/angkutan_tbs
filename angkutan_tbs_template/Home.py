# Home.py
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml import SafeLoader
from pages import input_data, dashboard, export_laporan

# Konfigurasi login
from utils.auth import load_authenticator

authenticator = load_authenticator()
name, auth_status, username = authenticator.login("Login", "main")

if auth_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.write(f"Halo, {name}!")
    
    menu = st.sidebar.selectbox("Menu", ["Input Data", "Dashboard", "Export Laporan"])

    if menu == "Input Data":
        input_data.show()
    elif menu == "Dashboard":
        dashboard.show()
    elif menu == "Export Laporan":
        export_laporan.show()

elif auth_status is False:
    st.error("Username atau password salah")
elif auth_status is None:
    st.warning("Silakan login untuk melanjutkan")