# pages/dashboard.py
import streamlit as st
import pandas as pd

DATA_FILE = "data/kartu_kerja.csv"

def show():
    st.title("Dashboard Rekap Kartu Kerja")

    try:
        df = pd.read_csv(DATA_FILE, parse_dates=["tanggal"])
    except FileNotFoundError:
        st.warning("Belum ada data yang tersimpan.")
        return

    st.subheader("Filter Data")
    supir_list = df["supir"].dropna().unique().tolist()
    jenis_list = df["jenis_muatan"].dropna().unique().tolist()

    col1, col2 = st.columns(2)
    with col1:
        selected_supir = st.multiselect("Pilih Supir", supir_list, default=supir_list)
    with col2:
        selected_jenis = st.multiselect("Jenis Muatan", jenis_list, default=jenis_list)

    df_filtered = df[(df["supir"].isin(selected_supir)) & (df["jenis_muatan"].isin(selected_jenis))]

    st.subheader("Ringkasan")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Perjalanan", len(df_filtered))
    with col2:
        st.metric("Total Volume", f"{df_filtered['volume'].sum():,.0f} {df_filtered['satuan'].mode()[0]}")
    with col3:
        st.metric("Total BBM", f"{df_filtered['bbm_liter'].sum():,.2f} L")

    st.subheader("Data Lengkap")
    st.dataframe(df_filtered.sort_values(by="tanggal", ascending=False), use_container_width=True)

    with st.expander("Grafik Volume per Tanggal"):
        chart_data = df_filtered.groupby("tanggal")["volume"].sum()
        st.bar_chart(chart_data)
