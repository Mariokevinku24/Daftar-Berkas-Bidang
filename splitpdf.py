import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
import io
import zipfile

st.title("📄 PDF Splitter - Per Halaman")

# Upload file PDF
uploaded_file = st.file_uploader("Upload file PDF", type=["pdf"])

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    num_pages = len(reader.pages)
    st.info(f"PDF berhasil diupload: {num_pages} halaman ditemukan.")

    # Tombol untuk split dan unduh ZIP
    if st.button("Split PDF & Download ZIP"):
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for i in range(num_pages):
                writer = PdfWriter()
                writer.add_page(reader.pages[i])

                pdf_bytes = io.BytesIO()
                writer.write(pdf_bytes)
                pdf_bytes.seek(0)

                filename = f"page_{i+1}.pdf"
                zip_file.writestr(filename, pdf_bytes.read())

        zip_buffer.seek(0)
        st.success("PDF berhasil di-split! Klik tombol di bawah untuk mengunduh ZIP.")

        st.download_button(
            label="📥 Download ZIP",
            data=zip_buffer,
            file_name="split_pages.zip",
            mime="application/zip"
        )
