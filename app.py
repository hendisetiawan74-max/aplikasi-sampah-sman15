import streamlit as st
import pandas as pd
from datetime import date
import os

# --- PENGATURAN HALAMAN UTAMA ---
st.set_page_config(page_title="Bank Sampah Sekolah", page_icon="♻️", layout="centered")

# --- MEMBUAT FOLDER PENYIMPANAN FOTO ---
# Otomatis membuat folder 'dokumentasi' jika belum ada
if not os.path.exists("dokumentasi"):
    os.makedirs("dokumentasi")

# --- MENAMBAHKAN LOGO & JUDUL ---
col1, col2 = st.columns([1, 5])
with col1:
    try:
        st.image("logo.png", width=80)
    except:
        st.write("🖼️")

with col2:
    st.title("Sistem Monitoring Sampah")

st.write("Catat dan pantau setoran sampah harian beserta dokumentasinya!")

# --- SISTEM PENYIMPANAN DATA ---
DATA_FILE = "data_sampah.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Tanggal", "Kelas", "Petugas Piket", "Organik (Kg)", "Nama Foto"])

data = load_data()

# --- MEMBUAT DUA MENU (TAB) ---
tab1, tab2 = st.tabs(["📝 Input Setoran Kelas", "📊 Klasemen & Dashboard"])

# --- MENU 1: FORMULIR INPUT ---
with tab1:
    st.header("Formulir Setoran Harian")
    
    with st.form("form_setoran"):
        tanggal = st.date_input("Hari/Tanggal", date.today())
        daftar_kelas = ["10-1", "10-2", "10-3", "10-4", "10-5", "10-6", "11-1", "11-2", "11-3", "11-4", "11-5", "11-6", "12-1", "12-2", "12-3", "12-4", "12-5", "12-6", ]
        kelas = st.selectbox("Pilih Kelas", daftar_kelas)
        petugas = st.text_input("Nama Petugas Piket")
        organik = st.number_input("Berat Sampah Organik (Kg)", min_value=0.0, step=0.1)
        
        st.write("---")
        st.write("**Dokumentasi (Opsional)**")
        foto = st.file_uploader("Unggah Foto Timbangan / Kegiatan", type=['jpg', 'jpeg', 'png'])
            
        submit = st.form_submit_button("Simpan Data Setoran")
        
        if submit:
            nama_file_foto = "Tidak ada"
            
            # Jika ada foto yang diupload, simpan file fisiknya ke folder 'dokumentasi'
            if foto is not None:
                # Membuat nama foto unik gabungan dari kelas dan nama asli file
                nama_file_foto = f"{kelas}_{foto.name}"
                lokasi_simpan = os.path.join("dokumentasi", nama_file_foto)
                
                with open(lokasi_simpan, "wb") as f:
                    f.write(foto.getbuffer())
            
            # Simpan data ke Excel (CSV)
            data_baru = pd.DataFrame({
                "Tanggal": [tanggal],
                "Kelas": [kelas],
                "Petugas Piket": [petugas],
                "Organik (Kg)": [organik],
                "Anorganik (Kg)": [anorganik],
                "Nama Foto": [nama_file_foto]
            })
            data = pd.concat([data, data_baru], ignore_index=True)
            data.to_csv(DATA_FILE, index=False) 
            st.success(f"Data setoran kelas {kelas} berhasil disimpan!")

# --- MENU 2: DASHBOARD MONITORING ---
with tab2:
    st.header("Dashboard Monitoring Sekolah")
    
    if not data.empty:
        st.write("### 🏆 Klasemen Kelas Terbersih")
        rekap = data.groupby("Kelas")["Organik (Kg)"].sum().reset_index()
        rekap = rekap.sort_values(by="Organik (Kg)", ascending=False)
        st.bar_chart(rekap, x="Kelas", y="Organik (Kg)", color="#4CAF50")
        
        st.write("### 📋 Riwayat Setoran Lengkap")
        st.dataframe(data, use_container_width=True)
        
        # --- FITUR BARU: GALERI FOTO ---
        st.write("---")
        st.write("### 📸 Galeri Dokumentasi")
        
        # Mengecek apakah folder dokumentasi benar-benar ada
        if os.path.exists("dokumentasi"):
            # Mencari semua file
            semua_file = os.listdir("dokumentasi")
            
            # FITUR PINTAR: Menyaring hanya file yang berakhiran gambar saja
            daftar_foto = [file for file in semua_file if file.endswith(('.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG'))]
            
            if len(daftar_foto) > 0:
                kolom_galeri = st.columns(3)
                for indeks, nama_foto in enumerate(daftar_foto):
                    lokasi_foto = os.path.join("dokumentasi", nama_foto)
                    with kolom_galeri[indeks % 3]:
                        # Memperbarui kode ke versi terbaru: use_container_width
                        st.image(lokasi_foto, caption=nama_foto, use_container_width=True)
            else:
                st.info("Belum ada foto dokumentasi yang diunggah.")