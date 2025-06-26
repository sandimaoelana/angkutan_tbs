import streamlit as st
import pandas as pd
import database as db
import os

# Pastikan folder data ada
if not os.path.exists('data'):
    os.makedirs('data')

# Inisialisasi database saat aplikasi dimulai
db.init_db()

def login_page():
    st.title("Sistem Pengangkutan TBS")
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        role = db.verify_user(username, password)
        if role:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.session_state['role'] = role
            st.success(f"Selamat datang, {username}!")
            st.rerun() # Refresh untuk masuk ke halaman sesuai role
        else:
            st.error("Username atau password salah")

def supir_page():
    st.title(f"Halaman Supir - Input Data Harian ({st.session_state['username']})")

    st.subheader("Form Input Data Angkutan")
    with st.form("transport_form"):
        tanggal = st.date_input("Tanggal")
        jam = st.time_input("Jam")
        km_awal = st.number_input("KM Awal", min_value=0.0, format="%.2f")
        km_akhir = st.number_input("KM Akhir", min_value=0.0, format="%.2f")
        dari = st.text_input("Dari")
        ke = st.text_input("Ke")
        jenis_muatan = st.selectbox("Jenis Muatan", ["TBS"])
        volume = st.number_input("Volume", min_value=0.0, format="%.2f")
        satuan = st.selectbox("Satuan", ["Kg"])
        bbm = st.number_input("BBM (liter)", min_value=0.0, format="%.2f")
        biaya = st.number_input("Biaya (Rp)", min_value=0.0, format="%d")
        keterangan = st.text_area("Keterangan (opsional)")

        submitted = st.form_submit_button("Simpan Data")
        if submitted:
            if km_akhir < km_awal:
                st.error("KM Akhir tidak boleh lebih kecil dari KM Awal.")
            else:
                data = {
                    "tanggal": str(tanggal),
                    "jam": str(jam),
                    "km_awal": km_awal,
                    "km_akhir": km_akhir,
                    "dari": dari,
                    "ke": ke,
                    "jenis_muatan": jenis_muatan,
                    "volume": volume,
                    "satuan": satuan,
                    "bbm": bbm,
                    "biaya": biaya,
                    "supir": st.session_state['username'],
                    "keterangan": keterangan
                }
                db.insert_transport_data(data)
                st.success("Data berhasil disimpan!")

def pengawas_page():
    st.title("Halaman Pengawas - Review Data & Dashboard")

    st.subheader("Filter Data")
    col1, col2 = st.columns(2)
    with col1:
        filter_tanggal = st.date_input("Filter Tanggal (opsional)", value=None)
    with col2:
        filter_supir = st.text_input("Filter Supir (opsional)")

    filters = {}
    if filter_tanggal:
        filters['tanggal'] = str(filter_tanggal)
    if filter_supir:
        filters['supir'] = filter_supir

    data_records = db.get_transport_data(filters)
    df = pd.DataFrame(data_records)

    if not df.empty:
        st.subheader("Data Angkutan")
        st.dataframe(df)

        st.subheader("Dashboard Rekap")
        total_muatan = df['volume'].sum()
        total_bbm = df['bbm'].sum()
        jumlah_ritase = len(df)

        st.metric("Total Muatan TBS", f"{total_muatan:,.2f} Kg")
        st.metric("Total Konsumsi BBM", f"{total_bbm:,.2f} Liter")
        st.metric("Jumlah Ritase", jumlah_ritase)

        # Contoh Visualisasi (bisa dikembangkan)
        st.subheader("Muatan TBS per Tanggal")
        muatan_per_tanggal = df.groupby('tanggal')['volume'].sum().reset_index()
        st.bar_chart(muatan_per_tanggal.set_index('tanggal'))

        # Verifikasi Data (contoh)
        st.subheader("Verifikasi Data")
        record_to_verify_id = st.selectbox("Pilih ID Record untuk Verifikasi", df['id'].tolist())
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            if st.button("Setujui"):
                db.update_record_status(record_to_verify_id, 'verified')
                st.success(f"Record ID {record_to_verify_id} berhasil disetujui.")
                st.rerun()
        with col_v2:
            if st.button("Tolak"):
                db.update_record_status(record_to_verify_id, 'rejected')
                st.warning(f"Record ID {record_to_verify_id} berhasil ditolak.")
                st.rerun()

    else:
        st.info("Tidak ada data angkutan yang ditemukan.")

def admin_page():
    st.title("Halaman Admin - Pengelolaan Data & Export Laporan")

    st.subheader("Semua Data Angkutan")
    data_records = db.get_transport_data()
    df = pd.DataFrame(data_records)

    if not df.empty:
        st.dataframe(df)

        st.subheader("Export Data ke Excel")
        # Filter untuk export
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            export_start_date = st.date_input("Mulai Tanggal (Export)", value=None)
        with col_e2:
            export_end_date = st.date_input("Sampai Tanggal (Export)", value=None)

        df_filtered_for_export = df.copy()
        if export_start_date:
            df_filtered_for_export = df_filtered_for_export[df_filtered_for_export['tanggal'] >= str(export_start_date)]
        if export_end_date:
            df_filtered_for_export = df_filtered_for_export[df_filtered_for_export['tanggal'] <= str(export_end_date)]

        @st.cache_data
        def convert_df_to_excel(df_to_convert):
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df_to_convert.to_excel(writer, index=False, sheet_name='Laporan TBS')
            writer.close()
            processed_data = output.getvalue()
            return processed_data

        from io import BytesIO
        excel_data = convert_df_to_excel(df_filtered_for_export)
        st.download_button(
            label="Download Laporan Excel",
            data=excel_data,
            file_name="laporan_angkutan_tbs.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("Tidak ada data angkutan yang tersedia untuk di-export.")

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        login_page()
    else:
        st.sidebar.title("Navigasi")
        st.sidebar.write(f"Logged in as: **{st.session_state['username']}** ({st.session_state['role']})")
        
        if st.session_state['role'] == 'supir':
            st.sidebar.page_link("app.py", label="Input Data Harian")
        elif st.session_state['role'] == 'pengawas':
            st.sidebar.page_link("app.py", label="Review & Dashboard")
        elif st.session_state['role'] == 'admin':
            st.sidebar.page_link("app.py", label="Admin & Export")
        
        if st.sidebar.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ""
            st.session_state['role'] = ""
            st.rerun()

        if st.session_state['role'] == 'supir':
            supir_page()
        elif st.session_state['role'] == 'pengawas':
            pengawas_page()
        elif st.session_state['role'] == 'admin':
            admin_page()

if __name__ == "__main__":
    main()