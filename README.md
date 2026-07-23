# 🛡️ AuthCraft — Enterprise Password & Vault Manager

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python" alt="Python Version" />
  <img src="https://img.shields.io/badge/UI-CustomTkinter-indigo?style=for-the-badge" alt="CustomTkinter" />
  <img src="https://img.shields.io/badge/Encryption-AES--256-green?style=for-the-badge" alt="AES-256" />
  <img src="https://img.shields.io/badge/Security-HIBP%20k--Anonymity-orange?style=for-the-badge" alt="HIBP API" />
</p>

**AuthCraft**, modern, şık ve askeri düzeyde güvenlik sağlayan masaüstü şifre ve kasa yöneticisidir. Tüm gizli verilerinizi **AES-256** şifreleme algoritması ile yerel olarak korur ve sızdırılmış şifreleri **HaveIBeenPwned API (k-Anonymity)** entegrasyonu ile tespit eder.

---

## ✨ Özellikler

- 🔒 **AES-256-CBC & PBKDF2 Şifreleme**: Ana şifreniz (Master Password) ve kullanıcıya özel tuz (salt) kullanılarak türetilen 256-bit anahtar ile kasanızdaki tüm hassas veriler uçtan uca şifrelenir.
- 🛡️ **Canlı Sızıntı Taraması (HaveIBeenPwned API)**: *k-Anonymity* modelini kullanır. Şifreniz asla internete gönderilmez, yalnızca SHA-1 hash'inin ilk 5 karakteri ile veri ihlali veritabanında güvenli sorgulama yapılır.
- 🎨 **Modern Slate & Indigo Arayüzü**: CustomTkinter tabanlı karanlık mod, kategori filtreleri, anlık metrik istatistik kartları ve akıcı görsel deneyim.
- 🗂️ **Kategori Yönetimi**: Web Hesapları, Banka/Kredi Kartları, Wi-Fi Ağları ve Gizli Notlar için organize edilmiş saklama.
- ⚡ **Güçlü Şifre Üreteci**: Kriptografik rastgelelikle (`secrets` modülü) saniyeler içinde kırılması imkansız şifreler üretin.
- 🔍 **Anlık Arama & Filtreleme**: Kasa içeriklerinde başlık ve kullanıcı adına göre anında arama yapın.
- 📋 **Tek Tıkla Kopyalama & Göster/Gizle**: Şifreleri güvenle panoya kopyalayın veya maskelemeyi kaldırın.

---

## 🛠️ Kurulum & Çalıştırma

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/KULLANICI_ADI/Authcraft.git
cd Authcraft
```

### 2. Gerekli Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 3. Uygulamayı Başlatın
```bash
python main.py
```

---

## 📦 Executable (.exe) Derleme (PyInstaller)

AuthCraft'i tek tıkla çalıştırılabilir `.exe` dosyasına dönüştürmek için:

```bash
pyinstaller main.spec
```

Derlenen uygulama `dist/main/main.exe` konumunda hazır olacaktır.

---

## 📁 Proje Yapısı

```
Authcraft/
│── core/
│   ├── security.py       # AES-256 şifreleme, PBKDF2 KDF & HIBP API kontrolü
│   └── storage.py        # SQLite veritabanı yönetimi ve veri şifreleme katmanı
│── ui/
│   └── animated_widgets.py # Özel animasyonlu UI bileşenleri
│── main.py               # CustomTkinter GUI ana uygulama döngüsü ve ekranlar
│── main.spec             # PyInstaller yapılandırma dosyası
│── requirements.txt      # Proje bağımlılıkları
│── .gitignore            # Git takibinden hariç tutulacak dosyalar
└── README.md             # Proje dokümantasyonu
```

---

## 🔐 Güvenlik Mimarisi

1. **Master Password & Salt**: Kayıt sırasında kullanıcıya özel 16-byte cryptographically secure tuz üretilir.
2. **Kasa Verileri**: Her bir kasa kaydı (`secret_val`), PBKDF2HMAC (SHA-256, 100,000 iterasyon) ile türetilen AES-256 anahtarı ile şifrelenerek SQLite veritabanında tutulur.
3. **Sızıntı Sorgulama**: `check_pwned_password` fonksiyonu k-Anonymity protokolünü takip eder. Şifrenin SHA-1 hash'inin yalnızca ilk 5 karakteri HIBP API'ye iletilir, dönen hash kümesi yerelde eşleştirilir.

---

## 📜 Lisans

Bu proje MIT lisansı altında sunulmaktadır. Dilediğiniz gibi geliştirebilir ve kullanabilirsiniz.
