import streamlit as st
from docx import Document
from docxcompose.composer import Composer
from io import BytesIO

st.title("📄 Merge File Word (.docx) — Preserve Format 100%")

uploaded_files = st.file_uploader(
    "Upload beberapa file .docx", 
    type=["docx"], 
    accept_multiple_files=True
)

if uploaded_files:
    if st.button("Gabungkan File"):
        # Pakai dokumen pertama sebagai base
        base_doc = Document(uploaded_files[0])
        composer = Composer(base_doc)
        
        for idx, uploaded_file in enumerate(uploaded_files[1:], start=2):
            next_doc = Document(uploaded_file)
            composer.append(next_doc)
        
        # Simpan ke buffer
        buffer = BytesIO()
        composer.save(buffer)
        buffer.seek(0)

        st.success("File berhasil digabungkan (format utuh)!")

        st.download_button(
            label="📥 Download File Gabungan",
            data=buffer,
            file_name="merged_full_format.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

