import streamlit as st
from datetime import datetime
import pandas as pd
import os

st.set_page_config(page_title="Penilaian Kantor Ramah Lingkungan", layout="wide")
st.title("📋 Form Penilaian Kantor Ramah Lingkungan")

CSV_FILE = "penilaian.csv"
DELETE_PASSWORD = "admin123"

# Komponen penilaian
KOMPONEN = [
    "1. Nama",
    "2. Jabatan",
    "3. Partai",
    "4. Daerah",
]

def load_data():
    if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
        try:
            return pd.read_csv(CSV_FILE).to_dict("records")
        except Exception as e:
            st.error(f"Gagal membaca CSV: {e}")
    return []

def save_data(data):
    pd.DataFrame(data).to_csv(CSV_FILE, index=False)

# Load ke session
if "penilaian_data" not in st.session_state:
    st.session_state.penilaian_data = load_data()

with st.form("form_penilaian"):
    col1, col2 = st.columns(2)
    with col1:
        nama_instansi = st.text_input("Nama Instansi")
    with col2:
        nama_penilai = st.text_input("Nama Penilai")

    st.markdown("### Isikan Penilaian dengan Huruf (A, B, C, D, E)")
    nilai_komponen = {}

    for k in KOMPONEN:
        huruf = st.selectbox(k, options=["A", "B", "C", "D", "E"], key=k)
        nilai_komponen[k] = huruf

    submitted = st.form_submit_button("💾 Simpan Penilaian")

    if submitted and nama_instansi and nama_penilai:
        data_baru = {
            "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Nama Instansi": nama_instansi,
            "Nama Penilai": nama_penilai
        }
        data_baru.update(nilai_komponen)
        st.session_state.penilaian_data.append(data_baru)
        save_data(st.session_state.penilaian_data)
        st.success("✅ Penilaian berhasil disimpan!")

# Tampilkan data
st.markdown("---")
st.subheader("📑 Daftar Penilaian Tersimpan")

if st.session_state.penilaian_data:
    df = pd.DataFrame(st.session_state.penilaian_data)
    st.dataframe(df, use_container_width=True)

    st.download_button(
        label="⬇️ Download CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="data_penilaian_lengkap.csv",
        mime="text/csv"
    )

    st.markdown("### 🔐 Hapus Penilaian")
    idx_to_delete = st.number_input(
        "Masukkan nomor data yang ingin dihapus (mulai dari 1):",
        min_value=1,
        max_value=len(df),
        step=1
    )
    password = st.text_input("Masukkan password", type="password")
    if st.button("Hapus Data"):
        if password == DELETE_PASSWORD:
            st.session_state.penilaian_data.pop(idx_to_delete - 1)
            save_data(st.session_state.penilaian_data)
            st.success("✅ Data berhasil dihapus.")
            st.experimental_rerun()
        else:
            st.error("❌ Password salah.")
else:
    st.info("Belum ada data penilaian disimpan.")
