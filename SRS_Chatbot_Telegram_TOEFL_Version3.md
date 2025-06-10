# Software Requirements Specification (SRS)  
## 1. Pendahuluan

### 1.1. Latar Belakang
Lembaga ujian TOEFL ingin meningkatkan layanan informasi peserta melalui chatbot Telegram. Chatbot ini akan melayani pertanyaan-pertanyaan umum berbasis database yang dapat diupdate oleh admin melalui admin web GUI. Semua interaksi user dilakukan melalui aplikasi Telegram. Web GUI hanya untuk admin. Sistem akan berjalan di server Linux yang telah tersedia.

### 1.2. Tujuan
Dokumen ini mendefinisikan kebutuhan perangkat lunak chatbot Telegram untuk TOEFL, meliputi fitur utama, integrasi database, admin panel, penggunaan API AI, dan pengalihan ke sistem tiket eksternal bila diperlukan.

---

## 2. Ruang Lingkup

- Chatbot Telegram (user hanya berinteraksi via Telegram)
- Mode FAQ berbasis database
- Mode AI (API Gemini) jika tidak ada data di database
- Admin web GUI (hanya untuk admin, akses terbatas) untuk mengelola data pertanyaan/jawaban
- Pengalihan ke sistem tiket eksternal jika pertanyaan tidak bisa dijawab
- Semua sistem berjalan di server Linux yang sudah tersedia

---

## 3. Kebutuhan Sistem

### 3.1. Fungsional

#### 3.1.1. Interaksi Chatbot Telegram (User)
- User membuka chat Telegram ➔ Chatbot menyapa & menampilkan opsi kategori/topik pertanyaan
- User memilih kategori/topik ➔ Mendapatkan daftar pertanyaan
- User memilih pertanyaan ➔ Chatbot menjawab dari database
- Jika jawaban tidak ada ➔ Chatbot menawarkan mode AI (Gemini)
- Jika AI juga tidak bisa menjawab ➔ Chatbot mengarahkan ke web eksternal (sistem tiket)
- Jika user ingin reschedule ujian ➔ Langsung diarahkan ke web eksternal tiket
- Tidak ada interaksi user melalui web, hanya via Telegram

#### 3.1.2. Admin Web GUI (Hanya Admin)
- Login dan otorisasi admin
- CRUD data FAQ: tambah, edit, hapus pertanyaan/jawaban, kategori/topik
- Hanya admin yang dapat mengakses web GUI

#### 3.1.3. Database
- Menyimpan data FAQ (pertanyaan, jawaban, kategori/topik)

---

### 3.2. Non-Fungsional

- **Keamanan**: Otorisasi admin untuk akses web GUI; proteksi data
- **Ketersediaan**: Chatbot & web admin dapat diakses 24/7 di server Linux
- **Skalabilitas**: Sistem mampu menangani peningkatan jumlah user Telegram
- **Kemudahan Penggunaan**: Antarmuka chatbot Telegram dan web admin mudah digunakan

---

## 4. Use Case Diagram (Deskripsi)

- **User Telegram** membuka chat → Mendapatkan menu & kategori
- **User** memilih kategori → Daftar pertanyaan
- **User** memilih pertanyaan → Jawaban dari database
- Jika **pertanyaan tidak ditemukan** → Mode AI (Gemini)
- Jika **AI tidak bisa jawab** → Arahkan ke web tiket eksternal
- **User** ingin reschedule → Langsung diarahkan ke web tiket eksternal
- **Admin** login ke web GUI untuk kelola FAQ

---

## 5. Alur Kerja (Flow)

**User (Telegram saja):**  
1. Start chat  
2. Pilih kategori  
3. Pilih pertanyaan  
   - Jika ada di database → Jawaban dari database  
   - Jika tidak → Mode AI  
      - Jika AI tidak bisa jawab → Diberi link ke web tiket eksternal  
4. Jika ingin reschedule → Langsung diberi link ke web tiket eksternal

**Admin (Web GUI):**  
1. Login  
2. Kelola data FAQ (tambah/edit/hapus pertanyaan, jawaban, kategori)

---

## 6. Rekomendasi Tools dan Stack

### Backend & Database:
- **Python** (FastAPI/Flask)
- **PostgreSQL** atau **MySQL** (atau SQLite untuk development)
- **python-telegram-bot** (Telegram API integration)
- **Gemini API** (Google AI) untuk mode AI

### Web Admin (Hanya Admin):
- **ReactJS** atau **Vue.js** (untuk admin web GUI)
- **Docker** (untuk container/deployment di Linux Server)
- **Gunicorn/UWSGI** + **Nginx** (opsional, untuk production server di Linux)

### Lainnya:
- **Git** (version control)
- **Linux tools**: systemd, supervisor, crontab (untuk menjalankan & menjaga service tetap aktif)
- **SSL** untuk keamanan web GUI

---

## 7. Langkah-Langkah Pengembangan

1. **Analisis & Desain**
   - Finalisasi flow chatbot Telegram dan admin web GUI
   - Rancang skema database (FAQ, kategori)
   - Rancang wireframe web admin

2. **Setup Project di Server Linux**
   - Inisialisasi repo (Git)
   - Setup environment Python (virtualenv, pip)
   - Setup database (PostgreSQL/MySQL)
   - Setup SSL & domain (jika dibutuhkan untuk web admin)

3. **Pengembangan Backend & API**
   - REST API untuk FAQ & admin
   - Integrasi Gemini API
   - API untuk web admin (CRUD FAQ)

4. **Pengembangan Chatbot Telegram**
   - Koneksi ke Telegram API
   - Implementasi flow percakapan
   - Integrasi backend FAQ & AI

5. **Pengembangan Web Admin GUI**
   - Login admin (auth)
   - CRUD FAQ & kategori

6. **Integrasi & Testing**
   - Test chatbot Telegram end-to-end
   - Test CRUD FAQ via web admin
   - Test integrasi AI & pengalihan ke web tiket eksternal

7. **Deployment**
   - Deploy backend & admin GUI di server Linux (Docker/virtualenv)
   - Setup systemd/supervisor untuk daemon service

8. **Maintenance & Monitoring**
   - Monitor penggunaan & feedback
   - Update FAQ secara berkala

---

## 8. Catatan

- Semua interaksi user hanya melalui Telegram, tidak ada akses user ke web.
- Web GUI hanya untuk admin (akses internal).
- Semua sistem berjalan dan dimaintain di server Linux milik lembaga.

---

**Saran:**  
Prioritaskan keamanan web admin & backup database secara rutin di server Linux.
