import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Input Arsip Naskah", page_icon="🗂️", layout="wide")
st.title("🗂️ Form Input Arsip Naskah")

# --- Inisialisasi storage sesi ---
cols = [
    "No.",
    "Nomor Berkas",
    "Kode Klasifikasi",
    "Nomor Naskah",
    "Tanggal Naskah",
    "Uraian Naskah",
    "Jumlah Naskah",
    "Sifat Naskah",
    "Media Naskah",
    "Tingkat Perkembangan",
    "Kondisi Naskah",
    "Keterangan",
]

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=cols)

# --- Opsi pilihan (bisa diubah sesuai kebutuhan) ---
opsi_sifat = ["Biasa", "Penting", "Rahasia", "Lainnya"]
opsi_media = ["Kertas", "Digital", "Foto/Negatif", "Audio/Video", "Lainnya"]
opsi_tingkat = ["Asli", "Salinan", "Konsep/Draft", "Tembusan", "Lainnya"]
opsi_kondisi = ["Baik", "Rusak Ringan", "Rusak Sedang", "Rusak Berat", "Lainnya"]

with st.form("form_input"):
    c1, c2, c3, c4 = st.columns([1, 1.2, 1.2, 1.2])
    with c1:
        no = st.number_input("No.", min_value=1, step=1, format="%d")
        jumlah = st.number_input("Jumlah Naskah", min_value=0, step=1, format="%d")
    with c2:
        nomor_berkas = st.text_input("Nomor Berkas")
        kode_klas = st.text_input("Kode Klasifikasi")
    with c3:
        nomor_naskah = st.text_input("Nomor Naskah")
        tanggal_naskah = st.date_input("Tanggal Naskah", value=date.today())
    with c4:
        sifat = st.selectbox("Sifat Naskah", opsi_sifat)
        media = st.selectbox("Media Naskah", opsi_media)

    uraian = st.text_area("Uraian Naskah")
    c5, c6, c7 = st.columns(3)
    with c5:
        tingkat = st.selectbox("Tingkat Perkembangan", opsi_tingkat)
    with c6:
        kondisi = st.selectbox("Kondisi Naskah", opsi_kondisi)
    with c7:
        keterangan = st.text_area("Keterangan", height=90)

    # Validasi sederhana
    st.caption("Tip: Kolom bertanda * sebaiknya tidak kosong: Nomor Berkas*, Kode Klasifikasi*, Uraian Naskah*")
    submitted = st.form_submit_button("Simpan")

if submitted:
    if not nomor_berkas or not kode_klas or not uraian:
        st.error("Mohon lengkapi minimal: Nomor Berkas, Kode Klasifikasi, dan Uraian Naskah.")
    else:
        new_row = pd.DataFrame([[
            int(no),
            nomor_berkas.strip(),
            kode_klas.strip(),
            nomor_naskah.strip(),
            pd.to_datetime(tanggal_naskah).date(),
            uraian.strip(),
            int(jumlah),
            sifat,
            media,
            tingkat,
            kondisi,
            keterangan.strip()
        ]], columns=cols)

        # Cegah duplikat sederhana berdasarkan (No.) atau kombinasi kunci lain bila perlu
        if (st.session_state.data["No."].astype(str) == str(no)).any():
            st.warning(f"No. {no} sudah ada. Data baru tetap ditambahkan, pertimbangkan ganti No. agar unik.")
        st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
        st.success("Data berhasil disimpan ✅")

# --- Tabel data tersimpan ---
st.subheader("📋 Data Tersimpan (Sesi Ini)")
if len(st.session_state.data) == 0:
    st.info("Belum ada data.")
else:
    # Urutkan secara default berdasar No.
    try:
        st.session_state.data["No."] = pd.to_numeric(st.session_state.data["No."], errors="coerce")
        st.session_state.data.sort_values(by="No.", inplace=True, kind="stable")
    except Exception:
        pass

    st.dataframe(st.session_state.data, use_container_width=True, hide_index=True)

    # Tombol hapus semua (opsional)
    with st.expander("Opsi Lanjutan"):
        if st.button("Hapus semua data (sesi ini)"):
            st.session_state.data = pd.DataFrame(columns=cols)
            st.success("Semua data dihapus dari sesi ini.")

    # (Opsional) Unduh CSV — tidak menyimpan otomatis ke file, hanya download manual
    csv = st.session_state.data.to_csv(index=False).encode("utf-8")
    st.download_button("Unduh CSV", data=csv, file_name="arsip_naskah.csv", mime="text/csv")
