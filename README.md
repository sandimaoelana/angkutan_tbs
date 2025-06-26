# Sistem Digital Pengangkutan Tandan Buah Segar (TBS)

Sebuah sistem berbasis web sederhana untuk mengelola dan memantau operasional pengangkutan Tandan Buah Segar (TBS) menggunakan Python (Streamlit) dan database ringan (SQLite). Sistem ini dirancang agar mudah diakses melalui handphone maupun laptop, dengan fitur input data harian oleh supir, review dan dashboard oleh pengawas, serta ekspor laporan oleh admin.

---

## Fitur Utama

* **Akses Multi-Platform:** Dapat diakses melalui browser web di handphone atau laptop tanpa instalasi khusus.
* **Hosting Gratis:** Dirancang untuk deployment mudah di platform gratis seperti Streamlit Cloud.
* **Manajemen Peran Pengguna:**
    * **Supir:** Mengisi formulir data harian (tanggal, jam, KM awal/akhir, muatan, rute, BBM, biaya, hasil kerja).
    * **Pengawas:** Melihat, memfilter, dan memverifikasi data yang masuk; mengakses dashboard rekapitulasi.
    * **Admin:** Mengelola data keseluruhan dan mengekspor laporan ke Excel.
* **Dashboard Interaktif:** Menampilkan rekapitulasi total muatan TBS, konsumsi BBM, jumlah ritase, dan visualisasi data lainnya.
* **Ekspor Laporan:** Data dapat diekspor ke format Excel (`.xlsx`) kapan saja.
* **Database Ringan:** Menggunakan SQLite untuk penyimpanan data lokal yang mudah dikelola.

---

## Struktur Proyek
