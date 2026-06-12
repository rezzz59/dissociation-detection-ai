# NeuroDis — Diagnosis Awal Gangguan Disosiasi

NeuroDis adalah aplikasi **sistem pakar berbasis Flask** untuk skrining awal gejala gangguan disosiasi.  
Aplikasi ini menggunakan pendekatan **rule-based inference** (forward chaining sederhana) untuk menghitung tingkat kecocokan gejala terhadap beberapa kemungkinan kondisi psikologis.

> ⚠️ **Disclaimer penting:**  
> Hasil aplikasi ini **bukan diagnosis klinis** dan **tidak menggantikan** evaluasi oleh psikolog/psikiater berlisensi.

---

## Fitur Utama

- Antarmuka web interaktif untuk memilih gejala.
- Analisis berbasis aturan (rule base) dengan nilai **confidence** (% kecocokan).
- Menampilkan:
  - diagnosis teratas,
  - gejala yang cocok,
  - kemungkinan pemicu,
  - mekanisme pemicu,
  - rekomendasi awal.
- Endpoint API JSON untuk integrasi eksternal:
  - `POST /api/analyze`
- UI modern menggunakan Tailwind CSS (via CDN).

---

## Teknologi yang Digunakan

- **Backend:** Python + Flask
- **Template Engine:** Jinja2 (template `index.html`)
- **Frontend:** HTML + Tailwind CSS + JavaScript ringan
- **Inference:** Rule-based scoring (berdasarkan jumlah gejala yang cocok)

---

## Struktur Proyek

```bash
neurodis/
├── app.py
├── templates/
│   └── index.html
└── README.md
```

---

## Cara Menjalankan Proyek

## 1) Masuk ke folder proyek

```bash
cd /home/ahmad/Documents/sistem-pakar-jurusan/tes/neurodis
```

## 2) Buat virtual environment (disarankan)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3) Install dependency

```bash
pip install flask
```

## 4) Jalankan aplikasi

```bash
python app.py
```

Aplikasi akan aktif di:

- `http://127.0.0.1:5000`
- atau (karena host `0.0.0.0`) bisa diakses dari jaringan lokal sesuai IP mesin.

---

## Cara Penggunaan (Web UI)

1. Buka halaman utama `GET /`.
2. Pilih gejala yang relevan.
3. Klik **Mulai Analisis**.
4. Sistem menampilkan hasil skrining dan detail penjelasan.

---

## Endpoint API

## `POST /api/analyze`

Menerima list kode gejala, lalu mengembalikan hasil inferensi dalam JSON.

### Request Body (JSON)

```json
{
  "symptoms": ["G001", "G002", "G003"]
}
```

### Contoh cURL

```bash
curl -X POST http://127.0.0.1:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"symptoms":["G001","G002","G003"]}'
```

### Ringkasan Response

Response berisi data seperti:

- `status`
- `diagnosis`
- `subtitle`
- `category`
- `severity`
- `confidence`
- `match_count`
- `total_conditions`
- `explanation`
- `recommendation`
- `triggers`
- `trigger_explanation`
- `trigger_mechanism`
- `matched_labels`
- `selected_symptoms`
- `all_results`
- `wm_trace`

---

## Daftar Route

- `GET /`  
  Menampilkan halaman utama & form gejala.
- `POST /analyze`  
  Analisis dari form web, hasil dirender kembali ke halaman.
- `POST /api/analyze`  
  Analisis via JSON API.

---

## Ringkasan Cara Kerja Inference

1. User memilih gejala (mis. `G001`, `G003`, dst).
2. Sistem membuat *working memory* dari gejala terpilih.
3. Setiap rule dievaluasi:
   - hitung jumlah gejala yang cocok,
   - hitung confidence = `(matched / total kondisi rule) * 100`.
4. Hasil diurutkan dari confidence tertinggi.
5. Rule teratas dipakai sebagai hasil utama (jika semua 0%, status normal).

---

## Catatan Pengembangan Lanjutan (Opsional)

- Pisahkan knowledge base (`SYMPTOMS`, `RULES`) ke file terpisah (mis. JSON/YAML).
- Tambahkan validasi input API yang lebih ketat.
- Tambahkan unit test untuk engine inferensi (`run_inference`).
- Gunakan `requirements.txt` agar instalasi dependency lebih konsisten.

---
