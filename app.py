import os
import streamlit as st

from google import genai
from PIL import Image
from pypdf import PdfReader



# Streamlit sayfa ayarları
st.set_page_config(page_title="Fiş & Garanti Takibi", page_icon="🧾")
st.title("🧾 Fiş & Garanti Takip Asistanı")
st.write("Fiş, fatura (PDF) veya garanti belgenizin fotoğrafını yükleyin, bilgileri otomatik çıkaralım.")

# Gemini API istemcisini başlat
client = genai.Client()

# Dosya yükleyici (Artık PDF de kabul ediyor!)
uploaded_file = st.file_uploader(
    "Bir dosya seçin...", 
    type=["jpg", "jpeg", "png", "pdf"]
)

if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1].lower()
    
    # Dosya türüne göre işleme
    if file_extension in ["jpg", "jpeg", "png"]:
        image = Image.open(uploaded_file)
        st.image(image, caption="Yüklenen Belge (Görsel)", use_column_width=True)
        content_to_send = image
        
    elif file_extension == "pdf":
        st.info("📄 PDF dosyası algılandı, metinler okunuyor...")
        reader = PdfReader(uploaded_file)
        pdf_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pdf_text += text + "\n"
        
        st.write(f"Toplam {len(reader.pages)} sayfalık PDF okundu.")
        content_to_send = pdf_text

    if st.button("🚀 Belgeyi Analiz Et ve Bilgileri Çıkar"):
        with st.spinner("Gemini belgeyi analiz ediyor..."):
            try:
                prompt = """
                Bu belgedeki (fiş, fatura veya garanti belgesi) bilgileri analiz et ve şu başlıklar altında Türkçe olarak çıkar:
                1. Ürün / Mağaza Adı
                2. Tarih
                3. Toplam Tutar
                4. Garanti Süresi (varsa)
                5. Özet Bilgi
                """
                
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=[content_to_send, prompt]
                )
                
                st.success("Analiz Tamamlandı!")
                st.markdown("### 📌 Çıkarılan Bilgiler:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
