# 🌍 Çok Dilli Ses Çevirici

Türkçe, İngilizce ve Arapça arasında ses dosyalarını ve metinleri çeviren Streamlit uygulaması.

## 🚀 Özellikler

- **Ses Dosyası Çeviri**: MP3, WAV, MP4, M4A, WebM formatlarını destekler
- **Metin Çeviri**: Doğrudan metin girişi ile çeviri
- **Ses Sentezi**: Çevrilmiş metinleri seslendirme
- **Çoklu Dil Desteği**: Türkçe ↔ İngilizce ↔ Arapça
- **6 Farklı Ses Tonu**: alloy, echo, fable, onyx, nova, shimmer

## 🛠️ Kurulum

### 1. Gereksinimler
- Python 3.11+
- OpenAI API anahtarı

### 2. Ortam Kurulumu
```bash
# Conda ortamı oluştur
conda create -n streamlitenv python=3.11
conda activate streamlitenv

# Paketleri yükle
pip install -r requirements.txt
```

### 3. API Anahtarı
1. https://platform.openai.com/api-keys adresine gidin
2. Yeni API anahtarı oluşturun
3. `.env` dosyasına ekleyin veya uygulama içinde girin

## 🎯 Kullanım

### Uygulamayı Başlatma
```bash
conda activate streamlitenv
streamlit run app.py
```

Uygulama http://localhost:8501 adresinde açılacaktır.

### Kullanım Adımları
1. **OpenAI API anahtarınızı** sol menüden girin
2. **Kaynak dil** ve **hedef dili** seçin
3. **Ses tonu** seçin
4. **Ses Dosyası** veya **Metin** sekmesinden çeviri yapın

## 📁 Proje Yapısı

```
zehrases/
├── app.py              # Ana Streamlit uygulaması
├── requirements.txt    # Python paket gereksinimleri
├── .env               # API anahtarları (opsiyonel)
└── README.md          # Bu dosya
```

## 🔧 Teknik Detaylar

### Kullanılan Teknolojiler
- **Streamlit**: Web arayüzü
- **OpenAI Whisper**: Ses tanıma
- **OpenAI GPT-4o-mini**: Metin çevirisi
- **OpenAI TTS**: Ses sentezi

### Desteklenen Formatlar
- **Giriş**: MP3, WAV, MP4, M4A, WebM
- **Çıkış**: MP3

### Maliyet Bilgisi
- Whisper: $0.006 / dakika
- GPT-4o-mini: $0.00015 / 1K input token, $0.0006 / 1K output token
- TTS: $0.015 / 1K karakter

## 🔒 Güvenlik

- API anahtarları sadece oturum süresince hafızada tutulur
- Hiçbir veri kalıcı olarak saklanmaz
- Dosyalar geçici olarak işlenir ve silinir

## 🌐 Desteklenen Diller

- 🇹🇷 **Türkçe** (tr)
- 🇺🇸 **İngilizce** (en)  
- 🇸🇦 **Arapça** (ar)

## 📞 Destek

Herhangi bir sorun yaşarsanız:
1. OpenAI API anahtarınızın geçerli olduğundan emin olun
2. İnternet bağlantınızı kontrol edin
3. Conda ortamının aktif olduğundan emin olun

## 📄 Lisans

Bu proje açık kaynak kodludur ve MIT lisansı altında dağıtılmaktadır.
