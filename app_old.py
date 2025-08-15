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
        page_icon="�",
        layout="wide"
    )
    
    st.title("� Metin Seslendirici")
    st.markdown("**OpenAI TTS API** kullanarak metinleri ve ses dosyalarını seslendirin")
    
    
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
        
        
        st.markdown("**🎵 OpenAI Ses Seçenekleri:**")
        
        voice_option = st.selectbox(
            "Ses tonu seçin:",
            ["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
            help="Farklı ses tonlarını deneyebilirsiniz"
        )
            
        
        st.markdown("---")
        st.success("✅ OpenAI servisi - Yüksek kalite, stabil!")
        st.info("💡 Hugging Face 404 hataları nedeniyle geçici olarak devre dışı")
    
    
    if not api_key:
        st.error("⚠️ Lütfen sol taraftaki menüden OpenAI API anahtarınızı girin!")
        st.info("API anahtarı almak için: https://platform.openai.com/api-keys")
        return
        
    if source_lang == target_lang:
        st.error("⚠️ Lütfen farklı kaynak ve hedef dilleri seçin!")
        return
    
    
    tab1, tab2 = st.tabs(["🎙️ Ses Dosyası Çeviri", "📝 Metin Çeviri"])
    
    
    with tab1:
        
        st.header(f"1. {source_lang_name} Ses Dosyasını Yükleyin")
        uploaded_file = st.file_uploader(
            f"{source_lang_name} ses dosyasını seçin",
            type=['mp3', 'wav', 'mp4', 'm4a', 'webm'],
            help="Desteklenen formatlar: MP3, WAV, MP4, M4A, WebM"
        )
        
        if uploaded_file is not None:
            
            st.audio(uploaded_file, format='audio/wav')
            
            
            if st.button("🎯 Çeviriyi Başlat", type="primary", key="audio_translate"):
                with st.spinner("Ses dosyası işleniyor..."):
                    
                    
                    st.subheader("2. Ses Tanıma")
                    with st.spinner("Ses metne çevriliyor..."):
                        transcript = transcribe_audio(uploaded_file, api_key, source_lang)
                    
                    if transcript:
                        st.success("✅ Ses başarıyla metne çevrildi!")
                        st.write(f"**{source_lang_name} Metin:**")
                        st.write(transcript)
                        
                        
                        st.subheader("3. Çeviri")
                        with st.spinner(f"Metin {target_lang_name}'ya çevriliyor..."):
                            translated_text = translate_text(transcript, api_key, source_lang, target_lang)
                        
                        if translated_text:
                            st.success("✅ Metin başarıyla çevrildi!")
                            st.write(f"**{target_lang_name} Çeviri:**")
                            st.write(translated_text)
                            
                            
                            st.subheader("4. Ses Sentezi")
                            with st.spinner(f"{target_lang_name} metin sese çevriliyor..."):
                                audio_content = text_to_speech(translated_text, api_key, voice_option)
                            
                            if audio_content:
                                st.success("✅ Ses başarıyla oluşturuldu!")
                                
                                
                                st.write(f"**{target_lang_name} Ses:**")
                                st.audio(audio_content, format='audio/mp3')
                                
                                
                                filename = f"{target_lang_name.lower()}_ceviri.mp3"
                                st.download_button(
                                    label=f"📥 {target_lang_name} Ses Dosyasını İndir",
                                    data=audio_content,
                                    file_name=filename,
                                    mime="audio/mp3"
                                )
    
    
    with tab2:
        st.header(f"1. {source_lang_name} Metni Girin")
        input_text = st.text_area(
            f"{source_lang_name} metninizi buraya yazın:",
            height=150,
            placeholder=f"Çevirmek istediğiniz {source_lang_name} metni buraya yazın..."
        )
        
        if input_text and st.button("🎯 Metni Çevir ve Seslendir", type="primary", key="text_translate"):
            with st.spinner("Metin işleniyor..."):
                
                
                st.subheader("2. Çeviri")
                with st.spinner(f"Metin {target_lang_name}'ya çevriliyor..."):
                    translated_text = translate_text(input_text, api_key, source_lang, target_lang)
                
                if translated_text:
                    st.success("✅ Metin başarıyla çevrildi!")
                    
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**{source_lang_name} Metin:**")
                        st.write(input_text)
                    
                    with col2:
                        st.write(f"**{target_lang_name} Çeviri:**")
                        st.write(translated_text)
                    
                    
                    st.subheader("3. Ses Sentezi")
                    with st.spinner(f"{target_lang_name} metin sese çevriliyor..."):
                        audio_content = text_to_speech(translated_text, api_key, voice_option)
                    
                    if audio_content:
                        st.success("✅ Ses başarıyla oluşturuldu!")
                        
                        
                        st.write(f"**{target_lang_name} Ses:**")
                        st.audio(audio_content, format='audio/mp3')
                        
                        
                        filename = f"{target_lang_name.lower()}_metin_sesi.mp3"
                        st.download_button(
                            label=f"📥 {target_lang_name} Ses Dosyasını İndir",
                            data=audio_content,
                            file_name=filename,
                            mime="audio/mp3"
                        )
    
    
    with st.expander("ℹ️ Nasıl Kullanılır?"):
        st.markdown("""
        **Adımlar:**
        1. Sol menüden **OpenAI API anahtarınızı** girin
        2. **Kaynak dil** ve **hedef dili** seçin (Türkçe ↔ İngilizce ↔ Arapça)
        3. **Ses tonu** seçin (alloy, echo, fable, onyx, nova, shimmer)
        4. **Ses Dosyası Çeviri** için:
           - Ses dosyanızı yükleyin
           - "Çeviriyi Başlat" butonuna tıklayın
        5. **Metin Çeviri** için:
           - Metninizi yazın  
           - "Metni Çevir ve Seslendir" butonuna tıklayın
        6. İşlem tamamlandığında ses dosyasını indirin
        
        **🎯 OpenAI Avantajları:**
        ✅ **Yüksek kalite** - En iyi ses tanıma ve çeviri
        ✅ **Hızlı işlem** - Saniyeler içinde sonuç
        ✅ **Stabil servis** - 404 hataları yok
        ✅ **6 farklı ses tonu** - Erkek ve kadın sesler
        ✅ **Çok dilli destek** - 50+ dil destekli
        
        **Desteklenen Diller:**
        - 🇹🇷 Türkçe (tr)
        - 🇺🇸 İngilizce (en)
        - 🇸🇦 Arapça (ar)
        
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
        - GPT-4o-mini: $0.00015 / 1K input token, $0.0006 / 1K output token
        - TTS: $0.015 / 1K karakter
        """)
        
        st.markdown("**API Güvenliği:**")
        st.info("🔒 API anahtarınız sadece bu oturum için hafızada tutulur ve hiçbir yerde saklanmaz.")

if __name__ == "__main__":
    main()
