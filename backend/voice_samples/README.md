# Panduan Sampel Suara untuk Coqui XTTS

Folder ini digunakan untuk menyimpan sampel suara yang akan digunakan oleh model Coqui XTTS untuk menghasilkan suara yang lebih natural. Dengan peningkatan terbaru, sistem sekarang dapat menghasilkan suara yang jauh lebih natural dengan intonasi dan tanda baca yang tepat.

## Cara Menambahkan Sampel Suara

1. Rekam suara Anda dengan durasi 5-10 detik
2. Simpan dalam format WAV (16kHz, mono)
3. Beri nama file sesuai dengan jenis suara:
   - `default_male.wav` untuk suara pria
   - `default_female.wav` untuk suara wanita
   - Atau beri nama lain dan gunakan parameter `speaker_wav` saat memanggil fungsi

## Tips Merekam Suara Berkualitas

- Gunakan mikrofon yang baik
- Rekam di lingkungan yang tenang (minim noise)
- Bicara dengan jelas dan natural
- Hindari berbicara terlalu cepat atau terlalu lambat
- Gunakan intonasi yang natural
- **Baru!** Tambahkan variasi nada untuk hasil terbaik

## Contoh Kalimat untuk Sampel

Berikut adalah beberapa contoh kalimat yang baik untuk sampel suara:

1. "Selamat datang di aplikasi asisten virtual berbasis kecerdasan buatan."
2. "Teknologi ini memungkinkan interaksi yang lebih natural antara manusia dan komputer."
3. "Suara yang dihasilkan akan menyerupai karakteristik suara dalam sampel ini."
4. "Apakah Anda membutuhkan bantuan dengan pertanyaan Anda?" (Contoh kalimat tanya)
5. "Tolong dengarkan instruksi ini dengan seksama!" (Contoh kalimat perintah)

## Fitur Peningkatan Suara Terbaru

### 1. Pemrosesan Teks Cerdas

Sistem sekarang menggunakan pemrosesan teks cerdas yang mengenali pola kalimat dan menerapkan intonasi yang sesuai:

- Kalimat tanya akan memiliki intonasi naik di akhir
- Kalimat perintah akan memiliki penekanan yang tepat
- Tanda baca akan menghasilkan jeda natural

### 2. Peningkatan Kualitas Audio

Setiap output audio secara otomatis ditingkatkan dengan:

- Normalisasi volume untuk kejelasan
- Reverb ringan untuk kesan natural
- Peningkatan frekuensi suara manusia (1-3kHz)
- Penambahan bass ringan untuk kehangatan suara

### 3. Dukungan SSML untuk ElevenLabs

Untuk pengguna ElevenLabs, sistem sekarang mendukung Speech Synthesis Markup Language (SSML) yang memungkinkan kontrol lebih detail atas:

- Kecepatan bicara
- Pitch dan intonasi
- Jeda dan penekanan

## Penggunaan dalam Kode

```python
from TTS.api import TTS

# Inisialisasi TTS dengan model XTTS v2
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

# Gunakan sampel suara kustom dengan pengaturan untuk suara lebih natural
tts.tts_to_file(
    text="Halo, ini adalah contoh teks yang akan diubah menjadi suara.", 
    file_path="output.wav", 
    speaker_wav="path/to/voice_samples/default_male.wav", 
    language="id",
    speed=0.95,  # Sedikit lebih lambat untuk kejelasan
    temperature=0.75  # Lebih tinggi untuk variasi yang lebih natural
)
```

## Catatan Penting

- Semakin baik kualitas sampel suara, semakin baik pula hasil yang dihasilkan
- Sampel suara yang terlalu pendek (<3 detik) mungkin tidak memberikan hasil yang baik
- Sampel suara yang terlalu panjang (>30 detik) tidak akan meningkatkan kualitas secara signifikan
- **Baru!** Sistem sekarang secara otomatis meningkatkan kualitas audio output
- Pilih yang memberikan hasil terbaik
Contoh sampel suara yang disediakan:

- `male_1.wav` - Suara pria dewasa
- `female_1.wav` - Suara wanita dewasa
- `child_1.wav` - Suara anak-anak
