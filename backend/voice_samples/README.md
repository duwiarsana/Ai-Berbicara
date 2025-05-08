# Voice Samples untuk Coqui XTTS

Folder ini berisi sampel suara referensi untuk sintesis suara menggunakan Coqui XTTS. Dengan sampel suara yang tepat, Anda dapat menghasilkan suara yang sangat natural dan tidak seperti robot.

## Cara Menambahkan Sampel Suara

1. **Rekam Sampel Suara**:
   - Rekam suara Anda atau orang lain (5-10 detik)
   - Ucapkan kalimat yang jelas dalam Bahasa Indonesia
   - Pastikan kualitas rekaman baik (tidak ada noise)
   - Bicara dengan intonasi natural (tidak monoton)

2. **Format Sampel Suara**:
   - Format: WAV (16-bit, 22050Hz atau 44100Hz)
   - Durasi: 5-10 detik (tidak terlalu pendek)
   - Ukuran file: Idealnya di bawah 1MB

3. **Nama File**:
   - Gunakan nama yang deskriptif (misalnya `pria_dewasa.wav` atau `wanita_muda.wav`)
   - Untuk sampel default, gunakan nama `default_male.wav` atau `default_female.wav`

4. **Contoh Kalimat untuk Sampel**:

   ```text
   "Selamat datang di aplikasi asisten suara. Saya akan membantu Anda menjawab pertanyaan dan memberikan informasi yang Anda butuhkan."
   ```

## Penggunaan dalam API

Saat menggunakan API, Anda dapat menentukan sampel suara yang ingin digunakan dengan parameter `voice_type`.

```http
POST /api/voice
FormData: {
  audio: [file audio],
  voice_type: "pria_dewasa.wav"
}
```

Jika tidak menentukan `voice_type`, sistem akan mencari file `default_male.wav` di folder ini.

## Tips untuk Suara yang Lebih Natural

1. **Gunakan Sampel Suara Berkualitas Tinggi**:
   - Rekam di lingkungan yang tenang
   - Gunakan mikrofon yang baik
   - Jangan terlalu dekat atau jauh dari mikrofon

2. **Variasikan Intonasi**:
   - Hindari berbicara monoton
   - Gunakan intonasi natural seperti percakapan normal

3. **Eksperimen dengan Beberapa Sampel**:
   - Coba beberapa sampel suara berbeda
   - Pilih yang memberikan hasil terbaik


Contoh sampel suara yang disediakan:

- `male_1.wav` - Suara pria dewasa
- `female_1.wav` - Suara wanita dewasa
- `child_1.wav` - Suara anak-anak
