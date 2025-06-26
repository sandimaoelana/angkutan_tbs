# pages/export_laporan.py
import streamlit as st
import pandas as pd
from io import BytesIO

DATA_FILE = "data/kartu_kerja.csv"

def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Laporan TBS', index=False)
    processed_data = output.getvalue()
    return processed_data

def show():
    st.title("Export Laporan Kartu Kerja")

    try:
        df = pd.read_csv(DATA_FILE, parse_dates=["tanggal"])
    except FileNotFoundError:
        st.warning("Belum ada data yang bisa diexport.")
        return

    st.write("Berikut ini adalah data yang akan diexport:")
    st.dataframe(df.tail(20), use_container_width=True)

    excel_data = convert_df_to_excel(df)

    st.download_button(
        label="📥 Download Excel",
        data=excel_data,
        file_name="laporan_kartu_kerja.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
