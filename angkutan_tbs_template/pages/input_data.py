# pages/input_data.py
import streamlit as st
import pandas as pd
from datetime import date

DATA_FILE = "data/kartu_kerja.csv"


def show():
    st.title("Input Data Kartu Kerja - Supir")

    with st.form("form_input"):
        tanggal = st.date_input("Tanggal", value=date.today())
        jam_awal = st.text_input("Jam Awal")
        jam_akhir = st.text_input("Jam Akhir")
        dari = st.text_input("Dari")
        ke = st.text_input("Ke")
        jenis_muatan = st.selectbox("Jenis Muatan", ["TBS", "Pupuk", "Bibit", "Karyawan", "JJK", "Laterit", "Kosong"])
        volume = st.number_input("Volume", min_value=0.0)
        satuan = st.selectbox("Satuan", ["Kg", "Rit", "Pcs"])
        km_awal = st.number_input("KM Awal", min_value=0)
        km_akhir = st.number_input("KM Akhir", min_value=0)
        bbm_liter = st.number_input("BBM (Liter)", min_value=0.0)
        biaya = st.number_input("Biaya (Rp)", min_value=0.0)
        supir = st.text_input("Nama Supir")
        keterangan = st.text_area("Keterangan Tambahan")

        submitted = st.form_submit_button("Simpan")

        if submitted:
            new_data = pd.DataFrame([{
                "tanggal": tanggal,
                "jam_awal": jam_awal,
                "jam_akhir": jam_akhir,
                "dari": dari,
                "ke": ke,
                "jenis_muatan": jenis_muatan,
                "volume": volume,
                "satuan": satuan,
                "km_awal": km_awal,
                "km_akhir": km_akhir,
                "bbm_liter": bbm_liter,
                "biaya": biaya,
                "supir": supir,
                "keterangan": keterangan
            }])

            try:
                df = pd.read_csv(DATA_FILE)
                df = pd.concat([df, new_data], ignore_index=True)
            except FileNotFoundError:
                df = new_data

            df.to_csv(DATA_FILE, index=False)
            st.success("Data berhasil disimpan!")
