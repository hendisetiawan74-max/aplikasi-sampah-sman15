import streamlit as st
import pandas as pd
from datetime import date
import os

# --- PENGATURAN HALAMAN UTAMA ---
st.set_page_config(page_title="Bank Sampah Sekolah", page_icon="♻️", layout="centered")

# Judul Aplikasi
st.title("♻️ Sistem Monitoring Sampah Sekolah")
st.write("Catat dan pantau setoran sampah harian dari setiap kelas untuk lingkungan yang lebih bersih!")

# --- SISTEM PENYIMPANAN DATA SEMENTARA ---
# Kita menyimpan data di dalam file Excel versi sederhana (CSV)
DATA_FILE = "data_sampah.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        # Jika file belum ada, buat kerangka tabelnya
        return pd.DataFrame(columns=["Tanggal", "Kelas", "Organik (Kg)", "Anorganik (Kg)"])

data = load_data()

# --- MEMBUAT DUA MENU (TAB) ---
tab1, tab2 = st.tabs(["📝 Input Setoran Kelas", "📊 Klasemen & Dashboard"])

# --- MENU 1: FORMULIR INPUT ---
with tab1:
    st.header("Formulir Setoran Harian")
    st.write("Silakan masukkan data timbangan sampah di bawah ini:")
    
    # Membuat kotak formulir
    with st.form("form_setoran"):
        tanggal = st.date_input("Hari/Tanggal", date.today())
        
        # Bapak/Ibu bisa mengganti daftar kelas ini sesuai kondisi di sekolah
        daftar_kelas = ["10-1", "10-2", "10-3", "10-4", "10-5", "10-6", "11-1", "11-2", "11-3", "11-4", "11-5", "11-6", "12-1", "12-2", "12-3", "12-4", "12-5", "11-6", "11-1", "11-1",]
        kelas = st.selectbox("Pilih Kelas", daftar_kelas)
        
        # Membuat 2 kolom sejajar untuk input berat sampah
        col1, col2 = st.columns(2)
        with col1:
            organik = st.number_input("Berat Sampah Organik (Kg)", min_value=0.0, step=0.1)
        with col2:
            anorganik = st.number_input("Berat Sampah Anorganik (Kg)", min_value=0.0, step=0.1)
            
        # Tombol Simpan
        submit = st.form_submit_button("Simpan Data Setoran")
        
        if submit:
            # Jika tombol ditekan, masukkan data baru ke dalam tabel
            data_baru = pd.DataFrame({
                "Tanggal": [tanggal],
                "Kelas": [kelas],
                "Organik (Kg)": [organik],
                "Anorganik (Kg)": [anorganik]
            })
            data = pd.concat([data, data_baru], ignore_index=True)
            data.to_csv(DATA_FILE, index=False) # Simpan ke file
            st.success(f"Alhamdulillah, data dari kelas {kelas} berhasil disimpan!")

# --- MENU 2: DASHBOARD MONITORING ---
with tab2:
    st.header("Dashboard Monitoring Sekolah")
    
    if not data.empty:
        st.write("### 🏆 Klasemen Kelas Terbersih (Total Sampah)")
        
        # Menghitung total sampah per kelas secara otomatis
        rekap = data.groupby("Kelas")[["Organik (Kg)", "Anorganik (Kg)"]].sum().reset_index()
        rekap["Total Keseluruhan (Kg)"] = rekap["Organik (Kg)"] + rekap["Anorganik (Kg)"]
        
        # Mengurutkan dari yang paling berat
        rekap = rekap.sort_values(by="Total Keseluruhan (Kg)", ascending=False)
        
        # Menampilkan Grafik Batang (Bar Chart)
        st.bar_chart(rekap, x="Kelas", y=["Organik (Kg)", "Anorganik (Kg)"], color=["#4CAF50", "#2196F3"])
        
        st.write("### 📋 Riwayat Setoran Lengkap")
        # Menampilkan tabel data lengkap
        st.dataframe(data, use_container_width=True)
        
    else:
        st.info("Belum ada data setoran yang masuk. Silakan isi form di menu 'Input Setoran Kelas'.")