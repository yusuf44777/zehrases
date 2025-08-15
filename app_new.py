import streamlit as st
import openai
import tempfile
import os
from pathlib import Path

def transcribe_audio(audio_file, api_key, source_language="tr"):
    """Ses dosyasını metne çevirir - Sadece OpenAI"""
    try:
        client = openai.OpenAI(api_key=api_key)
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language=source_language
        )
        return transcript.text
    except Exception as e:
        st.error(f"OpenAI ses tanıma hatası: {str(e)}")
        return None

def text_to_speech(text, api_key, voice="alloy"):
    """Metni sese çevirir - Sadece OpenAI"""
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,  
            input=text,
        )
        return response.content
    except Exception as e:
        st.error(f"OpenAI ses sentezi hatası: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="Metin Seslendirici - OpenAI",
        page_icon="🎵",
        layout="wide"
    )
    
    st.title("🎵 Metin Seslendirici")
    st.markdown("**OpenAI API** kullanarak metinleri ve ses dosyalarını seslendirin")
    
    # Sidebar'da API ayarları
    with st.sidebar:
        st.header("🔑 OpenAI API Ayarları")
        
        api_key = st.text_input(
            "OpenAI API Anahtarınızı Girin:",
            type="password",
            help="API anahtarınız güvenli şekilde saklanır"
        )
        
        if api_key:
            st.success("✅ OpenAI API anahtarı girildi")
        else:
            st.warning("⚠️ OpenAI API anahtarınızı girin")
        
        st.markdown("---")
        
        # Dil seçenekleri
        st.markdown("**🌐 Ses Dili:**")
        
        language_options = {
            "Türkçe": "tr",
            "İngilizce": "en", 
            "Arapça": "ar",
            "Almanca": "de",
            "Fransızca": "fr",
            "İspanyolca": "es"
        }
        
        selected_lang_name = st.selectbox(
            "Seslendirme dili:",
            ["Türkçe", "İngilizce", "Arapça", "Almanca", "Fransızca", "İspanyolca"],
            help="Metnin seslendirilme dili"
        )
        
        selected_lang = language_options[selected_lang_name]
        
        st.markdown("---")
        
        # Ses seçenekleri
        st.markdown("**🎵 OpenAI Ses Seçenekleri:**")
        
        voice_option = st.selectbox(
            "Ses tonu seçin:",
            ["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
            help="Farklı ses tonlarını deneyebilirsiniz"
        )
            
        # Servis bilgisi
        st.markdown("---")
        st.success("✅ OpenAI servisi - Yüksek kalite, stabil!")
        st.info("💡 Sadece seslendirme özelliği aktif")
    
    # Ana içerik kontrolü
    if not api_key:
        st.error("⚠️ Lütfen sol taraftaki menüden OpenAI API anahtarınızı girin!")
        st.info("API anahtarı almak için: https://platform.openai.com/api-keys")
        return
    
    # Sekme yapısı oluştur
    tab1, tab2 = st.tabs(["🎙️ Ses Dosyası Seslendirme", "📝 Metin Seslendirme"])
    
    # Ses dosyası seslendirme sekmesi
    with tab1:
        st.header("1. Ses Dosyasını Yükleyin")
        uploaded_file = st.file_uploader(
            "Ses dosyasını seçin (metne çevrilip seslendirilecek)",
            type=['mp3', 'wav', 'mp4', 'm4a', 'webm'],
            help="Desteklenen formatlar: MP3, WAV, MP4, M4A, WebM"
        )
        
        if uploaded_file is not None:
            # Ses dosyasını göster
            st.audio(uploaded_file, format='audio/wav')
            
            # İşleme başla
            if st.button("🎯 Seslendirmeyi Başlat", type="primary", key="audio_tts"):
                with st.spinner("Ses dosyası işleniyor..."):
                    
                    # 1. Ses tanıma
                    st.subheader("2. Ses Tanıma")
                    with st.spinner("Ses metne çevriliyor..."):
                        transcript = transcribe_audio(uploaded_file, api_key, selected_lang)
                    
                    if transcript:
                        st.success("✅ Ses başarıyla metne çevrildi!")
                        st.write(f"**Algılanan Metin:**")
                        st.write(transcript)
                        
                        # 2. Ses sentezi
                        st.subheader("3. Yeni Ses Üretimi")
                        with st.spinner(f"{selected_lang_name} metin sese çevriliyor..."):
                            audio_content = text_to_speech(transcript, api_key, voice_option)
                        
                        if audio_content:
                            st.success("✅ Yeni ses başarıyla oluşturuldu!")
                            
                            # Ses çalma
                            st.write(f"**{selected_lang_name} Seslendirme:**")
                            st.audio(audio_content, format='audio/mp3')
                            
                            # İndirme butonu
                            filename = f"{selected_lang_name.lower()}_seslendirme.mp3"
                            st.download_button(
                                label=f"📥 {selected_lang_name} Ses Dosyasını İndir",
                                data=audio_content,
                                file_name=filename,
                                mime="audio/mp3"
                            )
    
    # Metin seslendirme sekmesi
    with tab2:
        st.header("1. Metni Girin")
        input_text = st.text_area(
            f"{selected_lang_name} metninizi buraya yazın:",
            height=150,
            placeholder=f"Seslendirmek istediğiniz {selected_lang_name} metni buraya yazın..."
        )
        
        if input_text and st.button("🎯 Metni Seslendir", type="primary", key="text_tts"):
            with st.spinner("Metin işleniyor..."):
                
                # 1. Metin gösterimi
                st.subheader("2. Girilen Metin")
                st.write(f"**{selected_lang_name} Metin:**")
                st.write(input_text)
                
                # 2. Ses sentezi
                st.subheader("3. Ses Üretimi")
                with st.spinner(f"{selected_lang_name} metin sese çevriliyor..."):
                    audio_content = text_to_speech(input_text, api_key, voice_option)
                
                if audio_content:
                    st.success("✅ Ses başarıyla oluşturuldu!")
                    
                    # Ses çalma
                    st.write(f"**{selected_lang_name} Seslendirme:**")
                    st.audio(audio_content, format='audio/mp3')
                    
                    # İndirme butonu
                    filename = f"{selected_lang_name.lower()}_metin_sesi.mp3"
                    st.download_button(
                        label=f"📥 {selected_lang_name} Ses Dosyasını İndir",
                        data=audio_content,
                        file_name=filename,
                        mime="audio/mp3"
                    )
    
    # Yardım bölümü
    with st.expander("ℹ️ Nasıl Kullanılır?"):
        st.markdown("""
        **Adımlar:**
        1. Sol menüden **OpenAI API anahtarınızı** girin
        2. **Seslendirme dili** seçin (Türkçe, İngilizce, Arapça, Almanca, Fransızca, İspanyolca)
        3. **Ses tonu** seçin (alloy, echo, fable, onyx, nova, shimmer)
        4. **Ses Dosyası Seslendirme** için:
           - Ses dosyanızı yükleyin
           - "Seslendirmeyi Başlat" butonuna tıklayın
           - Ses metne çevrilir ve yeniden seslendirilir
        5. **Metin Seslendirme** için:
           - Metninizi yazın  
           - "Metni Seslendir" butonuna tıklayın
        6. İşlem tamamlandığında ses dosyasını indirin
        
        **🎯 OpenAI Avantajları:**
        ✅ **Yüksek kalite** - En iyi ses tanıma ve sentezi
        ✅ **Hızlı işlem** - Saniyeler içinde sonuç
        ✅ **Stabil servis** - 404 hataları yok
        ✅ **6 farklı ses tonu** - Erkek ve kadın sesler
        ✅ **Çok dilli destek** - 50+ dil destekli
        
        **Desteklenen Diller:**
        - 🇹🇷 Türkçe (tr)
        - 🇺🇸 İngilizce (en)
        - 🇸🇦 Arapça (ar)
        - 🇩🇪 Almanca (de)
        - 🇫🇷 Fransızca (fr)
        - 🇪🇸 İspanyolca (es)
        
        **Desteklenen Formatlar:**
        - Giriş: MP3, WAV, MP4, M4A, WebM
        - Çıkış: MP3
        
        **🔑 OpenAI API Key Alma:**
        1. https://platform.openai.com/api-keys adresine gidin
        2. "Create new secret key" butonuna tıklayın
        3. API anahtarınızı kopyalayın
        4. Sol menüden yapıştırın
        
        **💰 Maliyet:**
        - Whisper: $0.006 / dakika
        - TTS: $0.015 / 1K karakter
        """)
        
        st.markdown("**API Güvenliği:**")
        st.info("🔒 API anahtarınız sadece bu oturum için hafızada tutulur ve hiçbir yerde saklanmaz.")

if __name__ == "__main__":
    main()
